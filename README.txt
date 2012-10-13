onlinestore-multi, Simple Online Store application 
(c) Noprianto <nop@tedut.com>
2010
GPL 


Features:
- Run as WSGI Application
- Multi Language (currently English and Bahasa Indonesia)
-  


Using:
- Python
- web.py
- jQuery (bundled, old version)
- PyYAML
- BeautifulSoup
- GeoIP
- Python Imaging Library
- MySQL 

 
Installation (with Python already installed):
- We will use Apache HTTP Server for WSGI.

- Install: web.py, PyYAML, BeautifulSoup, Python GeoIP, PIL, MySQL Server, Python MySQLDB
  Ubuntu-based distribution (put command in one line):
  $ sudo apt-get install python-webpy python-yaml python-beautifulsoup python-geoip python-imaging mysql-server python-mysqldb

- Download onlinestore-multi source code, or clone from GitHub
  $ git clone https://github.com/nopri/onlinestore-multi.git

- Change into root directory of source code:
  $ cd onlinestore-multi

- Create new MySQL database, restore from dump file, set admin password:
  $ mysql -u root -p
  mysql> create database onlinestore;
  mysql> grant all privileges on onlinestore.* to onlinestore@localhost identified by 'onlinestore_password';
  mysql> flush privileges;
  mysql> quit;

  $ mysql -D onlinestore -u onlinestore -p < ./db.sql 

  $ mysql -D onlinestore -u onlinestore -p
  mysql> update ms_user set password=md5('admin123') where id=1;

- In root directory of source code:
  $ cp config.ini.dist config.ini

- Edit config.ini

- If you are using /tmp/onlinestore-multi-session as session directory, 
  please make sure it is writeable by user who is running web server
  Ubuntu-based distribution:
  $ sudo chown www-data -R /tmp/onlinestore-multi-session

- Configure WSGI
  Ubuntu-based distribution:
  $ sudo apt-get install libapache2-mod-wsgi
  
  For default domain 
  (replace /tmp/onlinestore-multi with your configuration):

  $ sudo nano /etc/apache2/sites-available/default
  (put this line before VirtualHost definition)
  WSGIPythonPath /tmp/onlinestore-multi/

  (put these lines below DocumentRoot)

  WSGIScriptAlias / /tmp/onlinestore-multi/app.py/
  AddType text/html .py
  Alias /static /tmp/onlinestore-multi/static/
  
  $ sudo service apache2 reload
  
 
Thank you :)
