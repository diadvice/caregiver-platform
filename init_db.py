from datetime import date, time
from database import engine, SessionLocal
from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment

def drop_all_tables():
    """Drop all tables"""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

def create_all_tables():
    """Create all tables"""
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created.")

def insert_sample_data():
    """Insert sample data into all tables"""
    db = SessionLocal()
    
    try:
        print("Inserting sample data...")
        
        # Insert Users (15 users - 10 caregivers, 10 members, 5 are both)
        users_data = [
            # Caregivers
            {"email": "sarah.johnson@email.com", "given_name": "Sarah", "surname": "Johnson", 
             "city": "Astana", "phone_number": "+77011234567", 
             "profile_description": "Experienced babysitter with 5 years of experience.", "password": "pass123"},
            {"email": "mike.peterson@email.com", "given_name": "Mike", "surname": "Peterson", 
             "city": "Almaty", "phone_number": "+77011234568", 
             "profile_description": "Certified elderly care specialist.", "password": "pass123"},
            {"email": "emma.wilson@email.com", "given_name": "Emma", "surname": "Wilson", 
             "city": "Astana", "phone_number": "+77011234569", 
             "profile_description": "Professional playmate for children.", "password": "pass123"},
            {"email": "david.brown@email.com", "given_name": "David", "surname": "Brown", 
             "city": "Shymkent", "phone_number": "+77011234570", 
             "profile_description": "Loving babysitter with pediatric first aid training.", "password": "pass123"},
            {"email": "lisa.anderson@email.com", "given_name": "Lisa", "surname": "Anderson", 
             "city": "Astana", "phone_number": "+77011234571", 
             "profile_description": "Patient elderly caregiver with nursing background.", "password": "pass123"},
            {"email": "john.martinez@email.com", "given_name": "John", "surname": "Martinez", 
             "city": "Almaty", "phone_number": "+77011234572", 
             "profile_description": "Fun and energetic playmate for kids.", "password": "pass123"},
            {"email": "anna.taylor@email.com", "given_name": "Anna", "surname": "Taylor", 
             "city": "Astana", "phone_number": "+77011234573", 
             "profile_description": "Reliable babysitter with references.", "password": "pass123"},
            {"email": "robert.thomas@email.com", "given_name": "Robert", "surname": "Thomas", 
             "city": "Karaganda", "phone_number": "+77011234574", 
             "profile_description": "Compassionate elderly care provider.", "password": "pass123"},
            {"email": "maria.garcia@email.com", "given_name": "Maria", "surname": "Garcia", 
             "city": "Astana", "phone_number": "+77011234575", 
             "profile_description": "Creative playmate with art education.", "password": "pass123"},
            {"email": "james.lee@email.com", "given_name": "James", "surname": "Lee", 
             "city": "Almaty", "phone_number": "+77011234576", 
             "profile_description": "Experienced babysitter for infants and toddlers.", "password": "pass123"},
            
            # Members
            {"email": "amina.aminova@email.com", "given_name": "Amina", "surname": "Aminova", 
             "city": "Astana", "phone_number": "+77011234577", 
             "profile_description": "Looking for reliable childcare.", "password": "pass123"},
            {"email": "arman.armanov@email.com", "given_name": "Arman", "surname": "Armanov", 
             "city": "Almaty", "phone_number": "+77011234578", 
             "profile_description": "Need elderly care for my mother.", "password": "pass123"},
            {"email": "diana.kim@email.com", "given_name": "Diana", "surname": "Kim", 
             "city": "Astana", "phone_number": "+77011234579", 
             "profile_description": "Seeking playmate for my 6-year-old.", "password": "pass123"},
            {"email": "nurlan.bekov@email.com", "given_name": "Nurlan", "surname": "Bekov", 
             "city": "Shymkent", "phone_number": "+77011234580", 
             "profile_description": "Need babysitter for weekends.", "password": "pass123"},
            {"email": "zarina.saparova@email.com", "given_name": "Zarina", "surname": "Saparova", 
             "city": "Astana", "phone_number": "+77011234581", 
             "profile_description": "Looking for elderly care specialist.", "password": "pass123"},
            {"email": "timur.omarov@email.com", "given_name": "Timur", "surname": "Omarov", 
             "city": "Almaty", "phone_number": "+77011234582", 
             "profile_description": "Need someone to play with my children.", "password": "pass123"},
            {"email": "aida.sultanova@email.com", "given_name": "Aida", "surname": "Sultanova", 
             "city": "Astana", "phone_number": "+77011234583", 
             "profile_description": "Seeking babysitter for my twin girls.", "password": "pass123"},
            {"email": "yerlan.nazarov@email.com", "given_name": "Yerlan", "surname": "Nazarov", 
             "city": "Karaganda", "phone_number": "+77011234584", 
             "profile_description": "Need caregiver for elderly father.", "password": "pass123"},
            {"email": "gulnara.tokayeva@email.com", "given_name": "Gulnara", "surname": "Tokayeva", 
             "city": "Astana", "phone_number": "+77011234585", 
             "profile_description": "Looking for afternoon playmate.", "password": "pass123"},
            {"email": "serik.mustafin@email.com", "given_name": "Serik", "surname": "Mustafin", 
             "city": "Almaty", "phone_number": "+77011234586", 
             "profile_description": "Need reliable babysitter urgently.", "password": "pass123"},
        ]
        
        users = []
        for user_data in users_data:
            password = user_data.pop('password')
            user = User(**user_data)
            user.set_password(password)
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"Inserted {len(users)} users.")
        
        # Refresh to get IDs
        for user in users:
            db.refresh(user)
        
        # Insert Caregivers (first 10 users are caregivers)
        caregivers_data = [
            {"caregiver_user_id": users[0].user_id, "photo": "sarah_photo.jpg", "gender": "Female", 
             "caregiving_type": "Babysitter", "hourly_rate": 12.50},
            {"caregiver_user_id": users[1].user_id, "photo": "mike_photo.jpg", "gender": "Male", 
             "caregiving_type": "Elderly Care", "hourly_rate": 15.00},
            {"caregiver_user_id": users[2].user_id, "photo": "emma_photo.jpg", "gender": "Female", 
             "caregiving_type": "Playmate", "hourly_rate": 10.00},
            {"caregiver_user_id": users[3].user_id, "photo": "david_photo.jpg", "gender": "Male", 
             "caregiving_type": "Babysitter", "hourly_rate": 11.00},
            {"caregiver_user_id": users[4].user_id, "photo": "lisa_photo.jpg", "gender": "Female", 
             "caregiving_type": "Elderly Care", "hourly_rate": 16.50},
            {"caregiver_user_id": users[5].user_id, "photo": "john_photo.jpg", "gender": "Male", 
             "caregiving_type": "Playmate", "hourly_rate": 9.50},
            {"caregiver_user_id": users[6].user_id, "photo": "anna_photo.jpg", "gender": "Female", 
             "caregiving_type": "Babysitter", "hourly_rate": 13.00},
            {"caregiver_user_id": users[7].user_id, "photo": "robert_photo.jpg", "gender": "Male", 
             "caregiving_type": "Elderly Care", "hourly_rate": 14.00},
            {"caregiver_user_id": users[8].user_id, "photo": "maria_photo.jpg", "gender": "Female", 
             "caregiving_type": "Playmate", "hourly_rate": 8.50},
            {"caregiver_user_id": users[9].user_id, "photo": "james_photo.jpg", "gender": "Male", 
             "caregiving_type": "Babysitter", "hourly_rate": 12.00},
        ]
        
        caregivers = []
        for caregiver_data in caregivers_data:
            caregiver = Caregiver(**caregiver_data)
            db.add(caregiver)
            caregivers.append(caregiver)
        
        db.commit()
        print(f"Inserted {len(caregivers)} caregivers.")
        
        # Insert Members (last 10 users are members)
        members_data = [
            {"member_user_id": users[10].user_id, "house_rules": "No smoking. No pets.", 
             "dependent_description": "5-year-old son who likes painting and reading."},
            {"member_user_id": users[11].user_id, "house_rules": "Quiet environment preferred.", 
             "dependent_description": "82-year-old mother with limited mobility."},
            {"member_user_id": users[12].user_id, "house_rules": "Must be punctual. No pets.", 
             "dependent_description": "6-year-old daughter who loves outdoor activities."},
            {"member_user_id": users[13].user_id, "house_rules": "Non-smoker only.", 
             "dependent_description": "3-year-old twins, very energetic."},
            {"member_user_id": users[14].user_id, "house_rules": "Experience with dementia required. No pets.", 
             "dependent_description": "78-year-old grandmother with early-stage dementia."},
            {"member_user_id": users[15].user_id, "house_rules": "Pets friendly.", 
             "dependent_description": "Two children aged 4 and 7, love playing games."},
            {"member_user_id": users[16].user_id, "house_rules": "Must follow strict schedule.", 
             "dependent_description": "8-month-old baby girl and 3-year-old boy."},
            {"member_user_id": users[17].user_id, "house_rules": "Medical background preferred.", 
             "dependent_description": "85-year-old father with diabetes."},
            {"member_user_id": users[18].user_id, "house_rules": "Outdoor play encouraged. No pets.", 
             "dependent_description": "5-year-old boy who loves sports."},
            {"member_user_id": users[19].user_id, "house_rules": "Must be reliable and on time.", 
             "dependent_description": "2-year-old daughter, very curious and active."},
        ]
        
        members = []
        for member_data in members_data:
            member = Member(**member_data)
            db.add(member)
            members.append(member)
        
        db.commit()
        print(f"Inserted {len(members)} members.")
        
        # Insert Addresses (one for each member)
        addresses_data = [
            {"member_user_id": members[0].member_user_id, "house_number": "15", "street": "Kabanbay Batyr", "town": "Esil District"},
            {"member_user_id": members[1].member_user_id, "house_number": "42", "street": "Abay Avenue", "town": "Almaly District"},
            {"member_user_id": members[2].member_user_id, "house_number": "7", "street": "Mangilik El", "town": "Esil District"},
            {"member_user_id": members[3].member_user_id, "house_number": "88", "street": "Respublika Avenue", "town": "Central District"},
            {"member_user_id": members[4].member_user_id, "house_number": "23", "street": "Syganak Street", "town": "Baykonur District"},
            {"member_user_id": members[5].member_user_id, "house_number": "56", "street": "Dostyk Avenue", "town": "Medeu District"},
            {"member_user_id": members[6].member_user_id, "house_number": "31", "street": "Turan Avenue", "town": "Esil District"},
            {"member_user_id": members[7].member_user_id, "house_number": "99", "street": "Bukhar Zhyrau", "town": "Oktyabrsky District"},
            {"member_user_id": members[8].member_user_id, "house_number": "12", "street": "Kabanbay Batyr", "town": "Saryarka District"},
            {"member_user_id": members[9].member_user_id, "house_number": "67", "street": "Satpaev Street", "town": "Almaly District"},
        ]
        
        addresses = []
        for address_data in addresses_data:
            address = Address(**address_data)
            db.add(address)
            addresses.append(address)
        
        db.commit()
        print(f"Inserted {len(addresses)} addresses.")
        
        # Insert Jobs (10 jobs from members)
        jobs_data = [
            {"member_user_id": members[0].member_user_id, "required_caregiving_type": "Babysitter", 
             "other_requirements": "Looking for patient and soft-spoken babysitter. Must have experience with young children.", 
             "date_posted": date(2024, 11, 1)},
            {"member_user_id": members[1].member_user_id, "required_caregiving_type": "Elderly Care", 
             "other_requirements": "Need someone with medical background. Soft-spoken preferred.", 
             "date_posted": date(2024, 11, 2)},
            {"member_user_id": members[2].member_user_id, "required_caregiving_type": "Playmate", 
             "other_requirements": "Active person needed for outdoor activities.", 
             "date_posted": date(2024, 11, 3)},
            {"member_user_id": members[3].member_user_id, "required_caregiving_type": "Babysitter", 
             "other_requirements": "Must be experienced with twins. Energy required!", 
             "date_posted": date(2024, 11, 4)},
            {"member_user_id": members[4].member_user_id, "required_caregiving_type": "Elderly Care", 
             "other_requirements": "Dementia care experience essential. Patient and soft-spoken.", 
             "date_posted": date(2024, 11, 5)},
            {"member_user_id": members[5].member_user_id, "required_caregiving_type": "Playmate", 
             "other_requirements": "Must love playing board games and outdoor sports.", 
             "date_posted": date(2024, 11, 6)},
            {"member_user_id": members[6].member_user_id, "required_caregiving_type": "Babysitter", 
             "other_requirements": "Need someone reliable for evening hours.", 
             "date_posted": date(2024, 11, 7)},
            {"member_user_id": members[7].member_user_id, "required_caregiving_type": "Elderly Care", 
             "other_requirements": "Diabetes management knowledge required.", 
             "date_posted": date(2024, 11, 8)},
            {"member_user_id": members[8].member_user_id, "required_caregiving_type": "Playmate", 
             "other_requirements": "Sports enthusiast preferred. Outdoor activities.", 
             "date_posted": date(2024, 11, 9)},
            {"member_user_id": members[9].member_user_id, "required_caregiving_type": "Babysitter", 
             "other_requirements": "Morning hours, must be punctual and soft-spoken.", 
             "date_posted": date(2024, 11, 10)},
        ]
        
        jobs = []
        for job_data in jobs_data:
            job = Job(**job_data)
            db.add(job)
            jobs.append(job)
        
        db.commit()
        print(f"Inserted {len(jobs)} jobs.")
        
        # Refresh to get IDs
        for job in jobs:
            db.refresh(job)
        
        # Insert Job Applications (multiple applications per job)
        job_applications_data = [
            # Job 1 applications
            {"caregiver_user_id": caregivers[0].caregiver_user_id, "job_id": jobs[0].job_id, "date_applied": date(2024, 11, 2)},
            {"caregiver_user_id": caregivers[3].caregiver_user_id, "job_id": jobs[0].job_id, "date_applied": date(2024, 11, 3)},
            {"caregiver_user_id": caregivers[6].caregiver_user_id, "job_id": jobs[0].job_id, "date_applied": date(2024, 11, 4)},
            # Job 2 applications
            {"caregiver_user_id": caregivers[1].caregiver_user_id, "job_id": jobs[1].job_id, "date_applied": date(2024, 11, 3)},
            {"caregiver_user_id": caregivers[4].caregiver_user_id, "job_id": jobs[1].job_id, "date_applied": date(2024, 11, 4)},
            # Job 3 applications
            {"caregiver_user_id": caregivers[2].caregiver_user_id, "job_id": jobs[2].job_id, "date_applied": date(2024, 11, 4)},
            {"caregiver_user_id": caregivers[5].caregiver_user_id, "job_id": jobs[2].job_id, "date_applied": date(2024, 11, 5)},
            # Job 4 applications
            {"caregiver_user_id": caregivers[0].caregiver_user_id, "job_id": jobs[3].job_id, "date_applied": date(2024, 11, 5)},
            {"caregiver_user_id": caregivers[9].caregiver_user_id, "job_id": jobs[3].job_id, "date_applied": date(2024, 11, 6)},
            # Job 5 applications
            {"caregiver_user_id": caregivers[7].caregiver_user_id, "job_id": jobs[4].job_id, "date_applied": date(2024, 11, 6)},
            # Job 6 applications
            {"caregiver_user_id": caregivers[8].caregiver_user_id, "job_id": jobs[5].job_id, "date_applied": date(2024, 11, 7)},
            {"caregiver_user_id": caregivers[2].caregiver_user_id, "job_id": jobs[5].job_id, "date_applied": date(2024, 11, 8)},
            # Job 7 applications
            {"caregiver_user_id": caregivers[6].caregiver_user_id, "job_id": jobs[6].job_id, "date_applied": date(2024, 11, 8)},
            # Job 8 applications
            {"caregiver_user_id": caregivers[1].caregiver_user_id, "job_id": jobs[7].job_id, "date_applied": date(2024, 11, 9)},
            {"caregiver_user_id": caregivers[4].caregiver_user_id, "job_id": jobs[7].job_id, "date_applied": date(2024, 11, 10)},
        ]
        
        job_applications = []
        for app_data in job_applications_data:
            application = JobApplication(**app_data)
            db.add(application)
            job_applications.append(application)
        
        db.commit()
        print(f"Inserted {len(job_applications)} job applications.")
        
        # Insert Appointments (mix of pending, accepted, declined)
        appointments_data = [
            {"caregiver_user_id": caregivers[0].caregiver_user_id, "member_user_id": members[0].member_user_id, 
             "appointment_date": date(2024, 11, 15), "appointment_time": time(9, 0), "work_hours": 4.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[1].caregiver_user_id, "member_user_id": members[1].member_user_id, 
             "appointment_date": date(2024, 11, 16), "appointment_time": time(10, 0), "work_hours": 6.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[2].caregiver_user_id, "member_user_id": members[2].member_user_id, 
             "appointment_date": date(2024, 11, 17), "appointment_time": time(14, 0), "work_hours": 3.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[3].caregiver_user_id, "member_user_id": members[3].member_user_id, 
             "appointment_date": date(2024, 11, 18), "appointment_time": time(8, 0), "work_hours": 5.0, "status": "pending"},
            {"caregiver_user_id": caregivers[4].caregiver_user_id, "member_user_id": members[4].member_user_id, 
             "appointment_date": date(2024, 11, 19), "appointment_time": time(11, 0), "work_hours": 8.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[5].caregiver_user_id, "member_user_id": members[5].member_user_id, 
             "appointment_date": date(2024, 11, 20), "appointment_time": time(15, 0), "work_hours": 2.5, "status": "declined"},
            {"caregiver_user_id": caregivers[6].caregiver_user_id, "member_user_id": members[6].member_user_id, 
             "appointment_date": date(2024, 11, 21), "appointment_time": time(18, 0), "work_hours": 4.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[7].caregiver_user_id, "member_user_id": members[7].member_user_id, 
             "appointment_date": date(2024, 11, 22), "appointment_time": time(9, 30), "work_hours": 7.0, "status": "accepted"},
            {"caregiver_user_id": caregivers[8].caregiver_user_id, "member_user_id": members[8].member_user_id, 
             "appointment_date": date(2024, 11, 23), "appointment_time": time(13, 0), "work_hours": 3.5, "status": "pending"},
            {"caregiver_user_id": caregivers[9].caregiver_user_id, "member_user_id": members[9].member_user_id, 
             "appointment_date": date(2024, 11, 24), "appointment_time": time(7, 0), "work_hours": 5.5, "status": "accepted"},
            {"caregiver_user_id": caregivers[0].caregiver_user_id, "member_user_id": members[2].member_user_id, 
             "appointment_date": date(2024, 11, 25), "appointment_time": time(10, 0), "work_hours": 4.0, "status": "accepted"},
        ]
        
        appointments = []
        for appointment_data in appointments_data:
            appointment = Appointment(**appointment_data)
            db.add(appointment)
            appointments.append(appointment)
        
        db.commit()
        print(f"Inserted {len(appointments)} appointments.")
        
        print("\n=== Sample data insertion completed successfully! ===")
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_database():
    """Initialize database: drop existing tables, create new ones, and insert sample data"""
    drop_all_tables()
    create_all_tables()
    insert_sample_data()

if __name__ == "__main__":
    init_database()
