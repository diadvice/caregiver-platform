"""
Verification script to check if the project is set up correctly
Run this after installation to verify everything works
"""

import sys
import os

def check_environment():
    """Check if .env file exists and has required variables"""
    print("\n" + "="*60)
    print("1. Checking Environment Configuration...")
    print("="*60)
    
    if not os.path.exists('.env'):
        print("❌ ERROR: .env file not found!")
        print("   Create it from .env.example and add your DATABASE_URL")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            print("❌ ERROR: DATABASE_URL not set in .env file")
            return False
        
        print(f"✅ .env file exists")
        print(f"✅ DATABASE_URL is set")
        return True
    except ImportError:
        print("❌ ERROR: python-dotenv not installed")
        print("   Run: pip install -r requirements.txt")
        return False

def check_packages():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("2. Checking Python Packages...")
    print("="*60)
    
    required_packages = {
        'flask': 'Flask',
        'sqlalchemy': 'SQLAlchemy',
        'psycopg2': 'psycopg2-binary',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Run: pip install -r requirements.txt")
    
    return all_installed

def check_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("3. Testing Database Connection...")
    print("="*60)
    
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL")
            print(f"   Version: {version.split(',')[0]}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\n   Check your DATABASE_URL in .env file")
        print("   Make sure your Neon database is active")
        return False

def check_tables():
    """Check if tables exist"""
    print("\n" + "="*60)
    print("4. Checking Database Tables...")
    print("="*60)
    
    try:
        from database import engine
        from sqlalchemy import text, inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['users', 'caregivers', 'members', 'addresses', 
                          'jobs', 'job_applications', 'appointments']
        
        if not tables:
            print("❌ No tables found in database")
            print("   Run: python init_db.py")
            return False
        
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            print("   Run: python init_db.py")
            return False
        
        print(f"✅ All {len(required_tables)} required tables exist:")
        for table in required_tables:
            print(f"   - {table}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking tables: {str(e)}")
        return False

def check_data():
    """Check if sample data exists"""
    print("\n" + "="*60)
    print("5. Checking Sample Data...")
    print("="*60)
    
    try:
        from database import SessionLocal
        from models import User, Caregiver, Member, Job, Appointment
        
        db = SessionLocal()
        
        counts = {
            'Users': db.query(User).count(),
            'Caregivers': db.query(Caregiver).count(),
            'Members': db.query(Member).count(),
            'Jobs': db.query(Job).count(),
            'Appointments': db.query(Appointment).count()
        }
        
        db.close()
        
        if all(count == 0 for count in counts.values()):
            print("❌ No data found in database")
            print("   Run: python init_db.py")
            return False
        
        print("✅ Sample data found:")
        for entity, count in counts.items():
            status = "✅" if count >= 10 else "⚠️"
            print(f"   {status} {entity}: {count} records")
        
        return True
    except Exception as e:
        print(f"❌ Error checking data: {str(e)}")
        return False

def check_flask():
    """Check if Flask app can be imported"""
    print("\n" + "="*60)
    print("6. Checking Flask Application...")
    print("="*60)
    
    try:
        from app import app
        print("✅ Flask application imported successfully")
        print(f"✅ Routes configured: {len(app.url_map._rules)} routes")
        return True
    except Exception as e:
        print(f"❌ Error importing Flask app: {str(e)}")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + " "*10 + "CAREGIVER PLATFORM VERIFICATION" + " "*17 + "#")
    print("#" + " "*58 + "#")
    print("#"*60)
    
    checks = [
        check_environment,
        check_packages,
        check_database_connection,
        check_tables,
        check_data,
        check_flask
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if all(results):
        print("\n🎉 SUCCESS! Your project is set up correctly!")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Explore the web interface")
        print("4. Run queries: python queries.py")
    elif passed >= total - 2:
        print("\n⚠️  ALMOST THERE! Fix the errors above and try again.")
    else:
        print("\n❌ SETUP INCOMPLETE. Please fix the errors above.")
        print("\nQuick fix steps:")
        print("1. Ensure .env file exists with DATABASE_URL")
        print("2. Run: pip install -r requirements.txt")
        print("3. Run: python init_db.py")
        print("4. Run this script again: python verify_setup.py")
    
    print("\n" + "="*60 + "\n")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
