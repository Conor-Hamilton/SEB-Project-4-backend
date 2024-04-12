from app import app, db
from models.user import UserModel
from models.userType import UserType
from models.classType import ClassType
from models.classes import ClassModel
from models.classAttendee import ClassAttendee
from datetime import datetime


with app.app_context():
    try:
        print("Connected to the database!")
        db.drop_all()
        db.create_all()

        conor = UserModel(
            username="conor",
            email="conor@11thplanet.com",
            password="securepassword123",
        )

        db.session.add(conor)
        db.session.flush()

        conor_type = UserType(
            name="Admin",
            isAdmin=True,
            isCustomer=False,
            isCoach=False,
            user_id=conor.id,
        )

        db.session.add(conor_type)

        coach_kavanagh = UserModel(
            username="Coach Kavanagh",
            email="coach.kavanagh@11thplanet.com",
            password="securecoachpassword",
        )
        db.session.add(coach_kavanagh)
        db.session.flush()

        coach_kavanagh_type = UserType(
            name="Coach",
            isAdmin=False,
            isCustomer=False,
            isCoach=True,
            user_id=coach_kavanagh.id,
        )
        db.session.add(coach_kavanagh_type)

        alan = UserModel(
            username="Alan Customer",
            email="alan@example.com",
            password="securecustomerpassword",
        )
        db.session.add(alan)
        db.session.flush()

        alan_type = UserType(
            name="Customer",
            isAdmin=False,
            isCustomer=True,
            isCoach=False,
            user_id=alan.id,
        )
        db.session.add(alan_type)
        db.session.commit()

        mma_type = ClassType(
            name="MMA",
            description="MMA Class combining all forms of martial arts into one evolving and effective fighting system, including striking, wrestling, wall fighting, and grappling.",
        )
        db.session.add(mma_type)

        striking_type = ClassType(
            name="striking",
            description="Striking classes focus on the fundamentals of striking, including footwork, defence, the mechanics of throwing strikes (punches, kicks, knees and elbows) and clinch work.",
        )
        db.session.add(striking_type)

        db.session.commit() 

        morning_mma = ClassModel(
            title="Morning MMA",
            description="Early bird grappling.",
            start_time=datetime(2024, 9, 1, 6, 0),
            end_time=datetime(2024, 9, 1, 7, 30),
            location="Studio 3",
            creator_id=coach_kavanagh.id,
            class_type_id=mma_type.id,
        )
        db.session.add(morning_mma)

        evening_striking = ClassModel(
            title="Evening Boxing",
            description="Striking fundamentals.",
            start_time=datetime(2023, 9, 1, 18, 0),
            end_time=datetime(2023, 9, 1, 19, 30),
            location="Studio 1",
            creator_id=coach_kavanagh.id,
            class_type_id=striking_type.id,
        )
        db.session.add(evening_striking)

        attendee1 = ClassAttendee(class_id=morning_mma.id, user_id=conor.id)
        db.session.add(attendee1)

        db.session.commit()

        print("Seeding the data..")

    except Exception as e:
        print(e)
