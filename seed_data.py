# seed_data.py - بيانات تجريبية شاملة مع المعاملات المالية
from core import create_app, db
from core.models import (
    Company, User, Employee, Client, Supplier, Product,
    Project, Claim, DailyAttendance, DailyPayment,
    MenuItem, TableOrder, OrderItem,
    Patient, Doctor, Appointment,
    Student, Subject, Exam, Fee,
    Vehicle, Trip, FuelRecord,
    ProductionOrder, QualityCheck, Machine,
    WorkSite, Team, Visit,
    Service, ServiceOrder,
    Subscription, Payment, Plan,
    Purchase, PurchaseItem, SalesInvoice, SalesInvoiceItem,
    Salary, Deduction, Addition, Advance,
    Account, JournalEntry, JournalLine, GLJournal, GLJournalLine,
    LedgerEntry, LedgerLine
)
from helpers.constants import PLANS
from datetime import datetime, date, timedelta
import random
import json


def create_seed_data():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("🌱 بدء إنشاء البيانات التجريبية الشاملة")
        print("=" * 60)

        # ==================== 1. الخطط (Plans) ====================
        plans_data = [
            {'code': 'trial', 'name': 'تجربة مجانية', 'monthly_price': 0, 'max_users': 1, 'is_default': True},
            {'code': 'basic', 'name': 'الباقة الأساسية', 'monthly_price': 37500, 'max_users': 5},
            {'code': 'pro', 'name': 'الباقة الاحترافية', 'monthly_price': 87500, 'max_users': 20},
            {'code': 'enterprise', 'name': 'المؤسسات', 'monthly_price': 250000, 'max_users': 999},
        ]
        for p in plans_data:
            if not Plan.query.filter_by(code=p['code']).first():
                plan = Plan(
                    code=p['code'],
                    name=p['name'],
                    monthly_price=p['monthly_price'],
                    max_users=p['max_users'],
                    is_active=True,
                    is_default=p.get('is_default', False)
                )
                db.session.add(plan)
        print("✅ تم إنشاء الخطط (Plans)")

        # ==================== 2. الحسابات المحاسبية الافتراضية ====================
        default_accounts = [
            # الأصول
            ('1001', 'الصندوق', 'asset', 0),
            ('1002', 'البنك', 'asset', 0),
            ('1101', 'ذمم العملاء', 'asset', 0),
            ('1201', 'المخزون', 'asset', 0),
            # الخصوم
            ('2001', 'ذمم الموردين', 'liability', 0),
            ('2002', 'رواتب مستحقة', 'liability', 0),
            ('2003', 'ضرائب مستحقة', 'liability', 0),
            # حقوق الملكية
            ('3001', 'رأس المال', 'equity', 0),
            ('3002', 'الأرباح المحتجزة', 'equity', 0),
            # الإيرادات
            ('4001', 'إيرادات المبيعات', 'revenue', 0),
            ('4002', 'إيرادات الخدمات', 'revenue', 0),
            ('4003', 'إيرادات الاشتراكات', 'revenue', 0),
            # المصروفات
            ('5001', 'مصروفات الرواتب', 'expense', 0),
            ('5002', 'مصروفات المشتريات', 'expense', 0),
            ('5003', 'مصروفات الصيانة', 'expense', 0),
            ('5004', 'مصروفات النقل', 'expense', 0),
        ]

        # ==================== 3. الشركة الرئيسية (SUPER) ====================
        super_company = Company.query.filter_by(code='SUPER').first()
        if not super_company:
            super_company = Company(
                name='Al-Ghaith SaaS',
                code='SUPER',
                business_type='general',
                is_active=True,
                subscription_status='active',
                is_blocked=False,
                currency='YER'
            )
            db.session.add(super_company)
            db.session.flush()
            print(f"✅ شركة SUPER (ID: {super_company.id})")

            # إنشاء حسابات للشركة الرئيسية
            for code, name, acc_type, balance in default_accounts:
                acc = Account(
                    company_id=super_company.id,
                    code=code,
                    name=name,
                    type=acc_type,
                    balance=balance,
                    status='active'
                )
                db.session.add(acc)
            print(f"   ✅ تم إنشاء {len(default_accounts)} حساباً")

        # ==================== 4. Super Admin ====================
        if not User.query.filter_by(username='superadmin').first():
            super_admin = User(
                company_id=super_company.id,
                username='superadmin',
                full_name='Super Administrator',
                role='super_admin',
                is_active=True
            )
            super_admin.set_password('superadmin123')
            db.session.add(super_admin)
            print("✅ superadmin / superadmin123")

        # ==================== 5. إنشاء شركة مقاولات مع معاملات كاملة ====================
        company1 = Company.query.filter_by(code='CON001').first()
        if not company1:
            company1 = Company(
                name='شركة البناء الحديث للمقاولات',
                code='CON001',
                business_type='contracting',
                is_active=True,
                plan_code='pro',
                subscription_status='active',
                subscription_end=date.today() + timedelta(days=365),
                currency='YER'
            )
            db.session.add(company1)
            db.session.flush()
            print(f"\n✅ شركة مقاولات (ID: {company1.id})")

            # حسابات الشركة
            for code, name, acc_type, balance in default_accounts:
                acc = Account(
                    company_id=company1.id,
                    code=code,
                    name=name,
                    type=acc_type,
                    balance=balance,
                    status='active'
                )
                db.session.add(acc)

            # اشتراك الشركة
            subscription1 = Subscription(
                company_id=company1.id,
                plan_code='pro',
                status='active',
                start_date=date.today() - timedelta(days=30),
                end_date=date.today() + timedelta(days=335),
                monthly_price=87500,
                max_users=20,
                is_trial=False
            )
            db.session.add(subscription1)

            # دفعات الاشتراك (3 دفعات)
            for i in range(3):
                payment = Payment(
                    company_id=company1.id,
                    subscription_id=subscription1.id,
                    amount=87500,
                    payment_method='bank',
                    status='completed',
                    paid_at=date.today() - timedelta(days=30 * i),
                    created_at=date.today() - timedelta(days=30 * i)
                )
                db.session.add(payment)
                # قيد محاسبي للدفعة
                entry = LedgerEntry(
                    company_id=company1.id,
                    entry_date=date.today() - timedelta(days=30 * i),
                    entry_number=f"PAY-{company1.id}-{i + 1}",
                    description=f'دفعة اشتراك شهر {i + 1}',
                    total_debit=87500,
                    total_credit=87500,
                    status='posted'
                )
                db.session.add(entry)
            print(f"   ✅ اشتراك Pro + 3 دفعات")

            # مدير الشركة
            admin1 = User(
                company_id=company1.id,
                username='contracting_admin',
                full_name='أحمد العلي',
                role='admin',
                is_active=True
            )
            admin1.set_password('admin123')
            db.session.add(admin1)

            # موظفين ورواتب
            employees_data = [
                ('محمد حسن', 'مهندس مشاريع', 250000, 'monthly', 250000),
                ('خالد عمر', 'مشرف موقع', 180000, 'monthly', 180000),
                ('سعيد أحمد', 'محاسب', 150000, 'monthly', 150000),
                ('علي صالح', 'سائق', 15000, 'daily', 15000 * 26),
                ('حسن عبدالله', 'عامل', 12000, 'daily', 12000 * 26),
            ]
            for name, position, salary, wage_type, comp_salary in employees_data:
                emp = Employee(
                    company_id=company1.id,
                    name=name,
                    position=position,
                    join_date=date.today() - timedelta(days=random.randint(30, 365)),
                    wage_type=wage_type,
                    comprehensive_salary=comp_salary if wage_type == 'monthly' else 0,
                    daily_wage=salary if wage_type == 'daily' else 0,
                    basic_salary=comp_salary if wage_type == 'monthly' else salary * 26,
                    status='active'
                )
                db.session.add(emp)
            print(f"   ✅ {len(employees_data)} موظفين")

            # إنشاء رواتب لآخر 3 أشهر
            for emp in Employee.query.filter_by(company_id=company1.id).all():
                for month_offset in range(3):
                    month_date = date.today() - timedelta(days=30 * month_offset)
                    month_str = month_date.strftime('%Y-%m')

                    salary = Salary(
                        company_id=company1.id,
                        employee_id=emp.id,
                        month=month_str,
                        basic_salary=emp.basic_salary,
                        net_salary=emp.basic_salary,
                        is_paid=(month_offset == 0),
                        paid_date=date.today() if month_offset == 0 else None
                    )
                    db.session.add(salary)

                    # قيد محاسبي للراتب
                    if month_offset == 0:
                        entry = LedgerEntry(
                            company_id=company1.id,
                            entry_date=date.today(),
                            entry_number=f"SAL-{company1.id}-{emp.id}",
                            description=f'راتب {emp.name} - {month_str}',
                            total_debit=emp.basic_salary,
                            total_credit=emp.basic_salary,
                            status='posted'
                        )
                        db.session.add(entry)
            print(f"   ✅ تم إنشاء الرواتب")

            # مشتريات وفواتير
            suppliers = Supplier.query.filter_by(company_id=company1.id).all()
            for i, supplier in enumerate(suppliers[:2]):
                purchase = Purchase(
                    company_id=company1.id,
                    supplier_id=supplier.id,
                    date=date.today() - timedelta(days=i * 15),
                    total=500000,
                    paid=300000,
                    payment_method='cash',
                    invoice_number=f'INV-{company1.id}-{i + 1}'
                )
                db.session.add(purchase)

                # قيد محاسبي للمشتريات
                entry = LedgerEntry(
                    company_id=company1.id,
                    entry_date=date.today() - timedelta(days=i * 15),
                    entry_number=f"PUR-{company1.id}-{i + 1}",
                    description=f'فاتورة مشتريات من {supplier.name}',
                    total_debit=500000,
                    total_credit=500000,
                    status='posted'
                )
                db.session.add(entry)
            print(f"   ✅ تم إنشاء مشتريات وفواتير")

            # مبيعات وفواتير
            clients = Client.query.filter_by(company_id=company1.id).all()
            for i, client in enumerate(clients[:2]):
                invoice = SalesInvoice(
                    company_id=company1.id,
                    client_id=client.id,
                    date=date.today() - timedelta(days=i * 10),
                    total=750000,
                    paid=750000,
                    status='paid',
                    invoice_number=f'SINV-{company1.id}-{i + 1}'
                )
                db.session.add(invoice)

                # قيد محاسبي للمبيعات
                entry = LedgerEntry(
                    company_id=company1.id,
                    entry_date=date.today() - timedelta(days=i * 10),
                    entry_number=f"SAL-{company1.id}-{i + 1}",
                    description=f'فاتورة مبيعات لـ {client.name}',
                    total_debit=750000,
                    total_credit=750000,
                    status='posted'
                )
                db.session.add(entry)
            print(f"   ✅ تم إنشاء مبيعات وفواتير")

        # ==================== 6. شركة تجزئة ====================
        company2 = Company.query.filter_by(code='RET001').first()
        if not company2:
            company2 = Company(
                name='سوبر ماركت اليمن',
                code='RET001',
                business_type='retail',
                is_active=True,
                plan_code='basic',
                subscription_status='active',
                subscription_end=date.today() + timedelta(days=180),
                currency='YER'
            )
            db.session.add(company2)
            db.session.flush()
            print(f"\n✅ شركة تجزئة (ID: {company2.id})")

            # حسابات الشركة
            for code, name, acc_type, balance in default_accounts:
                acc = Account(
                    company_id=company2.id,
                    code=code,
                    name=name,
                    type=acc_type,
                    balance=balance,
                    status='active'
                )
                db.session.add(acc)

            # اشتراك الشركة
            subscription2 = Subscription(
                company_id=company2.id,
                plan_code='basic',
                status='active',
                start_date=date.today() - timedelta(days=45),
                end_date=date.today() + timedelta(days=135),
                monthly_price=37500,
                max_users=5,
                is_trial=False
            )
            db.session.add(subscription2)

            # دفعات الاشتراك
            for i in range(2):
                payment = Payment(
                    company_id=company2.id,
                    subscription_id=subscription2.id,
                    amount=37500,
                    payment_method='cash',
                    status='completed',
                    paid_at=date.today() - timedelta(days=45 - 30 * i)
                )
                db.session.add(payment)
            print(f"   ✅ اشتراك Basic + دفعات")

            admin2 = User(
                company_id=company2.id,
                username='retail_admin',
                full_name='محمود عباس',
                role='admin',
                is_active=True
            )
            admin2.set_password('admin123')
            db.session.add(admin2)
            print("   👤 retail_admin / admin123")

        # ==================== 7. بقية الشركات ====================
        companies_data = [
            {'code': 'RES001', 'name': 'مطعم الأندلس', 'type': 'restaurant', 'plan': 'trial',
             'username': 'restaurant_admin'},
            {'code': 'HOS001', 'name': 'مستشفى السلام', 'type': 'hospital', 'plan': 'enterprise',
             'username': 'hospital_admin'},
            {'code': 'SCH001', 'name': 'مدرسة النهضة', 'type': 'school', 'plan': 'basic', 'username': 'school_admin'},
            {'code': 'TRN001', 'name': 'شركة اليمن للنقل', 'type': 'transport', 'plan': 'pro',
             'username': 'transport_admin'},
            {'code': 'FAC001', 'name': 'مصنع اليمن للصناعات الغذائية', 'type': 'factory', 'plan': 'basic',
             'username': 'factory_admin'},
            {'code': 'SVC001', 'name': 'شركة الغيث للخدمات', 'type': 'service', 'plan': 'pro',
             'username': 'service_admin'},
            {'code': 'CLN001', 'name': 'شركة النظافة المثالية', 'type': 'cleaning', 'plan': 'basic',
             'username': 'cleaning_admin'},
        ]

        for comp_data in companies_data:
            company = Company.query.filter_by(code=comp_data['code']).first()
            if not company:
                company = Company(
                    name=comp_data['name'],
                    code=comp_data['code'],
                    business_type=comp_data['type'],
                    is_active=True,
                    plan_code=comp_data['plan'],
                    subscription_status='active' if comp_data['plan'] != 'trial' else 'trial',
                    subscription_end=date.today() + timedelta(days=30 if comp_data['plan'] != 'trial' else 14),
                    currency='YER'
                )
                db.session.add(company)
                db.session.flush()
                print(f"\n✅ {comp_data['name']} (ID: {company.id})")

                # حسابات الشركة
                for code, name, acc_type, balance in default_accounts:
                    acc = Account(
                        company_id=company.id,
                        code=code,
                        name=name,
                        type=acc_type,
                        balance=balance,
                        status='active'
                    )
                    db.session.add(acc)

                # اشتراك
                plan_info = PLANS.get(comp_data['plan'], PLANS['trial'])
                subscription = Subscription(
                    company_id=company.id,
                    plan_code=comp_data['plan'],
                    status='active',
                    start_date=date.today() - timedelta(days=random.randint(1, 30)),
                    end_date=date.today() + timedelta(days=plan_info.get('days', 30)),
                    monthly_price=plan_info.get('price', 0),
                    max_users=plan_info.get('max_users', 1),
                    is_trial=(comp_data['plan'] == 'trial')
                )
                db.session.add(subscription)

                # دفعة واحدة على الأقل
                if comp_data['plan'] != 'trial':
                    payment = Payment(
                        company_id=company.id,
                        subscription_id=subscription.id,
                        amount=plan_info.get('price', 0),
                        payment_method='bank',
                        status='completed',
                        paid_at=date.today() - timedelta(days=random.randint(1, 15))
                    )
                    db.session.add(payment)

                # مستخدم المدير
                admin = User(
                    company_id=company.id,
                    username=comp_data['username'],
                    full_name=f'مدير {comp_data["name"]}',
                    role='admin',
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print(f"   👤 {comp_data['username']} / admin123")
                print(f"   ✅ اشتراك {comp_data['plan']}")

        # ==================== قيود محاسبية إضافية ====================
        # إنشاء دفتر أستاذ عام لجميع الشركات
        for company in Company.query.all():
            # إيرادات
            revenue_entry = GLJournal(
                company_id=company.id,
                date=date.today() - timedelta(days=random.randint(1, 30)),
                description='إيرادات الشهر',
                total_debit=random.randint(100000, 500000),
                total_credit=random.randint(100000, 500000),
                created_by=1
            )
            db.session.add(revenue_entry)

            # مصروفات
            expense_entry = GLJournal(
                company_id=company.id,
                date=date.today() - timedelta(days=random.randint(1, 30)),
                description='مصروفات الشهر',
                total_debit=random.randint(50000, 200000),
                total_credit=random.randint(50000, 200000),
                created_by=1
            )
            db.session.add(expense_entry)

        print(f"\n   ✅ تم إنشاء قيود محاسبية لجميع الشركات")

        # حفظ جميع البيانات
        db.session.commit()

        print("\n" + "=" * 60)
        print("📊 ملخص البيانات التجريبية")
        print("=" * 60)
        print(f"🏢 عدد الشركات: {Company.query.count()}")
        print(f"👥 عدد المستخدمين: {User.query.count()}")
        print(f"📦 عدد الاشتراكات: {Subscription.query.count()}")
        print(f"💰 عدد المدفوعات: {Payment.query.count()}")
        print(f"📋 عدد الحسابات المحاسبية: {Account.query.count()}")
        print(f"📊 عدد القيود المحاسبية: {LedgerEntry.query.count()}")
        print(f"📈 عدد دفاتر الأستاذ: {GLJournal.query.count()}")

        print("\n🔐 بيانات تسجيل الدخول:")
        print("-" * 40)
        print("👑 Super Admin: superadmin / superadmin123")
        for comp in companies_data:
            print(f"   {comp['username']} / admin123")
        print("=" * 60)
        print("✅ تم إنشاء البيانات التجريبية بنجاح!")


if __name__ == "__main__":
    create_seed_data()