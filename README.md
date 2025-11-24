# Caregiver Platform - Database Management System

A comprehensive web application for connecting caregivers with families in need of care services. Built with Flask, PostgreSQL, and SQLAlchemy.

## 🎯 Project Overview

This project implements a complete caregiver platform featuring:
- User registration and management for caregivers and families
- Job posting and application system
- Appointment scheduling and management
- Full CRUD operations via web interface
- Complex SQL queries and data analysis

## 📋 Features

### Core Functionality
- **User Management**: Register users with personal information
- **Caregiver Profiles**: Specialized profiles with caregiving type, rates, and experience
- **Member Profiles**: Family members seeking care with specific requirements
- **Job Postings**: Members can post detailed job advertisements
- **Applications**: Caregivers can apply for suitable positions
- **Appointments**: Schedule and manage caregiving appointments with status tracking

### Caregiving Types
- 🍼 **Babysitter**: Professional childcare services
- 👴 **Elderly Care**: Compassionate care for seniors
- 🎨 **Playmate**: Engaging activities for children

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: PostgreSQL (Neon.tech)
- **ORM**: SQLAlchemy 2.0.23
- **Frontend**: Bootstrap 5.3, Font Awesome 6
- **Deployment**: Heroku
- **Python**: 3.11.6

## 📁 Project Structure

```
project2/
├── app.py                  # Main Flask application
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── init_db.py             # Database initialization script
├── queries.py             # Part 2 SQL queries implementation
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version specification
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── templates/             # HTML templates
    ├── base.html
    ├── index.html
    ├── users/
    ├── caregivers/
    ├── members/
    ├── addresses/
    ├── jobs/
    ├── applications/
    └── appointments/
```

## 🗄️ Database Schema

### Tables

1. **USERS**: Core user information
   - `user_id` (PK), `email`, `given_name`, `surname`, `city`, `phone_number`, `profile_description`, `password`

2. **CAREGIVERS**: Caregiver-specific data
   - `caregiver_user_id` (PK, FK to users), `photo`, `gender`, `caregiving_type`, `hourly_rate`

3. **MEMBERS**: Family member data
   - `member_user_id` (PK, FK to users), `house_rules`, `dependent_description`

4. **ADDRESSES**: Member addresses
   - Composite PK: `(member_user_id, house_number, street, town)`
   - `member_user_id` (FK to members)

5. **JOBS**: Job postings
   - `job_id` (PK), `member_user_id` (FK), `required_caregiving_type`, `other_requirements`, `date_posted`

6. **JOB_APPLICATIONS**: Applications to jobs
   - Composite PK: `(caregiver_user_id, job_id)`
   - Both fields are FKs

7. **APPOINTMENTS**: Scheduled appointments
   - `appointment_id` (PK), `caregiver_user_id` (FK), `member_user_id` (FK), `appointment_date`, `appointment_time`, `work_hours`, `status`

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project2
```

### 2. Set Up PostgreSQL Database (Neon.tech)

1. Go to https://neon.tech/
2. Create a free account
3. Create a new project
4. Copy the connection string (format: `postgresql://user:password@host/database`)

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy from example
copy .env.example .env
```

Edit `.env` and add your database URL:

```
DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 4. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
# Create tables and insert sample data
python init_db.py
```

This will:
- Create all tables according to the schema
- Insert 20 users (10 caregivers, 10 members)
- Insert sample data for all tables (10+ records each)

### 6. Run Part 2 Queries

```bash
python queries.py
```

This executes all required SQL queries:
- Updates (3.1, 3.2)
- Deletes (4.1, 4.2)
- Simple queries (5.1-5.4)
- Complex queries (6.1-6.4)
- Derived attribute query (7)
- View operation (8)

### 7. Run Flask Application Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🌐 Deployment to Heroku

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon (or use Neon.tech DATABASE_URL)
heroku addons:create heroku-postgresql:mini

# Or set your Neon database URL
heroku config:set DATABASE_URL="postgresql://your-neon-connection-string"

# Set other environment variables
heroku config:set SECRET_KEY="your-secret-key"

# Deploy
git add .
git commit -m "Initial deployment"
git push heroku main

# Initialize database on Heroku
heroku run python init_db.py

# Open the app
heroku open
```

## 📊 Part 2: SQL Queries Documentation

### 3. Update Queries

**3.1** Update Arman Armanov's phone number to +77773414141
```python
# Updates single user phone number
user.phone_number = '+77773414141'
```

**3.2** Add commission to caregiver rates
- +$0.3 if hourly rate < $10
- +10% if hourly rate >= $10
```python
if old_rate < 10:
    new_rate = old_rate + 0.3
else:
    new_rate = old_rate * 1.10
```

### 4. Delete Queries

**4.1** Delete all jobs posted by Amina Aminova
```python
# Cascades to delete related job applications
db.query(Job).filter(Job.member_user_id == amina_id).delete()
```

**4.2** Delete members living on Kabanbay Batyr street
```python
# Finds members by address and deletes with cascades
addresses = db.query(Address).filter(Address.street == 'Kabanbay Batyr')
```

### 5. Simple Queries

