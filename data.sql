CREATE TABLE sessions (
  session_id char(128) UNIQUE NOT NULL,
  atime integer NOT NULL default current_timestamp,
  data text,
  PRIMARY KEY (session_id)
);

CREATE TABLE ms_bank (
  id integer primary key autoincrement,
  name varchar(64) default NULL,
  account varchar(64) default NULL,
  currency_id integer default NULL,
  holder varchar(64) default NULL,
  branch varchar(64) default NULL,
  address varchar(255) default NULL,
  country varchar(64) default NULL,
  swift varchar(64) default NULL,
  active integer default 1,
  note text,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_blog_category (
  id integer primary key autoincrement,
  log_id integer default NULL,
  category text,
  active integer default 1,
  extra text
);

CREATE TABLE ms_category (
  id integer primary key autoincrement,
  name text,
  priority integer default NULL,
  active integer default 1,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_config (
  param varchar(64) NOT NULL default '',
  value text,
  log_id integer default NULL,
  PRIMARY KEY  (param)
);

INSERT INTO ms_config (param, value, log_id) VALUES ('allow_user','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('another_email','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('blog_show_style','date',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('cart_check_stock','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('currency','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('expose_error','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('extra_info','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('general_error_message','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('homepage','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('invoice_extra_info','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('invoice_show_bank','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('invoice_show_paypal','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('lang','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('logo_file','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('news_max','5',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('offline','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('payment_month','12',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('promo_host','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('secure','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('site_description','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('site_keywords','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('sticky_info','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('template','default',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('template_param','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('use_cart','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('expose_time','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('promote','1',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('payments','1,2,3,',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('max_product_category','100',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('max_product','500',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('max_file_size','512000',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('max_files','500',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('mail_smtp','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('mail_user','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('mail_pass','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('mail_default','',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('url_base','/',NULL);
INSERT INTO ms_config (param, value, log_id) VALUES ('font_dir','/usr/share/fonts/truetype/freefont/',NULL);

CREATE TABLE ms_currency (
  id integer primary key autoincrement,
  name varchar(8) default NULL,
  csymbol varchar(8) default NULL,
  log_id integer default NULL,
  extra text
);

INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (1,'IDR','Rp',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (2,'USD','$',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (3,'SGD','$',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (4,'MYR','RM',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (5,'HKD','$',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (6,'JPY','¥',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (7,'CNY','¥',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (8,'GBP','£',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (9,'AUD','$',NULL,NULL);
INSERT INTO ms_currency (id, name, csymbol, log_id, extra) VALUES (10,'NZD','$',NULL,NULL);

CREATE TABLE ms_file (
  id integer primary key autoincrement,
  log_id integer default NULL,
  name varchar(255) default NULL,
  name_add varchar(8) default NULL,
  size integer default NULL,
  description varchar(255) default NULL,
  type varchar(255) default NULL,
  type_options text,
  disposition varchar(255) default NULL,
  disposition_options text,
  content blob,
  date_file integer default NULL,
  headers text,
  purpose varchar(64) default NULL,
  extra text
);

CREATE TABLE ms_group (
  id integer primary key autoincrement,
  name varchar(64) default NULL,
  extra text,
  log_id integer default NULL
);

INSERT INTO ms_group (id, name, extra, log_id) VALUES (1,'ADMIN',NULL,NULL);
INSERT INTO ms_group (id, name, extra, log_id) VALUES (2,'USER',NULL,NULL);

CREATE TABLE ms_link (
  id integer primary key autoincrement,
  code text,
  purpose varchar(64) default NULL,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_payment_type (
  id integer primary key autoincrement,
  name varchar(64) default NULL,
  log_id integer default NULL,
  extra text
);

INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (1,'Cash',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (2,'Cash On Delivery',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (3,'Bank/Wire Transfer',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (4,'Credit',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (5,'Debit Card',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (6,'Credit Card',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (7,'Voucher',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (8,'Gift Card',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (9,'PayPal',NULL,NULL);
INSERT INTO ms_payment_type (id, name, log_id, extra) VALUES (10,'Other',NULL,NULL);

CREATE TABLE ms_paypal (
  id integer primary key autoincrement,
  account varchar(255) default NULL,
  active integer default 1,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_product (
  id integer primary key autoincrement,
  name text,
  category_id integer default NULL,
  description text,
  full_info text,
  file_id integer default NULL,
  related text,
  active integer default 1,
  priority integer default NULL,
  allow_comment integer default 0,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_product_variant (
  id integer primary key autoincrement,
  product_id integer default NULL,
  name text,
  stock integer default NULL,
  price real default NULL,
  currency_id integer default NULL,
  taxratio real default NULL,
  variant_file_id integer default NULL,
  active integer default 1,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_redirect (
  id integer primary key autoincrement,
  url varchar(255) default NULL,
  target varchar(255) default NULL,
  type varchar(64) default NULL,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_user (
  id integer primary key autoincrement,
  name varchar(64) default NULL,
  group_id integer default NULL,
  password varchar(64) default NULL,
  first_name varchar(64) default NULL,
  last_name varchar(64) default NULL,
  email text,
  phone text,
  fax text,
  web text,
  icontact text,
  acontact text,
  govid text,
  address text,
  active integer default 1,
  payment text,
  photo blob,
  log_id integer default NULL,
  extra text
);

INSERT INTO ms_user
    (id, name, group_id, password, first_name, last_name, 
    email, phone, fax, web, icontact, acontact, govid, 
    address, active, payment, photo, log_id, extra) 
    VALUES (1,'admin',1,'21232f297a57a5a743894a0e4a801fc3',
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL);

CREATE TABLE ms_user_content (
  id integer primary key autoincrement,
  page text,
  content text,
  active integer default 1,
  show_in_menu integer default NULL,
  priority integer default NULL,
  log_id integer default NULL,
  extra text
);

CREATE TABLE ms_yahoo (
  id integer primary key autoincrement,
  account varchar(255) default NULL,
  type varchar(8) default NULL,
  log_id integer default NULL,
  extra text
);

CREATE TABLE tr_blog (
  id integer primary key autoincrement,
  log_id integer default NULL,
  category_id integer default NULL,
  date_news integer default NULL,
  title text,
  description text,
  blog text,
  allow_comment integer default 0,
  active integer default 1,
  extra text
);

CREATE TABLE tr_comment (
  id integer primary key autoincrement,
  log_id integer default NULL,
  date_comment integer default NULL,
  product_id integer default NULL,
  blog_id integer default NULL,
  nested_comment_id integer default NULL,
  url varchar(255) default NULL,
  author varchar(64) default NULL,
  email varchar(255) default NULL,
  web varchar(255) default NULL,
  comment text,
  published integer default NULL,
  extra text
);

CREATE TABLE tr_faq (
  id integer primary key autoincrement,
  log_id integer default NULL,
  category text,
  question text,
  answer text,
  file_id integer default NULL,
  extra text
);

CREATE TABLE tr_invoice_detail (
  id integer primary key autoincrement,
  header_id integer default NULL,
  product_variant integer default NULL,
  saved_price real default NULL,
  saved_tax real default NULL,
  amount integer default NULL,
  log_id integer default NULL
);

CREATE TABLE tr_invoice_header (
  id integer primary key autoincrement,
  cart_id varchar(64) default NULL,
  log_id integer default NULL,
  total real default NULL,
  date_purchase integer default NULL,
  date_due integer default NULL,
  date_paid integer default NULL,
  payment_type integer default NULL,
  used_currency integer default NULL,
  cust_name varchar(64) default NULL,
  cust_email varchar(255) default NULL,
  ship_addr text,
  note text,
  payment_info text,
  confirm_info text,
  invoice_text text,
  invoice_lang varchar(8) default NULL,
  done integer default 0,
  extra text
);

CREATE TABLE tr_log (
  id integer primary key autoincrement,
  date_log integer default NULL,
  date_log_last integer default NULL,
  activity integer default NULL,
  ip varchar(64) default NULL,
  country varchar(64) default NULL,
  referer varchar(255) default NULL,
  url varchar(255) default NULL,
  url_last varchar(255) default NULL,
  method varchar(8) default NULL,
  user_agent varchar(255) default NULL,
  user_id integer default NULL,
  user_id_last integer default NULL,
  login_activity text,
  audit text,
  extra text
);

CREATE TABLE tr_news (
  id integer primary key autoincrement,
  log_id integer default NULL,
  date_news integer default NULL,
  title text,
  description text,
  news text,
  file_id integer default NULL,
  extra text
);
