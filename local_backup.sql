PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE company (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	code VARCHAR(20), 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	address VARCHAR(200), 
	tax_number VARCHAR(50), 
	commercial_reg VARCHAR(50), 
	activity VARCHAR(100), 
	business_type VARCHAR(20), 
	slogan VARCHAR(200), 
	primary_color VARCHAR(7), 
	is_active BOOLEAN, 
	created_at DATETIME, 
	subscription_status VARCHAR(20), 
	subscription_end DATE, 
	is_blocked BOOLEAN, 
	plan_code VARCHAR(50), 
	currency VARCHAR(10), 
	exchange_rate FLOAT, 
	currency_locked BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (code)
);
INSERT INTO company VALUES(1,'Al-Ghaith SaaS','SUPER',NULL,NULL,NULL,NULL,NULL,NULL,'general',NULL,'#1a73e8',1,'2026-05-22 23:38:35.605322','active',NULL,0,'trial','YER',1.0,0);
INSERT INTO company VALUES(2,'شركة البناء الحديث للمقاولات','CON001','','','','','','','contracting','','#7489a4',1,'2026-05-22 23:38:36.511805','active','2027-05-23',0,'pro','YER',1.0,0);
INSERT INTO company VALUES(3,'سوبر ماركت اليمن','RET001',NULL,NULL,NULL,NULL,NULL,NULL,'retail',NULL,'#1a73e8',1,'2026-05-22 23:38:37.786734','active','2026-11-19',0,'basic','YER',1.0,0);
INSERT INTO company VALUES(4,'مطعم الأندلس','RES001',NULL,NULL,NULL,NULL,NULL,NULL,'restaurant',NULL,'#1a73e8',1,'2026-05-22 23:38:38.819504','trial','2026-06-06',0,'trial','YER',1.0,0);
INSERT INTO company VALUES(5,'مستشفى السلام','HOS001',NULL,NULL,NULL,NULL,NULL,NULL,'hospital',NULL,'#1a73e8',1,'2026-05-22 23:38:39.774511','active','2026-06-22',0,'enterprise','YER',1.0,0);
INSERT INTO company VALUES(6,'مدرسة النهضة','SCH001',NULL,NULL,NULL,NULL,NULL,NULL,'school',NULL,'#1a73e8',1,'2026-05-22 23:38:40.751795','active','2026-06-22',0,'basic','YER',1.0,0);
INSERT INTO company VALUES(7,'شركة اليمن للنقل','TRN001',NULL,NULL,NULL,NULL,NULL,NULL,'transport',NULL,'#1a73e8',1,'2026-05-22 23:38:41.747331','active','2026-06-22',0,'pro','YER',1.0,0);
INSERT INTO company VALUES(8,'مصنع اليمن للصناعات الغذائية','FAC001',NULL,NULL,NULL,NULL,NULL,NULL,'factory',NULL,'#1a73e8',1,'2026-05-22 23:38:42.704433','active','2026-06-22',0,'basic','YER',1.0,0);
INSERT INTO company VALUES(9,'شركة الغيث للخدمات','SVC001',NULL,NULL,NULL,NULL,NULL,NULL,'service',NULL,'#1a73e8',1,'2026-05-22 23:38:43.643992','active','2026-06-22',0,'pro','YER',1.0,0);
INSERT INTO company VALUES(10,'شركة النظافة المثالية','CLN001',NULL,NULL,NULL,NULL,NULL,NULL,'cleaning',NULL,'#1a73e8',1,'2026-05-22 23:38:44.576211','active','2026-06-22',0,'basic','YER',1.0,0);
INSERT INTO company VALUES(11,'TestCompany','C0011',NULL,NULL,NULL,NULL,NULL,NULL,'general',NULL,'#1a73e8',1,'2026-05-22 23:46:13.756612','active','2026-06-06',0,'trial','YER',1.0,0);
INSERT INTO company VALUES(12,'SecondTest','C0012',NULL,NULL,NULL,NULL,NULL,NULL,'retail',NULL,'#1a73e8',1,'2026-05-22 23:51:14.030470','active','2026-06-22',0,'pro','YER',1.0,0);
INSERT INTO company VALUES(13,'BrowserTest','C0013',NULL,NULL,NULL,NULL,NULL,NULL,'restaurant',NULL,'#1a73e8',1,'2026-05-22 23:55:07.286881','active','2026-06-22',0,'basic','YER',1.0,0);
INSERT INTO company VALUES(14,'FlowTest','C0014',NULL,NULL,NULL,NULL,NULL,NULL,'general',NULL,'#1a73e8',1,'2026-05-23 00:00:28.444478','active','2026-06-06',0,'trial','YER',1.0,0);
INSERT INTO company VALUES(15,'متعهد عمال الدكة','C0015',NULL,NULL,NULL,NULL,NULL,NULL,'service',NULL,'#1a73e8',1,'2026-05-23 00:03:44.262252','active','2026-06-06',0,'trial','YER',1.0,0);
INSERT INTO company VALUES(16,'ServiceTest','C0016',NULL,NULL,NULL,NULL,NULL,NULL,'service',NULL,'#1a73e8',1,'2026-05-23 00:10:13.867570','active','2026-06-22',0,'pro','YER',1.0,0);
INSERT INTO company VALUES(17,'حركة السكر','C0017',NULL,NULL,NULL,NULL,NULL,NULL,'employee_transport',NULL,'#1a73e8',1,'2026-05-23 14:03:43.331581','active','2026-06-06',0,'trial','YER',1.0,0);
CREATE TABLE IF NOT EXISTS "plan" (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	code VARCHAR(50) NOT NULL, 
	monthly_price FLOAT, 
	yearly_price FLOAT, 
	max_users INTEGER, 
	description TEXT, 
	features TEXT, 
	is_active BOOLEAN, 
	is_default BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (code)
);
INSERT INTO "plan" VALUES(1,'تجربة مجانية','trial',0.0,0.0,1,NULL,NULL,1,1);
INSERT INTO "plan" VALUES(2,'الباقة الأساسية','basic',37500.0,0.0,5,NULL,NULL,1,0);
INSERT INTO "plan" VALUES(3,'الباقة الاحترافية','pro',87500.0,0.0,20,NULL,NULL,1,0);
INSERT INTO "plan" VALUES(4,'المؤسسات','enterprise',250000.0,0.0,999,NULL,NULL,1,0);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(256) NOT NULL, 
	full_name VARCHAR(120), 
	email VARCHAR(120), 
	phone VARCHAR(20), 
	role VARCHAR(20), 
	permissions TEXT, 
	is_active BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_company_username UNIQUE (company_id, username), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO user VALUES(1,1,'superadmin','pbkdf2:sha256:600000$PZDcHWgfkAbWluiL$0ccd11de574732e08d77cb4097107ee8badd6cce8e5af3b5853a89b2ccf32214','Super Administrator',NULL,NULL,'super_admin','{}',1,'2026-05-22 23:38:36.509694');
