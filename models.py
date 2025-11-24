from sqlalchemy import Column, Integer, String, Numeric, Date, Time, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}', name='{self.given_name} {self.surname}')>"


class Caregiver(Base):
    __tablename__ = 'caregivers'
    
    caregiver_user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(20))
    caregiving_type = Column(String(50), nullable=False)  # babysitter, elderly care, playmate
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Caregiver(user_id={self.caregiver_user_id}, type='{self.caregiving_type}', rate={self.hourly_rate})>"


class Member(Base):
    __tablename__ = 'members'
    
    member_user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="member")
    addresses = relationship("Address", back_populates="member", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member(user_id={self.member_user_id})>"


class Address(Base):
    __tablename__ = 'addresses'
    
    member_user_id = Column(Integer, ForeignKey('members.member_user_id'), primary_key=True, nullable=False)
    house_number = Column(String(20), primary_key=True, nullable=False)
    street = Column(String(100), primary_key=True, nullable=False)
    town = Column(String(100), primary_key=True, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(member_id={self.member_user_id}, address='{self.house_number} {self.street}, {self.town}')>"


class Job(Base):
    __tablename__ = 'jobs'
    
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey('members.member_user_id'), nullable=False)
    required_caregiving_type = Column(String(50), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="jobs")
    job_applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(job_id={self.job_id}, type='{self.required_caregiving_type}', posted={self.date_posted})>"


class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    caregiver_user_id = Column(Integer, ForeignKey('caregivers.caregiver_user_id'), primary_key=True, nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True, nullable=False)
    date_applied = Column(Date, nullable=False)
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="job_applications")
    
    def __repr__(self):
        return f"<JobApplication(caregiver_id={self.caregiver_user_id}, job_id={self.job_id})>"


class Appointment(Base):
    __tablename__ = 'appointments'
    
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregivers.caregiver_user_id'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('members.member_user_id'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Numeric(5, 2), nullable=False)
    status = Column(String(20), nullable=False)  # pending, accepted, declined
    
    # Relationships
    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment(id={self.appointment_id}, date={self.appointment_date}, status='{self.status}')>"
