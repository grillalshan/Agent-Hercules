"""Upload and process member data page."""

import streamlit as st
from services.auth_service import AuthService
from agents.excel_processor import ExcelProcessor
from agents.subscription_agent import SubscriptionAgent


# Check authentication
auth = AuthService()
if not auth.is_authenticated():
    st.warning("Please login first")
    st.stop()

# Page config
st.title("📊 Upload Member Data")
st.markdown(f"### {auth.get_current_gym_name()}")

st.markdown("---")

# Instructions
with st.expander("📋 Quick Instructions"):
    st.markdown("""
    1. Prepare your Excel file with member subscription data
    2. Required columns: Customer Name, Contact, Subscription Start Date, Subscription End Date
    3. Upload the file below
    4. Wait for AI agent to process
    5. Go to Messages page to view and export results
    """)

st.markdown("---")

# File uploader
st.subheader("📤 Upload Excel File")

uploaded_file = st.file_uploader(
    "Choose an Excel file (.xlsx or .xls)",
    type=['xlsx', 'xls'],
    help="Maximum file size: 10MB"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")

    # Process button
    if st.button("🤖 Run AI Agent", type="primary", use_container_width=True):
        with st.spinner("Processing your data..."):
            # Initialize processor
            processor = ExcelProcessor()

            # Process file
            success, message, cleaned_df, errors = processor.process_file(uploaded_file)

            if not success:
                st.error(f"❌ {message}")
                if errors:
                    with st.expander("View Errors"):
                        for error in errors:
                            st.write(f"• {error}")
                st.stop()

            # Show processing summary
            st.info(message)

            # Show errors if any (but processing continued)
            if errors:
                with st.expander(f"⚠️ {len(errors)} rows were skipped"):
                    for error in errors[:20]:  # Show first 20 errors
                        st.write(f"• {error}")
                    if len(errors) > 20:
                        st.write(f"... and {len(errors) - 20} more errors")

            # Run AI agent
            st.markdown("---")
            st.subheader("🤖 Agent Hercules Processing")

            with st.status("Agent Hercules is analyzing your data...", expanded=True) as status:
                st.write("Step 1: Calculating days remaining...")
                st.write("Step 2: Classifying into expiry clusters...")
                st.write("Step 3: Generating personalized messages...")
                st.write("Step 4: Saving to database...")

                # Initialize agent
                agent = SubscriptionAgent(
                    user_id=auth.get_current_user_id(),
                    gym_name=auth.get_current_gym_name()
                )

                # Process
                result = agent.process(cleaned_df, uploaded_file.name)

                if result['success']:
                    status.update(label="✅ Processing complete!", state="complete", expanded=False)
                else:
                    status.update(label="❌ Processing failed", state="error", expanded=True)
                    st.error(f"Error: {result['error']}")
                    st.stop()

            # Show results
            st.markdown("---")
            st.subheader("📊 Processing Results")

            st.success(f"✅ Successfully processed {result['total_processed']} members")

            # Cluster breakdown
            st.markdown("### Expiry Cluster Breakdown")

            col1, col2, col3, col4 = st.columns(4)

            cluster_counts = result['cluster_counts']

            with col1:
                count_1 = cluster_counts.get(1, 0)
                st.metric(
                    label="🔴 Urgent (1 day)",
                    value=count_1,
                    help="Expires today/tomorrow or already expired"
                )

            with col2:
                count_3 = cluster_counts.get(3, 0)
                st.metric(
                    label="🟡 3 Days",
                    value=count_3,
                    help="Expires within 3 days"
                )

            with col3:
                count_7 = cluster_counts.get(7, 0)
                st.metric(
                    label="🟢 7 Days",
                    value=count_7,
                    help="Expires within 7 days"
                )

            with col4:
                count_30 = cluster_counts.get(30, 0)
                st.metric(
                    label="🔵 30 Days",
                    value=count_30,
                    help="Expires within 30 days"
                )

            # Store batch_id in session for Messages page
            st.session_state['latest_batch_id'] = result['batch_id']
            st.session_state['processing_complete'] = True

            # Preview messages
            st.markdown("---")
            st.markdown("### 💬 Message Preview (First 5)")

            preview_messages = result['messages'][:5]

            for msg in preview_messages:
                with st.expander(f"{msg['customer_name']} - {msg['phone_number']}"):
                    st.write(f"**Expiry:** {msg['days_remaining']} days")
                    st.write(f"**Cluster:** {msg['cluster']}-day")
                    st.code(msg['message'])

            st.markdown("---")

            # Next steps
            st.success("🎉 Processing complete! Go to **Messages** page (in sidebar) to view all messages and export.")

else:
    st.info("👆 Please upload an Excel file to get started")

    # Show recent uploads
    from database.db_manager import DatabaseManager

    db = DatabaseManager()
    history = db.get_upload_history(auth.get_current_user_id(), limit=5)

    if history:
        st.markdown("---")
        st.markdown("### 📋 Recent Uploads")

        for record in history:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

            with col1:
                st.write(f"**{record['filename']}**")
            with col2:
                st.write(f"{record['processed_rows']} rows")
            with col3:
                st.write(f"{record['upload_date'][:10]}")
            with col4:
                if st.button("View", key=f"view_{record['batch_id']}"):
                    st.session_state['latest_batch_id'] = record['batch_id']
                    st.info("Batch selected! Go to Messages page in sidebar")
