# helpers/constants.py

BUSINESS_TYPES = {
    'service': {'name': 'شركة خدمات', 'icon': 'fa-briefcase', 'desc': 'شركة تقدم خدمات للشركات الأخرى'},
    'retail': {'name': 'متجر / بقالة / سوبر ماركت', 'icon': 'fa-store', 'desc': 'بيع وشراء المنتجات'},
    'trading': {'name': 'شركة تجارية', 'icon': 'fa-building', 'desc': 'استيراد وتصدير وتجارة عامة'},
    'contracting': {'name': 'شركة مقاولات', 'icon': 'fa-helmet-safety', 'desc': 'مقاولات وإنشاءات'},
    'restaurant': {'name': 'مطعم / كافتيريا', 'icon': 'fa-utensils', 'desc': 'خدمات طعام ومشروبات'},
    'employee_transport': {'name': 'نقل موظفين', 'icon': 'fa-bus', 'desc': 'إدارة باصات وسائقين وخطوط سير للموظفين'},
    'general': {'name': 'أخرى', 'icon': 'fa-globe', 'desc': 'نشاط عام - جميع الوحدات متاحة'},
}

PLANS = {
    'trial': {'name': 'تجربة مجانية', 'price': 0, 'days': 14, 'max_users': 1, 'color': '#6c757d'},
    'basic': {'name': 'الباقة الأساسية', 'price': 37500, 'days': 30, 'max_users': 5, 'color': '#1a73e8'},
    'pro': {'name': 'الباقة الاحترافية', 'price': 87500, 'days': 30, 'max_users': 20, 'color': '#34a853'},
    'enterprise': {'name': 'المؤسسات', 'price': 250000, 'days': 30, 'max_users': 999, 'color': '#fbbc04'},
}