INSERT INTO user VALUES(2,2,'contracting_admin','pbkdf2:sha256:600000$YigyMxQ2SchwenNl$c842b8147da0104f7e4285e287acaecfa68a7631cbd160c4b53bc5585c318e58','أحمد العلي',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:37.736517');
INSERT INTO user VALUES(3,3,'retail_admin','pbkdf2:sha256:600000$gbCThCg2cCm0skDE$e0480a745d279f91cd47647246e2f0d449db541ac9c6c50ae4a04ab75b5729a2','محمود عباس',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:38.812485');
INSERT INTO user VALUES(4,4,'restaurant_admin','pbkdf2:sha256:600000$rZdVXETCc7yiS0l6$286d98deb69f35e0b987ef6118002ed073e0e8606ff44dcceb85492198436966','مدير مطعم الأندلس',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:39.771400');
INSERT INTO user VALUES(5,5,'hospital_admin','pbkdf2:sha256:600000$OWjJNkb4WdzZNmzE$f68f2d83676941d1ed5bd97ba92cc62eb64d469d317d3161ba556d550b1a5c7b','مدير مستشفى السلام',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:40.744957');
INSERT INTO user VALUES(6,6,'school_admin','pbkdf2:sha256:600000$Jm86dL7RvSSkQQk3$8cce4f65a9c9f4c774bc48b02ab07f7c8a96d17cfa07259b1532ef24b4d867d1','مدير مدرسة النهضة',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:41.744349');
INSERT INTO user VALUES(7,7,'transport_admin','pbkdf2:sha256:600000$1ay1yjVCqAWJbdbu$2820b9146295d157b2e7b8074add160cb6c08433e82aede5bdde5e94521f8c8e','مدير شركة اليمن للنقل',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:42.701158');
INSERT INTO user VALUES(8,8,'factory_admin','pbkdf2:sha256:600000$mI7QeoP1MCDdu81C$7952d259608072027befe63ddf5c3873536886c7810abd92a7dbe5135a86fe58','مدير مصنع اليمن للصناعات الغذائية',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:43.642448');
INSERT INTO user VALUES(9,9,'service_admin','pbkdf2:sha256:600000$tqMJCBIeckIgCCI6$ecb452aaaf2ac94183732b41ab4ba2b86fa3bf5daa53ec086d3c77f1502daa08','مدير شركة الغيث للخدمات',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:44.574688');
INSERT INTO user VALUES(10,10,'cleaning_admin','pbkdf2:sha256:600000$P2eWTtd0GdGI6hZd$93cf5c8ebd5b555cc701dc67399f3c7a9d834e12cf344f6e440d5abc8d3a505e','مدير شركة النظافة المثالية',NULL,NULL,'admin','{}',1,'2026-05-22 23:38:45.492422');
INSERT INTO user VALUES(11,11,'testuser','pbkdf2:sha256:600000$pcAfIWJ7MlQ9QhP6$55f509dff4ae6fc64db7d1b4e248e954edbd503858181037a26061b3b5399296','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-22 23:46:14.731195');
INSERT INTO user VALUES(12,12,'retailadmin','pbkdf2:sha256:600000$UPCzzxhzZXH6Hecq$b49c2eb49c94de03f95b6685c07d977589e878acc65a58d5961e22f07a00a156','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-22 23:51:15.259799');
INSERT INTO user VALUES(13,13,'browseruser','pbkdf2:sha256:600000$RbQypAXObnPBFGji$8da0331245f8f0affcdf569bb7f453c1b1e7582932d061904ba193714ac39ffc','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-22 23:55:08.817208');
INSERT INTO user VALUES(14,14,'flowuser','pbkdf2:sha256:600000$UhvAxlbAdZOa6qBl$bcb9c27e6d212ed73b19359b8543d8234b58a150ca5f51133c94de35942d7376','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-23 00:00:29.170857');
INSERT INTO user VALUES(15,15,'admin','pbkdf2:sha256:600000$LCZBy3auCeTUrmtd$0f8aac913020e19cbb008e3a0636a89cabe74c2f87e584c7d06c836c277df868','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-23 00:03:45.568926');
INSERT INTO user VALUES(16,16,'svcadmin','pbkdf2:sha256:600000$HlQRBowjaYaMvmI2$fcd2b60868526877e7e99e7ed0ce654273f80a070a22d4e3710c6eb467b2430f','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-23 00:10:15.092894');
INSERT INTO user VALUES(17,17,'admin123','pbkdf2:sha256:600000$U2JDDQXbOud1JFDM$21d84084f18f1f3ec622d0045cee8d0facaa53f4d047c064c7e6eddeb598db26','مدير النظام',NULL,NULL,'admin','{}',1,'2026-05-23 14:03:45.874653');
INSERT INTO user VALUES(18,17,'maged','pbkdf2:sha256:600000$wOqXir3VBBKxX784$dc6438f224255684f3d1b0a7e07f1c5f8efb411680eddb758fcfa301205e2264','ماجد الريمي',NULL,NULL,'driver','{}',1,'2026-05-23 18:20:21.528901');
INSERT INTO user VALUES(19,17,'maad','pbkdf2:sha256:600000$4E5sZK8NXk483fMx$aeb90f561a75ba674c204f3b3b228179836eb0ce828d60497974a42f47e1c6de','معاذ الحكيمي',NULL,NULL,'driver','{}',1,'2026-05-24 07:58:48.562449');
CREATE TABLE client (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	company_name VARCHAR(120), 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	address VARCHAR(200), 
	tax_number VARCHAR(50), 
	balance FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO client VALUES(1,2,'الشركة اليمنية لتكرير السكر',NULL,'0500000000','info1@ard-aljawharah.com','الحديدة-الصليف-راس عيسى','',0.0,'active','','2026-05-23 12:43:18.370436');
INSERT INTO client VALUES(2,17,'الشركة اليمنية لتكرير السكر',NULL,'0500000000','info1@ard-aljawharah.com','الحديدة-الصليف-راس عيسى','',0.0,'deleted','','2026-05-23 19:45:32.522181');
CREATE TABLE supplier (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	company_name VARCHAR(120), 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	address VARCHAR(200), 
	tax_number VARCHAR(50), 
	balance FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE employee (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	card_number VARCHAR(50), 
	code VARCHAR(50), 
	birth_date DATE, 
	birth_place VARCHAR(100), 
	position VARCHAR(100), 
	join_date DATE, 
	wage_type VARCHAR(20), 
	comprehensive_salary FLOAT, 
	basic_salary FLOAT, 
	daily_wage FLOAT, 
	area VARCHAR(100), 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO employee VALUES(1,2,'محمد حسن',NULL,NULL,NULL,NULL,'مهندس مشاريع','2025-05-28','monthly',250000.0,250000.0,0.0,'غير محدد','active',NULL,'2026-05-22 23:38:37.715297');
INSERT INTO employee VALUES(2,2,'خالد عمر',NULL,NULL,NULL,NULL,'مشرف موقع','2025-10-14','monthly',180000.0,180000.0,0.0,'غير محدد','active',NULL,'2026-05-22 23:38:37.715324');
INSERT INTO employee VALUES(3,2,'سعيد أحمد',NULL,NULL,NULL,NULL,'محاسب','2026-02-01','monthly',150000.0,150000.0,0.0,'غير محدد','active',NULL,'2026-05-22 23:38:37.715339');
INSERT INTO employee VALUES(4,2,'علي صالح',NULL,NULL,NULL,NULL,'سائق','2026-01-13','daily',0.0,390000.0,15000.0,'غير محدد','active',NULL,'2026-05-22 23:38:37.715353');
INSERT INTO employee VALUES(5,2,'حسن عبدالله',NULL,NULL,NULL,NULL,'عامل','2026-01-23','daily',0.0,312000.0,12000.0,'غير محدد','active',NULL,'2026-05-22 23:38:37.715368');
INSERT INTO employee VALUES(6,17,'محمد سعيد احمد','','345','2026-05-23','الصليف','عامل خدمات','2026-05-23','monthly',0.0,0.0,0.0,'الصليف','active','','2026-05-23 18:22:50.480468');
INSERT INTO employee VALUES(7,17,'سعيد عبدالله عمر باسري',NULL,'ET-001','1993-05-23','الصليف','عامل خدمات','2026-05-23','monthly',0.0,0.0,0.0,'الصليف','active','','2026-05-23 22:20:29.856983');
INSERT INTO employee VALUES(8,17,'نادر مصطفى محمد',NULL,'ET-002',NULL,'الصليف','عامل خدمات','2026-05-24','monthly',0.0,0.0,0.0,'الصليف','active','','2026-05-23 22:40:32.038555');
INSERT INTO employee VALUES(9,17,'سعد احمد',NULL,'ET-003',NULL,'الصليف','مهندس','2026-05-24','monthly',0.0,0.0,0.0,'الحديدة','active','','2026-05-23 23:08:32.998059');
INSERT INTO employee VALUES(10,17,'ايمن نعمان قايد حسن',NULL,'ET-004',NULL,'الصليف','مهندس','2026-05-24','monthly',0.0,0.0,0.0,'الحديدة','active','','2026-05-23 23:10:31.129738');
INSERT INTO employee VALUES(11,17,'محمد عبده',NULL,'TEMP-1779603807',NULL,NULL,NULL,'2026-05-24','monthly',0.0,0.0,0.0,'غير محدد','active',NULL,'2026-05-24 09:23:27.296701');
INSERT INTO employee VALUES(12,17,'نعان علي',NULL,'TEMP-1779610168',NULL,NULL,NULL,'2026-05-24','monthly',0.0,0.0,0.0,'غير محدد','active',NULL,'2026-05-24 11:09:28.450833');
INSERT INTO employee VALUES(13,17,'احمد محمد',NULL,'TEMP-1779610348',NULL,NULL,NULL,'2026-05-24','monthly',0.0,0.0,0.0,'غير محدد','active',NULL,'2026-05-24 11:12:28.828948');
INSERT INTO employee VALUES(14,17,'علي سعيد',NULL,'TEMP-1779616167',NULL,NULL,NULL,'2026-05-24','monthly',0.0,0.0,0.0,'غير محدد','active',NULL,'2026-05-24 12:49:27.593843');
INSERT INTO employee VALUES(15,17,'نعمان محمد',NULL,'TEMP-1779616736',NULL,NULL,'مهندس','2026-05-24','monthly',0.0,0.0,0.0,'غير محدد','active',NULL,'2026-05-24 12:58:56.857291');
CREATE TABLE product (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	category VARCHAR(50), 
	type VARCHAR(20), 
	unit VARCHAR(20), 
	purchase_price FLOAT, 
	sale_price FLOAT, 
	quantity FLOAT, 
	min_quantity FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE evaluation_criteria (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	max_score INTEGER, 
	weight FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	order_num INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE menu_item (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	category VARCHAR(50), 
	price FLOAT, 
	cost FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE table_order (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	table_number VARCHAR(10), 
	date DATE, 
	total FLOAT, 
	paid FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE patient (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	birth_date DATE, 
	gender VARCHAR(10), 
	address VARCHAR(200), 
	emergency_contact VARCHAR(120), 
	blood_type VARCHAR(5), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE doctor (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	specialty VARCHAR(100), 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	license_number VARCHAR(50), 
	status VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE medicine (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	category VARCHAR(50), 
	price FLOAT, 
	quantity FLOAT, 
	expiry_date DATE, 
	status VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE student (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	student_id VARCHAR(50), 
	grade VARCHAR(50), 
	class_name VARCHAR(50), 
	phone VARCHAR(20), 
	parent_name VARCHAR(120), 
	parent_phone VARCHAR(20), 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE vehicle (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	plate_number VARCHAR(20) NOT NULL, 
	type VARCHAR(50), 
	model VARCHAR(50), 
	year INTEGER, 
	capacity FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE production_order (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	product_name VARCHAR(120) NOT NULL, 
	quantity FLOAT, 
	start_date DATE, 
	end_date DATE, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE machine (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	type VARCHAR(50), 
	status VARCHAR(20), 
	last_maintenance DATE, 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE service (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	category VARCHAR(50), 
	price FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE equipment (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	type VARCHAR(50), 
	model VARCHAR(50), 
	serial_number VARCHAR(50), 
	purchase_date DATE, 
	purchase_cost FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE account (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	code VARCHAR(20) NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	parent_id INTEGER, 
	balance FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(parent_id) REFERENCES account (id)
);
INSERT INTO account VALUES(1,1,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615519');
INSERT INTO account VALUES(2,1,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615538');
INSERT INTO account VALUES(3,1,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615548');
INSERT INTO account VALUES(4,1,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615557');
INSERT INTO account VALUES(5,1,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615565');
INSERT INTO account VALUES(6,1,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615573');
INSERT INTO account VALUES(7,1,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615581');
INSERT INTO account VALUES(8,1,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615588');
INSERT INTO account VALUES(9,1,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615595');
INSERT INTO account VALUES(10,1,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615603');
INSERT INTO account VALUES(11,1,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615610');
INSERT INTO account VALUES(12,1,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615617');
INSERT INTO account VALUES(13,1,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615623');
INSERT INTO account VALUES(14,1,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615625');
INSERT INTO account VALUES(15,1,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615629');
INSERT INTO account VALUES(16,1,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:35.615632');
INSERT INTO account VALUES(17,2,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705314');
INSERT INTO account VALUES(18,2,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705325');
INSERT INTO account VALUES(19,2,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705329');
INSERT INTO account VALUES(20,2,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705333');
INSERT INTO account VALUES(21,2,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705337');
INSERT INTO account VALUES(22,2,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705342');
INSERT INTO account VALUES(23,2,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705346');
INSERT INTO account VALUES(24,2,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705350');
INSERT INTO account VALUES(25,2,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705354');
INSERT INTO account VALUES(26,2,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705358');
INSERT INTO account VALUES(27,2,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705362');
INSERT INTO account VALUES(28,2,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705366');
INSERT INTO account VALUES(29,2,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705371');
INSERT INTO account VALUES(30,2,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705374');
INSERT INTO account VALUES(31,2,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705378');
INSERT INTO account VALUES(32,2,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:37.705382');
INSERT INTO account VALUES(33,3,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811569');
INSERT INTO account VALUES(34,3,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811575');
INSERT INTO account VALUES(35,3,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811577');
INSERT INTO account VALUES(36,3,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811579');
INSERT INTO account VALUES(37,3,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811581');
INSERT INTO account VALUES(38,3,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811582');
INSERT INTO account VALUES(39,3,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811584');
INSERT INTO account VALUES(40,3,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811586');
INSERT INTO account VALUES(41,3,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811587');
INSERT INTO account VALUES(42,3,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811589');
INSERT INTO account VALUES(43,3,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811591');
INSERT INTO account VALUES(44,3,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811592');
INSERT INTO account VALUES(45,3,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811594');
INSERT INTO account VALUES(46,3,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811595');
INSERT INTO account VALUES(47,3,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811597');
INSERT INTO account VALUES(48,3,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:38.811599');
INSERT INTO account VALUES(49,4,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769155');
INSERT INTO account VALUES(50,4,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769165');
INSERT INTO account VALUES(51,4,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769169');
INSERT INTO account VALUES(52,4,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769174');
INSERT INTO account VALUES(53,4,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769178');
INSERT INTO account VALUES(54,4,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769182');
INSERT INTO account VALUES(55,4,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769186');
INSERT INTO account VALUES(56,4,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769191');
INSERT INTO account VALUES(57,4,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769195');
INSERT INTO account VALUES(58,4,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769199');
INSERT INTO account VALUES(59,4,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769203');
INSERT INTO account VALUES(60,4,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769207');
INSERT INTO account VALUES(61,4,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769211');
INSERT INTO account VALUES(62,4,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769215');
INSERT INTO account VALUES(63,4,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769219');
INSERT INTO account VALUES(64,4,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:39.769223');
INSERT INTO account VALUES(65,5,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744153');
INSERT INTO account VALUES(66,5,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744158');
INSERT INTO account VALUES(67,5,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744160');
INSERT INTO account VALUES(68,5,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744161');
INSERT INTO account VALUES(69,5,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744163');
INSERT INTO account VALUES(70,5,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744164');
INSERT INTO account VALUES(71,5,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744166');
INSERT INTO account VALUES(72,5,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744167');
INSERT INTO account VALUES(73,5,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744169');
INSERT INTO account VALUES(74,5,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744170');
INSERT INTO account VALUES(75,5,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744172');
INSERT INTO account VALUES(76,5,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744173');
INSERT INTO account VALUES(77,5,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744174');
INSERT INTO account VALUES(78,5,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744176');
INSERT INTO account VALUES(79,5,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744177');
INSERT INTO account VALUES(80,5,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:40.744179');
INSERT INTO account VALUES(81,6,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743547');
INSERT INTO account VALUES(82,6,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743552');
INSERT INTO account VALUES(83,6,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743553');
INSERT INTO account VALUES(84,6,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743555');
INSERT INTO account VALUES(85,6,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743556');
INSERT INTO account VALUES(86,6,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743558');
INSERT INTO account VALUES(87,6,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743559');
INSERT INTO account VALUES(88,6,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743561');
INSERT INTO account VALUES(89,6,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743563');
INSERT INTO account VALUES(90,6,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743564');
INSERT INTO account VALUES(91,6,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743566');
INSERT INTO account VALUES(92,6,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743567');
INSERT INTO account VALUES(93,6,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743568');
INSERT INTO account VALUES(94,6,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743570');
INSERT INTO account VALUES(95,6,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743571');
INSERT INTO account VALUES(96,6,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:41.743573');
INSERT INTO account VALUES(97,7,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:42.695987');
INSERT INTO account VALUES(98,7,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:42.695994');
INSERT INTO account VALUES(99,7,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:42.695997');
INSERT INTO account VALUES(100,7,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696000');
INSERT INTO account VALUES(101,7,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696002');
INSERT INTO account VALUES(102,7,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696005');
INSERT INTO account VALUES(103,7,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696008');
INSERT INTO account VALUES(104,7,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696010');
INSERT INTO account VALUES(105,7,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696012');
INSERT INTO account VALUES(106,7,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696015');
INSERT INTO account VALUES(107,7,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696017');
INSERT INTO account VALUES(108,7,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696020');
INSERT INTO account VALUES(109,7,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696022');
INSERT INTO account VALUES(110,7,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696024');
INSERT INTO account VALUES(111,7,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696027');
INSERT INTO account VALUES(112,7,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:42.696029');
INSERT INTO account VALUES(113,8,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641481');
INSERT INTO account VALUES(114,8,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641487');
INSERT INTO account VALUES(115,8,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641489');
INSERT INTO account VALUES(116,8,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641491');
INSERT INTO account VALUES(117,8,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641493');
INSERT INTO account VALUES(118,8,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641494');
INSERT INTO account VALUES(119,8,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641496');
INSERT INTO account VALUES(120,8,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641498');
INSERT INTO account VALUES(121,8,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641500');
INSERT INTO account VALUES(122,8,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641502');
INSERT INTO account VALUES(123,8,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641503');
INSERT INTO account VALUES(124,8,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641505');
INSERT INTO account VALUES(125,8,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641507');
INSERT INTO account VALUES(126,8,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641509');
INSERT INTO account VALUES(127,8,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641510');
INSERT INTO account VALUES(128,8,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:43.641512');
INSERT INTO account VALUES(129,9,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573699');
INSERT INTO account VALUES(130,9,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573705');
INSERT INTO account VALUES(131,9,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573707');
INSERT INTO account VALUES(132,9,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573709');
INSERT INTO account VALUES(133,9,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573711');
INSERT INTO account VALUES(134,9,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573713');
INSERT INTO account VALUES(135,9,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573714');
INSERT INTO account VALUES(136,9,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573716');
INSERT INTO account VALUES(137,9,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573718');
INSERT INTO account VALUES(138,9,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573720');
INSERT INTO account VALUES(139,9,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573722');
INSERT INTO account VALUES(140,9,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573724');
INSERT INTO account VALUES(141,9,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573725');
INSERT INTO account VALUES(142,9,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573727');
INSERT INTO account VALUES(143,9,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573729');
INSERT INTO account VALUES(144,9,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:44.573731');
INSERT INTO account VALUES(145,10,'1001','الصندوق','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491113');
INSERT INTO account VALUES(146,10,'1002','البنك','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491121');
INSERT INTO account VALUES(147,10,'1101','ذمم العملاء','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491124');
INSERT INTO account VALUES(148,10,'1201','المخزون','asset',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491126');
INSERT INTO account VALUES(149,10,'2001','ذمم الموردين','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491129');
INSERT INTO account VALUES(150,10,'2002','رواتب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491131');
INSERT INTO account VALUES(151,10,'2003','ضرائب مستحقة','liability',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491134');
INSERT INTO account VALUES(152,10,'3001','رأس المال','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491136');
INSERT INTO account VALUES(153,10,'3002','الأرباح المحتجزة','equity',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491138');
INSERT INTO account VALUES(154,10,'4001','إيرادات المبيعات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491141');
INSERT INTO account VALUES(155,10,'4002','إيرادات الخدمات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491143');
INSERT INTO account VALUES(156,10,'4003','إيرادات الاشتراكات','revenue',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491145');
INSERT INTO account VALUES(157,10,'5001','مصروفات الرواتب','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491147');
INSERT INTO account VALUES(158,10,'5002','مصروفات المشتريات','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491149');
INSERT INTO account VALUES(159,10,'5003','مصروفات الصيانة','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491152');
INSERT INTO account VALUES(160,10,'5004','مصروفات النقل','expense',NULL,0.0,NULL,'active','2026-05-22 23:38:45.491154');
CREATE TABLE area (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
CREATE TABLE subscription (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	plan_code VARCHAR(50), 
	status VARCHAR(20), 
	start_date DATE, 
	end_date DATE, 
	monthly_price FLOAT, 
	max_users INTEGER, 
	is_trial BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO subscription VALUES(1,2,'pro','active','2026-04-23','2027-04-23',87500.0,20,0,'2026-05-22 23:38:37.734367');
INSERT INTO subscription VALUES(2,3,'basic','active','2026-04-08','2026-10-05',37500.0,5,0,'2026-05-22 23:38:38.812291');
INSERT INTO subscription VALUES(3,4,'trial','active','2026-05-07','2026-06-06',0.0,1,1,'2026-05-22 23:38:39.771006');
INSERT INTO subscription VALUES(4,5,'enterprise','active','2026-05-18','2026-06-22',250000.0,999,0,'2026-05-22 23:38:40.744791');
INSERT INTO subscription VALUES(5,6,'basic','active','2026-05-16','2026-06-22',37500.0,5,0,'2026-05-22 23:38:41.744187');
INSERT INTO subscription VALUES(6,7,'pro','active','2026-05-13','2026-06-22',87500.0,20,0,'2026-05-22 23:38:42.700523');
INSERT INTO subscription VALUES(7,8,'basic','active','2026-04-26','2026-06-22',37500.0,5,0,'2026-05-22 23:38:43.642245');
INSERT INTO subscription VALUES(8,9,'pro','active','2026-05-11','2026-06-22',87500.0,20,0,'2026-05-22 23:38:44.574487');
INSERT INTO subscription VALUES(9,10,'basic','active','2026-05-03','2026-06-22',37500.0,5,0,'2026-05-22 23:38:45.492167');
INSERT INTO subscription VALUES(10,11,'trial','active','2026-05-23','2026-06-06',0.0,1,1,'2026-05-22 23:46:14.739524');
INSERT INTO subscription VALUES(11,12,'pro','active','2026-05-23','2026-06-22',87500.0,20,0,'2026-05-22 23:51:15.257439');
INSERT INTO subscription VALUES(12,13,'basic','active','2026-05-23','2026-06-22',37500.0,5,0,'2026-05-22 23:55:08.820702');
INSERT INTO subscription VALUES(13,14,'trial','active','2026-05-23','2026-06-06',0.0,1,1,'2026-05-23 00:00:29.182937');
INSERT INTO subscription VALUES(14,15,'trial','active','2026-05-23','2026-06-06',0.0,1,1,'2026-05-23 00:03:45.585525');
INSERT INTO subscription VALUES(15,16,'pro','active','2026-05-23','2026-06-22',87500.0,20,0,'2026-05-23 00:10:15.090584');
INSERT INTO subscription VALUES(16,17,'trial','active','2026-05-23','2026-06-06',0.0,1,1,'2026-05-23 14:03:45.904155');
CREATE TABLE client_contract (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	client_id INTEGER, 
	contract_number VARCHAR(50), 
	type VARCHAR(20), 
	start_date DATE, 
	end_date DATE, 
	amount FLOAT, 
	terms TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id)
);
INSERT INTO client_contract VALUES(1,2,1,'55','one-time','2026-05-23','2026-05-31',5000000.0,'','active','2026-05-23 12:44:25.767672');
CREATE TABLE purchase (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	supplier_id INTEGER, 
	date DATE, 
	total FLOAT, 
	paid FLOAT, 
	payment_method VARCHAR(20), 
	notes TEXT, 
	invoice_number VARCHAR(50), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(supplier_id) REFERENCES supplier (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE sales_invoice (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	client_id INTEGER, 
	date DATE, 
	total FLOAT, 
	paid FLOAT, 
	payment_method VARCHAR(20), 
	notes TEXT, 
	invoice_number VARCHAR(50), 
	status VARCHAR(20), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE salary (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	month VARCHAR(7) NOT NULL, 
	basic_salary FLOAT, 
	additions_total FLOAT, 
	deductions_total FLOAT, 
	advances_deduction FLOAT, 
	net_salary FLOAT, 
	is_paid BOOLEAN, 
	paid_date DATE, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
INSERT INTO salary VALUES(1,2,1,'2026-05',250000.0,0.0,0.0,0.0,250000.0,1,'2026-05-23','2026-05-22 23:38:37.766115');
INSERT INTO salary VALUES(2,2,1,'2026-04',250000.0,0.0,0.0,0.0,250000.0,0,NULL,'2026-05-22 23:38:37.766135');
INSERT INTO salary VALUES(3,2,1,'2026-03',250000.0,0.0,0.0,0.0,250000.0,0,NULL,'2026-05-22 23:38:37.766146');
INSERT INTO salary VALUES(4,2,2,'2026-05',180000.0,0.0,0.0,0.0,180000.0,1,'2026-05-23','2026-05-22 23:38:37.766156');
INSERT INTO salary VALUES(5,2,2,'2026-04',180000.0,0.0,0.0,0.0,180000.0,0,NULL,'2026-05-22 23:38:37.766167');
INSERT INTO salary VALUES(6,2,2,'2026-03',180000.0,0.0,0.0,0.0,180000.0,0,NULL,'2026-05-22 23:38:37.766176');
INSERT INTO salary VALUES(7,2,3,'2026-05',150000.0,0.0,0.0,0.0,150000.0,1,'2026-05-23','2026-05-22 23:38:37.766185');
INSERT INTO salary VALUES(8,2,3,'2026-04',150000.0,0.0,0.0,0.0,150000.0,0,NULL,'2026-05-22 23:38:37.766195');
INSERT INTO salary VALUES(9,2,3,'2026-03',150000.0,0.0,0.0,0.0,150000.0,0,NULL,'2026-05-22 23:38:37.766205');
INSERT INTO salary VALUES(10,2,4,'2026-05',390000.0,0.0,0.0,0.0,390000.0,1,'2026-05-23','2026-05-22 23:38:37.766214');
INSERT INTO salary VALUES(11,2,4,'2026-04',390000.0,0.0,0.0,0.0,390000.0,0,NULL,'2026-05-22 23:38:37.766224');
INSERT INTO salary VALUES(12,2,4,'2026-03',390000.0,0.0,0.0,0.0,390000.0,0,NULL,'2026-05-22 23:38:37.766233');
INSERT INTO salary VALUES(13,2,5,'2026-05',312000.0,0.0,0.0,0.0,312000.0,1,'2026-05-23','2026-05-22 23:38:37.766243');
INSERT INTO salary VALUES(14,2,5,'2026-04',312000.0,0.0,0.0,0.0,312000.0,0,NULL,'2026-05-22 23:38:37.766253');
INSERT INTO salary VALUES(15,2,5,'2026-03',312000.0,0.0,0.0,0.0,312000.0,0,NULL,'2026-05-22 23:38:37.766263');
INSERT INTO salary VALUES(16,2,1,'2026-06',250000.0,0.0,0.0,0.0,250000.0,0,NULL,'2026-05-23 13:30:35.393552');
INSERT INTO salary VALUES(17,2,2,'2026-06',180000.0,0.0,0.0,0.0,180000.0,0,NULL,'2026-05-23 13:30:35.428413');
INSERT INTO salary VALUES(18,2,3,'2026-06',150000.0,0.0,0.0,0.0,150000.0,0,NULL,'2026-05-23 13:30:35.433781');
INSERT INTO salary VALUES(19,2,4,'2026-06',390000.0,0.0,0.0,0.0,450000.0,0,NULL,'2026-05-23 13:30:35.443766');
INSERT INTO salary VALUES(20,2,5,'2026-06',312000.0,0.0,0.0,0.0,360000.0,0,NULL,'2026-05-23 13:30:35.448413');
CREATE TABLE deduction (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	type VARCHAR(50) NOT NULL, 
	amount FLOAT, 
	reason VARCHAR(200), 
	date DATE, 
	month VARCHAR(7), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE addition (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	type VARCHAR(50) NOT NULL, 
	amount FLOAT, 
	reason VARCHAR(200), 
	date DATE, 
	month VARCHAR(7), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE advance (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	amount FLOAT, 
	remaining FLOAT, 
	monthly_deduction FLOAT, 
	date DATE, 
	notes TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
CREATE TABLE evaluation (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	date DATE, 
	total_score FLOAT, 
	notes TEXT, 
	evaluator_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(evaluator_id) REFERENCES user (id)
);
CREATE TABLE project (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	client_id INTEGER, 
	contract_number VARCHAR(50), 
	contract_value FLOAT, 
	start_date DATE, 
	end_date DATE, 
	status VARCHAR(20), 
	description TEXT, 
	location VARCHAR(200), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id)
);
INSERT INTO project VALUES(1,2,'بناء غرفة',NULL,'55',5000000.0,'2026-05-23','2026-05-31','active','','الصليف','2026-05-23 12:48:17.275917');
CREATE TABLE order_item (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	menu_item_id INTEGER, 
	item_name VARCHAR(120), 
	quantity FLOAT, 
	price FLOAT, 
	total FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES table_order (id), 
	FOREIGN KEY(menu_item_id) REFERENCES menu_item (id)
);
CREATE TABLE appointment (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	patient_id INTEGER, 
	doctor_id INTEGER, 
	date DATE, 
	time VARCHAR(10), 
	status VARCHAR(20), 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(patient_id) REFERENCES patient (id), 
	FOREIGN KEY(doctor_id) REFERENCES doctor (id)
);
CREATE TABLE lab_test (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	patient_id INTEGER, 
	test_name VARCHAR(120), 
	date DATE, 
	result TEXT, 
	status VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(patient_id) REFERENCES patient (id)
);
CREATE TABLE subject (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	grade VARCHAR(50), 
	teacher_id INTEGER, 
	status VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(teacher_id) REFERENCES employee (id)
);
CREATE TABLE fee (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	student_id INTEGER, 
	amount FLOAT, 
	paid FLOAT, 
	due_date DATE, 
	status VARCHAR(20), 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(student_id) REFERENCES student (id)
);
CREATE TABLE trip (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	vehicle_id INTEGER, 
	driver_id INTEGER, 
	client_id INTEGER, 
	from_location VARCHAR(200), 
	to_location VARCHAR(200), 
	date DATE, 
	cost FLOAT, 
	revenue FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(vehicle_id) REFERENCES vehicle (id), 
	FOREIGN KEY(driver_id) REFERENCES employee (id), 
	FOREIGN KEY(client_id) REFERENCES client (id)
);
CREATE TABLE fuel_record (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	vehicle_id INTEGER, 
	date DATE, 
	quantity FLOAT, 
	cost FLOAT, 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(vehicle_id) REFERENCES vehicle (id)
);
CREATE TABLE vehicle_maintenance (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	vehicle_id INTEGER, 
	date DATE, 
	type VARCHAR(50), 
	cost FLOAT, 
	description TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(vehicle_id) REFERENCES vehicle (id)
);
CREATE TABLE quality_check (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	production_order_id INTEGER, 
	date DATE, 
	passed BOOLEAN, 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(production_order_id) REFERENCES production_order (id)
);
CREATE TABLE service_contract (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	client_id INTEGER, 
	contract_number VARCHAR(50), 
	start_date DATE, 
	end_date DATE, 
	amount FLOAT, 
	terms TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id)
);
CREATE TABLE service_order (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	client_id INTEGER, 
	service_id INTEGER, 
	date DATE, 
	amount FLOAT, 
	paid FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id), 
	FOREIGN KEY(service_id) REFERENCES service (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE equipment_maintenance (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	equipment_id INTEGER NOT NULL, 
	date DATE, 
	type VARCHAR(50), 
	cost FLOAT, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(equipment_id) REFERENCES equipment (id)
);
CREATE TABLE journal_entry (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	date DATE, 
	description VARCHAR(200), 
	entry_type VARCHAR(50), 
	reference VARCHAR(50), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE gl_journal (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	date DATE, 
	description VARCHAR(200), 
	reference VARCHAR(50), 
	created_by INTEGER, 
	total_debit FLOAT, 
	total_credit FLOAT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
INSERT INTO gl_journal VALUES(1,1,'2026-05-14','إيرادات الشهر',NULL,1,128352.0,190166.0,'2026-05-22 23:38:45.504668');
INSERT INTO gl_journal VALUES(2,1,'2026-04-26','مصروفات الشهر',NULL,1,153278.0,81356.0,'2026-05-22 23:38:45.504694');
INSERT INTO gl_journal VALUES(3,2,'2026-04-30','إيرادات الشهر',NULL,1,407461.0,172434.0,'2026-05-22 23:38:45.504707');
INSERT INTO gl_journal VALUES(4,2,'2026-05-15','مصروفات الشهر',NULL,1,157912.0,160940.0,'2026-05-22 23:38:45.504715');
INSERT INTO gl_journal VALUES(5,3,'2026-05-15','إيرادات الشهر',NULL,1,271819.0,162651.0,'2026-05-22 23:38:45.504722');
INSERT INTO gl_journal VALUES(6,3,'2026-05-14','مصروفات الشهر',NULL,1,157639.0,107079.0,'2026-05-22 23:38:45.504729');
INSERT INTO gl_journal VALUES(7,4,'2026-05-04','إيرادات الشهر',NULL,1,347729.0,340675.0,'2026-05-22 23:38:45.504737');
INSERT INTO gl_journal VALUES(8,4,'2026-05-16','مصروفات الشهر',NULL,1,133700.0,157044.0,'2026-05-22 23:38:45.504744');
INSERT INTO gl_journal VALUES(9,5,'2026-05-17','إيرادات الشهر',NULL,1,411333.0,350557.0,'2026-05-22 23:38:45.504751');
INSERT INTO gl_journal VALUES(10,5,'2026-05-10','مصروفات الشهر',NULL,1,186232.0,170548.0,'2026-05-22 23:38:45.504759');
INSERT INTO gl_journal VALUES(11,6,'2026-05-12','إيرادات الشهر',NULL,1,379233.0,265565.0,'2026-05-22 23:38:45.504766');
INSERT INTO gl_journal VALUES(12,6,'2026-04-29','مصروفات الشهر',NULL,1,69110.0,97787.0,'2026-05-22 23:38:45.504773');
INSERT INTO gl_journal VALUES(13,7,'2026-04-28','إيرادات الشهر',NULL,1,259757.0,355294.0,'2026-05-22 23:38:45.504780');
INSERT INTO gl_journal VALUES(14,7,'2026-05-07','مصروفات الشهر',NULL,1,98162.0,184839.0,'2026-05-22 23:38:45.504787');
INSERT INTO gl_journal VALUES(15,8,'2026-05-15','إيرادات الشهر',NULL,1,331639.0,112995.0,'2026-05-22 23:38:45.504794');
INSERT INTO gl_journal VALUES(16,8,'2026-05-05','مصروفات الشهر',NULL,1,78494.0,62241.0,'2026-05-22 23:38:45.504801');
INSERT INTO gl_journal VALUES(17,9,'2026-05-22','إيرادات الشهر',NULL,1,451322.0,307668.0,'2026-05-22 23:38:45.504808');
INSERT INTO gl_journal VALUES(18,9,'2026-05-14','مصروفات الشهر',NULL,1,106600.0,108841.0,'2026-05-22 23:38:45.504816');
INSERT INTO gl_journal VALUES(19,10,'2026-04-29','إيرادات الشهر',NULL,1,114254.0,153165.0,'2026-05-22 23:38:45.504824');
INSERT INTO gl_journal VALUES(20,10,'2026-05-17','مصروفات الشهر',NULL,1,53945.0,136616.0,'2026-05-22 23:38:45.504832');
CREATE TABLE payment (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	subscription_id INTEGER, 
	amount FLOAT, 
	payment_method VARCHAR(50), 
	transaction_id VARCHAR(100), 
	status VARCHAR(20), 
	notes TEXT, 
	paid_at DATETIME, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(subscription_id) REFERENCES subscription (id)
);
INSERT INTO payment VALUES(1,2,NULL,87500.0,'bank',NULL,'completed',NULL,'2026-05-23 00:00:00.000000','2026-05-23 00:00:00.000000');
INSERT INTO payment VALUES(2,2,NULL,87500.0,'bank',NULL,'completed',NULL,'2026-04-23 00:00:00.000000','2026-04-23 00:00:00.000000');
INSERT INTO payment VALUES(3,2,NULL,87500.0,'bank',NULL,'completed',NULL,'2026-03-24 00:00:00.000000','2026-03-24 00:00:00.000000');
INSERT INTO payment VALUES(4,3,NULL,37500.0,'cash',NULL,'completed',NULL,'2026-04-08 00:00:00.000000','2026-05-22 23:38:38.815146');
INSERT INTO payment VALUES(5,3,NULL,37500.0,'cash',NULL,'completed',NULL,'2026-05-08 00:00:00.000000','2026-05-22 23:38:38.815154');
INSERT INTO payment VALUES(6,5,NULL,250000.0,'bank',NULL,'completed',NULL,'2026-05-16 00:00:00.000000','2026-05-22 23:38:40.745811');
INSERT INTO payment VALUES(7,6,NULL,37500.0,'bank',NULL,'completed',NULL,'2026-05-14 00:00:00.000000','2026-05-22 23:38:41.744554');
INSERT INTO payment VALUES(8,7,NULL,87500.0,'bank',NULL,'completed',NULL,'2026-05-21 00:00:00.000000','2026-05-22 23:38:42.701774');
INSERT INTO payment VALUES(9,8,NULL,37500.0,'bank',NULL,'completed',NULL,'2026-05-16 00:00:00.000000','2026-05-22 23:38:43.642707');
INSERT INTO payment VALUES(10,9,NULL,87500.0,'bank',NULL,'completed',NULL,'2026-05-21 00:00:00.000000','2026-05-22 23:38:44.574944');
INSERT INTO payment VALUES(11,10,NULL,37500.0,'bank',NULL,'completed',NULL,'2026-05-19 00:00:00.000000','2026-05-22 23:38:45.492745');
CREATE TABLE ledger_entry (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	entry_date DATE, 
	entry_number VARCHAR(50), 
	description VARCHAR(500), 
	reference_type VARCHAR(50), 
	reference_id INTEGER, 
	total_debit FLOAT, 
	total_credit FLOAT, 
	status VARCHAR(20), 
	posted_at DATETIME, 
	posted_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	UNIQUE (entry_number), 
	FOREIGN KEY(posted_by) REFERENCES user (id)
);
INSERT INTO ledger_entry VALUES(1,2,'2026-05-23','PAY-2-1','دفعة اشتراك شهر 1',NULL,NULL,87500.0,87500.0,'posted','2026-05-22 23:38:37.727481',NULL,'2026-05-22 23:38:37.727486');
INSERT INTO ledger_entry VALUES(2,2,'2026-04-23','PAY-2-2','دفعة اشتراك شهر 2',NULL,NULL,87500.0,87500.0,'posted','2026-05-22 23:38:37.727489',NULL,'2026-05-22 23:38:37.727491');
INSERT INTO ledger_entry VALUES(3,2,'2026-03-24','PAY-2-3','دفعة اشتراك شهر 3',NULL,NULL,87500.0,87500.0,'posted','2026-05-22 23:38:37.727493',NULL,'2026-05-22 23:38:37.727495');
INSERT INTO ledger_entry VALUES(4,2,'2026-05-23','SAL-2-1','راتب محمد حسن - 2026-05',NULL,NULL,250000.0,250000.0,'posted','2026-05-22 23:38:37.760043',NULL,'2026-05-22 23:38:37.760049');
INSERT INTO ledger_entry VALUES(5,2,'2026-05-23','SAL-2-2','راتب خالد عمر - 2026-05',NULL,NULL,180000.0,180000.0,'posted','2026-05-22 23:38:37.760052',NULL,'2026-05-22 23:38:37.760054');
INSERT INTO ledger_entry VALUES(6,2,'2026-05-23','SAL-2-3','راتب سعيد أحمد - 2026-05',NULL,NULL,150000.0,150000.0,'posted','2026-05-22 23:38:37.760056',NULL,'2026-05-22 23:38:37.760058');
INSERT INTO ledger_entry VALUES(7,2,'2026-05-23','SAL-2-4','راتب علي صالح - 2026-05',NULL,NULL,390000.0,390000.0,'posted','2026-05-22 23:38:37.760060',NULL,'2026-05-22 23:38:37.760062');
INSERT INTO ledger_entry VALUES(8,2,'2026-05-23','SAL-2-5','راتب حسن عبدالله - 2026-05',NULL,NULL,312000.0,312000.0,'posted','2026-05-22 23:38:37.760064',NULL,'2026-05-22 23:38:37.760067');
CREATE TABLE contract (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	supplier_id INTEGER, 
	contract_number VARCHAR(50), 
	type VARCHAR(20), 
	start_date DATE, 
	end_date DATE, 
	amount FLOAT, 
	terms TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(supplier_id) REFERENCES supplier (id)
);
CREATE TABLE invoice (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	supplier_id INTEGER, 
	invoice_number VARCHAR(50), 
	date DATE, 
	amount FLOAT, 
	paid FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(supplier_id) REFERENCES supplier (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE purchase_item (
	id INTEGER NOT NULL, 
	purchase_id INTEGER NOT NULL, 
	product_id INTEGER, 
	product_name VARCHAR(120), 
	quantity FLOAT, 
	price FLOAT, 
	total FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(purchase_id) REFERENCES purchase (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE sales_invoice_item (
	id INTEGER NOT NULL, 
	invoice_id INTEGER NOT NULL, 
	product_id INTEGER, 
	product_name VARCHAR(120), 
	quantity FLOAT, 
	price FLOAT, 
	total FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(invoice_id) REFERENCES sales_invoice (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE daily_attendance (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	project_id INTEGER, 
	date DATE, 
	status VARCHAR(20), 
	hours FLOAT, 
	daily_wage FLOAT, 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(project_id) REFERENCES project (id)
);
INSERT INTO daily_attendance VALUES(1,2,1,1,'2026-05-23','present',8.0,5000.0,'','2026-05-23 13:26:48.061232');
CREATE TABLE daily_payment (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	project_id INTEGER, 
	date DATE, 
	amount FLOAT, 
	payment_method VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(project_id) REFERENCES project (id)
);
CREATE TABLE evaluation_score (
	id INTEGER NOT NULL, 
	evaluation_id INTEGER NOT NULL, 
	criteria_id INTEGER NOT NULL, 
	score FLOAT, 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(evaluation_id) REFERENCES evaluation (id), 
	FOREIGN KEY(criteria_id) REFERENCES evaluation_criteria (id)
);
CREATE TABLE claim (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	claim_number VARCHAR(50), 
	date DATE, 
	amount FLOAT, 
	approved_amount FLOAT, 
	paid_amount FLOAT, 
	completion_percentage FLOAT, 
	status VARCHAR(20), 
	notes TEXT, 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(project_id) REFERENCES project (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
INSERT INTO claim VALUES(1,2,1,'66','2026-05-23',5000000.0,2500000.0,2500000.0,50.0,'pending','دفعة من قيمة المشروع',2,'2026-05-23 12:49:29.350097');
CREATE TABLE material_purchase (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	supplier_id INTEGER, 
	project_id INTEGER, 
	date DATE, 
	total FLOAT, 
	paid FLOAT, 
	payment_method VARCHAR(20), 
	notes TEXT, 
	invoice_number VARCHAR(50), 
	created_by INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(supplier_id) REFERENCES supplier (id), 
	FOREIGN KEY(project_id) REFERENCES project (id), 
	FOREIGN KEY(created_by) REFERENCES user (id)
);
CREATE TABLE exam (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	subject_id INTEGER, 
	student_id INTEGER, 
	score FLOAT, 
	max_score FLOAT, 
	date DATE, 
	exam_type VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(subject_id) REFERENCES subject (id), 
	FOREIGN KEY(student_id) REFERENCES student (id)
);
CREATE TABLE work_site (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	client_id INTEGER, 
	address VARCHAR(200), 
	supervisor_id INTEGER, 
	worker_count INTEGER, 
	work_hours VARCHAR(50), 
	contract_id INTEGER, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id), 
	FOREIGN KEY(supervisor_id) REFERENCES employee (id), 
	FOREIGN KEY(contract_id) REFERENCES contract (id)
);
CREATE TABLE journal_line (
	id INTEGER NOT NULL, 
	entry_id INTEGER NOT NULL, 
	account_id INTEGER, 
	account VARCHAR(100), 
	description VARCHAR(200), 
	debit FLOAT, 
	credit FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(entry_id) REFERENCES journal_entry (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE gl_journal_line (
	id INTEGER NOT NULL, 
	journal_id INTEGER NOT NULL, 
	account_code VARCHAR(20), 
	account_name VARCHAR(100), 
	description VARCHAR(200), 
	debit FLOAT, 
	credit FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(journal_id) REFERENCES gl_journal (id)
);
CREATE TABLE ledger_line (
	id INTEGER NOT NULL, 
	entry_id INTEGER NOT NULL, 
	account_code VARCHAR(20), 
	account_name VARCHAR(200), 
	debit FLOAT, 
	credit FLOAT, 
	notes VARCHAR(500), 
	PRIMARY KEY (id), 
	FOREIGN KEY(entry_id) REFERENCES ledger_entry (id)
);
CREATE TABLE material_item (
	id INTEGER NOT NULL, 
	purchase_id INTEGER NOT NULL, 
	material_name VARCHAR(120), 
	quantity FLOAT, 
	unit VARCHAR(20), 
	price FLOAT, 
	total FLOAT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(purchase_id) REFERENCES material_purchase (id)
);
CREATE TABLE supervisor_report (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	site_id INTEGER, 
	supervisor_id INTEGER, 
	date DATE, 
	report TEXT, 
	issues TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(site_id) REFERENCES work_site (id), 
	FOREIGN KEY(supervisor_id) REFERENCES employee (id)
);
CREATE TABLE visit (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	site_id INTEGER, 
	visitor_id INTEGER, 
	date DATE, 
	notes TEXT, 
	rating INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(site_id) REFERENCES work_site (id), 
	FOREIGN KEY(visitor_id) REFERENCES employee (id)
);
CREATE TABLE complaint (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	client_id INTEGER, 
	site_id INTEGER, 
	date DATE, 
	description TEXT, 
	status VARCHAR(20), 
	resolution TEXT, 
	created_at DATETIME, 
	resolved_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(client_id) REFERENCES client (id), 
	FOREIGN KEY(site_id) REFERENCES work_site (id)
);
CREATE TABLE team (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	supervisor_id INTEGER, 
	site_id INTEGER, 
	status VARCHAR(20), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(supervisor_id) REFERENCES employee (id), 
	FOREIGN KEY(site_id) REFERENCES work_site (id)
);
CREATE TABLE team_member (
	id INTEGER NOT NULL, 
	team_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(team_id) REFERENCES team (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
CREATE TABLE et_shift_type (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	status VARCHAR(20), 
	created_at DATETIME, work_days INTEGER DEFAULT 6, vacation_days INTEGER DEFAULT 1, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO et_shift_type VALUES(2,1,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.005133',4,3);
INSERT INTO et_shift_type VALUES(3,1,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.005144',4,3);
INSERT INTO et_shift_type VALUES(4,1,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.005149',4,3);
INSERT INTO et_shift_type VALUES(5,1,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.005152',4,3);
INSERT INTO et_shift_type VALUES(6,1,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.005156',4,3);
INSERT INTO et_shift_type VALUES(7,1,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.005159',7,7);
INSERT INTO et_shift_type VALUES(8,1,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.005162',7,7);
INSERT INTO et_shift_type VALUES(9,1,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.005165',14,7);
INSERT INTO et_shift_type VALUES(10,1,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.005168',14,7);
INSERT INTO et_shift_type VALUES(11,1,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.005172',6,1);
INSERT INTO et_shift_type VALUES(12,1,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.005175',28,28);
INSERT INTO et_shift_type VALUES(13,1,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.005179',28,28);
INSERT INTO et_shift_type VALUES(14,1,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.005182',28,28);
INSERT INTO et_shift_type VALUES(15,1,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.005186',28,28);
INSERT INTO et_shift_type VALUES(16,1,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.005189',42,14);
INSERT INTO et_shift_type VALUES(17,1,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.005192',42,14);
INSERT INTO et_shift_type VALUES(18,1,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.005195',5,2);
INSERT INTO et_shift_type VALUES(19,1,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.005199',6,1);
INSERT INTO et_shift_type VALUES(20,1,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.005202',7,0);
INSERT INTO et_shift_type VALUES(21,1,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.005206',4,3);
INSERT INTO et_shift_type VALUES(22,1,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.005209',4,3);
INSERT INTO et_shift_type VALUES(23,1,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.005212',42,21);
INSERT INTO et_shift_type VALUES(24,1,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.005216',6,1);
INSERT INTO et_shift_type VALUES(25,1,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.005226',6,1);
INSERT INTO et_shift_type VALUES(26,1,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.005235',6,1);
INSERT INTO et_shift_type VALUES(27,1,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.005238',6,1);
INSERT INTO et_shift_type VALUES(28,1,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.005242',6,1);
INSERT INTO et_shift_type VALUES(29,1,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.005248',6,1);
INSERT INTO et_shift_type VALUES(30,2,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.029751',4,3);
INSERT INTO et_shift_type VALUES(31,2,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.029759',4,3);
INSERT INTO et_shift_type VALUES(32,2,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.029762',4,3);
INSERT INTO et_shift_type VALUES(33,2,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.029765',4,3);
INSERT INTO et_shift_type VALUES(34,2,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.029769',4,3);
INSERT INTO et_shift_type VALUES(35,2,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.029772',7,7);
INSERT INTO et_shift_type VALUES(36,2,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.029775',7,7);
INSERT INTO et_shift_type VALUES(37,2,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.029778',14,7);
INSERT INTO et_shift_type VALUES(38,2,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.029781',14,7);
INSERT INTO et_shift_type VALUES(39,2,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.029784',6,1);
INSERT INTO et_shift_type VALUES(40,2,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.029787',28,28);
INSERT INTO et_shift_type VALUES(41,2,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.029791',28,28);
INSERT INTO et_shift_type VALUES(42,2,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.029794',28,28);
INSERT INTO et_shift_type VALUES(43,2,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.029797',28,28);
INSERT INTO et_shift_type VALUES(44,2,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.029801',42,14);
INSERT INTO et_shift_type VALUES(45,2,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.029804',42,14);
INSERT INTO et_shift_type VALUES(46,2,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.029808',5,2);
INSERT INTO et_shift_type VALUES(47,2,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.029811',6,1);
INSERT INTO et_shift_type VALUES(48,2,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.029814',7,0);
INSERT INTO et_shift_type VALUES(49,2,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.029818',4,3);
INSERT INTO et_shift_type VALUES(50,2,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.029821',4,3);
INSERT INTO et_shift_type VALUES(51,2,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.029825',42,21);
INSERT INTO et_shift_type VALUES(52,2,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.029828',6,1);
INSERT INTO et_shift_type VALUES(53,2,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.029832',6,1);
INSERT INTO et_shift_type VALUES(54,2,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.029835',6,1);
INSERT INTO et_shift_type VALUES(55,2,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.029839',6,1);
INSERT INTO et_shift_type VALUES(56,2,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.029842',6,1);
INSERT INTO et_shift_type VALUES(57,2,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.029846',6,1);
INSERT INTO et_shift_type VALUES(58,3,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.048301',4,3);
INSERT INTO et_shift_type VALUES(59,3,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.048311',4,3);
INSERT INTO et_shift_type VALUES(60,3,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.048314',4,3);
INSERT INTO et_shift_type VALUES(61,3,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.048317',4,3);
INSERT INTO et_shift_type VALUES(62,3,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.048320',4,3);
INSERT INTO et_shift_type VALUES(63,3,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.048323',7,7);
INSERT INTO et_shift_type VALUES(64,3,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.048327',7,7);
INSERT INTO et_shift_type VALUES(65,3,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.048329',14,7);
INSERT INTO et_shift_type VALUES(66,3,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.048331',14,7);
INSERT INTO et_shift_type VALUES(67,3,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.048333',6,1);
INSERT INTO et_shift_type VALUES(68,3,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.048334',28,28);
INSERT INTO et_shift_type VALUES(69,3,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.048336',28,28);
INSERT INTO et_shift_type VALUES(70,3,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.048338',28,28);
INSERT INTO et_shift_type VALUES(71,3,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.048340',28,28);
INSERT INTO et_shift_type VALUES(72,3,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.048341',42,14);
INSERT INTO et_shift_type VALUES(73,3,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.048343',42,14);
INSERT INTO et_shift_type VALUES(74,3,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.048345',5,2);
INSERT INTO et_shift_type VALUES(75,3,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.048347',6,1);
INSERT INTO et_shift_type VALUES(76,3,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.048349',7,0);
INSERT INTO et_shift_type VALUES(77,3,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.048351',4,3);
INSERT INTO et_shift_type VALUES(78,3,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.048352',4,3);
INSERT INTO et_shift_type VALUES(79,3,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.048354',42,21);
INSERT INTO et_shift_type VALUES(80,3,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.048356',6,1);
INSERT INTO et_shift_type VALUES(81,3,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.048359',6,1);
INSERT INTO et_shift_type VALUES(82,3,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.048362',6,1);
INSERT INTO et_shift_type VALUES(83,3,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.048365',6,1);
INSERT INTO et_shift_type VALUES(84,3,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.048368',6,1);
INSERT INTO et_shift_type VALUES(85,3,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.048371',6,1);
INSERT INTO et_shift_type VALUES(86,4,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.063845',4,3);
INSERT INTO et_shift_type VALUES(87,4,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.063853',4,3);
INSERT INTO et_shift_type VALUES(88,4,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.063856',4,3);
INSERT INTO et_shift_type VALUES(89,4,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.063859',4,3);
INSERT INTO et_shift_type VALUES(90,4,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.063862',4,3);
INSERT INTO et_shift_type VALUES(91,4,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.063865',7,7);
INSERT INTO et_shift_type VALUES(92,4,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.063868',7,7);
INSERT INTO et_shift_type VALUES(93,4,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.063871',14,7);
INSERT INTO et_shift_type VALUES(94,4,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.063874',14,7);
INSERT INTO et_shift_type VALUES(95,4,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.063876',6,1);
INSERT INTO et_shift_type VALUES(96,4,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.063879',28,28);
INSERT INTO et_shift_type VALUES(97,4,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.063882',28,28);
INSERT INTO et_shift_type VALUES(98,4,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.063885',28,28);
INSERT INTO et_shift_type VALUES(99,4,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.063888',28,28);
INSERT INTO et_shift_type VALUES(100,4,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.063891',42,14);
INSERT INTO et_shift_type VALUES(101,4,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.063893',42,14);
INSERT INTO et_shift_type VALUES(102,4,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.063896',5,2);
INSERT INTO et_shift_type VALUES(103,4,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.063899',6,1);
INSERT INTO et_shift_type VALUES(104,4,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.063901',7,0);
INSERT INTO et_shift_type VALUES(105,4,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.063904',4,3);
INSERT INTO et_shift_type VALUES(106,4,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.063907',4,3);
INSERT INTO et_shift_type VALUES(107,4,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.063910',42,21);
INSERT INTO et_shift_type VALUES(108,4,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.063912',6,1);
INSERT INTO et_shift_type VALUES(109,4,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.063915',6,1);
INSERT INTO et_shift_type VALUES(110,4,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.063918',6,1);
INSERT INTO et_shift_type VALUES(111,4,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.063920',6,1);
INSERT INTO et_shift_type VALUES(112,4,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.063923',6,1);
INSERT INTO et_shift_type VALUES(113,4,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.063926',6,1);
INSERT INTO et_shift_type VALUES(114,5,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.078706',4,3);
INSERT INTO et_shift_type VALUES(115,5,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.078711',4,3);
INSERT INTO et_shift_type VALUES(116,5,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.078714',4,3);
INSERT INTO et_shift_type VALUES(117,5,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.078716',4,3);
INSERT INTO et_shift_type VALUES(118,5,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.078718',4,3);
INSERT INTO et_shift_type VALUES(119,5,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.078720',7,7);
INSERT INTO et_shift_type VALUES(120,5,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.078722',7,7);
INSERT INTO et_shift_type VALUES(121,5,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.078724',14,7);
INSERT INTO et_shift_type VALUES(122,5,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.078726',14,7);
INSERT INTO et_shift_type VALUES(123,5,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.078728',6,1);
INSERT INTO et_shift_type VALUES(124,5,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.078731',28,28);
INSERT INTO et_shift_type VALUES(125,5,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.078732',28,28);
INSERT INTO et_shift_type VALUES(126,5,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.078734',28,28);
INSERT INTO et_shift_type VALUES(127,5,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.078737',28,28);
INSERT INTO et_shift_type VALUES(128,5,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.078739',42,14);
INSERT INTO et_shift_type VALUES(129,5,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.078741',42,14);
INSERT INTO et_shift_type VALUES(130,5,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.078743',5,2);
INSERT INTO et_shift_type VALUES(131,5,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.078744',6,1);
INSERT INTO et_shift_type VALUES(132,5,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.078746',7,0);
INSERT INTO et_shift_type VALUES(133,5,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.078748',4,3);
INSERT INTO et_shift_type VALUES(134,5,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.078750',4,3);
INSERT INTO et_shift_type VALUES(135,5,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.078752',42,21);
INSERT INTO et_shift_type VALUES(136,5,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.078754',6,1);
INSERT INTO et_shift_type VALUES(137,5,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.078756',6,1);
INSERT INTO et_shift_type VALUES(138,5,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.078758',6,1);
INSERT INTO et_shift_type VALUES(139,5,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.078760',6,1);
INSERT INTO et_shift_type VALUES(140,5,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.078762',6,1);
INSERT INTO et_shift_type VALUES(141,5,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.078764',6,1);
INSERT INTO et_shift_type VALUES(142,6,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.093075',4,3);
INSERT INTO et_shift_type VALUES(143,6,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.093080',4,3);
INSERT INTO et_shift_type VALUES(144,6,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.093081',4,3);
INSERT INTO et_shift_type VALUES(145,6,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.093083',4,3);
INSERT INTO et_shift_type VALUES(146,6,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.093085',4,3);
INSERT INTO et_shift_type VALUES(147,6,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.093087',7,7);
INSERT INTO et_shift_type VALUES(148,6,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.093088',7,7);
INSERT INTO et_shift_type VALUES(149,6,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.093090',14,7);
INSERT INTO et_shift_type VALUES(150,6,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.093092',14,7);
INSERT INTO et_shift_type VALUES(151,6,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.093093',6,1);
INSERT INTO et_shift_type VALUES(152,6,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.093095',28,28);
INSERT INTO et_shift_type VALUES(153,6,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.093096',28,28);
INSERT INTO et_shift_type VALUES(154,6,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.093098',28,28);
INSERT INTO et_shift_type VALUES(155,6,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.093100',28,28);
INSERT INTO et_shift_type VALUES(156,6,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.093102',42,14);
INSERT INTO et_shift_type VALUES(157,6,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.093103',42,14);
INSERT INTO et_shift_type VALUES(158,6,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.093105',5,2);
INSERT INTO et_shift_type VALUES(159,6,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.093106',6,1);
INSERT INTO et_shift_type VALUES(160,6,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.093108',7,0);
INSERT INTO et_shift_type VALUES(161,6,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.093110',4,3);
INSERT INTO et_shift_type VALUES(162,6,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.093111',4,3);
INSERT INTO et_shift_type VALUES(163,6,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.093113',42,21);
INSERT INTO et_shift_type VALUES(164,6,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.093114',6,1);
INSERT INTO et_shift_type VALUES(165,6,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.093116',6,1);
INSERT INTO et_shift_type VALUES(166,6,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.093118',6,1);
INSERT INTO et_shift_type VALUES(167,6,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.093120',6,1);
INSERT INTO et_shift_type VALUES(168,6,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.093123',6,1);
INSERT INTO et_shift_type VALUES(169,6,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.093124',6,1);
INSERT INTO et_shift_type VALUES(170,7,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.105411',4,3);
INSERT INTO et_shift_type VALUES(171,7,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.105419',4,3);
INSERT INTO et_shift_type VALUES(172,7,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.105422',4,3);
INSERT INTO et_shift_type VALUES(173,7,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.105425',4,3);
INSERT INTO et_shift_type VALUES(174,7,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.105427',4,3);
INSERT INTO et_shift_type VALUES(175,7,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.105430',7,7);
INSERT INTO et_shift_type VALUES(176,7,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.105433',7,7);
INSERT INTO et_shift_type VALUES(177,7,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.105435',14,7);
INSERT INTO et_shift_type VALUES(178,7,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.105438',14,7);
INSERT INTO et_shift_type VALUES(179,7,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.105441',6,1);
INSERT INTO et_shift_type VALUES(180,7,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.105444',28,28);
INSERT INTO et_shift_type VALUES(181,7,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.105447',28,28);
INSERT INTO et_shift_type VALUES(182,7,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.105450',28,28);
INSERT INTO et_shift_type VALUES(183,7,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.105452',28,28);
INSERT INTO et_shift_type VALUES(184,7,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.105455',42,14);
INSERT INTO et_shift_type VALUES(185,7,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.105457',42,14);
INSERT INTO et_shift_type VALUES(186,7,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.105460',5,2);
INSERT INTO et_shift_type VALUES(187,7,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.105462',6,1);
INSERT INTO et_shift_type VALUES(188,7,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.105466',7,0);
INSERT INTO et_shift_type VALUES(189,7,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.105469',4,3);
INSERT INTO et_shift_type VALUES(190,7,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.105472',4,3);
INSERT INTO et_shift_type VALUES(191,7,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.105475',42,21);
INSERT INTO et_shift_type VALUES(192,7,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.105478',6,1);
INSERT INTO et_shift_type VALUES(193,7,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.105481',6,1);
INSERT INTO et_shift_type VALUES(194,7,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.105484',6,1);
INSERT INTO et_shift_type VALUES(195,7,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.105487',6,1);
INSERT INTO et_shift_type VALUES(196,7,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.105490',6,1);
INSERT INTO et_shift_type VALUES(197,7,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.105493',6,1);
INSERT INTO et_shift_type VALUES(198,8,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.125844',4,3);
INSERT INTO et_shift_type VALUES(199,8,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.125853',4,3);
INSERT INTO et_shift_type VALUES(200,8,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.125858',4,3);
INSERT INTO et_shift_type VALUES(201,8,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.125863',4,3);
INSERT INTO et_shift_type VALUES(202,8,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.125867',4,3);
INSERT INTO et_shift_type VALUES(203,8,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.125871',7,7);
INSERT INTO et_shift_type VALUES(204,8,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.125875',7,7);
INSERT INTO et_shift_type VALUES(205,8,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.125879',14,7);
INSERT INTO et_shift_type VALUES(206,8,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.125883',14,7);
INSERT INTO et_shift_type VALUES(207,8,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.125887',6,1);
INSERT INTO et_shift_type VALUES(208,8,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.125891',28,28);
INSERT INTO et_shift_type VALUES(209,8,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.125895',28,28);
INSERT INTO et_shift_type VALUES(210,8,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.125899',28,28);
INSERT INTO et_shift_type VALUES(211,8,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.125904',28,28);
INSERT INTO et_shift_type VALUES(212,8,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.125908',42,14);
INSERT INTO et_shift_type VALUES(213,8,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.125913',42,14);
INSERT INTO et_shift_type VALUES(214,8,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.125917',5,2);
INSERT INTO et_shift_type VALUES(215,8,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.125922',6,1);
INSERT INTO et_shift_type VALUES(216,8,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.125926',7,0);
INSERT INTO et_shift_type VALUES(217,8,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.125930',4,3);
INSERT INTO et_shift_type VALUES(218,8,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.125934',4,3);
INSERT INTO et_shift_type VALUES(219,8,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.125939',42,21);
INSERT INTO et_shift_type VALUES(220,8,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.125943',6,1);
INSERT INTO et_shift_type VALUES(221,8,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.125947',6,1);
INSERT INTO et_shift_type VALUES(222,8,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.125951',6,1);
INSERT INTO et_shift_type VALUES(223,8,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.125954',6,1);
INSERT INTO et_shift_type VALUES(224,8,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.125959',6,1);
INSERT INTO et_shift_type VALUES(225,8,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.125963',6,1);
INSERT INTO et_shift_type VALUES(226,9,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.141008',4,3);
INSERT INTO et_shift_type VALUES(227,9,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.141013',4,3);
INSERT INTO et_shift_type VALUES(228,9,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.141016',4,3);
INSERT INTO et_shift_type VALUES(229,9,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.141018',4,3);
INSERT INTO et_shift_type VALUES(230,9,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.141020',4,3);
INSERT INTO et_shift_type VALUES(231,9,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.141022',7,7);
INSERT INTO et_shift_type VALUES(232,9,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.141024',7,7);
INSERT INTO et_shift_type VALUES(233,9,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.141026',14,7);
INSERT INTO et_shift_type VALUES(234,9,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.141029',14,7);
INSERT INTO et_shift_type VALUES(235,9,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.141031',6,1);
INSERT INTO et_shift_type VALUES(236,9,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.141033',28,28);
INSERT INTO et_shift_type VALUES(237,9,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.141035',28,28);
INSERT INTO et_shift_type VALUES(238,9,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.141037',28,28);
INSERT INTO et_shift_type VALUES(239,9,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.141039',28,28);
INSERT INTO et_shift_type VALUES(240,9,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.141041',42,14);
INSERT INTO et_shift_type VALUES(241,9,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.141043',42,14);
INSERT INTO et_shift_type VALUES(242,9,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.141045',5,2);
INSERT INTO et_shift_type VALUES(243,9,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.141047',6,1);
INSERT INTO et_shift_type VALUES(244,9,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.141049',7,0);
INSERT INTO et_shift_type VALUES(245,9,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.141051',4,3);
INSERT INTO et_shift_type VALUES(246,9,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.141053',4,3);
INSERT INTO et_shift_type VALUES(247,9,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.141055',42,21);
INSERT INTO et_shift_type VALUES(248,9,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.141057',6,1);
INSERT INTO et_shift_type VALUES(249,9,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.141060',6,1);
INSERT INTO et_shift_type VALUES(250,9,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.141062',6,1);
INSERT INTO et_shift_type VALUES(251,9,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.141064',6,1);
INSERT INTO et_shift_type VALUES(252,9,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.141066',6,1);
INSERT INTO et_shift_type VALUES(253,9,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.141068',6,1);
INSERT INTO et_shift_type VALUES(254,10,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.157142',4,3);
INSERT INTO et_shift_type VALUES(255,10,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.157150',4,3);
INSERT INTO et_shift_type VALUES(256,10,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.157153',4,3);
INSERT INTO et_shift_type VALUES(257,10,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.157155',4,3);
INSERT INTO et_shift_type VALUES(258,10,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.157158',4,3);
INSERT INTO et_shift_type VALUES(259,10,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.157161',7,7);
INSERT INTO et_shift_type VALUES(260,10,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.157163',7,7);
INSERT INTO et_shift_type VALUES(261,10,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.157165',14,7);
INSERT INTO et_shift_type VALUES(262,10,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.157168',14,7);
INSERT INTO et_shift_type VALUES(263,10,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.157170',6,1);
INSERT INTO et_shift_type VALUES(264,10,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.157173',28,28);
INSERT INTO et_shift_type VALUES(265,10,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.157175',28,28);
INSERT INTO et_shift_type VALUES(266,10,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.157178',28,28);
INSERT INTO et_shift_type VALUES(267,10,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.157180',28,28);
INSERT INTO et_shift_type VALUES(268,10,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.157183',42,14);
INSERT INTO et_shift_type VALUES(269,10,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.157185',42,14);
INSERT INTO et_shift_type VALUES(270,10,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.157188',5,2);
INSERT INTO et_shift_type VALUES(271,10,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.157190',6,1);
INSERT INTO et_shift_type VALUES(272,10,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.157193',7,0);
INSERT INTO et_shift_type VALUES(273,10,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.157195',4,3);
INSERT INTO et_shift_type VALUES(274,10,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.157197',4,3);
INSERT INTO et_shift_type VALUES(275,10,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.157200',42,21);
INSERT INTO et_shift_type VALUES(276,10,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.157202',6,1);
INSERT INTO et_shift_type VALUES(277,10,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.157205',6,1);
INSERT INTO et_shift_type VALUES(278,10,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.157207',6,1);
INSERT INTO et_shift_type VALUES(279,10,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.157209',6,1);
INSERT INTO et_shift_type VALUES(280,10,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.157212',6,1);
INSERT INTO et_shift_type VALUES(281,10,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.157214',6,1);
INSERT INTO et_shift_type VALUES(282,11,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.173807',4,3);
INSERT INTO et_shift_type VALUES(283,11,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.173813',4,3);
INSERT INTO et_shift_type VALUES(284,11,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.173817',4,3);
INSERT INTO et_shift_type VALUES(285,11,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.173819',4,3);
INSERT INTO et_shift_type VALUES(286,11,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.173821',4,3);
INSERT INTO et_shift_type VALUES(287,11,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.173823',7,7);
INSERT INTO et_shift_type VALUES(288,11,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.173825',7,7);
INSERT INTO et_shift_type VALUES(289,11,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.173826',14,7);
INSERT INTO et_shift_type VALUES(290,11,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.173829',14,7);
INSERT INTO et_shift_type VALUES(291,11,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.173832',6,1);
INSERT INTO et_shift_type VALUES(292,11,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.173834',28,28);
INSERT INTO et_shift_type VALUES(293,11,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.173839',28,28);
INSERT INTO et_shift_type VALUES(294,11,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.173842',28,28);
INSERT INTO et_shift_type VALUES(295,11,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.173845',28,28);
INSERT INTO et_shift_type VALUES(296,11,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.173847',42,14);
INSERT INTO et_shift_type VALUES(297,11,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.173850',42,14);
INSERT INTO et_shift_type VALUES(298,11,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.173852',5,2);
INSERT INTO et_shift_type VALUES(299,11,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.173855',6,1);
INSERT INTO et_shift_type VALUES(300,11,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.173858',7,0);
INSERT INTO et_shift_type VALUES(301,11,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.173860',4,3);
INSERT INTO et_shift_type VALUES(302,11,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.173863',4,3);
INSERT INTO et_shift_type VALUES(303,11,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.173866',42,21);
INSERT INTO et_shift_type VALUES(304,11,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.173868',6,1);
INSERT INTO et_shift_type VALUES(305,11,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.173871',6,1);
INSERT INTO et_shift_type VALUES(306,11,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.173874',6,1);
INSERT INTO et_shift_type VALUES(307,11,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.173877',6,1);
INSERT INTO et_shift_type VALUES(308,11,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.173879',6,1);
INSERT INTO et_shift_type VALUES(309,11,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.173882',6,1);
INSERT INTO et_shift_type VALUES(310,12,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.190367',4,3);
INSERT INTO et_shift_type VALUES(311,12,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.190374',4,3);
INSERT INTO et_shift_type VALUES(312,12,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.190378',4,3);
INSERT INTO et_shift_type VALUES(313,12,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.190381',4,3);
INSERT INTO et_shift_type VALUES(314,12,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.190384',4,3);
INSERT INTO et_shift_type VALUES(315,12,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.190387',7,7);
INSERT INTO et_shift_type VALUES(316,12,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.190390',7,7);
INSERT INTO et_shift_type VALUES(317,12,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.190393',14,7);
INSERT INTO et_shift_type VALUES(318,12,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.190397',14,7);
INSERT INTO et_shift_type VALUES(319,12,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.190399',6,1);
INSERT INTO et_shift_type VALUES(320,12,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.190403',28,28);
INSERT INTO et_shift_type VALUES(321,12,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.190410',28,28);
INSERT INTO et_shift_type VALUES(322,12,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.190413',28,28);
INSERT INTO et_shift_type VALUES(323,12,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.190416',28,28);
INSERT INTO et_shift_type VALUES(324,12,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.190419',42,14);
INSERT INTO et_shift_type VALUES(325,12,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.190422',42,14);
INSERT INTO et_shift_type VALUES(326,12,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.190425',5,2);
INSERT INTO et_shift_type VALUES(327,12,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.190428',6,1);
INSERT INTO et_shift_type VALUES(328,12,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.190431',7,0);
INSERT INTO et_shift_type VALUES(329,12,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.190434',4,3);
INSERT INTO et_shift_type VALUES(330,12,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.190437',4,3);
INSERT INTO et_shift_type VALUES(331,12,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.190440',42,21);
INSERT INTO et_shift_type VALUES(332,12,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.190443',6,1);
INSERT INTO et_shift_type VALUES(333,12,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.190446',6,1);
INSERT INTO et_shift_type VALUES(334,12,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.190450',6,1);
INSERT INTO et_shift_type VALUES(335,12,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.190453',6,1);
INSERT INTO et_shift_type VALUES(336,12,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.190456',6,1);
INSERT INTO et_shift_type VALUES(337,12,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.190459',6,1);
INSERT INTO et_shift_type VALUES(338,13,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.206569',4,3);
INSERT INTO et_shift_type VALUES(339,13,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.206577',4,3);
INSERT INTO et_shift_type VALUES(340,13,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.206581',4,3);
INSERT INTO et_shift_type VALUES(341,13,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.206583',4,3);
INSERT INTO et_shift_type VALUES(342,13,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.206586',4,3);
INSERT INTO et_shift_type VALUES(343,13,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.206589',7,7);
INSERT INTO et_shift_type VALUES(344,13,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.206591',7,7);
INSERT INTO et_shift_type VALUES(345,13,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.206593',14,7);
INSERT INTO et_shift_type VALUES(346,13,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.206596',14,7);
INSERT INTO et_shift_type VALUES(347,13,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.206598',6,1);
INSERT INTO et_shift_type VALUES(348,13,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.206601',28,28);
INSERT INTO et_shift_type VALUES(349,13,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.206604',28,28);
INSERT INTO et_shift_type VALUES(350,13,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.206606',28,28);
INSERT INTO et_shift_type VALUES(351,13,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.206609',28,28);
INSERT INTO et_shift_type VALUES(352,13,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.206611',42,14);
INSERT INTO et_shift_type VALUES(353,13,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.206613',42,14);
INSERT INTO et_shift_type VALUES(354,13,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.206616',5,2);
INSERT INTO et_shift_type VALUES(355,13,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.206618',6,1);
INSERT INTO et_shift_type VALUES(356,13,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.206621',7,0);
INSERT INTO et_shift_type VALUES(357,13,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.206624',4,3);
INSERT INTO et_shift_type VALUES(358,13,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.206626',4,3);
INSERT INTO et_shift_type VALUES(359,13,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.206628',42,21);
INSERT INTO et_shift_type VALUES(360,13,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.206631',6,1);
INSERT INTO et_shift_type VALUES(361,13,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.206633',6,1);
INSERT INTO et_shift_type VALUES(362,13,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.206636',6,1);
INSERT INTO et_shift_type VALUES(363,13,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.206638',6,1);
INSERT INTO et_shift_type VALUES(364,13,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.206641',6,1);
INSERT INTO et_shift_type VALUES(365,13,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.206645',6,1);
INSERT INTO et_shift_type VALUES(366,14,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.221166',4,3);
INSERT INTO et_shift_type VALUES(367,14,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.221174',4,3);
INSERT INTO et_shift_type VALUES(368,14,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.221177',4,3);
INSERT INTO et_shift_type VALUES(369,14,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.221180',4,3);
INSERT INTO et_shift_type VALUES(370,14,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.221183',4,3);
INSERT INTO et_shift_type VALUES(371,14,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.221185',7,7);
INSERT INTO et_shift_type VALUES(372,14,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.221187',7,7);
INSERT INTO et_shift_type VALUES(373,14,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.221190',14,7);
INSERT INTO et_shift_type VALUES(374,14,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.221192',14,7);
INSERT INTO et_shift_type VALUES(375,14,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.221195',6,1);
INSERT INTO et_shift_type VALUES(376,14,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.221197',28,28);
INSERT INTO et_shift_type VALUES(377,14,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.221200',28,28);
INSERT INTO et_shift_type VALUES(378,14,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.221203',28,28);
INSERT INTO et_shift_type VALUES(379,14,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.221205',28,28);
INSERT INTO et_shift_type VALUES(380,14,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.221208',42,14);
INSERT INTO et_shift_type VALUES(381,14,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.221210',42,14);
INSERT INTO et_shift_type VALUES(382,14,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.221213',5,2);
INSERT INTO et_shift_type VALUES(383,14,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.221216',6,1);
INSERT INTO et_shift_type VALUES(384,14,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.221218',7,0);
INSERT INTO et_shift_type VALUES(385,14,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.221220',4,3);
INSERT INTO et_shift_type VALUES(386,14,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.221223',4,3);
INSERT INTO et_shift_type VALUES(387,14,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.221225',42,21);
INSERT INTO et_shift_type VALUES(388,14,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.221228',6,1);
INSERT INTO et_shift_type VALUES(389,14,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.221230',6,1);
INSERT INTO et_shift_type VALUES(390,14,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.221233',6,1);
INSERT INTO et_shift_type VALUES(391,14,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.221235',6,1);
INSERT INTO et_shift_type VALUES(392,14,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.221238',6,1);
INSERT INTO et_shift_type VALUES(393,14,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.221240',6,1);
INSERT INTO et_shift_type VALUES(394,15,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.237985',4,3);
INSERT INTO et_shift_type VALUES(395,15,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.237992',4,3);
INSERT INTO et_shift_type VALUES(396,15,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.237995',4,3);
INSERT INTO et_shift_type VALUES(397,15,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.237998',4,3);
INSERT INTO et_shift_type VALUES(398,15,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.238000',4,3);
INSERT INTO et_shift_type VALUES(399,15,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.238003',7,7);
INSERT INTO et_shift_type VALUES(400,15,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.238006',7,7);
INSERT INTO et_shift_type VALUES(401,15,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.238008',14,7);
INSERT INTO et_shift_type VALUES(402,15,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.238011',14,7);
INSERT INTO et_shift_type VALUES(403,15,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.238013',6,1);
INSERT INTO et_shift_type VALUES(404,15,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.238016',28,28);
INSERT INTO et_shift_type VALUES(405,15,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.238018',28,28);
INSERT INTO et_shift_type VALUES(406,15,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.238021',28,28);
INSERT INTO et_shift_type VALUES(407,15,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.238023',28,28);
INSERT INTO et_shift_type VALUES(408,15,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.238025',42,14);
INSERT INTO et_shift_type VALUES(409,15,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.238028',42,14);
INSERT INTO et_shift_type VALUES(410,15,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.238030',5,2);
INSERT INTO et_shift_type VALUES(411,15,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.238033',6,1);
INSERT INTO et_shift_type VALUES(412,15,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.238035',7,0);
INSERT INTO et_shift_type VALUES(413,15,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.238038',4,3);
INSERT INTO et_shift_type VALUES(414,15,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.238040',4,3);
INSERT INTO et_shift_type VALUES(415,15,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.238043',42,21);
INSERT INTO et_shift_type VALUES(416,15,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.238045',6,1);
INSERT INTO et_shift_type VALUES(417,15,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.238047',6,1);
INSERT INTO et_shift_type VALUES(418,15,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.238050',6,1);
INSERT INTO et_shift_type VALUES(419,15,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.238052',6,1);
INSERT INTO et_shift_type VALUES(420,15,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.238055',6,1);
INSERT INTO et_shift_type VALUES(421,15,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.238057',6,1);
INSERT INTO et_shift_type VALUES(422,16,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.257201',4,3);
INSERT INTO et_shift_type VALUES(423,16,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.257210',4,3);
INSERT INTO et_shift_type VALUES(424,16,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.257215',4,3);
INSERT INTO et_shift_type VALUES(425,16,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.257218',4,3);
INSERT INTO et_shift_type VALUES(426,16,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.257222',4,3);
INSERT INTO et_shift_type VALUES(427,16,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.257226',7,7);
INSERT INTO et_shift_type VALUES(428,16,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.257229',7,7);
INSERT INTO et_shift_type VALUES(429,16,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.257233',14,7);
INSERT INTO et_shift_type VALUES(430,16,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.257237',14,7);
INSERT INTO et_shift_type VALUES(431,16,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.257240',6,1);
INSERT INTO et_shift_type VALUES(432,16,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.257243',28,28);
INSERT INTO et_shift_type VALUES(433,16,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.257246',28,28);
INSERT INTO et_shift_type VALUES(434,16,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.257250',28,28);
INSERT INTO et_shift_type VALUES(435,16,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.257253',28,28);
INSERT INTO et_shift_type VALUES(436,16,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.257256',42,14);
INSERT INTO et_shift_type VALUES(437,16,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.257259',42,14);
INSERT INTO et_shift_type VALUES(438,16,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.257262',5,2);
INSERT INTO et_shift_type VALUES(439,16,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.257266',6,1);
INSERT INTO et_shift_type VALUES(440,16,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.257269',7,0);
INSERT INTO et_shift_type VALUES(441,16,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.257272',4,3);
INSERT INTO et_shift_type VALUES(442,16,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.257276',4,3);
INSERT INTO et_shift_type VALUES(443,16,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.257280',42,21);
INSERT INTO et_shift_type VALUES(444,16,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.257283',6,1);
INSERT INTO et_shift_type VALUES(445,16,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.257286',6,1);
INSERT INTO et_shift_type VALUES(446,16,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.257290',6,1);
INSERT INTO et_shift_type VALUES(447,16,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.257293',6,1);
INSERT INTO et_shift_type VALUES(448,16,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.257297',6,1);
INSERT INTO et_shift_type VALUES(449,16,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.257300',6,1);
INSERT INTO et_shift_type VALUES(450,17,'YCSR-A','ورديات من السبت الى الثلاثاء','active','2026-05-23 22:01:13.275072',4,3);
INSERT INTO et_shift_type VALUES(451,17,'YCSR-B','اداري من الاحد الى الاربعاء','active','2026-05-23 22:01:13.275078',4,3);
INSERT INTO et_shift_type VALUES(452,17,'YCSR-C','ورديات من الاثنين الى الخميس','active','2026-05-23 22:01:13.275081',4,3);
INSERT INTO et_shift_type VALUES(453,17,'YCSR-D','ورديات الاثنين والثلاثاء اجازة','active','2026-05-23 22:01:13.275084',4,3);
INSERT INTO et_shift_type VALUES(454,17,'YCSR-c','ورديات من الاربعاء الى السبت','active','2026-05-23 22:01:13.275086',4,3);
INSERT INTO et_shift_type VALUES(455,17,'YCSRW1','اسبوع * اسبوع','active','2026-05-23 22:01:13.275089',7,7);
INSERT INTO et_shift_type VALUES(456,17,'YCSRW2','اسبوع * اسبوع','active','2026-05-23 22:01:13.275092',7,7);
INSERT INTO et_shift_type VALUES(457,17,'YCSRK2','اسبوعين * اسبوع','active','2026-05-23 22:01:13.275094',14,7);
INSERT INTO et_shift_type VALUES(458,17,'YCSRK1','اسبوعين * اسبوع','active','2026-05-23 22:01:13.275097',14,7);
INSERT INTO et_shift_type VALUES(459,17,'YCSRSH1','ورديات عادية','active','2026-05-23 22:01:13.275099',6,1);
INSERT INTO et_shift_type VALUES(460,17,'N_PR28H1','شهر * شهر','active','2026-05-23 22:01:13.275102',28,28);
INSERT INTO et_shift_type VALUES(461,17,'N_PR28H2','شهر * شهر','active','2026-05-23 22:01:13.275104',28,28);
INSERT INTO et_shift_type VALUES(462,17,'N_PR28H3','شهر * شهر','active','2026-05-23 22:01:13.275106',28,28);
INSERT INTO et_shift_type VALUES(463,17,'N_PR28H4','شهر * شهر','active','2026-05-23 22:01:13.275114',28,28);
INSERT INTO et_shift_type VALUES(464,17,'SHIFT2','42 يوم * 14 يوم','active','2026-05-23 22:01:13.275117',42,14);
INSERT INTO et_shift_type VALUES(465,17,'YCSRK3','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.275119',42,14);
INSERT INTO et_shift_type VALUES(466,17,'NORMYS4','اداري من الاحد الى الخميس','active','2026-05-23 22:01:13.275122',5,2);
INSERT INTO et_shift_type VALUES(467,17,'NORMALY2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.275124',6,1);
INSERT INTO et_shift_type VALUES(468,17,'NORMALY3','دائم (بدون اجازة)','active','2026-05-23 22:01:13.275126',7,0);
INSERT INTO et_shift_type VALUES(469,17,'NORMYS5','اداري من السبت الى الثلاثاء','active','2026-05-23 22:01:13.275129',4,3);
INSERT INTO et_shift_type VALUES(470,17,'NORMYS6','اداري من الاثنين الى الخميس','active','2026-05-23 22:01:13.275131',4,3);
INSERT INTO et_shift_type VALUES(471,17,'NORMYS7','6 اسابيع * 3 اسابيع','active','2026-05-23 22:01:13.275135',42,21);
INSERT INTO et_shift_type VALUES(472,17,'N_YCSRE2','6 ايام * 1 يوم','active','2026-05-23 22:01:13.275146',6,1);
INSERT INTO et_shift_type VALUES(473,17,'غير محدد','نظام افتراضي','active','2026-05-23 22:01:13.275149',6,1);
INSERT INTO et_shift_type VALUES(474,17,'ورديات','ورديات عادية','active','2026-05-23 22:01:13.275152',6,1);
INSERT INTO et_shift_type VALUES(475,17,'ycsrsc','نظام عام','active','2026-05-23 22:01:13.275154',6,1);
INSERT INTO et_shift_type VALUES(476,17,'YCSRE1','6 ايام * 1 يوم','active','2026-05-23 22:01:13.275157',6,1);
INSERT INTO et_shift_type VALUES(477,17,'NORMYS2','ورديات المبيعات','active','2026-05-23 22:01:13.275159',6,1);
CREATE TABLE et_bus (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	plate_number VARCHAR(50) NOT NULL, 
	capacity INTEGER, 
	model VARCHAR(100), 
	color VARCHAR(50), 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
);
INSERT INTO et_bus VALUES(1,17,'20',30,'2023','ابيض','active','','2026-05-23 18:19:17.788618');
INSERT INTO et_bus VALUES(2,17,'14',30,'2014','اخضر','active','','2026-05-24 07:59:13.364929');
CREATE TABLE et_driver (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	phone VARCHAR(20), 
	license_number VARCHAR(50), 
	employee_id INTEGER, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, user_id INTEGER REFERENCES user(id), username VARCHAR(80), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
INSERT INTO et_driver VALUES(1,17,'ماجد الريمي','','',NULL,'active','','2026-05-23 18:20:21.540383',18,'maged');
INSERT INTO et_driver VALUES(2,17,'معاذ الحكيمي','','',NULL,'active','','2026-05-24 07:58:48.573939',19,'maad');
CREATE TABLE et_route (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	area VARCHAR(200), 
	departure_time TIME NOT NULL, 
	return_time TIME NOT NULL, 
	work_days VARCHAR(200), 
	shift_type_id INTEGER, 
	bus_id INTEGER, 
	driver_id INTEGER, 
	status VARCHAR(20), 
	notes TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(shift_type_id) REFERENCES et_shift_type (id), 
	FOREIGN KEY(bus_id) REFERENCES et_bus (id), 
	FOREIGN KEY(driver_id) REFERENCES et_driver (id)
);
INSERT INTO et_route VALUES(1,17,'المدينة','الحديدة','06:00:00.000000','20:00:00.000000','[0, 1, 2, 3, 4, 5, 6]',NULL,1,1,'active','','2026-05-23 18:22:08.575209');
INSERT INTO et_route VALUES(2,17,'شارع جمال','الحديدة','08:00:00.000000','17:00:00.000000','[0, 1, 2, 3, 4, 5, 6]',NULL,NULL,NULL,'active','','2026-05-23 23:20:24.715584');
CREATE TABLE et_assignment (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	route_id INTEGER NOT NULL, 
	shift_type_id INTEGER, 
	is_residential BOOLEAN, 
	status VARCHAR(20), 
	start_date DATE, 
	end_date DATE, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(route_id) REFERENCES et_route (id), 
	FOREIGN KEY(shift_type_id) REFERENCES et_shift_type (id)
);
INSERT INTO et_assignment VALUES(1,17,6,1,NULL,1,'active','2026-05-23',NULL,'2026-05-23 18:23:37.129719');
CREATE TABLE et_trip (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	route_id INTEGER NOT NULL, 
	bus_id INTEGER, 
	driver_id INTEGER, 
	date DATE NOT NULL, 
	departure_time TIME, 
	return_time TIME, 
	status VARCHAR(20), 
	departure_note TEXT, 
	return_note TEXT, 
	created_at DATETIME, started_at DATETIME, completed_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(route_id) REFERENCES et_route (id), 
	FOREIGN KEY(bus_id) REFERENCES et_bus (id), 
	FOREIGN KEY(driver_id) REFERENCES et_driver (id)
);
INSERT INTO et_trip VALUES(1,17,2,2,2,'2026-05-24','08:00:00.000000','17:00:00.000000','completed',NULL,NULL,'2026-05-24 12:32:07.209675',NULL,NULL);
INSERT INTO et_trip VALUES(2,17,1,1,1,'2026-05-24','06:00:00.000000','20:00:00.000000','completed',NULL,NULL,'2026-05-24 12:32:07.226006',NULL,NULL);
CREATE TABLE et_ride_log (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	trip_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	action VARCHAR(20) NOT NULL, 
	time DATETIME, 
	status VARCHAR(20), 
	method VARCHAR(20), 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(trip_id) REFERENCES et_trip (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id)
);
INSERT INTO et_ride_log VALUES(1,17,1,6,'assigned','2026-05-24 12:32:07.219055','on_time','manual',NULL);
INSERT INTO et_ride_log VALUES(2,17,2,8,'assigned','2026-05-24 12:32:07.228163','on_time','manual',NULL);
INSERT INTO et_ride_log VALUES(3,17,2,6,'board','2026-05-24 12:44:55.271364','on_time','manual',NULL);
INSERT INTO et_ride_log VALUES(4,17,2,8,'board','2026-05-24 12:45:34.201763','on_time','manual',NULL);
INSERT INTO et_ride_log VALUES(5,17,2,14,'board','2026-05-24 12:49:27.602346','on_time','manual',NULL);
INSERT INTO et_ride_log VALUES(6,17,1,15,'board','2026-05-24 12:58:56.876563','on_time','manual',NULL);
CREATE TABLE et_violation (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	trip_id INTEGER, 
	violation_type VARCHAR(50) NOT NULL, 
	description TEXT, 
	date DATE, 
	resolved BOOLEAN, 
	resolved_by INTEGER, 
	resolved_at DATETIME, 
	notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id), 
	FOREIGN KEY(employee_id) REFERENCES employee (id), 
	FOREIGN KEY(trip_id) REFERENCES et_trip (id), 
	FOREIGN KEY(resolved_by) REFERENCES user (id)
);
INSERT INTO et_violation VALUES(1,17,0,NULL,'invalid_code','كود غير صالح: 346','2026-05-24',0,NULL,NULL,NULL);
INSERT INTO et_violation VALUES(2,17,0,NULL,'invalid_code','كود غير صالح: 346','2026-05-24',0,NULL,NULL,NULL);
CREATE TABLE et_employee_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL UNIQUE REFERENCES employee(id),
                company_id INTEGER NOT NULL REFERENCES company(id),
                department VARCHAR(100),
                shift_type_id INTEGER REFERENCES et_shift_type(id),
                shift_start_date DATE,
                work_day VARCHAR(20),
                movement_status VARCHAR(50),
                is_administrative BOOLEAN DEFAULT 1,
                arrival_time TIME,
                departure_time TIME,
                route_id INTEGER REFERENCES et_route(id),
                city VARCHAR(100),
                residence_location VARCHAR(200),
                transport_type VARCHAR(50) DEFAULT 'يومي',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            , external_company VARCHAR(200));
INSERT INTO et_employee_info VALUES(1,6,17,'الشؤون',452,'2026-05-25','الإثنين','',1,'08:00:00.000000','20:00:00.000000',2,'الحديدة','جمال','ورديات','2026-05-23 19:21:21.293946','الشركة اليمنية لتكرير السكر');
INSERT INTO et_employee_info VALUES(2,7,17,'الشؤون',451,'2026-05-24','الأحد','',1,'08:00:00.000000','16:00:00.000000',1,'الحديدة','المقوات','إداري','2026-05-23 22:20:29.868446','الشركة اليمنية لتكرير السكر');
INSERT INTO et_employee_info VALUES(3,8,17,'الشؤون',452,'2026-05-25','الإثنين','',1,'08:00:00.000000','20:00:00.000000',1,'الحديدة','المقوات','ورديات','2026-05-23 22:40:32.088756','الشركة اليمنية لتكرير السكر');
INSERT INTO et_employee_info VALUES(4,9,17,'الشؤون',455,'2026-05-17','الأحد','',1,'08:00:00.000000','20:00:00.000000',1,'الحديدة','المقوات','ورديات','2026-05-23 23:08:33.031559','شركة راس عيسى الصناعية');
INSERT INTO et_employee_info VALUES(5,10,17,'الشؤون',455,'2026-05-18','الإثنين','',1,'08:00:00.000000','20:00:00.000000',1,'الحديدة','المقوات','ورديات','2026-05-23 23:10:31.134911','شركة راس عيسى الصناعية');
INSERT INTO et_employee_info VALUES(6,15,17,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,'يومي','2026-05-24 12:58:56.873412','شركة راس عيسى');
CREATE TABLE et_trip_route (
	id INTEGER NOT NULL, 
	trip_id INTEGER NOT NULL, 
	route_id INTEGER NOT NULL, 
	"order" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(trip_id) REFERENCES et_trip (id), 
	FOREIGN KEY(route_id) REFERENCES et_route (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('et_employee_info',6);
COMMIT;
