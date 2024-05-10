from app import app, db
from models.user import UserModel
from models.userType import UserType
from models.classes import ClassModel
from models.classAttendee import ClassAttendee
from models.classType import ClassType
from datetime import datetime, timedelta
from itertools import cycle

with app.app_context():
    try:
        print("Connected to the database!")
        db.drop_all()
        db.create_all()

        # Create Users
        conor = UserModel(
            username="Conor", email="conor@11thplanet.com", password="%RyI5-%(vT"
        )
        coach_kavanagh = UserModel(
            username="Coach Kavanagh",
            email="coach.kavanagh@11thplanet.com",
            password="%RyI5-%(vT",
        )
        coach_thomas = UserModel(
            username="Coach Thomas",
            email="coach.thomas@11thplanet.com",
            password="%RyI5-%(vT",
        )
        alan = UserModel(
            username="Alan Customer",
            email="alan@example.com",
            password="%RyI5-%(vT",
        )
        robert = UserModel(
            username="Robert Customer",
            email="robert@example.com",
            password="%RyI5-%(vT",
        )
        chris = UserModel(
            username="Chris Customer",
            email="chris@example.com",
            password="%RyI5-%(vT",
        )
        dani = UserModel(
            username="Dani Customer",
            email="dani@example.com",
            password="%RyI5-%(vT",
        )
        josh = UserModel(
            username="Josh Customer",
            email="josh@example.com",
            password="%RyI5-%(vT",
        )
        kate = UserModel(
            username="Kate Customer",
            email="kate@example.com",
            password="%RyI5-%(vT",
        )
        emily = UserModel(
            username="Emily Customer",
            email="emily@example.com",
            password="%RyI5-%(vT",
        )
        michael = UserModel(
            username="Michael Customer",
            email="michael@example.com",
            password="%RyI5-%(vT",
        )
        sarah = UserModel(
            username="Sarah Customer",
            email="sarah@example.com",
            password="%RyI5-%(vT",
        )

        db.session.add_all(
            [
                conor,
                coach_kavanagh,
                coach_thomas,
                alan,
                robert,
                chris,
                dani,
                josh,
                kate,
                emily,
                michael,
                sarah,
            ]
        )
        db.session.commit()

        # Create User Types
        admin = UserType(name="Admin")
        coach = UserType(name="Coach")
        customer = UserType(name="Customer")
        db.session.add_all([admin, coach, customer])
        db.session.commit()

        # Associate Users and User Types
        conor.user_types.append(admin)
        coach_kavanagh.user_types.append(coach)
        coach_thomas.user_types.append(coach)
        alan.user_types.append(customer)
        robert.user_types.append(customer)
        chris.user_types.append(customer)
        dani.user_types.append(customer)
        josh.user_types.append(customer)
        kate.user_types.append(customer)
        emily.user_types.append(customer)
        michael.user_types.append(customer)
        sarah.user_types.append(customer)
        db.session.commit()

        # Create Class Types
        mma_type = ClassType(
            name="MMA", description="MMA combining striking, wrestling, and grappling."
        )

        striking_type = ClassType(
            name="Striking", description="Focus on punches, kicks, and blocks."
        )

        grappling_type = ClassType(
            name="Grappling", description="Focus on no-gi grappling techniques."
        )

        judo_type = ClassType(
            name="Judo", description="Judo throws and takedown techniques."
        )

        wrestling_type = ClassType(
            name="Wrestling",
            description="Freestyle and Greco-Roman wrestling techniques.",
        )

        gi_jiu_jitsu_type = ClassType(
            name="Gi Jiu Jitsu", description="Traditional gi Brazilian Jiu Jitsu."
        )

        kickboxing_type = ClassType(
            name="Kickboxing",
            description="Kickboxing with focus on striking and movement.",
        )

        cardio_type = ClassType(
            name="Cardio Combat",
            description="High-intensity cardio with martial arts techniques.",
        )

        open_mat_type = ClassType(
            name="Open Mat - Grappling",
            description="Open mat for grappling practice and sparring. Suitable for all skill levels.",
        )

        advanced_mma_type = ClassType(
            name="Advanced MMA",
            description="Advanced mixed martial arts techniques for seasoned practitioners.",
        )

        advanced_striking_type = ClassType(
            name="Advanced Striking",
            description="Advanced striking techniques including combinations and footwork.",
        )

        competitive_grappling_type = ClassType(
            name="Competitive Grappling",
            description="Grappling techniques tailored for competition scenarios.",
        )

        advanced_judo_type = ClassType(
            name="Advanced Judo",
            description="Advanced judo techniques including advanced throws and counters.",
        )

        db.session.add_all(
            [
                mma_type,
                striking_type,
                grappling_type,
                judo_type,
                wrestling_type,
                gi_jiu_jitsu_type,
                kickboxing_type,
                cardio_type,
                open_mat_type,
                advanced_mma_type,
                advanced_striking_type,
                competitive_grappling_type,
                advanced_judo_type,
            ]
        )
        db.session.commit()

        # Create Classes
        base_date = datetime(2024, 5, 13)

        morning_mma = ClassModel(
            title="Morning MMA",
            description="Early bird MMA session focusing on all aspects of mixed martial arts.",
            start_time=base_date + timedelta(days=0, hours=6),
            end_time=base_date + timedelta(days=0, hours=7, minutes=30),
            location="Studio 3",
            creator_id=coach_kavanagh.id,
            class_type_id=mma_type.id,
        )

        advanced_mma = ClassModel(
            title="Advanced MMA",
            description="Advanced mixed martial arts techniques for seasoned practitioners.",
            start_time=base_date + timedelta(days=7, hours=9),
            end_time=base_date + timedelta(days=7, hours=10, minutes=30),
            location="Studio 3",
            creator_id=coach_kavanagh.id,
            class_type_id=mma_type.id,
        )

        brazilian_jiu_jitsu = ClassModel(
            title="Brazilian Jiu Jitsu",
            description="Brazilian Jiu Jitsu techniques for ground fighting.",
            start_time=base_date + timedelta(days=7, hours=12),
            end_time=base_date + timedelta(days=7, hours=15, minutes=30),
            location="Main Studio",
            creator_id=coach_kavanagh.id,
            class_type_id=gi_jiu_jitsu_type.id,
        )

        evening_boxing = ClassModel(
            title="Evening Boxing",
            description="Boxing techniques and drills.",
            start_time=base_date + timedelta(days=7, hours=18),
            end_time=base_date + timedelta(days=7, hours=19, minutes=30),
            location="Studio 1",
            creator_id=coach_kavanagh.id,
            class_type_id=striking_type.id,
        )

        no_gi_grappling = ClassModel(
            title="No-Gi Grappling",
            description="Advanced no-gi grappling techniques.",
            start_time=base_date + timedelta(days=8, hours=10),
            end_time=base_date + timedelta(days=8, hours=11, minutes=30),
            location="Mat Area",
            creator_id=coach_thomas.id,
            class_type_id=grappling_type.id,
        )

        advanced_grappling = ClassModel(
            title="Advanced Grappling",
            description="Advanced grappling techniques for experienced practitioners.",
            start_time=base_date + timedelta(days=8, hours=8),
            end_time=base_date + timedelta(days=8, hours=9, minutes=30),
            location="Main Studio",
            creator_id=coach_thomas.id,
            class_type_id=grappling_type.id,
        )

        muay_thai_techniques = ClassModel(
            title="Muay Thai Techniques",
            description="Muay Thai focusing on elbows, knees, and clinch work.",
            start_time=base_date + timedelta(days=9, hours=12),
            end_time=base_date + timedelta(days=9, hours=13, minutes=30),
            location="Ring Area",
            creator_id=coach_kavanagh.id,
            class_type_id=kickboxing_type.id,
        )

        advanced_judo = ClassModel(
            title="Advanced Judo",
            description="Advanced judo techniques including advanced throws and counters.",
            start_time=base_date + timedelta(days=10, hours=11),
            end_time=base_date + timedelta(days=10, hours=12, minutes=30),
            location="Studio 1",
            creator_id=coach_thomas.id,
            class_type_id=judo_type.id,
        )

        judo_fundamentals = ClassModel(
            title="Judo Fundamentals",
            description="Judo fundamentals with an emphasis on practical application.",
            start_time=base_date + timedelta(days=11, hours=14),
            end_time=base_date + timedelta(days=11, hours=15, minutes=30),
            location="Studio 1",
            creator_id=coach_thomas.id,
            class_type_id=judo_type.id,
        )

        wrestling_for_combat = ClassModel(
            title="Wrestling for Combat",
            description="Intensive wrestling tactics for combat sports.",
            start_time=base_date + timedelta(days=12, hours=16),
            end_time=base_date + timedelta(days=12, hours=17, minutes=30),
            location="Studio 2",
            creator_id=coach_kavanagh.id,
            class_type_id=wrestling_type.id,
        )

        gi_jiu_jitsu_training = ClassModel(
            title="Gi Jiu Jitsu Training",
            description="Gi Jiu Jitsu techniques for competition.",
            start_time=base_date + timedelta(days=13, hours=18),
            end_time=base_date + timedelta(days=13, hours=19, minutes=30),
            location="Mat Area",
            creator_id=coach_kavanagh.id,
            class_type_id=gi_jiu_jitsu_type.id,
        )

        cardio_kickboxing = ClassModel(
            title="Cardio Kickboxing",
            description="High-energy kickboxing session to boost stamina and fitness.",
            start_time=base_date + timedelta(days=14, hours=6),
            end_time=base_date + timedelta(days=14, hours=7, minutes=30),
            location="Fitness Room",
            creator_id=coach_thomas.id,
            class_type_id=cardio_type.id,
        )

        beginner_bjj = ClassModel(
            title="Beginner BJJ",
            description="Introduction to Brazilian Jiu Jitsu for beginners.",
            start_time=base_date + timedelta(days=14, hours=8),
            end_time=base_date + timedelta(days=14, hours=9, minutes=30),
            location="Main Studio",
            creator_id=coach_thomas.id,
            class_type_id=gi_jiu_jitsu_type.id,
        )

        advanced_striking = ClassModel(
            title="Advanced Striking",
            description="Advanced striking techniques including combinations and footwork.",
            start_time=base_date + timedelta(days=15, hours=17),
            end_time=base_date + timedelta(days=15, hours=18, minutes=30),
            location="Studio 1",
            creator_id=coach_kavanagh.id,
            class_type_id=striking_type.id,
        )

        competitive_grappling = ClassModel(
            title="Competitive Grappling",
            description="Grappling techniques tailored for competition scenarios.",
            start_time=base_date + timedelta(days=16, hours=19),
            end_time=base_date + timedelta(days=16, hours=20, minutes=30),
            location="Main Studio",
            creator_id=coach_thomas.id,
            class_type_id=grappling_type.id,
        )

        db.session.add_all(
            [
                morning_mma,
                evening_boxing,
                brazilian_jiu_jitsu,
                no_gi_grappling,
                advanced_grappling,
                muay_thai_techniques,
                judo_fundamentals,
                wrestling_for_combat,
                gi_jiu_jitsu_training,
                cardio_kickboxing,
                beginner_bjj,
                advanced_mma,
                advanced_striking,
                competitive_grappling,
                advanced_judo,
            ]
        )

        db.session.commit()

        # Create Class Attendees
        classes_to_distribute = [
            morning_mma,
            evening_boxing,
            brazilian_jiu_jitsu,
            no_gi_grappling,
            advanced_grappling,
            muay_thai_techniques,
            judo_fundamentals,
            wrestling_for_combat,
            gi_jiu_jitsu_training,
            cardio_kickboxing,
            beginner_bjj,
        ]

        users = db.session.query(UserModel).all()
        user_iterator = cycle(users)

        attendees = [
            ClassAttendee(class_id=morning_mma.id, user_id=alan.id),
            ClassAttendee(class_id=evening_boxing.id, user_id=robert.id),
            ClassAttendee(class_id=brazilian_jiu_jitsu.id, user_id=kate.id),
            ClassAttendee(class_id=no_gi_grappling.id, user_id=dani.id),
            ClassAttendee(class_id=advanced_grappling.id, user_id=michael.id),
            ClassAttendee(class_id=muay_thai_techniques.id, user_id=chris.id),
            ClassAttendee(class_id=judo_fundamentals.id, user_id=josh.id),
            ClassAttendee(class_id=wrestling_for_combat.id, user_id=sarah.id),
            ClassAttendee(class_id=gi_jiu_jitsu_training.id, user_id=emily.id),
            ClassAttendee(class_id=cardio_kickboxing.id, user_id=alan.id),
            ClassAttendee(class_id=beginner_bjj.id, user_id=josh.id),
            ClassAttendee(class_id=beginner_bjj.id, user_id=chris.id),
        ]

        db.session.add_all(attendees)
        db.session.commit()

        users = db.session.query(UserModel).all()
        for user in users:
            print(
                f"User: {user.username}, is_admin: {user.is_admin}, is_coach: {user.is_coach}"
            )

        print("Seeding the data..")
    except Exception as e:
        print(f"An error occurred: {e}")
