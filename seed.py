from app import app, db
from models.user import UserModel
from models.userType import UserType
from models.classes import ClassModel
from models.classAttendee import ClassAttendee
from models.classType import ClassType
from datetime import datetime

with app.app_context():
    try:
        print("Connected to the database!")
        db.drop_all()
        db.create_all()

        # Create Users
        conor = UserModel(
            username="conor", email="conor@11thplanet.com", password="securepassword123"
        )
        coach_kavanagh = UserModel(
            username="Coach Kavanagh",
            email="coach.kavanagh@11thplanet.com",
            password="securecoachpassword",
        )
        alan = UserModel(
            username="Alan Customer",
            email="alan@example.com",
            password="securecustomerpassword",
        )
        robert = UserModel(
            username="Robert Customer",
            email="robert@example.com",
            password="securecustomerpassword",
        )
        db.session.commit()

        # Create User Types
        admin = UserType(name="Admin")
        coach = UserType(name="Coach")
        customer = UserType(name="Customer")
        db.session.commit()

        # Associate Users and User Types
        conor.user_types.append(admin)
        coach_kavanagh.user_types.append(coach)
        alan.user_types.append(customer)
        robert.user_types.append(customer)

        # Save all to the database
        db.session.add_all(
            [conor, coach_kavanagh, alan, robert, admin, coach, customer]
        )
        db.session.commit()

        # Create Class Types
        mma_type = ClassType(
            name="MMA",
            description="MMA Class combining all forms of martial arts into one evolving and effective fighting system, including striking, wrestling, wall fighting, and grappling.",
        )
        striking_type = ClassType(
            name="striking",
            description="Striking classes focus on the fundamentals of striking, including footwork, defence, the mechanics of throwing strikes (punches, kicks, knees and elbows) and clinch work.",
        )
        db.session.add_all([mma_type, striking_type])
        db.session.commit()

        # Create Classes
        morning_mma = ClassModel(
            title="Morning MMA",
            description="Early bird grappling.",
            start_time=datetime(2024, 9, 1, 6, 0),
            end_time=datetime(2024, 9, 1, 7, 30),
            location="Studio 3",
            creator_id=coach_kavanagh.id,
            class_type_id=mma_type.id,
        )
        evening_striking = ClassModel(
            title="Evening Boxing",
            description="Striking fundamentals.",
            start_time=datetime(2024, 9, 1, 18, 0),
            end_time=datetime(2024, 9, 1, 19, 30),
            location="Studio 1",
            creator_id=coach_kavanagh.id,
            class_type_id=striking_type.id,
        )
        db.session.add_all([morning_mma, evening_striking])
        db.session.commit()

        # Create Class Attendees
        attendee1 = ClassAttendee(class_id=morning_mma.id, user_id=alan.id)
        attendee2 = ClassAttendee(class_id=evening_striking.id, user_id=alan.id)
        attendee3 = ClassAttendee(class_id=evening_striking.id, user_id=robert.id)
        db.session.add_all([attendee1, attendee2, attendee3])
        
        users = db.session.query(UserModel).all()
        for user in users:
            print(f"User: {user.username}, is_admin: {user.is_admin}, is_coach: {user.is_coach}")

        # Commit all the changes
        db.session.commit()

        print("Seeding the data..")

    except Exception as e:
        print(f"An error occurred: {e}")
