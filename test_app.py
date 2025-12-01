"""Test script to verify all components work."""

import sys
import os

print("=" * 60)
print("TESTING GYM SUBSCRIPTION MANAGER")
print("=" * 60)

# Test 1: Imports
print("\n[TEST 1] Testing imports...")
try:
    import streamlit as st
    import pandas as pd
    import bcrypt
    from langgraph.graph import StateGraph
    from dateutil import tz
    import openpyxl
    print("[OK] All imports successful")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 2: Database
print("\n[TEST 2] Testing database...")
try:
    from database.db_manager import DatabaseManager
    db = DatabaseManager()
    users = db.get_user_by_email("admin@sunrisegym.com")
    if users:
        print(f"[OK] Database working - Found user: {users['email']}")
    else:
        print("[FAIL] Database issue - Admin user not found")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Database error: {e}")
    sys.exit(1)

# Test 3: Authentication Service
print("\n[TEST 3] Testing authentication...")
try:
    from services.auth_service import AuthService
    auth = AuthService()

    # Test password hashing
    password_hash = auth.hash_password("TestPass123!")
    is_valid = auth.verify_password("TestPass123!", password_hash)

    if is_valid:
        print("[OK] Authentication service working")
    else:
        print("[FAIL] Password verification failed")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Auth error: {e}")
    sys.exit(1)

# Test 4: Excel Processor
print("\n[TEST 4] Testing Excel processor...")
try:
    from agents.excel_processor import ExcelProcessor
    processor = ExcelProcessor()
    print("[OK] Excel processor initialized")
except Exception as e:
    print(f"[FAIL] Excel processor error: {e}")
    sys.exit(1)

# Test 5: Date Helpers
print("\n[TEST 5] Testing date helpers...")
try:
    from utils.date_helpers import (
        calculate_days_remaining,
        classify_by_expiry,
        get_expiry_text
    )
    from datetime import datetime, timedelta

    # Test future date
    future_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    days = calculate_days_remaining(future_date)
    cluster = classify_by_expiry(days)
    text = get_expiry_text(days)

    print(f"[OK] Date helpers working - {days} days -> Cluster {cluster}: {text}")
except Exception as e:
    print(f"[FAIL] Date helper error: {e}")
    sys.exit(1)

# Test 6: Message Generator
print("\n[TEST 6] Testing message generator...")
try:
    from services.message_generator import MessageGenerator
    msg_gen = MessageGenerator("Test Gym")
    message = msg_gen.generate_message(
        cluster=1,
        customer_name="Test User",
        expiry_text="expires tomorrow",
        expiry_date="01-12-2025",
        days_remaining=1
    )
    print(f"[OK] Message generator working")
    print(f"  Sample: {message[:60]}...")
except Exception as e:
    print(f"[FAIL] Message generator error: {e}")
    sys.exit(1)

# Test 7: Subscription Agent
print("\n[TEST 7] Testing subscription agent...")
try:
    from agents.subscription_agent import SubscriptionAgent
    import pandas as pd
    from datetime import datetime, timedelta

    # Create test data
    test_data = pd.DataFrame({
        'customer_name': ['Test User'],
        'phone_number': ['+91-9876543210'],
        'subscription_start_date': [(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')],
        'subscription_end_date': [(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')]
    })

    agent = SubscriptionAgent(user_id=1, gym_name="Test Gym")
    result = agent.process(test_data, "test.xlsx")

    if result['success']:
        print(f"[OK] Subscription agent working - Processed {result['total_processed']} records")
    else:
        print(f"[FAIL] Agent processing failed: {result.get('error')}")
        sys.exit(1)
except Exception as e:
    print(f"[FAIL] Subscription agent error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nThe app is ready to use. Run: streamlit run app.py")
print("\nLogin credentials:")
print("  Email: admin@sunrisegym.com")
print("  Password: GymAdmin2024!")
print("=" * 60)
