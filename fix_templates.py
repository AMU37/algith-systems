# fix_all_templates.py
import os
import re


def fix_template(filepath):
    if not os.path.exists(filepath):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # استبدالات الروابط
    replacements = [
        # روابط الموظفين
        (r"url_for\('add_employee'\)", "url_for('employees.add_employee')"),
        (r"url_for\('edit_employee',", "url_for('employees.edit_employee',"),
        (r"url_for\('delete_employee',", "url_for('employees.delete_employee',"),
        (r"url_for\('generate_salaries',", "url_for('employees.generate_salaries',"),
        (r"url_for\('pay_salary',", "url_for('employees.pay_salary',"),

        # روابط الموردين
        (r"url_for\('add_supplier'\)", "url_for('suppliers.add_supplier')"),
        (r"url_for\('edit_supplier',", "url_for('suppliers.edit_supplier',"),
        (r"url_for\('delete_supplier',", "url_for('suppliers.delete_supplier',"),
        (r"url_for\('add_supplier_invoice'\)", "url_for('suppliers.add_supplier_invoice')"),
        (r"url_for\('delete_supplier_invoice',", "url_for('suppliers.delete_supplier_invoice',"),
        (r"url_for\('pay_supplier_invoice',", "url_for('suppliers.pay_supplier_invoice',"),

        # روابط العملاء
        (r"url_for\('add_client'\)", "url_for('clients.add_client')"),
        (r"url_for\('edit_client',", "url_for('clients.edit_client',"),
        (r"url_for\('delete_client',", "url_for('clients.delete_client',"),
        (r"url_for\('add_client_contract'\)", "url_for('clients.add_client_contract')"),

        # روابط المنتجات
        (r"url_for\('add_product'\)", "url_for('products.add_product')"),
        (r"url_for\('edit_product',", "url_for('products.edit_product',"),
        (r"url_for\('delete_product',", "url_for('products.delete_product',"),

        # روابط المشتريات
        (r"url_for\('add_purchase'\)", "url_for('purchases.add_purchase')"),
        (r"url_for\('delete_purchase',", "url_for('purchases.delete_purchase',"),

        # روابط المبيعات
        (r"url_for\('add_sale'\)", "url_for('sales.add_sale')"),
        (r"url_for\('delete_sale',", "url_for('sales.delete_sale',"),
        (r"url_for\('pay_sale',", "url_for('sales.pay_sale',"),

        # روابط المحاسبة
        (r"url_for\('add_account'\)", "url_for('accounting.add_account')"),
        (r"url_for\('edit_account',", "url_for('accounting.edit_account',"),
        (r"url_for\('delete_account',", "url_for('accounting.delete_account',"),
        (r"url_for\('add_journal_manual'\)", "url_for('accounting.add_journal_manual')"),

        # روابط الإعدادات
        (r"url_for\('update_settings'\)", "url_for('settings.update_settings')"),

        # روابط المستخدمين
        (r"url_for\('add_user'\)", "url_for('users.add_user')"),
        (r"url_for\('edit_user',", "url_for('users.edit_user',"),
        (r"url_for\('delete_user',", "url_for('users.delete_user',"),

        # روابط المقاولات
        (r"url_for\('add_project'\)", "url_for('contracting.add_project')"),
        (r"url_for\('add_claim'\)", "url_for('contracting.add_claim')"),
        (r"url_for\('add_attendance'\)", "url_for('employees.add_attendance')"),
        (r"url_for\('bulk_attendance'\)", "url_for('employees.bulk_attendance')"),
        (r"url_for\('add_daily_payment'\)", "url_for('employees.add_daily_payment')"),
        (r"url_for\('delete_daily_payment',", "url_for('employees.delete_daily_payment',"),
    ]

    for old, new in replacements:
        content = re.sub(old, new, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ تم إصلاح: {filepath}")
        return True
    else:
        print(f"⚠️ لا تغييرات: {filepath}")
        return False


def main():
    base_path = "D:\\ghith\\NEW\\alghith-systems\\templates"
    templates = [
        "employees.html", "salaries.html", "attendance.html", "daily_payments.html",
        "suppliers.html", "supplier_invoices.html", "supplier_contracts.html",
        "clients.html", "client_contracts.html",
        "products.html", "purchases.html", "sales.html",
        "accounts.html", "journal.html", "financial_dashboard.html", "reports.html",
        "settings.html", "users.html",
        "projects.html", "claims.html", "materials.html"
    ]

    print("=" * 60)
    print("🔧 إصلاح روابط القوالب")
    print("=" * 60)

    for template in templates:
        filepath = os.path.join(base_path, template)
        fix_template(filepath)

    print("=" * 60)
    print("✅ تم الانتهاء من إصلاح القوالب")
    print("=" * 60)


if __name__ == "__main__":
    main()