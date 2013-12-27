onlinestore-multi
Simple Online Store application 
(c) Noprianto <nop@tedut.com>
2010
GPL 
v1.03


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
- Custom Homepage URL
- Flash Animation as Product Picture
- Payment: Cash, Cash On Delivery, Bank/Wire Transfer
- More


REQUIREMENTS:
- Python
- web.py
- jQuery/jQueryUI (bundled, old version)
- PyYAML
- GeoIP or pygeoip (auto detect)
- Python Imaging Library
- Apache HTTP Server (and mod_wsgi)
  (or alternative web server/wsgi)

If you need simple web-based SQLite management tool, 
please consider sqliteboy, 
https://github.com/nopri/sqliteboy :) 


DEFAULT USER/PASSWORD: admin

 
INSTALLATION:
1) Install all the requirements above (except for bundled)

2) Download / clone onlinestore-multi: 
   https://github.com/nopri/onlinestore-multi.git

   For example, we put it in /tmp/onlinestore-multi

3) Make sure that installation directory is writable by the user 
   who is running web server.

   Please note that onlinestore-multi.db will be automatically 
   created (and populated) in installation directory.  
   
   Debian/Debian-based distribution:
   (run these commands as root, adjust accordingly)
   
   # chgrp www-data /tmp/onlinestore-multi
   # chmod g+w /tmp/onlinestore-multi

4) Configure WSGI:
   Debian/Debian-based distribution: 
   edit /etc/apache2/sites-available/default
   (put these lines below DocumentRoot, adjust accordingly)

        WSGIScriptAlias / /tmp/onlinestore-multi/app.py/
        Alias /static /tmp/onlinestore-multi/static/
  
5) Restart Apache HTTP Server
  
6) If you are using pygeoip:
   - Download http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
   - Extract and put GeoIP.dat in installation directory

7) Please login as admin, go to System Configuration, and set (at least):
   - Used currency
   - Site offline for maintenance
   - Default email 
   

THANK YOU :)
