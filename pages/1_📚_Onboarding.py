"""Onboarding and instructions page."""

import streamlit as st
from services.auth_service import AuthService


# Check authentication
auth = AuthService()
if not auth.is_authenticated():
    st.warning("Please login first")
    st.stop()

# Page config
st.title("📚 How to Use Gym Subscription Manager")
st.markdown(f"### Welcome to **{auth.get_current_gym_name()}**!")

st.markdown("---")

# Quick start guide
st.markdown("## 🚀 Quick Start Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Step 1️⃣")
    st.markdown("**Upload Excel File**")
    st.info("Go to 'Upload Data' and upload your member Excel file")

with col2:
    st.markdown("### Step 2️⃣")
    st.markdown("**AI Processing**")
    st.success("Our AI agent classifies members by expiry date automatically")

with col3:
    st.markdown("### Step 3️⃣")
    st.markdown("**Export Messages**")
    st.warning("Download personalized WhatsApp messages as CSV/Excel")

st.markdown("---")

# Excel format requirements
st.markdown("## 📊 Excel File Requirements")

st.markdown("""
Your Excel file must contain these columns (case-insensitive):

1. **Customer Name** - Full name of the gym member
2. **Contact / Phone** - 10-digit mobile number
3. **Subscription Start Date** - When membership started
4. **Subscription End Date** - When membership expires

**Accepted date formats:**
- DD-MM-YYYY (e.g., 25-12-2025)
- DD/MM/YYYY (e.g., 25/12/2025)
- YYYY-MM-DD (e.g., 2025-12-25)
""")

# Download sample template
st.markdown("### 📥 Download Sample Template")

st.download_button(
    label="⬇️ Download Sample Excel Template",
    data=open("assets/sample_template.xlsx", "rb").read() if st.session_state.get('sample_exists') else b"",
    file_name="gym_members_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    disabled=not st.session_state.get('sample_exists', False)
)

if not st.session_state.get('sample_exists', False):
    st.caption("Sample template will be available after setup")

st.markdown("---")

# How AI classification works
st.markdown("## 🤖 How Agent Hercules Works")

st.markdown("""
**Agent Hercules**, our intelligent AI agent, automatically classifies your members into **4 expiry clusters**:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 **Urgent (1-day)**")
    st.markdown("- Expires today or tomorrow")
    st.markdown("- Already expired memberships")

    st.markdown("#### 🟡 **3-Day Expiry**")
    st.markdown("- Expires within 3 days")
    st.markdown("- Needs immediate attention")

with col2:
    st.markdown("#### 🟢 **7-Day Expiry**")
    st.markdown("- Expires within 7 days")
    st.markdown("- Send reminder notifications")

    st.markdown("#### 🔵 **30-Day Expiry**")
    st.markdown("- Expires within 30 days")
    st.markdown("- Early renewal planning")

st.info("💡 Members with more than 30 days remaining are automatically skipped")

st.markdown("---")

# Message format
st.markdown("## 💬 Message Format")

st.markdown("Each member receives a **personalized message** like:")

with st.expander("🔴 Urgent (1-day) Message"):
    st.code("""
Hi Rahul, this is Sunrise Gym. Your membership expires tomorrow.
Renew now to continue your fitness journey!
    """)

with st.expander("🟡 3-Day Message"):
    st.code("""
Hi Priya, this is Sunrise Gym. Your membership will expire in 3 days on 15-12-2025.
Renew soon to avoid interruption!
    """)

with st.expander("🟢 7-Day Message"):
    st.code("""
Hi Amit, this is Sunrise Gym. Your membership will expire in 7 days on 22-12-2025.
Don't miss out on your fitness goals!
    """)

with st.expander("🔵 30-Day Message"):
    st.code("""
Hi Neha, this is Sunrise Gym. Your membership will expire in 30 days on 15-01-2026.
Plan your renewal today!
    """)

st.markdown("---")

# Export options
st.markdown("## 📤 Export Options")

st.markdown("""
After processing, you can export messages in two formats:

1. **CSV File** - Simple comma-separated format
   - Easy to import into WhatsApp Business tools
   - Works with all spreadsheet software

2. **Excel File** - Formatted with color-coding
   - Color-coded by cluster (Red, Yellow, Green, Blue)
   - Professional formatting
   - Auto-fit columns

You can export:
- All clusters together (one file)
- Individual clusters (separate files)
""")

st.markdown("---")

# Tips and best practices
st.markdown("## 💡 Tips & Best Practices")

tip1, tip2 = st.columns(2)

with tip1:
    st.markdown("""
    **Before Uploading:**
    - ✅ Ensure phone numbers are 10 digits
    - ✅ Check date format consistency
    - ✅ Remove duplicate entries
    - ✅ Verify end dates are after start dates
    """)

with tip2:
    st.markdown("""
    **After Processing:**
    - ✅ Review messages before sending
    - ✅ Send urgent (1-day) messages first
    - ✅ Track who responded
    - ✅ Re-upload weekly for updates
    """)

st.markdown("---")

# FAQ
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("What happens if my Excel has extra columns?"):
    st.write("No problem! The system only uses the required 4 columns. All other columns are ignored.")

with st.expander("Can I upload the same file twice?"):
    st.write("Yes! Each upload creates a new batch. The previous data is kept for history.")

with st.expander("What if some phone numbers are invalid?"):
    st.write("Invalid rows are skipped with error messages. Valid rows are processed normally.")

with st.expander("Can I customize the messages?"):
    st.write("Currently templates are fixed, but customization will be available in Phase 2.")

with st.expander("How do I send the WhatsApp messages?"):
    st.write("Export the CSV/Excel and use WhatsApp Business app or web to send manually. Automated sending will be added in Phase 2.")

st.markdown("---")

# CTA
st.success("✨ Ready to get started? Go to **Upload Data** in the sidebar!")
