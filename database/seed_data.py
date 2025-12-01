"""Seed dummy users for testing."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from database.db_manager import DatabaseManager


def seed_users():
    """Create dummy users for testing."""
    db = DatabaseManager()

    # Dummy users
    users = [
        {
            "email": "admin@sunrisegym.com",
            "password": "GymAdmin2024!",
            "gym_name": "Sunrise Gym"
        },
        {
            "email": "owner@fitclub.com",
            "password": "FitClub2024!",
            "gym_name": "FitClub Premium"
        }
    ]

    for user in users:
        # Hash password
        password_hash = bcrypt.hashpw(
            user['password'].encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')

        # Create user
        user_id = db.create_user(user['email'], password_hash, user['gym_name'])

        if user_id:
            print(f"[OK] Created user: {user['email']} (ID: {user_id})")
        else:
            print(f"[WARN] User already exists: {user['email']}")


if __name__ == "__main__":
    print("Seeding database with dummy users...\n")
    seed_users()
    print("\n[OK] Database seeding complete!")
    print("\nLogin credentials:")
    print("   Email: admin@sunrisegym.com")
    print("   Password: GymAdmin2024!")
    print("\n   Email: owner@fitclub.com")
    print("   Password: FitClub2024!")
