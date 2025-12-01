# Gym Subscription Management AI Agent - Project Plan

## System Design Analysis & Potential Issues

### 🚨 Critical Issues to Address:

1. **WhatsApp Business API Limitations**
   - WhatsApp Business API requires Meta Business verification (can take weeks)
   - Cannot send bulk messages without approved message templates
   - Rate limits: ~1000 messages per day for new businesses
   - **Alternative Solution**: Use Twilio WhatsApp API or implement gradual rollout

2. **Excel File Security**
   - Need validation for malicious files
   - Size limits (max 10MB recommended)
   - Schema validation required

3. **Database Choice**
   - SQLite for MVP (simple, file-based)
   - Can migrate to PostgreSQL later if needed

4. **Session Management**
   - Streamlit's session state can reset on reruns
   - Need persistent storage for user credentials

5. **Date Calculation Edge Cases**
   - Timezone handling
   - Expired memberships (negative days)
   - Leap years

### 💡 Suggestions for Improvement:

1. **Add Email Notifications** as backup/alternative to WhatsApp
2. **Dashboard Analytics**: Show subscription trends, renewal rates
3. **Bulk Upload History**: Track past uploads and messages sent
4. **Message Templates**: Let gym owners customize messages
5. **Dry Run Mode**: Preview who will get messages before sending
6. **Export Functionality**: Download processed data as Excel
7. **Multi-language Support**: For different regions

### 🏗️ System Architecture:

```
├── app.py (Main Streamlit entry point)
├── database/
│   ├── db_manager.py (SQLite operations)
│   └── models.py (Database schema)
├── agents/
│   ├── subscription_agent.py (LangGraph agent logic)
│   └── excel_processor.py (File parsing & validation)
├── services/
│   ├── whatsapp_service.py (WhatsApp API integration)
│   └── auth_service.py (Login & session management)
├── utils/
│   ├── validators.py (Input validation)
│   └── date_helpers.py (Date calculations)
├── pages/
│   ├── 1_onboarding.py (Instructions page)
│   ├── 2_upload.py (File upload page)
│   └── 3_settings.py (WhatsApp credentials)
└── requirements.txt
```

---

## 📋 Todo List

### Phase 1: Project Setup & Database
- [ ] Create project structure (folders)
- [ ] Set up requirements.txt with dependencies
- [ ] Create SQLite database schema (users, subscriptions, messages, settings)
- [ ] Implement database manager with CRUD operations
- [ ] Add seed data with dummy gym owner credentials

### Phase 2: Authentication & Onboarding
- [ ] Build login page with session management
- [ ] Create onboarding/instructions page
- [ ] Implement settings page for WhatsApp credentials
- [ ] Add sidebar navigation

### Phase 3: Excel Upload & Validation
- [ ] Create file upload component
- [ ] Implement Excel validator (schema, size, format)
- [ ] Build Excel parser to extract client data
- [ ] Store uploaded client data in database

### Phase 4: AI Agent (LangChain + LangGraph)
- [ ] Set up LangGraph workflow for subscription processing
- [ ] Implement date calculation logic
- [ ] Create classification system (1, 3, 7, 30 day clusters)
- [ ] Add error handling for edge cases

### Phase 5: WhatsApp Integration
- [ ] Create WhatsApp service module
- [ ] Implement message templates for each cluster
- [ ] Add "Send WhatsApp Alerts" functionality
- [ ] Add message history tracking
- [ ] Implement dry-run preview mode

### Phase 6: UI/UX Polish
- [ ] Add loading indicators for agent processing
- [ ] Display classified clients in tables/cards
- [ ] Add success/error notifications
- [ ] Create simple analytics dashboard (optional)

### Phase 7: Testing & Error Handling
- [ ] Test with various Excel formats
- [ ] Test date edge cases (expired, today, leap year)
- [ ] Test WhatsApp API error scenarios
- [ ] Add comprehensive error messages
- [ ] Security testing (SQL injection, file upload attacks)

### Phase 8: Documentation
- [ ] Add inline code comments
- [ ] Create README.md with setup instructions
- [ ] Document WhatsApp Business API setup process
- [ ] Create sample Excel template for users

---

## 🔐 Dummy Credentials for Testing

**Default Gym Owner Account:**
- Username: `admin@sunrisegym.com`
- Password: `GymAdmin2024!`

**Test Account 2:**
- Username: `owner@fitclub.com`
- Password: `FitClub2024!`

**WhatsApp Test Credentials (Mock):**
- Phone Number: `+1234567890`
- Business ID: `123456789012345`
- Auth Key: `test_auth_key_abc123xyz`

---

## 📊 Database Schema

### Users Table
```sql
- id (PRIMARY KEY)
- email (UNIQUE)
- password_hash
- gym_name
- created_at
- whatsapp_phone
- whatsapp_business_id
- whatsapp_auth_key
```

### Subscriptions Table
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- client_name
- client_phone
- start_date
- end_date
- days_remaining
- cluster (1, 3, 7, 30)
- upload_batch_id
- created_at
```

### Messages Table
```sql
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- subscription_id (FOREIGN KEY)
- message_text
- sent_at
- status (pending, sent, failed)
```

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/Agent**: LangChain + LangGraph
- **Database**: SQLite (can upgrade to PostgreSQL)
- **WhatsApp**: Twilio WhatsApp API (easier than Meta Business API)
- **Excel Processing**: pandas, openpyxl
- **Authentication**: bcrypt for password hashing
- **Date Handling**: python-dateutil

---

## ⚠️ Known Limitations & Workarounds

1. **WhatsApp Business API Approval**
   - **Issue**: Meta requires business verification
   - **Workaround**: Use Twilio WhatsApp Sandbox for testing
   - **Production**: Guide users through Meta verification process

2. **Streamlit Session State**
   - **Issue**: Can reset unexpectedly
   - **Workaround**: Store critical data in database + session

3. **Large Excel Files**
   - **Issue**: Performance degradation
   - **Workaround**: Limit to 10MB, show progress bar

4. **Timezone Handling**
   - **Issue**: Different gym locations
   - **Workaround**: Store timezone in user settings, calculate accordingly

---

## Review Section
(To be filled after implementation)

### Changes Made:
- TBD

### Challenges Encountered:
- TBD

### Future Enhancements:
- TBD
