"""Authentication service for user login and session management."""

import bcrypt
import streamlit as st
from typing import Optional, Dict
from database.db_manager import DatabaseManager


class AuthService:
    """Handles authentication and session management."""

    def __init__(self):
        """Initialize auth service."""
        self.db = DatabaseManager()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    def login(self, email: str, password: str) -> Optional[Dict]:
        """
        Authenticate user and create session.
        Returns user dict if successful, None otherwise.
        """
        # Get user from database
        user = self.db.get_user_by_email(email)

        if not user:
            return None

        # Verify password
        if not self.verify_password(password, user['password_hash']):
            return None

        # Update last login
        self.db.update_last_login(user['id'])

        # Create session
        st.session_state['authenticated'] = True
        st.session_state['user_id'] = user['id']
        st.session_state['user_email'] = user['email']
        st.session_state['gym_name'] = user['gym_name']

        return user

    def signup(self, email: str, password: str, gym_name: str) -> Optional[Dict]:
        """
        Create new user account.
        Returns user dict if successful, None if email already exists.
        """
        # Hash password
        password_hash = self.hash_password(password)

        # Create user
        user_id = self.db.create_user(email, password_hash, gym_name)

        if not user_id:
            return None

        # Auto-login after signup
        user = {
            'id': user_id,
            'email': email,
            'gym_name': gym_name
        }

        st.session_state['authenticated'] = True
        st.session_state['user_id'] = user_id
        st.session_state['user_email'] = email
        st.session_state['gym_name'] = gym_name

        return user

    def logout(self):
        """Clear session and logout user."""
        st.session_state.clear()

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return st.session_state.get('authenticated', False)

    def get_current_user_id(self) -> Optional[int]:
        """Get current logged-in user ID."""
        return st.session_state.get('user_id')

    def get_current_gym_name(self) -> Optional[str]:
        """Get current logged-in user's gym name."""
        return st.session_state.get('gym_name')

    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """
        Validate password strength.
        Returns (is_valid, error_message).
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"

        return True, ""

    def validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validate email format.
        Returns (is_valid, error_message).
        """
        if not email or '@' not in email or '.' not in email:
            return False, "Please enter a valid email address"

        return True, ""
