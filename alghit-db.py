# create_users.py
from core import create_app, db
from core.models import Company, User
from werkzeug.security import generate_password_hash


def create_users():
    app = create_app()
    with app.app_context():
        # الحصول على الشركات
        companies = Company.query.all()

        if not companies:
            print("❌ لا توجد شركات")
            return

        # إنشاء المستخدمين
        users_data = [
            {'username': 'superadmin', 'password': 'superadmin123', 'role': 'super_admin',
             'company_id': companies[0].id},
            {'username': 'admin1', 'password': 'admin123', 'role': 'admin',
             'company_id': companies[1].id if len(companies) > 1 else companies[0].id},
            {'username': 'admin2', 'password': 'admin123', 'role': 'admin',
             'company_id': companies[2].id if len(companies) > 2 else companies[0].id},
            {'username': 'admin3', 'password': 'admin123', 'role': 'admin',
             'company_id': companies[3].id if len(companies) > 3 else companies[0].id},
        ]

        for data in users_data:
            # التحقق من عدم وجود المستخدم
            existing = User.query.filter_by(username=data['username']).first()
            if existing:
                db.session.delete(existing)
                print(f"🗑️ تم حذف المستخدم القديم: {data['username']}")

            # إنشاء مستخدم جديد
            user = User(
                company_id=data['company_id'],
                username=data['username'],
                full_name=f'مدير {data["username"]}',
                role=data['role'],
                is_active=True
            )
            user.set_password(data['password'])
            db.session.add(user)
            print(f"✅ تم إنشاء المستخدم: {data['username']} / {data['password']}")

        db.session.commit()
        print("\n🎉 تم إنشاء جميع المستخدمين بنجاح!")


if __name__ == "__main__":
    create_users()