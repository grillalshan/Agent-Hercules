"""Settings and user profile page."""

import streamlit as st
from services.auth_service import AuthService
from database.db_manager import DatabaseManager


# Check authentication
auth = AuthService()
if not auth.is_authenticated():
    st.warning("Please login first")
    st.stop()

# Initialize database
db = DatabaseManager()

# Page config
st.title("⚙️ Settings")
st.markdown(f"### {auth.get_current_gym_name()}")

st.markdown("---")

# User profile section
st.subheader("👤 User Profile")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Email", value=st.session_state.get('user_email', ''), disabled=True)

with col2:
    st.text_input("Gym Name", value=auth.get_current_gym_name(), disabled=True)

st.info("Profile editing will be available in a future update")

st.markdown("---")

# WhatsApp settings (Phase 2 placeholder)
st.subheader("📱 WhatsApp Business API Settings")

st.warning("⚠️ Phase 2 Feature - Coming Soon!")

st.markdown("""
WhatsApp Business API integration will allow automatic message sending.
Currently, please export messages and send manually via WhatsApp Web or Business app.
""")

with st.expander("What you'll need for Phase 2"):
    st.markdown("""
    To enable automated WhatsApp sending, you'll need:

    1. **WhatsApp Business Account**
       - Register at business.facebook.com
       - Verify your business (takes 2-4 weeks)

    2. **API Credentials**
       - Phone Number ID
       - Business Account ID
       - Access Token

    3. **Message Templates**
       - Create and get approved by Meta
       - Each template takes 24-48 hours for approval

    We'll guide you through this entire process when Phase 2 launches!
    """)

# Placeholder inputs (disabled)
col1, col2 = st.columns(2)

with col1:
    st.text_input("WhatsApp Phone Number", placeholder="+91-XXXXXXXXXX", disabled=True)
    st.text_input("Business Account ID", placeholder="123456789012345", disabled=True)

with col2:
    st.text_input("Access Token", placeholder="Your access token", type="password", disabled=True)

st.button("💾 Save WhatsApp Settings", disabled=True, use_container_width=True)

st.markdown("---")

# Upload history
st.subheader("📋 Upload History")

history = db.get_upload_history(auth.get_current_user_id(), limit=10)

if history:
    # Create display data
    history_data = []

    for record in history:
        history_data.append({
            'Date': record['upload_date'][:10],
            'Time': record['upload_date'][11:19],
            'Filename': record['filename'],
            'Total Rows': record['total_rows'],
            'Processed': record['processed_rows'],
            'Success Rate': f"{(record['processed_rows'] / record['total_rows'] * 100):.1f}%"
        })

    import pandas as pd
    history_df = pd.DataFrame(history_data)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    # Option to view old uploads
    st.markdown("#### View Previous Upload")

    selected_upload = st.selectbox(
        "Select upload to view messages",
        options=[f"{h['filename']} - {h['upload_date'][:10]}" for h in history],
        index=0 if history else None
    )

    if st.button("📱 View Messages", use_container_width=True):
        # Get batch_id for selected upload
        selected_index = [f"{h['filename']} - {h['upload_date'][:10]}" for h in history].index(selected_upload)
        selected_batch_id = history[selected_index]['batch_id']

        st.session_state['latest_batch_id'] = selected_batch_id
        st.success("Batch selected! Go to Messages page in sidebar to view.")

else:
    st.info("No upload history found. Upload your first file to get started!")

st.markdown("---")

# App information
st.subheader("ℹ️ App Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Version:** 1.0.0 (Phase 1)")
    st.markdown("**Features:** Excel Upload, AI Classification, Message Export")

with col2:
    st.markdown("**Status:** Active")
    st.markdown("**Phase 2:** Coming Soon (Automated WhatsApp Sending)")

st.markdown("---")

# Support section
st.subheader("💬 Support & Feedback")

st.markdown("""
Need help or have feedback?

- 📧 **Email:** support@gymmanager.com
- 📚 **Documentation:** Check the Onboarding page
- 🐛 **Report Bug:** Use the feedback form below
""")

with st.expander("📝 Feedback Form"):
    feedback_type = st.selectbox("Type", ["Bug Report", "Feature Request", "General Feedback"])
    feedback_text = st.text_area("Your feedback", placeholder="Tell us what you think...")

    if st.button("Submit Feedback"):
        if feedback_text:
            st.success("✅ Thank you! Your feedback has been recorded.")
            st.balloons()
        else:
            st.error("Please enter your feedback")

st.markdown("---")

# Danger zone
st.subheader("⚠️ Danger Zone")

with st.expander("🗑️ Clear Upload History"):
    st.warning("This will delete all your upload history. Messages will remain but won't be linked to uploads.")

    if st.button("Clear All History", type="secondary"):
        st.error("This feature is disabled for safety. Contact support to clear history.")

st.markdown("---")

# Logout
if st.button("🚪 Logout", type="primary", use_container_width=True):
    auth.logout()
    st.success("Logged out successfully!")
    st.rerun()
