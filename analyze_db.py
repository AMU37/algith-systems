# sync_schema_to_supabase.py
import psycopg2
from sqlalchemy import create_engine, text

# رابط قاعدة بيانات Supabase (PostgreSQL)
SUPABASE_DB_URL = "postgresql://postgres.tdkpriaqfpanelmebhsh:ali1993mubark@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"


def create_schema_on_supabase():
    """إنشاء هيكل قاعدة البيانات بالكامل في Supabase باستخدام SQLAlchemy"""

    # إنشاء اتصال SQLAlchemy بـ Supabase
    engine = create_engine(SUPABASE_DB_URL)

    print("=" * 60)
    print("🔧 إنشاء هيكل قاعدة البيانات في Supabase")
    print("=" * 60)

    # هذا الأمر سينشئ جميع الجداول والأعمدة بناءً على نماذج SQLAlchemy الخاصة بك
    # يجب استيراد النماذج أولاً
    from core import db
    from core.models import (
        Company, User, CompanyMember, Employee, Client, Supplier, Product,
        Subscription, Payment, Plan, Purchase, SalesInvoice, WorkSite, Zone,
        Project, ClientContract, Team, WorkerAllocation, Attendance, DailyVisit,
        Complaint, Equipment, Vehicle, FuelLog, CashAdvance, Expense, ClientInvoice,
        Salary, Deduction, Addition, Advance, Evaluation, EvaluationCriteria,
        EvaluationScore, JournalEntry, JournalLine, Account, LedgerEntry, LedgerLine,
        GLJournal, GLJournalLine, Service, ServiceOrder, ServiceContract,
        Patient, Doctor, Appointment, Student, Subject, Exam, Fee,
        MenuItem, TableOrder, OrderItem, ProductionOrder, QualityCheck, Machine,
        Trip, VehicleMaintenance, FuelRecord, MaterialItem, MaterialPurchase,
        Medicine, LabTest, Invoice, Contract, SupervisorReport, TeamMember
    )

    # إنشاء جميع الجداول
    db.create_all(bind=engine)

    print("\n✅ تم إنشاء جميع الجداول والأعمدة بنجاح!")

    # عرض الجداول التي تم إنشاؤها (باستخدام PostgreSQL)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = result.fetchall()

        print(f"\n📊 عدد الجداول في قاعدة البيانات: {len(tables)}")
        print("📋 قائمة الجداول (أول 20):")
        for table in tables[:20]:
            print(f"   - {table[0]}")
        if len(tables) > 20:
            print(f"   ... و {len(tables) - 20} جدول آخر")


if __name__ == "__main__":
    create_schema_on_supabase()