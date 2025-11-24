import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date, time
from database import SessionLocal
from models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
from sqlalchemy import desc

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database session helper
def get_db():
    return SessionLocal()

# ==================== HOME & DASHBOARD ====================

@app.route('/')
def index():
    """Home page with statistics"""
    db = get_db()
    try:
        stats = {
            'caregivers': db.query(Caregiver).count(),
            'members': db.query(Member).count(),
            'jobs': db.query(Job).count(),
            'appointments': db.query(Appointment).count(),
        }
        return render_template('index.html', stats=stats)
    finally:
        db.close()

# ==================== USERS CRUD ====================

@app.route('/users')
def users_list():
    """List all users"""
    db = get_db()
    try:
        users = db.query(User).all()
        return render_template('users/list.html', users=users)
    finally:
        db.close()

@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    """Create a new user"""
    if request.method == 'POST':
        db = get_db()
        try:
            user = User(
                email=request.form['email'],
                given_name=request.form['given_name'],
                surname=request.form['surname'],
                city=request.form['city'],
                phone_number=request.form['phone_number'],
                profile_description=request.form['profile_description']
            )
            user.set_password(request.form['password'])
            db.add(user)
            db.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'danger')
        finally:
            db.close()
    
    return render_template('users/create.html')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def users_edit(user_id):
    """Edit a user"""
    db = get_db()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('users_list'))
        
        if request.method == 'POST':
            user.email = request.form['email']
            user.given_name = request.form['given_name']
            user.surname = request.form['surname']
            user.city = request.form['city']
            user.phone_number = request.form['phone_number']
            user.profile_description = request.form['profile_description']
            if request.form['password']:
                user.set_password(request.form['password'])
            db.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('users_list'))
        
        return render_template('users/edit.html', user=user)
    finally:
        db.close()

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete a user"""
    db = get_db()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('users_list'))

# ==================== CAREGIVERS CRUD ====================

@app.route('/caregivers')
def caregivers_list():
    """List all caregivers"""
    db = get_db()
    try:
        caregivers = db.query(Caregiver, User).join(User).all()
        return render_template('caregivers/list.html', caregivers=caregivers)
    finally:
        db.close()

@app.route('/caregivers/create', methods=['GET', 'POST'])
def caregivers_create():
    """Create a new caregiver"""
    db = get_db()
    try:
        if request.method == 'POST':
            caregiver = Caregiver(
                caregiver_user_id=request.form['caregiver_user_id'],
                photo=request.form['photo'],
                gender=request.form['gender'],
                caregiving_type=request.form['caregiving_type'],
                hourly_rate=request.form['hourly_rate']
            )
            db.add(caregiver)
            db.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        
        # Get users who are not yet caregivers
        users = db.query(User).filter(~User.user_id.in_(
            db.query(Caregiver.caregiver_user_id)
        )).all()
        return render_template('caregivers/create.html', users=users)
    except Exception as e:
        flash(f'Error creating caregiver: {str(e)}', 'danger')
        return redirect(url_for('caregivers_list'))
    finally:
        db.close()

@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
def caregivers_edit(caregiver_id):
    """Edit a caregiver"""
    db = get_db()
    try:
        caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()
        if not caregiver:
            flash('Caregiver not found!', 'danger')
            return redirect(url_for('caregivers_list'))
        
        if request.method == 'POST':
            caregiver.photo = request.form['photo']
            caregiver.gender = request.form['gender']
            caregiver.caregiving_type = request.form['caregiving_type']
            caregiver.hourly_rate = request.form['hourly_rate']
            db.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('caregivers_list'))
        
        user = db.query(User).filter(User.user_id == caregiver.caregiver_user_id).first()
        return render_template('caregivers/edit.html', caregiver=caregiver, user=user)
    finally:
        db.close()

@app.route('/caregivers/<int:caregiver_id>/delete', methods=['POST'])
def caregivers_delete(caregiver_id):
    """Delete a caregiver"""
    db = get_db()
    try:
        caregiver = db.query(Caregiver).filter(Caregiver.caregiver_user_id == caregiver_id).first()
        if caregiver:
            db.delete(caregiver)
            db.commit()
            flash('Caregiver deleted successfully!', 'success')
        else:
            flash('Caregiver not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting caregiver: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('caregivers_list'))

# ==================== MEMBERS CRUD ====================

@app.route('/members')
def members_list():
    """List all members"""
    db = get_db()
    try:
        members = db.query(Member, User).join(User).all()
        return render_template('members/list.html', members=members)
    finally:
        db.close()

@app.route('/members/create', methods=['GET', 'POST'])
def members_create():
    """Create a new member"""
    db = get_db()
    try:
        if request.method == 'POST':
            member = Member(
                member_user_id=request.form['member_user_id'],
                house_rules=request.form['house_rules'],
                dependent_description=request.form['dependent_description']
            )
            db.add(member)
            db.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('members_list'))
        
        # Get users who are not yet members
        users = db.query(User).filter(~User.user_id.in_(
            db.query(Member.member_user_id)
        )).all()
        return render_template('members/create.html', users=users)
    except Exception as e:
        flash(f'Error creating member: {str(e)}', 'danger')
        return redirect(url_for('members_list'))
    finally:
        db.close()

@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def members_edit(member_id):
    """Edit a member"""
    db = get_db()
    try:
        member = db.query(Member).filter(Member.member_user_id == member_id).first()
        if not member:
            flash('Member not found!', 'danger')
            return redirect(url_for('members_list'))
        
        if request.method == 'POST':
            member.house_rules = request.form['house_rules']
            member.dependent_description = request.form['dependent_description']
            db.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('members_list'))
        
        user = db.query(User).filter(User.user_id == member.member_user_id).first()
        return render_template('members/edit.html', member=member, user=user)
    finally:
        db.close()

@app.route('/members/<int:member_id>/delete', methods=['POST'])
def members_delete(member_id):
    """Delete a member"""
    db = get_db()
    try:
        member = db.query(Member).filter(Member.member_user_id == member_id).first()
        if member:
            db.delete(member)
            db.commit()
            flash('Member deleted successfully!', 'success')
        else:
            flash('Member not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting member: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('members_list'))

# ==================== ADDRESSES CRUD ====================

@app.route('/addresses')
def addresses_list():
    """List all addresses"""
    db = get_db()
    try:
        addresses = db.query(Address, User).join(
            Member, Member.member_user_id == Address.member_user_id
        ).join(User, User.user_id == Member.member_user_id).all()
        return render_template('addresses/list.html', addresses=addresses)
    finally:
        db.close()

@app.route('/addresses/create', methods=['GET', 'POST'])
def addresses_create():
    """Create a new address"""
    db = get_db()
    try:
        if request.method == 'POST':
            address = Address(
                member_user_id=request.form['member_user_id'],
                house_number=request.form['house_number'],
                street=request.form['street'],
                town=request.form['town']
            )
            db.add(address)
            db.commit()
            flash('Address created successfully!', 'success')
            return redirect(url_for('addresses_list'))
        
        members = db.query(Member, User).join(User).all()
        return render_template('addresses/create.html', members=members)
    except Exception as e:
        flash(f'Error creating address: {str(e)}', 'danger')
        return redirect(url_for('addresses_list'))
    finally:
        db.close()

@app.route('/addresses/<int:member_id>/edit', methods=['GET', 'POST'])
def addresses_edit(member_id):
    """Edit an address"""
    db = get_db()
    try:
        address = db.query(Address).filter(Address.member_user_id == member_id).first()
        if not address:
            flash('Address not found!', 'danger')
            return redirect(url_for('addresses_list'))
        
        if request.method == 'POST':
            address.house_number = request.form['house_number']
            address.street = request.form['street']
            address.town = request.form['town']
            db.commit()
            flash('Address updated successfully!', 'success')
            return redirect(url_for('addresses_list'))
        
        member = db.query(Member, User).join(User).filter(
            Member.member_user_id == address.member_user_id
        ).first()
        return render_template('addresses/edit.html', address=address, member=member)
    finally:
        db.close()

@app.route('/addresses/<int:member_id>/delete', methods=['POST'])
def addresses_delete(member_id):
    """Delete an address"""
    db = get_db()
    try:
        address = db.query(Address).filter(Address.member_user_id == member_id).first()
        if address:
            db.delete(address)
            db.commit()
            flash('Address deleted successfully!', 'success')
        else:
            flash('Address not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting address: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('addresses_list'))

# ==================== JOBS CRUD ====================

@app.route('/jobs')
def jobs_list():
    """List all jobs"""
    db = get_db()
    try:
        jobs = db.query(Job, User).join(
            Member, Member.member_user_id == Job.member_user_id
        ).join(User, User.user_id == Member.member_user_id).all()
        return render_template('jobs/list.html', jobs=jobs)
    finally:
        db.close()

@app.route('/jobs/create', methods=['GET', 'POST'])
def jobs_create():
    """Create a new job"""
    db = get_db()
    try:
        if request.method == 'POST':
            job = Job(
                member_user_id=request.form['member_user_id'],
                required_caregiving_type=request.form['required_caregiving_type'],
                other_requirements=request.form['other_requirements'],
                date_posted=datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            )
            db.add(job)
            db.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('jobs_list'))
        
        members = db.query(Member, User).join(User).all()
        return render_template('jobs/create.html', members=members)
    except Exception as e:
        flash(f'Error creating job: {str(e)}', 'danger')
        return redirect(url_for('jobs_list'))
    finally:
        db.close()

@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def jobs_edit(job_id):
    """Edit a job"""
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            flash('Job not found!', 'danger')
            return redirect(url_for('jobs_list'))
        
        if request.method == 'POST':
            job.required_caregiving_type = request.form['required_caregiving_type']
            job.other_requirements = request.form['other_requirements']
            job.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%d').date()
            db.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs_list'))
        
        member = db.query(Member, User).join(User).filter(
            Member.member_user_id == job.member_user_id
        ).first()
        return render_template('jobs/edit.html', job=job, member=member)
    finally:
        db.close()

@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def jobs_delete(job_id):
    """Delete a job"""
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if job:
            db.delete(job)
            db.commit()
            flash('Job deleted successfully!', 'success')
        else:
            flash('Job not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting job: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('jobs_list'))

# ==================== JOB APPLICATIONS CRUD ====================

@app.route('/applications')
def applications_list():
    """List all job applications"""
    db = get_db()
    try:
        applications = db.query(JobApplication).all()
        app_details = []
        for app in applications:
            caregiver_user = db.query(User).filter(
                User.user_id == app.caregiver_user_id
            ).first()
            job = db.query(Job).filter(Job.job_id == app.job_id).first()
            app_details.append((app, caregiver_user, job))
        
        return render_template('applications/list.html', applications=app_details)
    finally:
        db.close()

@app.route('/applications/create', methods=['GET', 'POST'])
def applications_create():
    """Create a new job application"""
    db = get_db()
    try:
        if request.method == 'POST':
            application = JobApplication(
                caregiver_user_id=request.form['caregiver_user_id'],
                job_id=request.form['job_id'],
                date_applied=datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
            )
            db.add(application)
            db.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('applications_list'))
        
        caregivers = db.query(Caregiver, User).join(User).all()
        jobs = db.query(Job).all()
        return render_template('applications/create.html', caregivers=caregivers, jobs=jobs)
    except Exception as e:
        flash(f'Error creating application: {str(e)}', 'danger')
        return redirect(url_for('applications_list'))
    finally:
        db.close()

@app.route('/applications/<int:caregiver_id>/<int:job_id>/edit', methods=['GET', 'POST'])
def applications_edit(caregiver_id, job_id):
    """Edit a job application"""
    db = get_db()
    try:
        application = db.query(JobApplication).filter(
            JobApplication.caregiver_user_id == caregiver_id,
            JobApplication.job_id == job_id
        ).first()
        if not application:
            flash('Job application not found!', 'danger')
            return redirect(url_for('applications_list'))
        
        if request.method == 'POST':
            application.date_applied = datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
            db.commit()
            flash('Job application updated successfully!', 'success')
            return redirect(url_for('applications_list'))
        
        caregiver_user = db.query(User).filter(
            User.user_id == application.caregiver_user_id
        ).first()
        job = db.query(Job).filter(Job.job_id == application.job_id).first()
        
        return render_template('applications/edit.html', 
                             application=application,
                             caregiver_user=caregiver_user,
                             job=job)
    finally:
        db.close()

@app.route('/applications/<int:caregiver_id>/<int:job_id>/delete', methods=['POST'])
def applications_delete(caregiver_id, job_id):
    """Delete a job application"""
    db = get_db()
    try:
        application = db.query(JobApplication).filter(
            JobApplication.caregiver_user_id == caregiver_id,
            JobApplication.job_id == job_id
        ).first()
        if application:
            db.delete(application)
            db.commit()
            flash('Job application deleted successfully!', 'success')
        else:
            flash('Job application not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting application: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('applications_list'))

# ==================== APPOINTMENTS CRUD ====================

@app.route('/appointments')
def appointments_list():
    """List all appointments"""
    db = get_db()
    try:
        appointments = db.query(Appointment).all()
        appt_details = []
        for appt in appointments:
            caregiver_user = db.query(User).filter(
                User.user_id == appt.caregiver_user_id
            ).first()
            member_user = db.query(User).filter(
                User.user_id == appt.member_user_id
            ).first()
            appt_details.append((appt, caregiver_user, member_user))
        
        return render_template('appointments/list.html', appointments=appt_details)
    finally:
        db.close()

@app.route('/appointments/create', methods=['GET', 'POST'])
def appointments_create():
    """Create a new appointment"""
    db = get_db()
    try:
        if request.method == 'POST':
            appointment = Appointment(
                caregiver_user_id=request.form['caregiver_user_id'],
                member_user_id=request.form['member_user_id'],
                appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(request.form['appointment_time'], '%H:%M').time(),
                work_hours=request.form['work_hours'],
                status=request.form['status']
            )
            db.add(appointment)
            db.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('appointments_list'))
        
        caregivers = db.query(Caregiver, User).join(User).all()
        members = db.query(Member, User).join(User).all()
        return render_template('appointments/create.html', caregivers=caregivers, members=members)
    except Exception as e:
        flash(f'Error creating appointment: {str(e)}', 'danger')
        return redirect(url_for('appointments_list'))
    finally:
        db.close()

@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def appointments_edit(appointment_id):
    """Edit an appointment"""
    db = get_db()
    try:
        appointment = db.query(Appointment).filter(
            Appointment.appointment_id == appointment_id
        ).first()
        if not appointment:
            flash('Appointment not found!', 'danger')
            return redirect(url_for('appointments_list'))
        
        if request.method == 'POST':
            appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
            appointment.appointment_time = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
            appointment.work_hours = request.form['work_hours']
            appointment.status = request.form['status']
            db.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appointments_list'))
        
        caregiver_user = db.query(User).filter(
            User.user_id == appointment.caregiver_user_id
        ).first()
        member_user = db.query(User).filter(
            User.user_id == appointment.member_user_id
        ).first()
        
        return render_template('appointments/edit.html', 
                             appointment=appointment, 
                             caregiver=caregiver_user, 
                             member=member_user)
    finally:
        db.close()

@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def appointments_delete(appointment_id):
    """Delete an appointment"""
    db = get_db()
    try:
        appointment = db.query(Appointment).filter(
            Appointment.appointment_id == appointment_id
        ).first()
        if appointment:
            db.delete(appointment)
            db.commit()
            flash('Appointment deleted successfully!', 'success')
        else:
            flash('Appointment not found!', 'danger')
    except Exception as e:
        flash(f'Error deleting appointment: {str(e)}', 'danger')
    finally:
        db.close()
    return redirect(url_for('appointments_list'))

if __name__ == '__main__':
    app.run(debug=True)
