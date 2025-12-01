"""LangGraph agent for subscription processing."""

import uuid
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, END
import pandas as pd
from utils.date_helpers import (
    calculate_days_remaining,
    classify_by_expiry,
    get_expiry_text,
    format_date_indian
)
from services.message_generator import MessageGenerator
from database.db_manager import DatabaseManager


class SubscriptionState(TypedDict):
    """State for subscription processing workflow."""
    user_id: int
    gym_name: str
    data: pd.DataFrame
    batch_id: str
    processed_subscriptions: List[Dict]
    messages: List[Dict]
    cluster_counts: Dict[int, int]
    total_processed: int
    error: str


class SubscriptionAgent:
    """LangGraph agent for processing gym subscriptions."""

    def __init__(self, user_id: int, gym_name: str):
        """Initialize agent."""
        self.user_id = user_id
        self.gym_name = gym_name
        self.db = DatabaseManager()
        self.message_gen = MessageGenerator(gym_name)
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """Create LangGraph workflow."""
        workflow = StateGraph(SubscriptionState)

        # Add nodes
        workflow.add_node("calculate_days", self._calculate_days_node)
        workflow.add_node("classify_clusters", self._classify_clusters_node)
        workflow.add_node("generate_messages", self._generate_messages_node)
        workflow.add_node("save_to_database", self._save_to_database_node)

        # Add edges
        workflow.set_entry_point("calculate_days")
        workflow.add_edge("calculate_days", "classify_clusters")
        workflow.add_edge("classify_clusters", "generate_messages")
        workflow.add_edge("generate_messages", "save_to_database")
        workflow.add_edge("save_to_database", END)

        return workflow.compile()

    def _calculate_days_node(self, state: SubscriptionState) -> SubscriptionState:
        """Node 1: Calculate days remaining for each subscription."""
        df = state['data'].copy()

        # Calculate days remaining
        df['days_remaining'] = df['subscription_end_date'].apply(calculate_days_remaining)

        state['data'] = df
        return state

    def _classify_clusters_node(self, state: SubscriptionState) -> SubscriptionState:
        """Node 2: Classify subscriptions into expiry clusters."""
        df = state['data'].copy()

        # Classify into clusters
        df['cluster'] = df['days_remaining'].apply(classify_by_expiry)

        # Filter out cluster 0 (>30 days, skip)
        df = df[df['cluster'] > 0]

        # Count clusters
        cluster_counts = df['cluster'].value_counts().to_dict()

        state['data'] = df
        state['cluster_counts'] = cluster_counts
        state['total_processed'] = len(df)

        return state

    def _generate_messages_node(self, state: SubscriptionState) -> SubscriptionState:
        """Node 3: Generate personalized messages for each member."""
        df = state['data'].copy()

        messages = []

        for _, row in df.iterrows():
            # Get expiry text
            expiry_text = get_expiry_text(row['days_remaining'])
            formatted_date = format_date_indian(row['subscription_end_date'])

            # Generate message
            message = self.message_gen.generate_message(
                cluster=row['cluster'],
                customer_name=row['customer_name'],
                expiry_text=expiry_text,
                expiry_date=formatted_date,
                days_remaining=row['days_remaining']
            )

            messages.append({
                'customer_name': row['customer_name'],
                'phone_number': row['phone_number'],
                'subscription_end_date': row['subscription_end_date'],
                'days_remaining': row['days_remaining'],
                'cluster': row['cluster'],
                'message': message
            })

        state['messages'] = messages
        return state

    def _save_to_database_node(self, state: SubscriptionState) -> SubscriptionState:
        """Node 4: Save subscriptions and messages to database."""
        batch_id = state['batch_id']
        user_id = state['user_id']

        # Prepare subscription records
        subscription_records = []
        for msg in state['messages']:
            subscription_records.append({
                'user_id': user_id,
                'upload_batch_id': batch_id,
                'customer_name': msg['customer_name'],
                'phone_number': msg['phone_number'],
                'subscription_start_date': state['data'][state['data']['customer_name'] == msg['customer_name']]['subscription_start_date'].iloc[0],
                'subscription_end_date': msg['subscription_end_date'],
                'days_remaining': msg['days_remaining'],
                'cluster': msg['cluster']
            })

        # Save subscriptions
        self.db.save_subscriptions(subscription_records)

        # Get subscription IDs for message linking
        saved_subscriptions = self.db.get_subscriptions_by_batch(batch_id)

        # Prepare message records
        message_records = []
        for i, msg in enumerate(state['messages']):
            if i < len(saved_subscriptions):
                message_records.append({
                    'subscription_id': saved_subscriptions[i]['id'],
                    'message_text': msg['message'],
                    'cluster': msg['cluster']
                })

        # Save messages
        self.db.save_messages(message_records)

        state['processed_subscriptions'] = saved_subscriptions

        return state

    def process(self, df: pd.DataFrame, filename: str) -> Dict:
        """
        Process subscription data through the workflow.

        Args:
            df: Cleaned dataframe from Excel processor
            filename: Original filename

        Returns:
            Processing result dictionary
        """
        # Generate batch ID
        batch_id = str(uuid.uuid4())

        # Initialize state
        initial_state = {
            'user_id': self.user_id,
            'gym_name': self.gym_name,
            'data': df,
            'batch_id': batch_id,
            'processed_subscriptions': [],
            'messages': [],
            'cluster_counts': {},
            'total_processed': 0,
            'error': ''
        }

        try:
            # Run workflow
            final_state = self.workflow.invoke(initial_state)

            # Save upload history
            self.db.save_upload_history(
                user_id=self.user_id,
                batch_id=batch_id,
                filename=filename,
                total_rows=len(df),
                processed_rows=final_state['total_processed']
            )

            return {
                'success': True,
                'batch_id': batch_id,
                'total_processed': final_state['total_processed'],
                'cluster_counts': final_state['cluster_counts'],
                'messages': final_state['messages']
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
