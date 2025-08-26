import os
from app import app, db
from app.models import User, Category, Location, Organization, Advertisement, Notification, AuditLog
from datetime import datetime

def add_dummy_data():
    with app.app_context():
        # Add Categories
        cat1 = Category(
            name="Health",
            description="Health related charities",
            icon_url="https://example.com/health.png",
            color_code="#FF0000",
            is_active=True,
            sort_order=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        cat2 = Category(
            name="Education",
            description="Education charities",
            icon_url="https://example.com/edu.png",
            color_code="#0000FF",
            is_active=True,
            sort_order=2,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add_all([cat1, cat2])
        db.session.commit()

        # Add Locations
        loc1 = Location(
            country="USA",
            state_province="NY",
            city="New York",
            postal_code="10001",
            latitude=40.7128,
            longitude=-74.0060,
            timezone="America/New_York",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        loc2 = Location(
            country="UK",
            state_province="England",
            city="London",
            postal_code="EC1A",
            latitude=51.5074,
            longitude=-0.1278,
            timezone="Europe/London",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add_all([loc1, loc2])
        db.session.commit()

        # Add Users
        user1 = User(
            name="Alice",
            email="alice@example.com",
            password_hash="hash1",
            role="admin",
            is_verified=True,
            google_id="alice_google",
            profile_picture="https://example.com/alice.png",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_login=datetime.now()
        )
        user2 = User(
            name="Bob",
            email="bob@example.com",
            password_hash="hash2",
            role="visitor",
            is_verified=False,
            google_id="bob_google",
            profile_picture="https://example.com/bob.png",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_login=datetime.now()
        )
        db.session.add_all([user1, user2])
        db.session.commit()

        # Add Organizations
        org1 = Organization(
            name="Charity Health Org",
            mission="Health for all",
            description="Org for health",
            category_id=cat1.category_id,
            location_id=loc1.location_id,
            address="123 Health St",
            phone="1234567890",
            email="org1@example.com",
            website="https://org1.com",
            donation_link="https://org1.com/donate",
            logo_url="https://org1.com/logo.png",
            operating_hours="9-5",
            established_year=2000,
            status="active",
            verification_level="high",
            admin_user_id=user1.user_id,
            approved_by=user2.user_id,
            approval_date=datetime.now(),
            rejection_reason=None,
            view_count=100,
            bookmark_count=10,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        org2 = Organization(
            name="Charity Edu Org",
            mission="Education for all",
            description="Org for education",
            category_id=cat2.category_id,
            location_id=loc2.location_id,
            address="456 Edu St",
            phone="0987654321",
            email="org2@example.com",
            website="https://org2.com",
            donation_link="https://org2.com/donate",
            logo_url="https://org2.com/logo.png",
            operating_hours="8-4",
            established_year=2010,
            status="pending",
            verification_level="basic",
            admin_user_id=user2.user_id,
            approved_by=user1.user_id,
            approval_date=datetime.now(),
            rejection_reason="Incomplete docs",
            view_count=50,
            bookmark_count=5,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add_all([org1, org2])
        db.session.commit()

        # Add Advertisements
        ad1 = Advertisement(
            org_id=org1.org_id,
            title="Health Ad",
            description="Ad for health org",
            image_url="https://org1.com/ad.png",
            target_url="https://org1.com",
            ad_type="Banner",
            placement="Homepage",
            start_date=datetime.now(),
            end_date=datetime.now(),
            budget=1000.00,
            clicks_count=10,
            impressions_count=100,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        ad2 = Advertisement(
            org_id=org2.org_id,
            title="Edu Ad",
            description="Ad for edu org",
            image_url="https://org2.com/ad.png",
            target_url="https://org2.com",
            ad_type="Sidebar",
            placement="Dashboard",
            start_date=datetime.now(),
            end_date=datetime.now(),
            budget=500.00,
            clicks_count=5,
            impressions_count=50,
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add_all([ad1, ad2])
        db.session.commit()

        # Add Notifications
        notif1 = Notification(
            user_id=user1.user_id,
            message="Welcome Alice!",
            is_read=False,
            created_at=datetime.now()
        )
        notif2 = Notification(
            user_id=user2.user_id,
            message="Welcome Bob!",
            is_read=True,
            created_at=datetime.now()
        )
        db.session.add_all([notif1, notif2])
        db.session.commit()

        # Add Audit Logs
        log1 = AuditLog(
            user_id=user1.user_id,
            action_type="create",
            target_type="organization",
            target_id=org1.org_id,
            old_values={"field": "value"},
            new_values={"field": "new_value"},
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
            timestamp=datetime.now()
        )
        log2 = AuditLog(
            user_id=user2.user_id,
            action_type="update",
            target_type="organization",
            target_id=org2.org_id,
            old_values={"field": "old_value"},
            new_values={"field": "new_value"},
            ip_address="127.0.0.2",
            user_agent="Mozilla/5.0",
            timestamp=datetime.now()
        )
        db.session.add_all([log1, log2])
        db.session.commit()

        print("Dummy data added successfully.")

if __name__ == "__main__":
    add_dummy_data()
