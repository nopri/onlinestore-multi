onlinestore-multi, Simple Online Store application 
(c) Noprianto <nop@tedut.com>
2010
GPL 

Screenshots: https://github.com/nopri/onlinestore-multi/wiki


Features:
- Run as WSGI Application
- Multi Language (currently English and Bahasa Indonesia)
- Pretty URL
- Template/Theme Support (bundled: 4)
- File Manager 
- Product Category/Group/Item
- Link/Widget Support
- News Module
- FAQ Module
- User Contents (+Menu)
- Shopping Cart
- Simple Invoice Management
- Simple Statistics  
- Send Email (Cart Checkout, Contact, etc)
- Captcha (Random Font)
- Custom Logo 
- Custom URL Redirect
- Flash Animation as Product Picture
- Payment: Cash, Cash On Delivery, Bank/Wire Transfer
- More


Using:
- Python
- web.py
- jQuery/jQueryUI (bundled, old version)
- PyYAML
- BeautifulSoup
- GeoIP or pygeoip (auto detect)
- Python Imaging Library
- MySQL (and MySQLdb) 


Default user/password: admin

 
Installation (with Python already installed):
- We will use Apache HTTP Server for WSGI.

- Install: web.py, PyYAML, BeautifulSoup, Python GeoIP (or pygeoip, noted below), 
  PIL, MySQL Server, Python MySQLdb
  Ubuntu-based distribution (put command in one line):
  $ sudo apt-get install python-webpy python-yaml python-beautifulsoup python-geoip python-imaging mysql-server python-mysqldb

- Download onlinestore-multi source code, or clone from GitHub
  $ git clone https://github.com/nopri/onlinestore-multi.git

- Change into root directory of source code:
  $ cd onlinestore-multi

- Create new MySQL database and restore from dump file:
  $ mysql -u root -p
  mysql> create database onlinestore;
  mysql> grant all privileges on onlinestore.* to onlinestore@localhost identified by 'onlinestore_password';
  mysql> flush privileges;
  mysql> quit;

  $ mysql -D onlinestore -u onlinestore -p < ./db.sql 

- In root directory of source code:
  $ cp config.ini.dist config.ini

- Edit config.ini

- Configure WSGI
  Ubuntu-based distribution:
  $ sudo apt-get install libapache2-mod-wsgi
  
  For default domain 
  (replace /tmp/onlinestore-multi with your configuration):

  $ sudo nano /etc/apache2/sites-available/default
  (put these lines below DocumentRoot)

  WSGIScriptAlias / /tmp/onlinestore-multi/app.py/
  AddType text/html .py
  Alias /static /tmp/onlinestore-multi/static/
  
  $ sudo service apache2 reload
  
- If you are using pygeoip:
  - Download http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
  - Extract and put GeoIP.dat into application directory


Thank you :)
