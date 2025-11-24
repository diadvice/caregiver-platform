"""
Part 2: SQL Queries Implementation
All queries required for the project using SQLAlchemy
"""

from sqlalchemy import func, text, and_, or_
from database import SessionLocal
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment

def print_section(title):
    """Helper function to print section headers"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")

# =============================================================================
# 3. UPDATE SQL STATEMENTS
# =============================================================================

def update_3_1():
    """3.1 Update the phone number of Arman Armanov to +77773414141"""
    print_section("3.1 Update phone number of Arman Armanov")
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.given_name == 'Arman',
            User.surname == 'Armanov'
        ).first()
        
        if user:
            old_phone = user.phone_number
            user.phone_number = '+77773414141'
            db.commit()
            print(f"Updated Arman Armanov's phone number from {old_phone} to {user.phone_number}")
        else:
            print("Arman Armanov not found")
    finally:
        db.close()

def update_3_2():
    """3.2 Add $0.3 commission fee to hourly rate if < $10, or 10% if >= $10"""
    print_section("3.2 Update caregiver hourly rates with commission")
    
    db = SessionLocal()
    try:
        caregivers = db.query(Caregiver).all()
        
        for caregiver in caregivers:
            old_rate = float(caregiver.hourly_rate)
            if old_rate < 10:
                caregiver.hourly_rate = old_rate + 0.3
            else:
                caregiver.hourly_rate = old_rate * 1.10
            
            print(f"Caregiver ID {caregiver.caregiver_user_id}: ${old_rate:.2f} -> ${float(caregiver.hourly_rate):.2f}")
        
        db.commit()
        print(f"\nUpdated {len(caregivers)} caregiver rates")
    finally:
        db.close()

# =============================================================================
# 4. DELETE SQL STATEMENTS
# =============================================================================

def delete_4_1():
    """4.1 Delete the jobs posted by Amina Aminova"""
    print_section("4.1 Delete jobs posted by Amina Aminova")
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.given_name == 'Amina',
            User.surname == 'Aminova'
        ).first()
        
        if user and user.member:
            jobs = db.query(Job).filter(Job.member_user_id == user.member.member_user_id).all()
            count = len(jobs)
            
            for job in jobs:
                print(f"Deleting Job ID: {job.job_id} - {job.required_caregiving_type}")
                db.delete(job)
            
            db.commit()
            print(f"\nDeleted {count} jobs posted by Amina Aminova")
        else:
            print("Amina Aminova not found or not a member")
    finally:
        db.close()

def delete_4_2():
    """4.2 Delete all members who live on Kabanbay Batyr street"""
    print_section("4.2 Delete members living on Kabanbay Batyr street")
    
    db = SessionLocal()
    try:
        addresses = db.query(Address).filter(Address.street == 'Kabanbay Batyr').all()
        member_ids = [addr.member_user_id for addr in addresses]
        
        members = db.query(Member).filter(Member.member_user_id.in_(member_ids)).all()
        
        for member in members:
            user = db.query(User).filter(User.user_id == member.member_user_id).first()
            print(f"Deleting Member: {user.given_name} {user.surname}")
            db.delete(member)
            db.delete(user)
        
        db.commit()
        print(f"\nDeleted {len(members)} members living on Kabanbay Batyr street")
    finally:
        db.close()

# =============================================================================
# 5. SIMPLE QUERIES
# =============================================================================

def simple_5_1():
    """5.1 Select caregiver and member names for the accepted appointments"""
    print_section("5.1 Caregiver and member names for accepted appointments")
    
    db = SessionLocal()
    try:
        results = db.query(
            User.given_name.label('caregiver_name'),
            User.surname.label('caregiver_surname'),
            User.given_name.label('member_name'),
            User.surname.label('member_surname'),
            Appointment.appointment_date
        ).join(
            Caregiver, Caregiver.caregiver_user_id == Appointment.caregiver_user_id
        ).join(
            User, User.user_id == Caregiver.caregiver_user_id
        ).join(
            Member, Member.member_user_id == Appointment.member_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).all()
        
        # Need to fix this query - let me redo it properly
        results = db.query(
            Appointment.appointment_id,
            Appointment.appointment_date,
            Appointment.status
        ).filter(Appointment.status == 'accepted').all()
        
        for result in results:
            appointment = db.query(Appointment).filter(
                Appointment.appointment_id == result.appointment_id
            ).first()
            
            caregiver_user = db.query(User).filter(
                User.user_id == appointment.caregiver_user_id
            ).first()
            
            member_user = db.query(User).filter(
                User.user_id == appointment.member_user_id
            ).first()
            
            print(f"Caregiver: {caregiver_user.given_name} {caregiver_user.surname} | "
                  f"Member: {member_user.given_name} {member_user.surname} | "
                  f"Date: {appointment.appointment_date}")
        
        print(f"\nTotal accepted appointments: {len(results)}")
    finally:
        db.close()

def simple_5_2():
    """5.2 List job ids that contain 'soft-spoken' in their other requirements"""
    print_section("5.2 Jobs with 'soft-spoken' in requirements")
    
    db = SessionLocal()
    try:
        jobs = db.query(Job).filter(
            Job.other_requirements.like('%soft-spoken%')
        ).all()
        
        for job in jobs:
            print(f"Job ID: {job.job_id} - {job.required_caregiving_type}")
            print(f"  Requirements: {job.other_requirements}")
        
        print(f"\nTotal jobs with 'soft-spoken': {len(jobs)}")
    finally:
        db.close()

def simple_5_3():
    """5.3 List the work hours of all babysitter positions"""
    print_section("5.3 Work hours for babysitter positions")
    
    db = SessionLocal()
    try:
        results = db.query(
            Appointment.appointment_id,
            Appointment.work_hours,
            Appointment.appointment_date
        ).join(
            Caregiver, Caregiver.caregiver_user_id == Appointment.caregiver_user_id
        ).filter(
            Caregiver.caregiving_type == 'Babysitter'
        ).all()
        
        for result in results:
            print(f"Appointment ID: {result.appointment_id} - "
                  f"Work Hours: {result.work_hours} - "
                  f"Date: {result.appointment_date}")
        
        print(f"\nTotal babysitter appointments: {len(results)}")
    finally:
        db.close()

def simple_5_4():
    """5.4 List members looking for Elderly Care in Astana with 'No pets.' rule"""
    print_section("5.4 Members seeking Elderly Care in Astana with 'No pets.' rule")
    
    db = SessionLocal()
    try:
        results = db.query(User, Member).join(
            Member, Member.member_user_id == User.user_id
        ).filter(
            and_(
                User.city == 'Astana',
                Member.house_rules.like('%No pets.%')
            )
        ).all()
        
        for user, member in results:
            # Check if they posted elderly care jobs
            has_elderly_job = db.query(Job).filter(
                and_(
                    Job.member_user_id == member.member_user_id,
                    Job.required_caregiving_type == 'Elderly Care'
                )
            ).first()
            
            if has_elderly_job:
                print(f"Member: {user.given_name} {user.surname}")
                print(f"  City: {user.city}")
                print(f"  House Rules: {member.house_rules}")
                print()
        
    finally:
        db.close()

# =============================================================================
# 6. COMPLEX QUERIES
# =============================================================================

def complex_6_1():
    """6.1 Count the number of applicants for each job posted by a member"""
    print_section("6.1 Number of applicants per job")
    
    db = SessionLocal()
    try:
        results = db.query(
            Job.job_id,
            Job.required_caregiving_type,
            User.given_name,
            User.surname,
            func.count(JobApplication.caregiver_user_id).label('applicant_count')
        ).join(
            Member, Member.member_user_id == Job.member_user_id
        ).join(
            User, User.user_id == Member.member_user_id
        ).outerjoin(
            JobApplication, JobApplication.job_id == Job.job_id
        ).group_by(
            Job.job_id, Job.required_caregiving_type, User.given_name, User.surname
        ).all()
        
        for result in results:
            print(f"Job ID: {result.job_id} - {result.required_caregiving_type}")
            print(f"  Posted by: {result.given_name} {result.surname}")
            print(f"  Applicants: {result.applicant_count}")
            print()
        
    finally:
        db.close()

def complex_6_2():
    """6.2 Total hours spent by caregivers for all accepted appointments"""
    print_section("6.2 Total work hours per caregiver (accepted appointments)")
    
    db = SessionLocal()
    try:
        results = db.query(
            User.given_name,
            User.surname,
            Caregiver.caregiving_type,
            func.sum(Appointment.work_hours).label('total_hours')
        ).join(
            Caregiver, Caregiver.caregiver_user_id == User.user_id
        ).join(
            Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).group_by(
            User.given_name, User.surname, Caregiver.caregiving_type
        ).all()
        
        for result in results:
            print(f"Caregiver: {result.given_name} {result.surname}")
            print(f"  Type: {result.caregiving_type}")
            print(f"  Total Hours: {result.total_hours}")
            print()
        
    finally:
        db.close()

def complex_6_3():
    """6.3 Average pay of caregivers based on accepted appointments"""
    print_section("6.3 Average earnings per caregiver (accepted appointments)")
    
    db = SessionLocal()
    try:
        results = db.query(
            User.given_name,
            User.surname,
            Caregiver.hourly_rate,
            func.avg(Appointment.work_hours).label('avg_hours')
        ).join(
            Caregiver, Caregiver.caregiver_user_id == User.user_id
        ).join(
            Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).group_by(
            User.given_name, User.surname, Caregiver.hourly_rate
        ).all()
        
        for result in results:
            avg_pay = float(result.hourly_rate) * float(result.avg_hours or 0)
            print(f"Caregiver: {result.given_name} {result.surname}")
            print(f"  Hourly Rate: ${result.hourly_rate}")
            print(f"  Average Hours per Appointment: {result.avg_hours:.2f}")
            print(f"  Average Pay per Appointment: ${avg_pay:.2f}")
            print()
        
    finally:
        db.close()

def complex_6_4():
    """6.4 Caregivers who earn above average based on accepted appointments"""
    print_section("6.4 Caregivers earning above average")
    
    db = SessionLocal()
    try:
        # First, calculate overall average earnings
        avg_earnings_result = db.query(
            func.avg(Caregiver.hourly_rate * Appointment.work_hours).label('avg_earnings')
        ).join(
            Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).first()
        
        overall_avg = float(avg_earnings_result.avg_earnings or 0)
        print(f"Overall average earnings per appointment: ${overall_avg:.2f}\n")
        
        # Now find caregivers earning above average
        results = db.query(
            User.given_name,
            User.surname,
            Caregiver.hourly_rate,
            func.sum(Caregiver.hourly_rate * Appointment.work_hours).label('total_earnings'),
            func.count(Appointment.appointment_id).label('appointment_count')
        ).join(
            Caregiver, Caregiver.caregiver_user_id == User.user_id
        ).join(
            Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).group_by(
            User.given_name, User.surname, Caregiver.hourly_rate, Caregiver.caregiver_user_id
        ).having(
            func.avg(Caregiver.hourly_rate * Appointment.work_hours) > overall_avg
        ).all()
        
        for result in results:
            avg_per_appointment = float(result.total_earnings) / float(result.appointment_count)
            print(f"Caregiver: {result.given_name} {result.surname}")
            print(f"  Hourly Rate: ${result.hourly_rate}")
            print(f"  Total Earnings: ${result.total_earnings:.2f}")
            print(f"  Appointments: {result.appointment_count}")
            print(f"  Average per Appointment: ${avg_per_appointment:.2f}")
            print()
        
    finally:
        db.close()

# =============================================================================
# 7. QUERY WITH DERIVED ATTRIBUTE
# =============================================================================

def derived_7():
    """7. Calculate the total cost to pay for a caregiver for all accepted appointments"""
    print_section("7. Total cost for each caregiver (accepted appointments)")
    
    db = SessionLocal()
    try:
        results = db.query(
            User.given_name,
            User.surname,
            Caregiver.hourly_rate,
            Caregiver.caregiving_type,
            func.sum(Appointment.work_hours).label('total_hours'),
            func.sum(Caregiver.hourly_rate * Appointment.work_hours).label('total_cost')
        ).join(
            Caregiver, Caregiver.caregiver_user_id == User.user_id
        ).join(
            Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id
        ).filter(
            Appointment.status == 'accepted'
        ).group_by(
            User.given_name, User.surname, Caregiver.hourly_rate, Caregiver.caregiving_type
        ).all()
        
        grand_total = 0
        for result in results:
            print(f"Caregiver: {result.given_name} {result.surname}")
            print(f"  Type: {result.caregiving_type}")
            print(f"  Hourly Rate: ${result.hourly_rate}")
            print(f"  Total Hours: {result.total_hours}")
            print(f"  TOTAL COST: ${float(result.total_cost):.2f}")
            print()
            grand_total += float(result.total_cost)
        
        print(f"GRAND TOTAL for all caregivers: ${grand_total:.2f}")
        
    finally:
        db.close()

# =============================================================================
# 8. VIEW OPERATION
# =============================================================================

def view_8():
    """8. View all job applications and the applicants"""
    print_section("8. Job Applications View")
    
    db = SessionLocal()
    try:
        # Create a view-like query
        results = db.query(
            JobApplication.caregiver_user_id,
            JobApplication.job_id,
            JobApplication.date_applied,
            Job.required_caregiving_type,
            Job.other_requirements,
            User.given_name.label('member_name'),
            User.surname.label('member_surname')
        ).join(
            Job, Job.job_id == JobApplication.job_id
        ).join(
            Member, Member.member_user_id == Job.member_user_id
        ).join(
            User, User.user_id == Member.member_user_id
        ).all()
        
        for result in results:
            # Get caregiver info
            application = db.query(JobApplication).filter(
                JobApplication.caregiver_user_id == result.caregiver_user_id,
                JobApplication.job_id == result.job_id
            ).first()
            
            caregiver_user = db.query(User).filter(
                User.user_id == application.caregiver_user_id
            ).first()
            
            print(f"Application: Caregiver {result.caregiver_user_id} -> Job {result.job_id}")
            print(f"  Job Type: {result.required_caregiving_type}")
            print(f"  Posted by: {result.member_name} {result.member_surname}")
            print(f"  Applicant: {caregiver_user.given_name} {caregiver_user.surname}")
            print(f"  Date Applied: {result.date_applied}")
            print(f"  Requirements: {result.other_requirements}")
            print()
        
        print(f"Total applications: {len(results)}")
        
    finally:
        db.close()

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_all_queries():
    """Run all queries in sequence"""
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*20 + "PART 2: SQL QUERIES EXECUTION" + " "*28 + "#")
    print("#" + " "*78 + "#")
    print("#"*80)
    
    # Update queries
    update_3_1()
    update_3_2()
    
    # Delete queries
    delete_4_1()
    delete_4_2()
    
    # Simple queries
    simple_5_1()
    simple_5_2()
    simple_5_3()
    simple_5_4()
    
    # Complex queries
    complex_6_1()
    complex_6_2()
    complex_6_3()
    complex_6_4()
    
    # Derived attribute query
    derived_7()
    
    # View operation
    view_8()
    
    print("\n" + "#"*80)
    print("#" + " "*25 + "ALL QUERIES COMPLETED" + " "*32 + "#")
    print("#"*80 + "\n")

if __name__ == "__main__":
    run_all_queries()
