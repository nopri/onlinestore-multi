onlinestore-multi, Simple Online Store application 
(c) Noprianto <nop@tedut.com>
2010
GPL 


SCREENSHOTS / USERS: https://github.com/nopri/onlinestore-multi/wiki


FEATURES:
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


REQUIREMENTS:
- Python
- web.py
- jQuery/jQueryUI (bundled, old version)
- PyYAML
- BeautifulSoup
- GeoIP or pygeoip (auto detect)
- Python Imaging Library
- MySQL (and MySQLdb) 
- Apache HTTP Server (and mod_wsgi)


DEFAULT USER/PASSWORD: admin

 
INSTALLATION:
1) Install all the requirements above (except for bundled)

2) Download / clone onlinestore-multi: https://github.com/nopri/onlinestore-multi.git

3) Change into application directory:  
   $ cd onlinestore-multi

4) Create new MySQL database and restore from dump file:
   $ mysql -u root -p
   mysql> create database onlinestore;
   mysql> grant all privileges on onlinestore.* to onlinestore@localhost identified by 'onlinestore_password';
   mysql> flush privileges;
   mysql> quit;

   $ mysql -D onlinestore -u onlinestore -p < ./db.sql 

5) Copy config.ini.dist to config.ini, edit accordingly

6) Configure WSGI:
   Ubuntu-based distribution: edit /etc/apache2/sites-available/default
   (put these lines below DocumentRoot, adjust accordingly)

        WSGIScriptAlias / /tmp/onlinestore-multi/app.py/
        AddType text/html .py
        Alias /static /tmp/onlinestore-multi/static/
  
7) Restart Apache HTTP Server
  
8) If you are using pygeoip:
   - Download http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
   - Extract and put GeoIP.dat into root directory of source code

9) Please login as admin, go to System Configuration, and set (at least):
   - Enable shopping cart
   - Used currency
   - Site offline for maintenance
   - Default email 
   

THANK YOU :)
