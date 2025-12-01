"""Main Streamlit application for Gym Subscription Management."""

import streamlit as st
from services.auth_service import AuthService


# Page config
st.set_page_config(
    page_title="Gym Subscription Manager",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Agent Hercules - AI Gym Manager"
    }
)


def show_login_page():
    """Display login/signup page."""
    st.title("💪 Gym Subscription Manager")
    st.markdown("### Powered by Agent Hercules - AI Subscription Management")

    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    auth = AuthService()

    # Login tab
    with tab1:
        st.subheader("Login to Your Account")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="admin@sunrisegym.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    user = auth.login(email, password)
                    if user:
                        st.success(f"Welcome back, {user['gym_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")

        # Show test credentials
        with st.expander("🔑 Test Credentials"):
            st.code("""
Email: admin@sunrisegym.com
Password: GymAdmin2024!

Email: owner@fitclub.com
Password: FitClub2024!
            """)

    # Signup tab
    with tab2:
        st.subheader("Create New Account")

        with st.form("signup_form"):
            gym_name = st.text_input("Gym Name", placeholder="Sunrise Gym")
            email = st.text_input("Email", placeholder="owner@yourgym.com")
            password = st.text_input("Password", type="password", placeholder="Min 8 chars, 1 uppercase, 1 number")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Create Account", use_container_width=True)

            if submit:
                # Validate inputs
                if not gym_name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Validate email
                    is_valid_email, email_error = auth.validate_email(email)
                    if not is_valid_email:
                        st.error(email_error)
                    else:
                        # Validate password strength
                        is_valid_password, password_error = auth.validate_password_strength(password)
                        if not is_valid_password:
                            st.error(password_error)
                        else:
                            # Create user
                            user = auth.signup(email, password, gym_name)
                            if user:
                                st.success(f"Account created successfully! Welcome, {gym_name}!")
                                st.rerun()
                            else:
                                st.error("Email already exists. Please use a different email.")


def show_main_app():
    """Display main application for authenticated users."""
    auth = AuthService()

    # Sidebar
    with st.sidebar:
        st.title("💪 Menu")
        st.markdown(f"**{auth.get_current_gym_name()}**")
        st.caption("🤖 Agent Hercules")
        st.divider()

        # Navigation
        st.markdown("### 📚 Navigation")
        st.markdown("Use the pages above")

        st.divider()

        # Logout button
        if st.button("Logout", use_container_width=True):
            auth.logout()
            st.rerun()

    # Main content
    st.title("Welcome to Gym Subscription Manager!")
    st.markdown("### Get started by uploading your client data")

    # Quick stats (if data exists)
    from database.db_manager import DatabaseManager
    db = DatabaseManager()
    latest_batch = db.get_latest_batch_id(auth.get_current_user_id())

    if latest_batch:
        st.success("✅ You have data uploaded. Go to **Messages** to view and export!")

        # Show cluster counts
        counts = db.get_cluster_counts(latest_batch)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🔴 Urgent (1 day)", counts.get(1, 0))
        with col2:
            st.metric("🟡 3 Days", counts.get(3, 0))
        with col3:
            st.metric("🟢 7 Days", counts.get(7, 0))
        with col4:
            st.metric("🔵 30 Days", counts.get(30, 0))
    else:
        st.info("👉 Click **Upload Data** in the sidebar to get started!")

    # Features overview
    st.markdown("---")
    st.markdown("### ✨ Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📤 Easy Upload")
        st.write("Upload your Excel file with customer subscription data")

    with col2:
        st.markdown("#### 🤖 AI Classification")
        st.write("Automatically classify members by expiry date (1, 3, 7, 30 days)")

    with col3:
        st.markdown("#### 💬 Message Export")
        st.write("Export personalized WhatsApp messages as CSV/Excel")


def main():
    """Main application logic."""
    auth = AuthService()

    if auth.is_authenticated():
        show_main_app()
    else:
        show_login_page()


if __name__ == "__main__":
    main()