**5.1** Select caregiver and member names for accepted appointments
- Joins: Appointment → Caregiver → User, Appointment → Member → User
- Filter: status = 'accepted'

**5.2** List jobs containing 'soft-spoken' in requirements
- Uses LIKE operator: `%soft-spoken%`

**5.3** List work hours for all babysitter positions
- Joins: Appointment → Caregiver
- Filter: caregiving_type = 'Babysitter'

**5.4** Members seeking Elderly Care in Astana with "No pets." rule
- Multiple filters: city, house_rules, job type

### 6. Complex Queries (with Aggregation)

**6.1** Count applicants per job
```sql
SELECT job_id, COUNT(application_id) 
FROM jobs JOIN job_applications 
GROUP BY job_id
```

**6.2** Total hours per caregiver for accepted appointments
```sql
SELECT caregiver_id, SUM(work_hours)
FROM appointments
WHERE status = 'accepted'
GROUP BY caregiver_id
```

**6.3** Average pay per caregiver
```sql
SELECT caregiver_id, hourly_rate, AVG(work_hours)
FROM caregivers JOIN appointments
GROUP BY caregiver_id
```

**6.4** Caregivers earning above average (nested query)
```sql
-- Subquery calculates overall average
-- Main query finds caregivers with HAVING clause
AVG(hourly_rate * work_hours) > overall_average
```

### 7. Derived Attribute Query

Calculate total cost for each caregiver:
```sql
SELECT caregiver_id, 
       SUM(hourly_rate * work_hours) as total_cost
FROM caregivers JOIN appointments
WHERE status = 'accepted'
GROUP BY caregiver_id
```

### 8. View Operation

Creates a view-like query showing all job applications with applicant details:
```sql
SELECT application_id, job_id, caregiver_name, 
       member_name, date_applied, requirements
FROM job_applications
JOIN jobs, caregivers, members, users
```

## 🎨 Web Interface Features

### CRUD Operations Available for All Tables:

- **Users**: Create, Read, Update, Delete
- **Caregivers**: Create, Read, Update, Delete
- **Members**: Create, Read, Update, Delete
- **Addresses**: Create, Read, Update, Delete
- **Jobs**: Create, Read, Update, Delete
- **Job Applications**: Create, Read, Delete
- **Appointments**: Create, Read, Update, Delete

### Dashboard
- Statistics cards showing counts of caregivers, members, jobs, and appointments
- Quick navigation to all modules
- Informative overview of platform features

### Design Features
- Responsive Bootstrap 5 design
- Gradient sidebar with Font Awesome icons
- Color-coded badges for status and types
- Hover effects and smooth transitions
- Alert messages for user feedback

## 📝 Sample Data

The database is pre-populated with:
- 20 Users (caregivers and members from various cities)
- 10 Caregivers (Babysitters, Elderly Care, Playmates)
- 10 Members (with various requirements)
- 10 Addresses (across different streets and districts)
- 10 Job postings (with diverse requirements)
- 15 Job applications (multiple per job)
- 11 Appointments (accepted, pending, declined)

## 🔐 Security Features

✅ **Implemented Security Measures**:
- ✅ Password hashing using Werkzeug (bcrypt-based)
- ✅ Passwords never stored in plain text
- ✅ Environment variables for database credentials
- ✅ SQLAlchemy parameterized queries (SQL injection protection)

⚠️ **For Production, Also Add**:
- User authentication and authorization
- HTTPS only
- CSRF protection
- Input validation and sanitization
- Database connection pooling
- Rate limiting

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Test database connection
python -c "from database import engine; print(engine.connect())"
```

### Port Already in Use
```bash
# Use a different port
flask run --port 5001
```

### Missing Tables
```bash
# Re-initialize database
python init_db.py
```

### Heroku Deployment Issues
```bash
# Check logs
heroku logs --tail

# Restart app
heroku restart
```

## 📚 Assignment Requirements Met

### Part 1 (20 points) ✅
- ✅ Physical database created with PostgreSQL
- ✅ All tables match provided schema
- ✅ Primary keys and foreign keys defined
- ✅ 10+ instances per table inserted
- ✅ Sample data designed for non-empty query results

### Part 2 (40 points) ✅
- ✅ Python3 with SQLAlchemy connection
- ✅ Create SQL statements (in init_db.py)
- ✅ Insert SQL statements (in init_db.py)
- ✅ Update queries (3.1, 3.2)
- ✅ Delete queries (4.1, 4.2)
- ✅ Simple queries (5.1, 5.2, 5.3, 5.4)
- ✅ Complex queries with aggregation (6.1, 6.2, 6.3, 6.4)
- ✅ Derived attribute query (7)
- ✅ View operation (8)

### Part 3 (40 points) ✅
- ✅ Web application with CRUD operations
- ✅ Flask framework used
- ✅ All tables accessible via web interface
- ✅ Create, Read, Update, Delete for each entity
- ✅ Ready for deployment (Heroku configuration included)

## 👥 Authors

Database Management System Course Project

## 📄 License

This project is for educational purposes.

---

**Note**: Remember to replace placeholders (database URLs, secret keys) with your actual values. Never commit sensitive information to version control.
