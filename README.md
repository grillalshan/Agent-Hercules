# Gym Subscription Management AI Agent

AI-powered subscription renewal management system for gym owners built with Streamlit, LangChain, and LangGraph.

## Features

- **Excel Upload** - Upload gym member subscription data
- **AI Classification** - Automatically classify members by expiry date (1, 3, 7, 30 days)
- **Message Generation** - Generate personalized WhatsApp renewal messages
- **Export** - Download messages as CSV/Excel for manual sending
- **Dashboard** - View subscription analytics and member clusters
- **Multi-user** - Separate accounts for different gym owners

## Tech Stack

- **Frontend**: Streamlit 1.30+
- **AI/Agent**: LangChain + LangGraph
- **Database**: SQLite3
- **Excel Processing**: pandas + openpyxl
- **Authentication**: bcrypt
- **Date Handling**: python-dateutil (IST timezone)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to project directory**
```bash
cd "d:\Nov 2025\Gym_stremalit_v1"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Seed database with dummy users**
```bash
python database/seed_data.py
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open browser** - App will open at `http://localhost:8501`

## Login Credentials

### Test Account 1
- **Email**: `admin@sunrisegym.com`
- **Password**: `GymAdmin2024!`
- **Gym**: Sunrise Gym

### Test Account 2
- **Email**: `owner@fitclub.com`
- **Password**: `FitClub2024!`
- **Gym**: FitClub Premium

## Usage Guide

### 1. Login
- Use one of the test accounts above
- Or create a new account via Sign Up

### 2. Upload Excel File
- Go to **Upload Data** page
- Upload Excel file with these columns:
  - Customer Name
  - Contact (10-digit phone number)
  - Subscription Start Date
  - Subscription End Date

**Accepted date formats**: DD-MM-YYYY, DD/MM/YYYY, or YYYY-MM-DD

### 3. Run AI Agent
- Click "Run AI Agent" button
- Wait for processing (automatic classification)
- View results by cluster

### 4. Export Messages
- Go to **Messages** page
- Download all messages (CSV or Excel)
- OR download by cluster separately
- Send manually via WhatsApp Business

## Excel File Requirements

Your Excel file must contain:

| Column Name | Description | Example |
|------------|-------------|---------|
| Customer Name | Full name | Rahul Sharma |
| Contact / Phone | 10-digit number | 9876543210 |
| Subscription Start Date | When membership started | 25-10-2025 |
| Subscription End Date | When membership expires | 25-12-2025 |

Additional columns are okay but will be ignored.

## Expiry Clusters

The AI automatically classifies members into 4 clusters:

- **🔴 Urgent (1-day)** - Expires today/tomorrow or already expired
- **🟡 3-Day** - Expires within 3 days
- **🟢 7-Day** - Expires within 7 days
- **🔵 30-Day** - Expires within 30 days

Members with >30 days remaining are automatically skipped.

## Message Templates

Each cluster gets a personalized message:

**1-Day Example:**
```
Hi Rahul, this is Sunrise Gym. Your membership expires tomorrow.
Renew now to continue your fitness journey!
```

**3-Day Example:**
```
Hi Priya, this is Sunrise Gym. Your membership will expire in 3 days on 15-12-2025.
Renew soon to avoid interruption!
```

## Project Structure

```
gym_streamlit_v1/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── database/
│   ├── db_manager.py               # Database operations
│   ├── models.py                   # Schema definitions
│   ├── seed_data.py                # Seed script
│   └── gym_management.db           # SQLite database
├── agents/
│   ├── subscription_agent.py       # LangGraph agent logic
│   └── excel_processor.py          # Excel parsing & validation
├── services/
│   ├── auth_service.py             # Authentication
│   └── message_generator.py       # Message templates
├── utils/
│   ├── validators.py               # Input validation
│   └── date_helpers.py             # Date calculations (IST)
└── pages/
    ├── 1_📚_Onboarding.py          # Instructions
    ├── 2_📊_Upload_Data.py         # Upload & process
    ├── 3_📱_Messages.py            # View & export
    └── 4_⚙️_Settings.py            # User settings
```

## Troubleshooting

### Database Error
If you see database errors, reseed the database:
```bash
python database/seed_data.py
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Excel Upload Fails
Check that your Excel file:
- Has the required 4 columns
- Is in .xlsx or .xls format
- Is under 10MB in size
- Has valid dates in DD-MM-YYYY format

### Missing Modules
If you get "No module named X" error:
```bash
pip install [module-name]
```

## Current Limitations (Phase 1)

- ❌ No automated WhatsApp sending (manual export only)
- ❌ No email notifications
- ❌ No message customization (fixed templates)
- ❌ No analytics dashboard

## Phase 2 Roadmap (Future)

1. **WhatsApp Business API Integration** - Automated sending
2. **SMS Support** - Via Fast2SMS with DLT
3. **Email Notifications** - Backup communication
4. **Analytics Dashboard** - Renewal trends, revenue projections
5. **Custom Templates** - Edit message templates
6. **Multi-gym Management** - Manage multiple locations
7. **Scheduled Sending** - Auto-send at specific times

## Support

For issues or questions:
- Check the **Onboarding** page in the app
- Review this README
- Contact: support@gymmanager.com

## License

Proprietary - All rights reserved

## Author

Built with Claude Code

---

**Version**: 1.0.0 (Phase 1)
**Last Updated**: November 2025
