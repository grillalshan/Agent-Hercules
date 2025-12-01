"""View and export messages page."""

import streamlit as st
import pandas as pd
from io import BytesIO
from services.auth_service import AuthService
from database.db_manager import DatabaseManager
from utils.date_helpers import get_cluster_emoji, get_cluster_name


# Check authentication
auth = AuthService()
if not auth.is_authenticated():
    st.warning("Please login first")
    st.stop()

# Initialize database
db = DatabaseManager()

# Page config
st.title("📱 WhatsApp Messages")
st.markdown(f"### {auth.get_current_gym_name()}")

st.markdown("---")

# Get latest batch ID
batch_id = st.session_state.get('latest_batch_id') or db.get_latest_batch_id(auth.get_current_user_id())

if not batch_id:
    st.info("No data found. Please upload member data first from the Upload Data page in the sidebar.")
    st.stop()

# Get messages
messages = db.get_messages_by_batch(batch_id)
subscriptions = db.get_subscriptions_by_batch(batch_id)

if not messages:
    st.error("No messages found for this batch")
    st.stop()

# Cluster counts
cluster_counts = db.get_cluster_counts(batch_id)

# Display summary
st.subheader(f"📊 Total Messages: {len(messages)}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"{get_cluster_emoji(1)} Urgent (1 day)",
        value=cluster_counts.get(1, 0)
    )

with col2:
    st.metric(
        label=f"{get_cluster_emoji(3)} 3 Days",
        value=cluster_counts.get(3, 0)
    )

with col3:
    st.metric(
        label=f"{get_cluster_emoji(7)} 7 Days",
        value=cluster_counts.get(7, 0)
    )

with col4:
    st.metric(
        label=f"{get_cluster_emoji(30)} 30 Days",
        value=cluster_counts.get(30, 0)
    )

st.markdown("---")

# Export section
st.subheader("📤 Export Messages")

col1, col2 = st.columns(2)

# Prepare data for export
export_data = []
for msg in messages:
    export_data.append({
        'Customer Name': msg['customer_name'],
        'Phone Number': msg['phone_number'],
        'Expiry Date': msg['subscription_end_date'],
        'Days Remaining': msg['days_remaining'],
        'Cluster': f"{msg['cluster']}-day",
        'Message': msg['message_text']
    })

export_df = pd.DataFrame(export_data)

# CSV export
with col1:
    st.markdown("#### CSV Format")
    csv = export_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download All as CSV",
        data=csv,
        file_name=f"gym_messages_{batch_id[:8]}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Excel export with formatting
with col2:
    st.markdown("#### Excel Format")

    # Create Excel file with formatting
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Messages')

        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Messages']

        # Auto-fit columns
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

    excel_data = output.getvalue()

    st.download_button(
        label="⬇️ Download All as Excel",
        data=excel_data,
        file_name=f"gym_messages_{batch_id[:8]}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.markdown("---")

# Export by cluster
st.subheader("📤 Export by Cluster")

cluster_cols = st.columns(4)

for idx, cluster in enumerate([1, 3, 7, 30]):
    with cluster_cols[idx]:
        cluster_messages = [msg for msg in messages if msg['cluster'] == cluster]

        if cluster_messages:
            cluster_export_data = []
            for msg in cluster_messages:
                cluster_export_data.append({
                    'Customer Name': msg['customer_name'],
                    'Phone Number': msg['phone_number'],
                    'Expiry Date': msg['subscription_end_date'],
                    'Days Remaining': msg['days_remaining'],
                    'Message': msg['message_text']
                })

            cluster_df = pd.DataFrame(cluster_export_data)
            cluster_csv = cluster_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label=f"{get_cluster_emoji(cluster)} {cluster}-day ({len(cluster_messages)})",
                data=cluster_csv,
                file_name=f"cluster_{cluster}day_{batch_id[:8]}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"download_cluster_{cluster}"
            )
        else:
            st.button(
                label=f"{get_cluster_emoji(cluster)} {cluster}-day (0)",
                disabled=True,
                use_container_width=True,
                key=f"disabled_cluster_{cluster}"
            )

st.markdown("---")

# View messages by cluster
st.subheader("👀 View Messages")

# Cluster filter
selected_cluster = st.selectbox(
    "Filter by Cluster",
    options=["All"] + [f"{get_cluster_emoji(c)} {get_cluster_name(c)}" for c in [1, 3, 7, 30]],
    index=0
)

# Filter messages
if selected_cluster == "All":
    filtered_messages = messages
else:
    cluster_num = int(selected_cluster.split()[1])
    filtered_messages = [msg for msg in messages if msg['cluster'] == cluster_num]

# Display messages in table
st.markdown(f"#### Showing {len(filtered_messages)} messages")

# Create display dataframe
display_data = []
for msg in filtered_messages:
    display_data.append({
        '': get_cluster_emoji(msg['cluster']),
        'Name': msg['customer_name'],
        'Phone': msg['phone_number'],
        'Expiry': msg['subscription_end_date'],
        'Days': msg['days_remaining'],
        'Message Preview': msg['message_text'][:50] + '...' if len(msg['message_text']) > 50 else msg['message_text']
    })

display_df = pd.DataFrame(display_data)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

# Expandable detailed view
st.markdown("---")
st.subheader("📄 Detailed Messages")

for msg in filtered_messages[:20]:  # Show first 20
    with st.expander(f"{get_cluster_emoji(msg['cluster'])} {msg['customer_name']} - {msg['phone_number']}"):
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Phone:** {msg['phone_number']}")
            st.write(f"**Expiry Date:** {msg['subscription_end_date']}")

        with col2:
            st.write(f"**Days Remaining:** {msg['days_remaining']}")
            st.write(f"**Cluster:** {get_cluster_name(msg['cluster'])}")

        st.markdown("**Message:**")
        st.code(msg['message_text'], language=None)

        # Copy button (for convenience)
        st.caption("💡 Tip: Use the export buttons above to download all messages")

if len(filtered_messages) > 20:
    st.info(f"Showing first 20 of {len(filtered_messages)} messages. Download to see all.")

st.markdown("---")

# Next steps
st.success("✅ Messages are ready! Download and send via WhatsApp Business.")

with st.expander("💡 How to send these messages"):
    st.markdown("""
    **Using WhatsApp Business App:**
    1. Download the CSV or Excel file
    2. Open WhatsApp Business on your phone
    3. For each member:
       - Start a new chat with their phone number
       - Copy and paste the personalized message
       - Send!

    **Using WhatsApp Web:**
    1. Go to web.whatsapp.com
    2. Open the exported file
    3. For each member:
       - Click on their phone number or search
       - Copy and paste the message
       - Send!

    **Bulk Sending (Advanced):**
    - Use WhatsApp Business API tools like WATI, Interakt
    - Import your CSV file
    - Schedule bulk sending
    - (This feature will be built-in in Phase 2)
    """)
