#
# onlinestore-multi
# simple online store application
# (c) Noprianto <nop@tedut.com> 
# 2010
# GPL
# 
# migrated from MySQL to SQLite on 2013-12-17 


################################ IMPORT ################################


import os
CURDIR = os.path.abspath(os.path.dirname(__file__))
PS = os.path.sep
 
import sys
sys.path.append(CURDIR)

import re
import ConfigParser
import time
import datetime
import decimal
import urlparse
import random
import cStringIO

#
try: 
   from hashlib import md5
except ImportError:
   from md5 import md5
#
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
#
fgeo = None
try: 
    import GeoIP
    ogeo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
    fgeo = ogeo.country_name_by_addr
except ImportError:
    try:
        import pygeoip
        ogeo = pygeoip.GeoIP(CURDIR + PS + 'GeoIP.dat', pygeoip.MEMORY_CACHE)
        fgeo = ogeo.country_name_by_addr
    except:
        fgeo = None
#
import web
import yaml
from HTMLParser import HTMLParser
import sqlite3
import messages as m
reload(m)

class StripHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)


############################# MODULE PARAM #############################


web.config.debug = False
web.config.session_parameters['cookie_name'] = 'SESSION'
web.config.session_parameters['ignore_expiry'] = True 
web.config.session_parameters['timeout'] = 1800 #30 minute


############################ URLS / WEB APP ############################


URLS = (
    '/', 'index',
    '/browser/set/(.*)', 'browser_set',
    '/captcha', 'captcha',
    '/product', 'product',
    '/lang/set/(.*)', 'lang_set',
    '/fs/(\d+)', 'fs',
    '/cart', 'cart',
    '/cart/add', 'cart_add',
    '/cart/del', 'cart_del',
    '/cart/empty', 'cart_empty',
    '/cart/checkout', 'cart_checkout',
    '/cart/checkout/done', 'cart_checkout_done',
    '/payment/confirm', 'payment_confirm',
    '/contact', 'contact',
    '/login', 'login',
    '/logout', 'logout',
    '/news', 'news',
    '/faq', 'faq',
    '/news/hide', 'news_hide',
    '/go/(\d+)', 'go',
    '/admin', 'admin',
    '/passwd', 'passwd',
    '/profile', 'profile',
    '/promote', 'promote',
    '/admin/fs', 'admin_fs',
    '/admin/fs/del', 'admin_fs_del',
    '/admin/fs/upload', 'admin_fs_upload',
    '/admin/fs/view/(\d+)', 'admin_fs_view',    
    '/admin/system', 'admin_system',
    '/admin/product', 'admin_product',
    '/admin/product/category', 'admin_product_category',
    '/admin/product/category/del', 'admin_product_category_del',
    '/admin/product/category/save', 'admin_product_category_save',
    '/admin/product/group', 'admin_product_group',
    '/admin/product/group/del', 'admin_product_group_del',
    '/admin/product/group/save', 'admin_product_group_save',
    '/admin/product/group/edit/(\d+)', 'admin_product_group_edit',
    '/admin/product/item', 'admin_product_item',
    '/admin/product/item/del', 'admin_product_item_del',
    '/admin/product/item/save', 'admin_product_item_save',
    '/admin/bank', 'admin_bank',
    '/admin/bank/del', 'admin_bank_del',
    '/admin/bank/save', 'admin_bank_save',
    '/admin/paypal', 'admin_paypal',
    '/admin/paypal/del', 'admin_paypal_del',
    '/admin/paypal/save', 'admin_paypal_save',
    '/admin/yahoo', 'admin_yahoo',
    '/admin/yahoo/del', 'admin_yahoo_del',
    '/admin/yahoo/save', 'admin_yahoo_save',
    '/admin/link', 'admin_link',
    '/admin/link/del', 'admin_link_del',
    '/admin/link/save', 'admin_link_save',
    '/admin/news', 'admin_news',
    '/admin/news/del', 'admin_news_del',
    '/admin/news/save', 'admin_news_save',
    '/admin/news/edit/(\d+)', 'admin_news_edit',
    '/admin/faq', 'admin_faq',
    '/admin/faq/del', 'admin_faq_del',
    '/admin/faq/save', 'admin_faq_save',
    '/admin/faq/edit/(\d+)', 'admin_faq_edit',
    '/admin/invoice', 'admin_invoice',
    '/admin/invoice/view/(\d+)', 'admin_invoice_view',
    '/admin/invoice/approval', 'admin_invoice_approval',
    '/admin/stat', 'admin_stat',
    '/admin/doc', 'admin_doc',
    '/admin/redir', 'admin_redir',
    '/admin/redir/del', 'admin_redir_del',
    '/admin/redir/save', 'admin_redir_save',
    '/admin/go', 'admin_go',
    '/admin/go/del', 'admin_go_del',
    '/admin/go/save', 'admin_go_save',
    '/admin/go/edit/(\d+)', 'admin_go_edit',
    '/(.*)', 'redir',
    )

wapp = web.application(URLS, globals())


############################## DATABASE ################################


DATA_SQL_DEFAULT = 'data.sql'
DATA_FILE_DEFAULT = 'onlinestore-multi.db'
DATA_SQL = os.path.join(CURDIR, DATA_SQL_DEFAULT) 
DATA_FILE = os.path.join(CURDIR, DATA_FILE_DEFAULT)

db_error = False
if not os.path.exists(DATA_FILE) or not os.path.getsize(DATA_FILE):
    try:
        test_db = sqlite3.connect(DATA_FILE)
        test_db.executescript(open(DATA_SQL).read())
        test_db.close()
    except:
        db_error = True
else:
    if not os.access(DATA_FILE, os.W_OK):
        db_error = True

db = None
if not db_error:
    try:
        conn = web.database(dbn = 'sqlite', db = DATA_FILE)
    except:
        conn = None
    if conn and hasattr(conn, 'query'):
        db = conn
    else:
        db = None
    del conn


##################### FROM SQLITEBOY (UNMODIFIED) ######################


def sqliteboy_chunk(s, n, separator, justify, padding):
    s = str(s)
    separator = str(separator)
    padding = str(padding)
    #
    if (not n) or (not s) or (n < 1):
        return s
    #
    if padding: 
        pad = padding[0]
    else:
        pad = ' '
    #
    if not justify:
        justify = 0
    #
    mod = len(s) % n
    if mod:
        ln = len(s) + (n - mod)
        if justify == 0: #left
            s = s.ljust(ln, pad)
        else: #right
            s = s.rjust(ln, pad)
    #
    res = [s[i:i+n] for i in range(0, len(s), n)]
    ret = separator.join(res)
    #
    return ret


########################### IMPORTANT FUNCTION #########################


def query(q, a = {}):
    global db
    #
    r = db.query(q, vars = a)
    try:
        ret = list(r)
    except:
        ret = r
    #
    return ret


def rget(r, key, count=1, index=0, default='', to_yaml=False):
    try:
        test = r and len(r) >= count and r[index].has_key(key)
    except:
        test = False
    #
    if test and r[index].get(key):
        ret = r[index].get(key)
    else:
        ret = default   
    #
    if to_yaml:
        try:
            ret2 = yaml.load(ret)
        except:
            ret2 = ret
    else:
        ret2 = ret
    #
    return ret2
    

def pget(option, default='', strip=True, callback=None):
    q = 'select value from ms_config where param=$p'
    a = {'p': option}
    r = query(q, a)
    ret = rget(r, 'value', default=default)
    #
    if strip and hasattr(ret, 'strip'):
        ret = ret.strip()
    #
    if callback:
        ret = callback(id=ret, pget_helper=True)
    #
    return ret


############################### CONSTANT ###############################


VERSION = '1.03'
NAME = 'onlinestore-multi'
PRECISION = 2
TEMPLATE_DIR = CURDIR + PS + 'template'
DOC_ADMIN = CURDIR + PS + 'README.txt'
DOMAIN = ''
BASEURL_DEFAULT = '/store' 
HOME_DEFAULT = '/product'
TEMPLATE_DEFAULT = 'default'
LANG_DEFAULT = 'en_US'
MAIL_DEFAULT = ''
FORCE_SINGLE_CURRENCY = True
CWIDTH = {'product': 42, 'qty': 8, 'price': 17, 'vat': 16, 'subtotal': 18}
CSPACE = '  '
CART_ADD_MAX = 10
ADMIN_URL_GROUP = ('/profile', '/passwd', '/promote')
REGEX_EMAIL = r'^[\w\.\+-]+@[\w\.-]+\.[a-zA-Z]+$'


################################ GLOBAL ################################


sess = None
if not db_error:
    sess = web.session.Session(wapp, web.session.DBStore(
        db, 'sessions'), 
        initializer={
            'captcha': '',
            'p' : {},
            'lang' : '',
            'c': {}, 
            'u': None,
            'log': None,
            'co': {},
            'newsread': False,
            'msg': [],
            'browserclass': '',
            'fullpath': None,
        }
    )


msgs = ''


menu = ''


mobile = ''

#new res hack, eliminate app_global_conf.py
#as of 16-October-2012
#quick hack, once again, put config in database
#as of 22-October-2012
res_fix = ['cart', 'user_content', 'blog']
res = {
        'cart'                        : True,
        'user_content'                : True,
        'blog'                        : True,        
        'promote'                     : True,
        'payments'                    : [1,2,3],
        'value'                       : 200,
        'max_product_category'        : 100,
        'max_product'                 : 500,
        'max_file_size'               : 600 * 1024,
        'max_files'                   : 600,
}

#quick hack as of 18-October-2012
FORCE_PROMOTE = res['promote']
PAYMENT_TYPE = res['payments']

rendertime = [0, 0]


############################### FUNCTION ###############################


def is_valid_email(email):
    #previous implementation was based on codes from internet
    #(around 2010, thank you very much, however, i forgot the site :( )
    #as of 21-April-2013, regex is used
    if re.match(REGEX_EMAIL, email):
        return True
    #
    return False
    

def detect_ua(ua):
    ret = {}
    ret['mobile_document'] = ua
    return ret


def number_format(number, localeset='', places=0):
    '''from sqliteboy, modified'''
    
    n = str(number)
    decimals = places
    decimal_point = m.t(m.NUMBER_FORMAT, localeset)['decimal_point']
    thousands_sep = m.t(m.NUMBER_FORMAT, localeset)['thousands_separator']
    #
    neg = False
    try:
        f = float(n)
        if f < 0:
            neg = True
    except:
        return n
    #
    if 'e' in n.lower():
        efmt = '%%.%sf' %len(n)
        n = efmt %float(n)
    #
    dec = decimals
    if not isinstance(dec, int) or dec < 0:
        dec = 0
    #
    nn = ''
    dd = ''
    if '.' in n: #float
        nn, dd = n.split('.')
    else:
        nn = n
    nn = nn.replace('-', '')
    nn = nn.replace('+', '')
    nn = nn.strip()
    dd = dd.strip()
    #
    if dd:
        if dec <= len(dd):
            dd = dd[:dec]
        else:
            dd = dd.ljust(dec, '0')
    #
    nn = sqliteboy_chunk(nn, 3, thousands_sep, 1, '').strip()
    dd = dd.strip()
    #
    if neg:
        nn = '-' + nn
    #
    if dd:
        ret = nn + decimal_point + dd
    else:
        ret = nn
    #
    return ret
    

def now(format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format)


def dtf(t):
    t0 = time.strptime(t, m.t(m.DATETIME_FORMAT, 'default')['datetime'])
    return time.strftime(m.t(m.DATETIME_FORMAT, sess.lang)['datetime'], t0)


def nf(number, decimal=PRECISION):
    return number_format(number, sess.lang, decimal)


def striphtml(text):
    data = StripHTMLParser()
    data.feed(text)
    ret = ''.join(data.text)
    return ret


def stripsall(text, remove, ignorecase=True):
    if ignorecase:
        premove = remove.lower()
        pat = re.compile(premove, re.IGNORECASE)
        text = pat.sub(premove, text)
    else:
        premove = remove
        text = text
    #
    ret = text
    while True:
        newtext = ret
        ret = web.utils.strips(newtext, premove)
        if ret == newtext:
            break
    #
    return ret


def sendmail(to, subject, message, reply_to=MAIL_DEFAULT):
    #
    UA = '%s v%s' %(NAME, VERSION)
    XM = UA
    #
    try:
        web.config.smtp_server = pget('mail_smtp')
        web.config.smtp_username = pget('mail_user')
        web.config.smtp_password = pget('mail_pass')
        #
        web.sendmail(MAIL_DEFAULT, to, subject, message,
            headers=({'User-Agent': UA, 'X-Mailer': XM, 'Reply-To': reply_to})
            )
    except:
        web.config.smtp_server = ''
        web.config.smtp_username = ''
        web.config.smtp_password = ''
        #
        web.sendmail(MAIL_DEFAULT, to, subject, message,
            headers=({'User-Agent': UA, 'X-Mailer': XM, 'Reply-To': reply_to})
            )

                
def mlget(field, default=m.COUNTRY['default'][0], all=False, get_non_empty=True):
    global sess
    #
    if not field:
        return ''
    #
    try:
        d = yaml.load(field)
    except:
        return ''
    #
    if not type(d) == type({}):
        return d
    #
    langs = [x[0] for x in m.COUNTRY.values()]
    #
    if not all:
        if sess.lang in d.keys() and d[sess.lang]:
            return d[sess.lang]
        else:
            if d.has_key(default) and d[default]:
                return d[default]          
            else:
                if get_non_empty:
                    ne = ''
                    for i in d.keys():
                        if d[i]:
                            ne = d[i]
                            break
                    #
                    return ne
                else:
                    return ''
    else:
        for i in langs:
            if not d.has_key(i):
                d[i] = ''
        return d
    #
    #error, should not reach this
    return ''


def ub(url):
    base = pget('url_base', default=BASEURL_DEFAULT)
    if base == '/':
        ret = url
    else:
        ret = base + url
    return ret


def tget(page, globals={}):
    p = page + '.html'
    tdir = TEMPLATE_DIR
    tdd = tdir + PS + TEMPLATE_DEFAULT
    tdc = tdd + PS + p
    tud = tdir + PS + pget('template', default=TEMPLATE_DEFAULT)
    tuc = tud + PS + p
    if os.path.exists(tuc):
        tc = tud
    elif os.path.exists(tdc):
        tc = tdd
    else:
        return None
    #
    info = tinfo(pget('template'))
    if not info:
        tc = tdd
    else:
        try:
            owner = info['general']['owner']
        except:
            owner = ''
        if owner and DOMAIN.lower() not in owner:
            tc = tdd
    #
    ret = web.template.render(tc, globals=globals)
    return ret
    

def cidget():
    q = '''
    select seq from sqlite_sequence where 
    name='tr_invoice_header';
    '''
    r = query(q)
    p1 = rget(r, 'seq', default=0)
    p2 = str(time.time())[-5:].replace('.','')
    #
    ret = '%d-%s' %(p1, p2)
    return ret


def dnews(id=0, read_session=True):
    global sess
    #
    ret = []
    #
    if read_session:
        if sess.newsread:
            return ret
    #
    max = pget('news_max')
    try:
        imax = int(max)
    except:
        imax = None
    #
    if id:
        q = 'select * from tr_news where id=$id'
        a = {'id': id}                
    else:
        if imax:
            q = 'select * from tr_news order by id desc limit $limit'
            a = {'limit': imax}
        else:
            q = 'select * from tr_news order by id desc'
            a = {}        
    #
    r = query(q, a)
    for i in r:
        i.date_news = dtf(i.date_news)
        i.title = (mlget(i.title, all=True), mlget(i.title))
        i.description = (mlget(i.description, all=True), mlget(i.description))
        i.news = (mlget(i.news, all=True), mlget(i.news))
        ret.append(i)
    #
    return ret

        
def dyahoo(id=0, field='*', format=True, format_type=1):
    if format: field='*'
    if id:
        q = 'select $field from ms_yahoo where id=$id order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_yahoo order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    for i in r:
        a = i.account
        t = i.type
        if format_type:
            t = format_type
        y = 'http://opi.yahoo.com/online?u=%s&m=g&t=%s' %(a, t)
        aty = ()
        if format:
            aty = (a, t, y)
        #
        a2 = (a, aty)
        i.account = a2
    #
    return r


def dpro():
    ret = []
    q = 'select id,name from ms_category where active=1 order by priority desc' 
    r = query(q)
    for i in r:
        #check 1
        nameall = mlget(i.name, all=True)
        if disblank(nameall, False): continue
        #
        #check 2
        q_cat = 'select id from ms_product where category_id=$category_id'
        a_cat = {'category_id': i.id}
        r_cat = query(q_cat, a_cat)
        if not r_cat: continue
        #
        #
        i.name = mlget(i.name)
        #
        temp = []
        q2 = 'select id,name,description,full_info,file_id as file from ms_product where active=1 and category_id=$cid order by priority desc'
        a2 = {'cid': i.id}
        r2 = query(q2, a2)
        for j in r2:
            #
            q_file = 'select id,name,type from ms_file where id=$file_id'
            a_file = {'file_id': j.file}
            r_file = query(q_file, a_file)
            if r_file: 
                finfo = r_file[0]
                j.file = (ub('/fs' + '/' + str(j.file)), finfo)
            else:
                finfo = []
                j.file = []
            #
            j.name = mlget(j.name)
            j.description = mlget(j.description)
            j.full_info = mlget(j.full_info)
            #
            if pget('cart_check_stock') == '1':
                q3 = 'select id,name,stock,price,currency_id,variant_file_id from ms_product_variant where active=1 and product_id=$pid and stock > 0 order by id'
            else:                
                q3 = 'select id,name,stock,price,currency_id,variant_file_id from ms_product_variant where active=1 and product_id=$pid order by id'
            a3 = {'pid': j.id}
            r3 = query(q3, a3)
            for k in r3:
                k.name = mlget(k.name)
                #
                k.price = nf(k.price)
                if FORCE_SINGLE_CURRENCY:
                    k.currency = pget('currency', callback=dcur).csymbol
                else:
                    q4 = 'select csymbol from ms_currency where id=$currid'
                    a4 = {'currid': k.currency_id}
                    r4 = query(q4, a4)
                    k.currency = r4[0].csymbol
                #
                #stock check
                if pget('cart_check_stock') == '1':
                    if sess.c.has_key(k.id) and sess.c[k.id]:
                        in_cart = sess.c[k.id]
                    else:
                        in_cart = 0
                    k.stock = k.stock - in_cart
                    if k.stock > CART_ADD_MAX:
                        k.stock = CART_ADD_MAX
                else:
                    k.stock = CART_ADD_MAX
                #
                #

            temp.append((j, r3))
        #
        ret.append( ( (i.id, i.name) , temp) )
    #
    return ret


def dcart():
    global db
    global sess
    #
    carts = []
    keys = sess.c.keys()
    keys.sort()
    #
    total = 0
    for i in keys:
        vid = i
        qty = sess.c[i]
        sqty = nf(qty, 0)
        #
        q = '''
        select name from ms_product where id in 
        (select product_id from ms_product_variant where id=$vid)
        '''
        a = {'vid': vid}
        r = query(q, a)
        product = rget(r, 'name')
        product = mlget(product)
        #
        q = '''
        select csymbol from ms_currency where id in 
        (select currency_id from ms_product_variant where id=$vid)
        '''
        a = {'vid': vid}
        r = query(q, a)
        csymbol = rget(r, 'csymbol')
        #
        q = 'select name,price,taxratio from ms_product_variant where id=$vid'
        a = {'vid': vid}
        r = query(q, a)
        variant = rget(r, 'name')
        variant = mlget(variant)
        price = rget(r, 'price', default=0)
        sprice = nf(price)
        tax = rget(r, 'taxratio', default=0) * price
        stax = nf(tax)
        #
        pv = '%s - %s' %(product, variant)
        #
        subt = qty * (price+tax)
        ssubt = nf(subt)
        #
        temp = (vid, csymbol, pv, (qty, sqty), (price, sprice), (tax, stax), (subt, ssubt))
        carts.append(temp)
        #
        total += subt
    #
    stotal = nf(total)
    #
    q = 'select id,name from ms_payment_type order by id'
    r = query(q)
    r_pay = []
    for i in r: 
        if i.id in PAYMENT_TYPE: 
            r_pay.append(i)
    #
    if FORCE_SINGLE_CURRENCY:
        currency = pget('currency', callback=dcur).csymbol 
    else:
        currency = ''
    #
    ret = (carts, (total, stotal), r_pay, currency)
    #
    return ret


def dadmin(section=['user', 'admin']):
    global sess
    #
    ret = []
    #
    if not sess.u: return ret
    #
    sorted = []
    #
    mall = []
    for i in section:
        stemp = m.t(m.MENUADMIN, sess.lang)[i]
        if i == 'admin' or i.startswith('admin.'):
            if isadmin():
                for i in stemp:
                    mall.append(i)
        else:
            for i in stemp:
                mall.append(i)
        #
    #
    for i in mall:
        if i[3]:#check res
            if res[i[3]]: 
                sorted.append(i[2])
        else:
            sorted.append(i[2])
    #
    sorted.sort()
    #
    for i in sorted:
        for j in mall:
            if j[2] == i:
                ret.append( (j[0], ub(j[1]), j[2]) )
    #
    return ret
        

def ddata(fields):
    global msgs
    #
    ret = {}
    if 'yahoo' in fields:
        ret['yahoo'] = dyahoo()
    #
    if 'link' in fields:
        ret['link'] = dlink()
    #
    if 'extra' in fields:
        extra = pget('extra_info')
        extra = mlget(extra)
        ret['extra'] = extra
    #
    if 'sticky' in fields:
        sticky = pget('sticky_info')
        sticky = mlget(sticky)
        ret['sticky'] = sticky
    #
    if 'promo_host' in fields:
        if pget('promo_host') == '1' or FORCE_PROMOTE:
            promo_host = msgs['promo_host_default']
        else:
            promo_host = ''
        ret['promo_host'] = promo_host
    #
    if 'news' in fields:
        ret['news'] = dnews()
    #
    if 'product' in fields:
        ret['product'] = dpro()
    #
    if 'cart' in fields:
        ret['cart'] = dcart()
    #
    return ret


def ucget(all=False):
    ret = []
    #
    if all:
        q = 'select id,page,priority from ms_user_content where active=1 order by priority asc'
    else:
        q = 'select id,page,priority from ms_user_content where active=1 and show_in_menu=1 order by priority asc'
    r = query(q)
    for i in r:
        i.page = mlget(i.page)
        url = '/go/%s' %(i.id)
        temp = (i.page, ub(url), i.priority, url)
        ret.append(temp)
    #
    return ret


def menugen(hidden_user_content=False):
    global menu
    global sess
    #
    all = []
    all2 = []
    sorted = []
    all3 = []
    #
    for i in menu['default']: 
        all.append(i)
    if pget('use_cart') == '1' and res['cart']: 
        for i in menu['cart']:
            all.append(i)
    if dfaq(): 
        for i in menu['faq']:
            all.append(i)
    if dnews(read_session=False): 
        for i in menu['news']:
            all.append(i)
    if sess.u:
        for i in menu['auth']:
            all.append(i)
    else:
        for i in menu['noauth']:
            all.append(i)
    #
    for i in all:
        all2.append( ( i[0], ub(i[1]), i[2], i[1] ) )
        sorted.append(i[2])
    #
    if res['user_content']:
        if hidden_user_content:
            uc = ucget(True)
        else:
            uc = ucget()
        for i in uc:
            all2.append(i)
            sorted.append(i[2])
    #
    sorted.sort()
    for i in sorted:
        for j in all2:
            if j[2] == i:
                all3.append(j)
    #
    return all3


def invoicegen(cartdata, cart_id, date_purchase, payment, cust_name, cust_email, ship_addr, note):
    global msgs
    #
    carts = cartdata[0]
    #
    cw_pro = CWIDTH['product']
    cw_qty = CWIDTH['qty']
    cw_price = CWIDTH['price']
    cw_vat = CWIDTH['vat']
    cw_subt = CWIDTH['subtotal']
    #
    maxlen = 0
    for i in CWIDTH.keys(): maxlen += CWIDTH[i]
    line = '-' * maxlen
    endl = '\r\n'
    invtext = ''
    
    #info
    invtext += DOMAIN + endl
    site_desc = pget('site_description')
    site_desc = mlget(site_desc)
    if site_desc: 
        invtext +=  site_desc + endl
    inv_extra = pget('invoice_extra_info')
    inv_extra = mlget(inv_extra)
    if inv_extra:
        invtext +=  inv_extra + endl 
    
    #to
    inv_to = '%s <%s>' %(cust_name, cust_email)
    
    #payment
    q = 'select name from ms_payment_type where id=$payment'
    a = {'payment': payment}
    r_pay_type = query(q, a)
    payment_type = rget(r_pay_type, 'name')
    
    #header
    invtext += endl + msgs['header_cart_invoice_date'].capitalize() + ': ' + date_purchase 
    invtext += endl + msgs['header_cart_invoice'].capitalize() + ': ' + cart_id 
    invtext += endl + msgs['header_cart_invoice_to'].capitalize() + ': ' + inv_to 
    invtext += endl + msgs['header_cart_invoice_addr'].capitalize() + ': ' + ship_addr
    invtext += endl + msgs['header_cart_invoice_payment'].capitalize() + ': ' + payment_type
    invtext += endl + msgs['header_cart_invoice_note'].capitalize() + ': ' + note
    #
    invtext += endl + endl + line + endl
    invtext += msgs['header_cart_product'].capitalize().center(cw_pro)
    invtext += msgs['header_cart_qty'].capitalize().center(cw_qty)
    invtext += msgs['header_cart_price'].capitalize().center(cw_price)
    invtext += msgs['header_cart_vat'].center(cw_vat)
    invtext += msgs['header_cart_subtotal'].capitalize().center(cw_subt)
    invtext += endl + line + endl
    
    #detail
    for i in carts:
        if FORCE_SINGLE_CURRENCY:
            csym = cartdata[3][:3].ljust(3)        
        else:
            csym = '' #fixme when multi currency is supported
        lcsym = len(csym)
        lcs = len(CSPACE)
        #
        c_pro = cw_pro - lcs
        c_qty = cw_qty - lcs
        c_price = cw_price - lcs - lcsym
        c_vat = cw_vat - lcs - lcsym
        c_subt = cw_subt - lcs - lcsym
        c_totstr = c_pro + lcs + c_qty + lcs + lcsym + c_price + lcs + lcsym + c_vat 
        #
        i_pro = i[2][:c_pro].ljust(c_pro) 
        i_qty = i[3][1][:c_qty].rjust(c_qty) 
        i_price = i[4][1][:c_price].rjust(c_price) 
        i_vat = i[5][1][:c_vat].rjust(c_vat) 
        i_subt = i[6][1][:c_subt].rjust(c_subt) 
        #
        invtext += i_pro + CSPACE + i_qty + CSPACE + csym + i_price + CSPACE + csym + i_vat + CSPACE + csym + i_subt + endl
    #
    invtext += line + endl
    invtext += msgs['header_cart_total'].capitalize().rjust(c_totstr) + CSPACE + csym + cartdata[1][1][:c_subt].rjust(c_subt) + endl
    invtext += line + endl
    
    #bank info
    show_bank = pget('invoice_show_bank')
    if show_bank == '1':
        q = 'select * from ms_bank where active=1 order by id'
        r_bank = query(q)
        if r_bank:
            invtext += msgs['header_cart_bank_account'].capitalize() + ':' + endl
            for i in r_bank:
                invtext += i.name + ' ' + i.branch + ' ' + '(' + i.holder + '/' + i.account+ ')' + endl
            invtext += endl
                
    #paypal info
    show_pp = pget('invoice_show_paypal')
    if show_pp == '1':
        q = 'select * from ms_paypal where active=1 order by id'
        r_pp = query(q)
        if r_pp:
            invtext += msgs['header_cart_paypal_account'].capitalize() + ':' + endl
            for i in r_pp:
                invtext += i.account + endl
            invtext += endl
    #
    return invtext
    

def invoicesave(payment, cust_name, cust_email, ship_addr, note, clear_cart=True, mail=True):
    global db
    global sess
    global msgs
    #
    ret = 0
    #
    cartdata = dcart()
    carts = cartdata[0]
    #
    curid = None
    if FORCE_SINGLE_CURRENCY:
        curid = pget('currency', default=0)
    #
    cart_id = cidget()    
    date_purchase = now()
    invtext = invoicegen(cartdata, cart_id, date_purchase, payment, cust_name, cust_email, ship_addr, note)
    #
    t = db.transaction()
    try:
        insert_id = db.insert('tr_invoice_header', cart_id=cart_id, 
                    log_id=sess.log, total=cartdata[1][0], date_purchase=date_purchase,
                    payment_type=payment, used_currency=curid,
                    cust_name=cust_name, cust_email=cust_email,
                    ship_addr=ship_addr, note=note, invoice_text=invtext,
                    invoice_lang=sess.lang
                    )
        #
        for i in carts:
            db.insert('tr_invoice_detail', header_id=insert_id,
            product_variant=i[0], saved_price=i[4][0], saved_tax=i[5][0], 
            amount=i[3][0], log_id=sess.log)
        #
    except:
        t.rollback()
    else:
        t.commit()
        #
        ret = insert_id
        #
        sess.co['invoice_text'] = invtext
        #
        if clear_cart:
            sess.c = {}    
        #
        if mail:
            subj = msgs['header_cart_invoice'].capitalize() + ': ' + cart_id 
            subj_copy = msgs['msg_copy_of'].capitalize() + ' ' + msgs['header_cart_invoice'].capitalize() + ': ' + cart_id 
            sendmail(cust_email, subj, invtext)
            sendmail(MAIL_DEFAULT, subj_copy, invtext)
            sess.co['mail_sent'] = msgs['header_cart_invoice_mail_sent']
        else:
            sess.co['mail_sent'] = ''
    #
    return ret

        
def dfs(id=0, content=False, name_add=True, format=True, format_div=1, filter=None):
    if not id:
        if content:
            q = 'select id, name, name_add, size, type, type_options, disposition, disposition_options, date_file, headers, content from ms_file order by id desc'
        else:
            q = 'select id, name, name_add, size, type, type_options, disposition, disposition_options, date_file, headers from ms_file order by id desc'
        a = {}
    else:
        if content:
            q = 'select id, name, name_add, size, type, type_options, disposition, disposition_options, date_file, headers, content from ms_file where id=$id order by id desc'
        else:
            q = 'select id, name, name_add, size, type, type_options, disposition, disposition_options, date_file, headers from ms_file where id=$id order by id desc'
        a = {'id': id}
    r = query(q, a)
    #
    for i in r:
        if format:
            if not i.size: i.size = 0
            i.size = nf(float(i.size)/format_div)
        if name_add:
            if i.name_add:
                i.name = '%s (%s)' %(i.name, i.name_add)
        i.type_options = yaml.load(i.type_options)
        i.disposition_options = yaml.load(i.disposition_options)
        i.headers = yaml.load(i.headers)
    #
    if filter:
        ret = []
        for i in r:
            for j in filter:
                if i.type.find(j) > -1:
                    ret.append(i)
                    break
    else:
        ret = r
    return ret


def smget(next=[]):
    ret = sess.msg or []
    sess.msg = next
    return ret


def mlset(input, field_prefix, separator='.', strip=True, strip_br=True, check_empty_html=True):
    data = {}
    ccode = [m.COUNTRY[x][0] for x in m.COUNTRY.keys()]
    for i in input.keys():
        try:
            s = i.split(separator)
        except:
            s = []
        if len(s) == 2 and s[0] == field_prefix and s[1] in ccode:
            inputi = input[i]
            if strip and hasattr(inputi, 'strip'):
                inputi = inputi.strip()
            #
            if strip_br:
                inputi = stripsall(inputi, '<br>')
            #
            data[s[1]] = inputi
            #
            if check_empty_html:
                empcheck = striphtml(inputi).strip()
                if empcheck:
                    data[s[1]] = inputi
                else:
                    data[s[1]] = ''
                
    #
    ret = yaml.dump(data)
    #
    return ret
    

def isadmin():
    if not sess.u: return False
    #
    q = "select id from ms_user where id=$uid and group_id in (select id from ms_group where name='ADMIN')";
    a = {'uid': sess.u}
    r = query(q, a)
    if r:
        return True
    #
    return False


def ypget(option, default={}, lang=True):
    o = pget(option, default=default)
    if not o: o = '{}'
    o2 = yaml.load(o)
    #
    if not lang:
        return o2
    #
    ccode = [m.COUNTRY[x][0] for x in m.COUNTRY.keys()]
    #
    ret = {}
    #
    for i in ccode:
        if not o2.has_key(i):
            ret[i] = ''
        else:
            ret[i] = o2[i]
    #
    return ret    


def dpro_category(id=0, field='*'):
    if id:
        q = 'select $field from ms_category where active=1 and id=$id order by priority desc'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_category where active=1 order by priority desc'
        a = {'field': web.SQLLiteral(field)}
    #
    ret = query(q, a)
    for i in ret:
        if i.has_key('priority'):
            if not i.priority: i.priority = 0
        if i.has_key('name'):
            i.name = (mlget(i.name, all=True), mlget(i.name) )
    return ret


def disblank(data, is_yaml, strip=True):
    if is_yaml:
        try:
            ydata = yaml.load(data)
        except:
            return True
    else:
        ydata = data
    #
    ret = True
    for k in ydata.keys():
        test = ydata[k]
        if strip and hasattr(test, 'strip'):
            test = test.strip()
        if test:
            ret = False
            break
    #
    return ret


def dpro_group(id=0, field='*'):
    cat = [int(x.id) for x in dpro_category(field='id')]
    ret = []
    if id:
        q = 'select $field,category_id from ms_product where active=1 and id=$id order by priority desc'
        a = {'id': id, 'field': web.SQLLiteral(field), 'cid': id}
        test = query(q, a)
        if test[0].category_id in cat:
            ret = test
    else:
        for i in cat:
            q = 'select $field,category_id from ms_product where active=1 and category_id=$cid order by priority desc'
            a = {'field': web.SQLLiteral(field), 'cid': i}
            ret += query(q, a)
    #
    for i in ret:
        if i.has_key('category_id'):
            cat = dpro_category(id=i.category_id, field='name')
            i.category_id = (i.category_id, cat[0].name[1])
        if i.has_key('name'):
            i.name = (mlget(i.name, all=True), mlget(i.name) )
        if i.has_key('description'):
            i.description = (mlget(i.description, all=True), mlget(i.description) )
        if i.has_key('full_info'):
            i.full_info = (mlget(i.full_info, all=True), mlget(i.full_info) )
    return ret


def dpro_item(id=0, field='*'):
    group = [int(x.id) for x in dpro_group(field='id')]
    ret = []
    if id:
        q = 'select $field,product_id,currency_id from ms_product_variant where active=1 and id=$id order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
        test = query(q, a)
        if test and test[0].product_id in group:
            ret = test
    else:
        for i in group:
            q = 'select $field,product_id,currency_id from ms_product_variant where active=1 and product_id=$pid order by id'
            a = {'field': web.SQLLiteral(field), 'pid': i}
            ret += query(q, a)
    #
    for i in ret:
        group = dpro_group(id=i.product_id, field='name')
        i.product_id = (i.product_id, group[0].name[1])
        if i.has_key('name'):
            i.name = (mlget(i.name, all=True), mlget(i.name), '%s - %s' %(group[0].name[1], mlget(i.name))  )
        if i.has_key('currency_id'):
            if FORCE_SINGLE_CURRENCY:
                curoptions = ()
                mcur = pget('currency', callback=dcur).csymbol
            else:
                curoptions = ()
                mcur = ''
            #
            r_csymbol = query('select csymbol from ms_currency where id=$curid', {'curid': i.currency_id})
            csymbol = rget(r_csymbol, 'csymbol', default='')
            i.currency_id = (i.currency_id, csymbol, curoptions, mcur)
        if i.has_key('taxratio'):
            if not i.taxratio: 
                i.taxratio = 0
            else:
                i.taxratio = nrfloat(i.taxratio)
        if i.has_key('price'):
            i.price = nrfloat(i.price)
    return ret

        
def siget(input, field_prefix, field_suffix, separator='.', strip=True, strip_br=True, check_empty_html=True):
    ret = ''
    for i in input.keys():
        try:
            s = i.split(separator)
        except:
            s = []
        if len(s) == 2 and s[0] == field_prefix and s[1] == field_suffix:
            ret = input[i]
    #
    if strip and hasattr(ret, 'strip'):
        ret = ret.strip()
    #
    if strip_br:
        ret = stripsall(ret, '<br>')
    #
    if check_empty_html:
        empcheck = striphtml(ret).strip()
        if not empcheck:
            ret = ''
    #
    return ret


def nlimit(number, min, max):
    ret = number
    if number < min:
        ret = min
    elif number > max:
        ret = max
    #
    return ret


def nrfloat(snumber, precision=PRECISION, round=decimal.ROUND_UP):
    le = '0' * precision
    if not le:
        dec = '1'
    else:
        dec = '.' + le
    #
    num = str(snumber)
    try:
        d = decimal.Decimal(num)
        ret = d.quantize(decimal.Decimal(dec), rounding=round)
    except:
        ret = None
    #
    return ret
        

def rt(precision=4, show_second=True):
    if not pget('expose_time') == '1': return ''
    #
    x = rendertime[1] - rendertime[0]
    if x <= 0:
        x = 0
    #
    if x:
        ret = nrfloat(x, precision, decimal.ROUND_DOWN)
        if show_second:
            ret = '%s %s' %(ret, msgs['header_second'])
    else:
        ret = 0
        if show_second:
            ret = ''
    #
    return ret
    

def dcur(id=0, field='*', pget_helper=''):
    if id:
        q = 'select $field from ms_currency where id=$id order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_currency order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    #
    if pget_helper:
        if not id or id == 0 or not r: 
            no = {'csymbol': '', 'id': '', 'name': ''}
            no = web.utils.storify(no)
            return no
        else:
            return r[0]
    #
    return r


def atpl():
    ret = []
    tdir = TEMPLATE_DIR
    files = os.listdir(tdir)
    for i in files:
        info = tinfo(i)
        try:
            owner = info['general']['owner']
        except:
            owner = ''
        if owner and DOMAIN.lower() not in owner:
            pass
        else:
            ret.append(i)
    return ret


def dbank(id=0, field='*', complete_name=False):
    if complete_name:
        field = '*'
    if id:
        q = 'select $field from ms_bank where id=$id and active=1 order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_bank  where active=1 order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    #
    if complete_name:
        for i in r:
            cur = dcur(id=i.currency_id)[0].csymbol
            if i.branch:
                branch = '(%s)' %(i.branch)
            else:
                branch = ''
            i.name = '%s %s - %s - %s - %s' %(i.name, branch, i.holder, i.account, cur)
    #
    return r
    

def captcha_gen_word(allowed='aAbBdDeEGhHnNQrRtT23456789', min=4, max=7):
    ret = ''
    length_choice = range(min, max+1)
    length = random.choice(length_choice)
    for i in range(length):
        r = random.choice(allowed)
        ret += r
    return ret


def captcha_gen_image(word, font_file='', font_size=20, format='JPEG', fg=-1, bg=-1):
    if fg == -1:
        fg = random.randint(0, 0xffffff)
    if bg == -1:
        bg = fg ^ 0xffffff
    #
    font_dir = pget('font_dir') 
    if not font_file:
        try:
            font_file = random.choice(os.listdir(font_dir))
            font_file = font_dir + PS + font_file
        except:
            font_file = ''
    else:
        font_file = font_dir + PS + font_file
    #
    if os.path.exists(font_file):
        font = ImageFont.truetype(font_file, font_size)
    else:
        font = ImageFont.load_default()
    #
    size = font.getsize(word)
    #
    img = Image.new('RGB', (size[0]+random.randint(0,10), 
            size[1]+random.randint(0,10)), bg)
    draw = ImageDraw.Draw(img)
    #
    for i in range(5):
        lines = []
        for i in range(random.randint(3,5)):
            lines.append((random.randint(0, 100), random.randint(0, 100)))        
        draw.polygon(lines, outline=fg)
    #
    width = size[0]/len(word)
    i = 0
    for w in word:
        x = (i * width) + random.randint(-1, 2)
        y = random.randint(-1, 4)
        draw.text((x, y), w, font=font, fill=fg)
        i += 1
    #
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img


def ulangd(x):
    return x or msgs['header_no_translation'].capitalize()


def ucart():
    return str(  int(bool(pget('use_cart', '')) and res['cart'])  )


def uid():
    return sess.u
    
    
def title(ttl):
    host = web.ctx.env.get('HTTP_HOST', msgs['host_default'])
    desc = pget('site_description', default='')
    desc = mlget(desc)
    if desc:
        ret = '[%s] %s - %s' %(host, desc, ttl)
    else:
        ret = '[%s] - %s' %(host, ttl)
    return ret


def ddatab():
    #return ddata(fields=['extra','promo_host','news','sticky'])
    return ddata(fields=['yahoo','extra','promo_host','news','sticky','link'])    


def ddatac(p):
    return ddata(fields=[p])
    
    
def tpl(page):
    return tget(page, 
            globals={
                'ub': ub, 
                'ucart': ucart, 
                'uid': uid, 
                'msg': msgs, 
                'ulang': m.COUNTRY, 
                'ulangd': ulangd, 
                'rt': rt, 
                'now': now,
                'iflash': iflash,
                'logo': logo,
                'meta': meta,
                'dkget': dkget,
                'favicon': favicon,
                'adminurlgroup': ADMIN_URL_GROUP,
                'mobile': mobile,
            })     


def tplb(o):
    return tpl('base').base(menugen(), ddatab(), o, web.ctx.path)
    

def logo():
    id = int(pget('logo_file', default=-1))
    return dfs(id=id)


def meta():
    ret = [
            {'name': 'keywords', 'content': pget('site_keywords')},
            {'name': 'description', 'content': mlget(pget('site_description'))},
        ]
    return ret
    
    
def lastlog():
    return None
    
    
def lastupdate():
    return None


def iflash(name, quality='high', wmode='transparent', scale='exactfit', width='100%', height='100%'):
    ret = '''
        <object classid='clsid:D27CDB6E-AE6D-11cf-96B8-444553540000' codebase='http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0' width='%s' height='%s'>
            <param name='movie' value='%s'>
            <param name='quality' value='%s'>
            <param name='wmode' value='%s'>
            <param name='scale' value='%s'>
        <embed src='%s' width='%s' height='%s' scale='%s' quality='%s' pluginspage='http://www.macromedia.com/go/getflashplayer' type='application/x-shockwave-flash' wmode='%s'>
        </embed> 
        </object>                        
    '''  %(
        width, height,
        name,
        quality,
        wmode,
        scale,
        name, width, height, scale, quality, wmode
    )  
    return ret
    

def dkget(dictionary, key, prefix='', suffix='', default='', strip=True):
    ret = default
    if dictionary.has_key(key):
        if dictionary[key]:
            ret = dictionary[key]
            ret = '%s%s%s' %(prefix, ret, suffix)
    #
    if ret and hasattr(ret, 'strip'):
        ret = ret.strip()
    #
    return ret
    

def dprofile(id, field='*'):
    ret = {}
    #
    q = 'select $field from ms_user where active=1 and id=$id'
    a = {'field': web.SQLLiteral(field), 'id': id}
    ret = query(q, a)
    #
    if ret:
        ret = ret[0]
        if ret.has_key('password'): ret['password'] = ''
        for i in ['email', 'phone', 'fax', 'web','icontact','acontact','govid']:
            if ret.has_key(i):
                if ret[i]:
                    ret[i] = ','.join(yaml.load(ret[i]))
    #
    return ret
    

def sepnorm(field, separator=',', remove_space=True, unique=True, replace_underscore_with_space=True, as_string=True):
    strs = field.strip()
    splitted = strs.split(separator)
    splitted2 = [x.strip() for x in splitted]
    if remove_space:
        splitted3 = [x.replace(' ', '') for x in splitted2]
    else:
        splitted3 = splitted2
    
    if unique:
        splitted4 = []
        for i in splitted3:
            if i not in splitted4:
                splitted4.append(i)
    else:
        splitte4 = splitted3

    if replace_underscore_with_space:
        splitted5 = [x.replace('_', ' ') for x in splitted4]
    else:
        splitted5 = splitted4
        
    newlist = []
    for part in splitted5:
        if part:
            newlist.append(part)
    #
    if not as_string:
        ret = newlist
    else:
        ret = separator.join(newlist)
    #
    return ret

    

def favicon():
    rel = ['SHORTCUT ICON', 'icon']
    f = ub('/static/favicon.ico')
    ret = ''
    for i in rel:
        ret += "<link rel='%s' href='%s'>" %(i, f)
    #
    return ret


def dpaypal(id=0, field='*'):
    if id:
        q = 'select $field from ms_paypal where id=$id and active=1 order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_paypal where active=1 order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    #
    return r


def dlink(id=0, field='*'):
    if id:
        q = 'select $field from ms_link where id=$id order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_link order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    #
    return r


def dpromote():
    ret = []
    url = "http://%s%s" %(DOMAIN, ub('/'))
    #
    bbcode = {
        'style' : 'BBCode',
        'code'  : "[url=%s]%s[/url]" %(url, DOMAIN),
        }
    #    
    a = {
        'style' : 'HTML Link',
        'code'  : "<a href='%s'>%s</a>" %(url, DOMAIN),
        }
    #
    aimg = {
        'style' : 'HTML Link (image)',
        'code'  : "<a href='%s'><img src='%s/fs/%s'></a>" %(url, url, pget('logo_file')),
        }
    #
    markdown = {
        'style' : 'Markdown',
        'code'  : "[%s](%s)" %(DOMAIN, url),
        }
    #
    mediawiki = {
        'style' : 'MediaWiki',
        'code'  : "[%s %s]" %(url, DOMAIN),
        }    
    #
    textile = {
        'style' : 'Textile',
        'code'  : '"%s":%s' %(DOMAIN, url),
        }    
    #
    ret.append(a)
    if pget('logo_file'): ret.append(aimg)
    ret.append(bbcode)
    ret.append(markdown)
    ret.append(mediawiki)
    ret.append(textile)
    #
    return ret


def dfaq(id=0, field='*', group=False):
    if id:
        q = 'select $field from tr_faq where id=$id order by id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from tr_faq order by id'
        a = {'field': web.SQLLiteral(field)}
    r = query(q, a)
    #
    for i in r:
        if i.has_key('category'):
            i.category = (mlget(i.category, all=True), mlget(i.category))
        if i.has_key('question'):
            i.question = (mlget(i.question, all=True), mlget(i.question))
        if i.has_key('answer'):
            i.answer = (mlget(i.answer, all=True), mlget(i.answer))
    #
    if group:
        q_cat = 'select distinct category from tr_faq order by id'
        a_cat = {}
        r_cat = query(q_cat, a_cat)
        ret = {}
        for i in r_cat:
            cat = mlget(i.category)
            ret[cat] = []
            #
            for j in r:
                if j.category[1] == cat:
                    ret[cat].append( j )
    else:
        ret = r
    #
    return ret


def dinvoice(id=0, field='*', date_from='', date_to='', closed=False, all_confirm=False):
    if id:
        q = 'select $field from tr_invoice_header where id=$id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from tr_invoice_header where date_purchase >= $df and date_purchase <= date($dt, "+1 days") and done=$closed order by date_purchase desc'
        a = {'field': web.SQLLiteral(field), 'df': date_from, 'dt': date_to, 'closed': closed}
    r = query(q, a)
    #
    for i in r:
        if i.has_key('total'):
            i.total = (i.total, nf(i.total))
        
        if i.has_key('used_currency'):
            if FORCE_SINGLE_CURRENCY:
                i.used_currency = pget('currency', callback=dcur).csymbol
            else:
                q = 'select csymbol from ms_currency where id=$curid'
                a = {'curid': i.used_currency}
                r_cur = query(q, a)
                i.used_currency = rget(r_cur, 'csymbol')
        
        if i.has_key('confirm_info'):
            confirm = rget([i], 'confirm_info', default=[], to_yaml=True)
            i.confirm_info = confirm
            if confirm:
                if all_confirm == False:
                    i.confirm_info = confirm[-1]
    #
    return r


def dstat(date_from='', date_to=''):
    ret = []
    #
    all = [
            [ 
                msgs['header_stat_country'], 
                'select count(*) as count from tr_log where date_log>=$df and date_log<= date($dt, "+1 days")',
                'select distinct country as var,count(country) as val from tr_log where date_log>=$df and date_log <= date($dt, "+1 days") group by var order by val desc',
                None,
            ],
            [ 
                msgs['header_stat_top_products'], 
                'select count(*) as count from tr_invoice_detail where header_id in (select id from tr_invoice_header where date_purchase>=$df and date_purchase<= date($dt, "+1 days"))',
                'select distinct product_variant as var,count(product_variant) as val from tr_invoice_detail where header_id in (select id from tr_invoice_header where date_purchase>=$df and date_purchase<= date($dt, "+1 days")) group by var order by val desc',
                (dpro_item, 'name', True, 2),
            ],            
        ]   
    #
    for x in all:
        temp = {'category': x[0]}
        q = x[1]
        a = {'df': date_from, 'dt': date_to}
        r_total = query(q, a)
        c_total = rget(r_total, 'count', default=1)
        q = x[2]
        r = query(q, a)
        counted = 0
        for i in r:
            counted += i.val
        for i in r:
            if not i.var:
                i.var = msgs['msg_unknown']
                i.val = c_total - counted
            percent = nrfloat((float(i.val) * 100)/c_total, round=decimal.ROUND_DOWN)
            #
            if not x[3]:
                i.var = str(i.var)
            else:
                if x[3][2]: #mlget
                    try:
                        #i.var = mlget(x[3][0](i.var)[0].name)
                        i.var = x[3][0](i.var)[0][ x[3][1] ][ x[3][3]  ]
                    except:
                        i.var = msgs['msg_unknown']
                else:
                    try:
                        i.var = x[3][0](i.var)[0].name
                    except:
                        i.var = msgs['msg_unknown']
            #
            i.val = (i.val,  '%s%%' %(percent))
        temp['stat'] = r
        temp['total'] = c_total
        if r:
            ret.append(temp)
    #
    return ret
    

def tinfo(template, separator=','):
    ret = {}
    #
    tdir = TEMPLATE_DIR
    info = tdir + PS + template + PS + 'info'
    #
    t = ConfigParser.ConfigParser()
    try:
        t.read(info)
    except:
        return ret
    #
    sections = t.sections()
    for i in sections:
        items = t.options(i)
        temp = {}
        for j in items:
            citem = t.get(i, j)
            if hasattr(citem, 'strip'):
                citem = citem.strip()
            if citem and citem[0] == '[' and citem[-1] == ']':
                sitem = citem[1:-1].split(separator)
                item = [x.strip() for x in sitem]
            else:
                item = citem.strip()    
            temp[j] = item
        ret[i] = temp
    #
    return ret
    

def dredir(id=0, field='*'):
    if id:
        q = 'select $field from ms_redirect where id=$id'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_redirect order by id'
        a = {'field': web.SQLLiteral(field)}
    #
    ret = query(q, a)
    return ret


def dgo(id=0, field='*'):
    if id:
        q = 'select $field from ms_user_content where id=$id and active=1'
        a = {'id': id, 'field': web.SQLLiteral(field)}
    else:
        q = 'select $field from ms_user_content where active=1 order by priority asc,id desc'
        a = {'field': web.SQLLiteral(field)}
    #
    ret = query(q, a)
    for i in ret:
        if i.has_key('priority'):
            if not i.priority: i.priority = 0
        if i.has_key('page'):
            i.page = (mlget(i.page, all=True), mlget(i.page) )        
        if i.has_key('content'):
            i.content = (mlget(i.content, all=True), mlget(i.content) )        
    return ret

    
    
############################# CUSTOM ERROR #############################


def notfound():
    expose_error = pget('expose_error')
    general_error_message = pget('general_error_message')
    if expose_error == '1':
        t = tpl('error_notfound')
        ttl = msgs['msg_error'].capitalize()
        o = t.error_notfound(title(ttl), general_error_message)
        o = tplb(o)
        return web.notfound(o)
    #
    raise web.seeother('/')


def internalerror():
    expose_error = pget('expose_error')
    general_error_message = pget('general_error_message')
    ttl = msgs['msg_error'].capitalize()
    if expose_error == '1':
        t = tpl('error_internalerror')
        o = t.error_internalerror(title(ttl), general_error_message)
        o = tplb(o)
        return web.internalerror(o)
    #
    return web.internalerror(ttl)


class nomethod(web.webapi.HTTPError):
    def __init__(self, cls=None):
        status = '405 Method Not Allowed'
        headers = {}
        headers['Content-Type'] = 'text/html'
        
        methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
        if cls:
            methods = [method for method in methods if hasattr(cls, method)]

        headers['Allow'] = ', '.join(methods)
        data = 'REQUEST METHOD ERROR'
        web.webapi.HTTPError.__init__(self, status, headers, data)

        
wapp.notfound = notfound
wapp.internalerror = internalerror
web.webapi.nomethod = nomethod

########################### WSGI + PROCESSOR ###########################


def proc_db_check(handle):
    if db_error or not os.path.exists(DATA_FILE) or not os.access(DATA_FILE, os.W_OK):
        msgs = m.t(m.MSG, LANG_DEFAULT)
        return msgs['msg_error_db_connect']
    return handle()
    

def proc_set_log(handle):
    if sess.log: 
        q = 'update tr_log set date_log_last=$log_last,activity=activity+1,user_id_last=$user_id_last where id=$log_id'
        a = {'log_last': now(), 'log_id': sess.log, 'user_id_last': sess.u}
        r = query(q, a)
        return handle()
    #
    ip = web.ctx.ip
    ref = web.ctx.env.get('HTTP_REFERER', '')
    ua = web.ctx.env.get('HTTP_USER_AGENT', '')
    url = web.ctx.fullpath
    met = web.ctx.method
    dt = now()
    #
    country = None
    if callable(fgeo):
        country = fgeo(ip)
        if not country: country = None
    #
    insert_id = db.insert('tr_log', 
                date_log=dt, date_log_last=dt, activity=1, ip=ip, 
                country=country, referer=ref, url=url,
                user_agent=ua, method=met, user_id=sess.u
                )
    if insert_id:
        sess.log = insert_id
    return handle()


def proc_set_lang(handle):
    global msgs
    global menu
    #
    lang = LANG_DEFAULT
    #
    if sess.lang: #already set
        lang = sess.lang
    else: #not set
        plang = pget('lang') #read db
        if plang:
            lang = plang
        else:
            #auto
            ip = web.ctx.ip
            #
            country = None
            if callable(fgeo):
                country = fgeo(ip)
                if not country: country = None
            #
            #
            if m.COUNTRY.has_key(country):
                lang = m.COUNTRY[country][0]            
    #set
    sess.lang = lang
    #
    msgs = m.t(m.MSG, lang)
    menu = m.t(m.MENU, lang)
    #    
    return handle()


def proc_limit_cart(handle):
    if ucart() != '1' or not res['cart']:
        path = web.ctx.fullpath.lower()
        if path.startswith('/cart') or path.startswith('/payment') or path.startswith('/admin/invoice'):
            raise web.notfound()
    #
    return handle()


def proc_limit_user_content(handle):
    if not res['user_content']:
        path = web.ctx.fullpath.lower()
        if path.startswith('/go') or path.startswith('/admin/go') or path.startswith('/admin/redir'):
            raise web.notfound()
    #
    return handle()

def proc_limit_blog(handle):
    if not res['blog']:
        path = web.ctx.fullpath.lower()
        if path.startswith('/blog') or path.startswith('/admin/blog') or path.startswith('/admin/comment'):
            raise web.notfound()
    #
    return handle()


def proc_check_offline(handle):
    path = web.ctx.fullpath.lower()
    off = pget('offline')
    if off  and path != '/login' \
            and path != '/logout' \
            and path != '/contact' \
            and not path.startswith('/lang/set/') \
            and not path.startswith('/admin') \
            and not path.startswith('/captcha') \
            and not path.startswith('/fs/') \
            and not path.startswith('/passwd') \
            and not path.startswith('/profile') \
            and not path.startswith('/promote') \
            :
        t = tpl('offline')
        ttl = msgs['title_offline'].capitalize()
        o = t.offline(title(ttl), '')
        o = tplb(o)
        return o
    #
    return handle()
    

def proc_check_auth(handle):
    path = web.ctx.fullpath.lower()
    if path.startswith('/admin/'):
        if not sess.u:
            raise web.seeother('/login')
        #
        if not isadmin():
            raise web.internalerror()
    #
    if path == '/passwd' or path == '/admin' or path == '/profile' or path == '/promote':
        if not sess.u:
            raise web.seeother('/login')
    #
    return handle()


def proc_check_already_auth(handle):
    path = web.ctx.fullpath.lower()
    met = web.ctx.method
    if sess.u and path == '/login':
        if met.lower() == 'get':
            raise web.seeother('/admin')
        else:
            return 'error'
    #
    return handle()


def proc_detect_ua(handle):
    global mobile
    #
    if sess.browserclass == 'mobile':
        mobile = 'xhtmlmp'
    elif sess.browserclass == 'wap':
        mobile = 'wml'
    elif sess.browserclass == 'desktop':
        mobile = ''
    else:
        #detect
        ua = web.ctx.env.get('HTTP_USER_AGENT', '')
        mobile = detect_ua(ua)['mobile_document']
    #
    return handle()


def proc_calc_render_start(handle):
    rendertime[0] = time.time()
    return handle()


def proc_calc_render_finish(handle):
    rendertime[1] = time.time()
    return handle()


def proc_check_http_env(handle):
    ret = False
    #
    host = web.ctx.host.lower()
    method = web.ctx.method.lower()
    domain = DOMAIN.lower()
    ref = web.ctx.env.get('HTTP_REFERER', '')

    #get checked host
    if method == 'post' and ref:
        p = urlparse.urlparse(ref)
        phost = p[1].split(':')
        chost = phost[0]
    else:
        chost = host

    #from allowed domain
    if chost == domain:
        ret = True
    else:
        s = chost.split('.')
        ret = True #quick hack as of 13-October-2012
        #if len(s) == 3 and '.'.join(s[1:]) == domain and s[0] in ALLOWED_SUBDOMAIN:
        #   ret = True
    
    #
    if ret:
        return handle()
    #
    raise web.forbidden('access forbidden')


def proc_audit_post(handle):
    path = web.ctx.fullpath
    met = web.ctx.method.lower()
    if sess.log and met == 'post':
        q = 'select audit from tr_log where id=$logid'
        a = {'logid': sess.log}
        r = query(q, a)
        if r:
            audit = rget(r, 'audit', default=[], to_yaml=True)
            audit.append(
                    (now(), path)
                )
            r2 = db.update('tr_log', where='id=$logid', audit=yaml.dump(audit), vars={'logid': sess.log})
    return handle()
    

def proc_set_fullpath(handle):
    path0 = web.ctx.path
    path = web.ctx.fullpath
    menu = [ x[3] for x in menugen(True) ]
    if sess.has_key('fullpath') and path0 in menu:
        sess['fullpath'] = path
    #
    return handle()


def proc_set_res(handle):
    global res
    global FORCE_PROMOTE
    global PAYMENT_TYPE
    global DOMAIN
    global MAIL_DEFAULT
    #
    for _rk in res.keys():
        if _rk in res_fix: continue
        _rt = pget(_rk).lower()
        _rtv = ''
        if _rk == 'promote':
            _rtv = False
            if _rt == '1':
                _rtv = True
        elif _rk == 'payments':
            if _rt.find(',') > 0:
                try:
                    _rtv = [x for x in _rt.split(',')]
                    _rtv.remove('')
                    _rtv = [int(x) for x in _rtv]
                except:
                    _rtv = res['payments']        
        else:
            try:
                _rtv = int(_rt)
            except:
                pass
        #
        if type(_rtv) in [type(True), type(0), type([])]: res[_rk] = _rtv
    #
    FORCE_PROMOTE = res['promote']
    PAYMENT_TYPE = res['payments']
    DOMAIN = web.ctx.env.get('HTTP_HOST', '')
    MAIL_DEFAULT = '%s <%s>' %(DOMAIN, pget('mail_default'))
    #
    return handle()


wapp.add_processor(proc_db_check)
wapp.add_processor(proc_calc_render_start)
wapp.add_processor(proc_set_res)
wapp.add_processor(proc_detect_ua)
wapp.add_processor(proc_set_lang)
wapp.add_processor(proc_set_log)
wapp.add_processor(proc_check_http_env)
wapp.add_processor(proc_check_offline)
wapp.add_processor(proc_check_auth)
wapp.add_processor(proc_check_already_auth)
wapp.add_processor(proc_limit_cart)
wapp.add_processor(proc_limit_user_content)
wapp.add_processor(proc_limit_blog)
wapp.add_processor(proc_audit_post)
wapp.add_processor(proc_set_fullpath)
wapp.add_processor(proc_calc_render_finish)


application = wapp.wsgifunc()


################################# CLASS ################################


class index:
    def GET(self):
        target = HOME_DEFAULT
        menu = [ x[1] for x in menugen() ]
        #
        home = pget('homepage')
        if home:
            if ub(home) in menu:
                target = home
        #
        raise web.seeother(target)
    
    def POST(self):
        raise web.seeother('/')


class captcha:
    def GET(self):
        word = captcha_gen_word()
        #
        img = captcha_gen_image(word, bg=0xcccccc, fg=0x000000)
        f = cStringIO.StringIO()
        img.save(f, 'GIF')
        del img
        #
        f.seek(0)
        content = f.read()
        f.close()
        del f
        #
        sess.captcha = word
        #
        web.header('Content-type', 'image/gif')
        return content
    
    def POST(self):
        raise web.seeother('/')


class redir:
    def GET(self, url):
        q = 'select type, target from ms_redirect where url=$url order by id limit 1'
        a = {'url': url}
        r = query(q, a)
        if len(r) == 1 and r[0].target:
            if r[0].type == 'redirect':
                raise web.redirect(r[0].target)
            else:
                raise web.seeother(r[0].target)
        #
        raise web.notfound()
            
    def POST(self):
        raise web.seeother('/')


class product:
    def GET(self):
        t = tpl('product')
        ttl = msgs['title_product'].capitalize()
        o = t.product(title(ttl), ddata(['product', 'news']))
        o = tplb(o)
        return o
    
    def POST(self):
        raise web.seeother('/')


class promote:
    def GET(self):
        t = tpl('promote')
        ttl = msgs['title_promote'].capitalize()
        data = {'promote': dpromote()}
        o = t.promote(title(ttl), data)
        o = tplb(o)
        return o
    
    def POST(self):
        raise web.seeother('/')


class login:
    def GET(self):
        t = tpl('login')
        ttl = msgs['title_login'].capitalize()
        o = t.login(title(ttl), None)
        o = tplb(o)
        return o
    
    def POST(self):
        i = web.input(username='', password='', api=0)
        iusername = i.username.strip()
        ipassword = i.password.strip()
        if not iusername or not ipassword:
            return 'value'
        #
        ipassword_md5 = md5(ipassword).hexdigest()
        q = 'select id from ms_user where name=$username and password=$password and active=1'
        a = {'username': iusername, 'password': ipassword_md5}
        r = query(q, a)
        if len(r) == 1:
            try:
                sess.u = r[0].id
                return 'ok'
            except:
                return 'error'
        else:
            return 'failed'
        #
        return 'error'


class logout:
    def GET(self):
        sess.u = None
        raise web.seeother('/')            

    def POST(self):
        raise web.seeother('/')


class contact:
    def GET(self):
        t = tpl('contact')
        ttl = msgs['title_contact'].capitalize()
        data = dprofile(1)
        o = t.contact(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        i = web.input(name='', email='', msg='', captcha='', api=0)
        iname = i.name.strip()
        iemail = i.email.strip()
        imsg = i.msg.strip()
        #
        if not i.captcha == sess.captcha:
            return 'captcha'
        #
        if not iname or not iemail or not imsg:
            return 'value'
        #
        if not is_valid_email(iemail):
            return 'invalid_email'
        #
        content = ' %s: %s \r\n %s: %s \r\n %s: %s \r\n %s:  \r\n %s' %(
                msgs['header_contact_date'].capitalize(), now(), 
                msgs['header_contact_from'].capitalize(), iname, 
                msgs['header_contact_email'].capitalize(), iemail, 
                msgs['header_contact_message'].capitalize(), imsg
                )
        sendmail(MAIL_DEFAULT, msgs['header_contact_email_subject'].capitalize(), content, iemail)
        return 'ok'


class cart:
    def GET(self):
        t = tpl('cart')
        ttl = msgs['title_cart'].capitalize()
        o = t.cart(title(ttl), ddatac('cart'))
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class cart_add:
    def GET(self):
        raise web.seeother('/')
        
    def POST(self):
        i = web.input(vid='', amt='', api=0)
        try:
            ivid = int(i.vid)
            iamt = int(i.amt)
        except ValueError:
            return 'value,-1'
        except:
            return 'error,-1'
        #
        p = dpro_item(id=ivid)
        if not p:
            return 'value,-1'
        #
        if pget('cart_check_stock') == '1':
            stock = p[0].stock
            amt = 0
            #
            if sess.c.has_key(ivid):
                in_cart = sess.c[ivid]
            else:
                in_cart = 0
            #
            avail = stock - in_cart
            left = avail - iamt
            #
            if left > CART_ADD_MAX:
                left = CART_ADD_MAX
            #
            if avail < 1 or left < 0:
                return 'outofstock, -1'
            else:
                amt = iamt
        else:
            left = CART_ADD_MAX
            amt = iamt
        #
        if sess.c.has_key(ivid):
            sess.c[ivid] += amt
        else:
            sess.c[ivid] = amt
        #
        return 'ok,%s' %(left)


class cart_del:
    def GET(self):
        raise web.seeother('/')

    def POST(self):
        i = web.input(vid='', api=0)
        try:
            ivid = int(i.vid)
        except ValueError:
            return 'value'
        except:
            return 'error'
        #
        if not sess.c.has_key(ivid):
            return 'value'
        #
        sess.c.pop(ivid)
        return 'ok'


class cart_empty:
    def GET(self):
        raise web.seeother('/')
    
    def POST(self):
        i = web.input(api=0)
        try:
            sess.c = {}
        except:
            return 'error'
        #
        return 'ok'
        

class cart_checkout:
    def GET(self):
        if not sess.c:
            raise web.seeother('/cart')
        else:
            t = tpl('checkout')
            ttl = msgs['title_checkout'].capitalize()
            o = t.checkout(title(ttl), ddatac('cart'))
            o = tplb(o)
            return o

    def POST(self):
        raise web.seeother('/')


class cart_checkout_done:
    def GET(self):
        if not sess.co:
            raise web.seeother('/')
        else:
            codata = sess.co
            sess.co = {}
            t = tpl('checkout_done')
            ttl = msgs['title_checkout'].capitalize()
            o = t.checkout_done(title(ttl), codata)
            o = tplb(o)
            return o
    
    def POST(self):
        i = web.input(payment=0, cust_name='', cust_email='', ship_addr='', note='', captcha='', api=0)
        if not sess.c:
            return 'error'
        #
        try:
            payment = int(i.payment)
        except:
            return 'error'
        #
        if i.captcha != sess.captcha:
            return 'captcha'
        #
        cust_name = i.cust_name.strip()
        cust_email = i.cust_email.strip()
        ship_addr = i.ship_addr.strip()
        note = i.note.strip()
        if not payment > 0 or not cust_name or not cust_email or not ship_addr:
            return 'value'
        #
        if not is_valid_email(cust_email):
            return 'invalid_email'
        #
        invoice_id = invoicesave(payment, cust_name, cust_email, ship_addr, note)
        if invoice_id:
            return 'ok'
        #
        return 'error'


class payment_confirm:
    def GET(self):
        t = tpl('payment_confirm')
        ttl = msgs['title_payment_confirm'].capitalize()
        data = {}
        yy = int(time.strftime('%Y'))
        mm = int(time.strftime('%m'))
        dd = int(time.strftime('%d'))
        data['date_range'] = ( (range(1,32), dd), (range(1,13), mm), ((yy-1, yy, yy+1), yy))
        data['all_bank'] = dbank(complete_name=True)
        data['method'] = m.t(m.BANK_PAYMENT_METHOD, sess.lang)['method']
        data['message'] = smget()
        o = t.payment_confirm(title(ttl), data)
        o = tplb(o)
        return o
    
    def POST(self):
        i = web.input(api=0, invoice='', 
            date_day=0, date_month=0, date_year=0, name='', account='',
            total=0, bank='', method='', note='', captcha='')
        try:
            iday = int(i.date_day)    
            imonth = int(i.date_month)
            iyear = int(i.date_year)
            dt = datetime.date(iyear, imonth, iday)
        except:
            dt = None
        #
        invoice = i.invoice.strip()
        name = i.name.strip()
        account = i.account.strip()
        bank = i.bank.strip()
        method = i.method.strip()
        note = i.note.strip()
        try:
            total = nrfloat(i.total)
        except:
            total = 0
        #
        if not i.captcha == sess.captcha:
            sess.msg = ['error', msgs['msg_input_error_captcha']]
            raise web.seeother('/payment/confirm')                
        #
        if not invoice or not name or not total or not bank or not method:
            sess.msg = ['error', msgs['msg_payment_confirm_error_required']]
            raise web.seeother('/payment/confirm')                
        #
        if not dt:
            sess.msg = ['error', msgs['msg_payment_confirm_error_invalid_date']]
            raise web.seeother('/payment/confirm')
        #
        q = 'select cart_id, confirm_info from tr_invoice_header where cart_id=$cart_id and done <> 1'
        a = {'cart_id': invoice}
        r = query(q, a)
        cart_id = rget(r, 'cart_id')
        confirm = rget(r, 'confirm_info', default=[], to_yaml=True)
        if not cart_id:
            sess.msg = ['error', msgs['msg_payment_confirm_error_notfound']]
            raise web.seeother('/payment/confirm')
        #
        #ok
        confirm.append ({
                'date': dt,
                'name': name,
                'account': account,
                'bank': bank,
                'method': method,
                'total': total,
                'note': note,
            })
        confirm_info = yaml.dump(confirm)
        q = 'update tr_invoice_header set confirm_info=$confirm_info,log_id=$logid where cart_id=$cart_id'
        a = {'cart_id': invoice, 'confirm_info': confirm_info, 'logid': sess.log}
        r = query(q, a)
        #
        email_field = (
                        msgs['header_payment_confirm_date'].capitalize(), dt,
                        msgs['header_payment_confirm_invoice'].capitalize(), invoice,
                        msgs['header_payment_confirm_name'].capitalize(), name,
                        msgs['header_payment_confirm_bank'].capitalize(), bank,
                        msgs['header_payment_confirm_method'].capitalize(), method,
                        msgs['header_payment_confirm_account'].capitalize(), account,
                        msgs['header_payment_confirm_total'].capitalize(), total,
                        msgs['header_payment_confirm_note'].capitalize(), note,
                    )
        email_text = ' %s: %s \r\n %s: %s \r\n %s: %s \r\n %s: %s \r\n %s: %s \r\n %s: %s \r\n %s: %s \r\n %s: \r\n %s' %email_field
        #
        sendmail(MAIL_DEFAULT, msgs['header_payment_confirm_email_subject'].capitalize(), email_text)
        #
        sess.msg = ['ok', '']
        raise web.seeother('/payment/confirm')
        

class fs:
    def GET(self, id):
        f = dfs(id, content=True, format=False, name_add=False)
        if not f:
            raise web.notfound()
        #
        disposition = 'attachment; filename=' + f[0].name
        inline = ['flash', 'image']
        for i in inline:
            if i in f[0].type.lower():
                disposition = 'inline; filename=' + f[0].name
                break
        #
        if web.input(download='').download == '1':
            disposition = 'attachment; filename=' + f[0].name
        #
        web.header('Content-Type', f[0].type)
        web.header('Content-Length', f[0].size)
        web.header('Content-Disposition', disposition)
        return f[0].content

    def POST(self):
        raise web.seeother('/')


class lang_set:
    def GET(self, lang):
        testmsg = m.t(m.MSG, lang)
        if testmsg: 
            sess.lang = lang
        #
        path = '/'
        if sess.has_key('fullpath'):
            test = sess['fullpath']
            if test:
                path = sess['fullpath']
        #    
        raise web.seeother(path)

    def POST(self):
        raise web.seeother('/')


class browser_set:
    def GET(self, category):
        category = category.lower().strip()
        sess.browserclass = ''
        if category in ['mobile', 'wap', 'desktop']:
            sess.browserclass = category
        #
        raise web.seeother('/')

    def POST(self):
        raise web.seeother('/')


class news:
    def GET(self):
        i = web.input(id=0, api=0)
        t = tpl('news')
        ttl = msgs['title_news'].capitalize()
        cdata = {'news': dnews(read_session=False)}
        o = t.news(title(ttl), cdata)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class news_hide:
    def GET(self):
        raise web.seeother('/news')
        
    def POST(self):
        i = web.input(api=0)
        sess.newsread = True
        if sess.newsread:
            return 'ok'
        #
        return 'error'


class faq:
    def GET(self):
        t = tpl('faq')
        ttl = msgs['title_faq'].capitalize()
        data = {'faq': dfaq(group=True)}
        o = t.faq(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')

        
class go:
    def GET(self, id):
        if not id:
            raise web.notfound()
        #
        q = 'select page,content from ms_user_content where active=1 and id=$id'
        a = {'id': id}
        r = query(q, a)
        if not r:
            raise web.notfound()
        #
        uc = r[0]
        uc['page'] = mlget(uc['page'])
        uc['content'] = mlget(uc['content'])
        #
        t = tpl('go')
        ttl = uc['page'].capitalize()
        o = t.go(title(ttl), uc)
        o = tplb(o)
        return o
        
    def POST(self):
        raise web.seeother('/')
        
    
class admin:
    def GET(self):
        t = tpl('admin')
        ttl = msgs['title_admin'].capitalize()
        #
        data = {}
        data['menu'] = dadmin()
        #
        log_size_r = query('select count(id) as count from tr_log')
        log_size = rget(log_size_r, 'count', default=0)
        #
        if isadmin():
            data['version'] = VERSION
            data['database_size'] = nf(os.path.getsize(DATA_FILE))
            data['log_size'] = nf(log_size)
        else:
            data['version'] = ''
            data['database_size'] = ''
            data['log_size'] = ''
        #
        o = t.admin(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class passwd:
    def GET(self):
        t = tpl('passwd')
        ttl = msgs['title_passwd'].capitalize()
        o = t.passwd(title(ttl), '')
        o = tplb(o)
        return o
    
    def POST(self):
        i = web.input(old_password='', new_password_1='', new_password_2='', api=0)
        #
        if not i.new_password_1 or not i.new_password_2:
            return 'value'
        #
        if i.new_password_1 != i.new_password_2:
            return 'mismatch'
        #
        oldpassword_md5 = md5(i.old_password).hexdigest()
        q = 'select id from ms_user where id=$uid and password=$password and active=1'
        a = {'uid': sess.u, 'password': oldpassword_md5}
        r = query(q, a)
        if len(r) != 1:
            return 'auth'
        #
        newpassword_md5 = md5(i.new_password_1).hexdigest()
        if oldpassword_md5 == newpassword_md5:
            return 'same'
        #
        a = {'uid': sess.u, 'newpassword': newpassword_md5}
        r = db.update('ms_user', where='id=$uid', password=newpassword_md5, log_id=sess.log, vars=a)
        if r:
            return 'ok'
        #
        return 'error'


class profile:
    def GET(self):
        t = tpl('profile')
        ttl = msgs['title_profile'].capitalize()
        data = {}
        data['profile'] = dprofile(id=sess.u)
        data['message'] = smget()
        o = t.profile(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        i = web.input(first_name='', last_name='', email='', phone='', fax='', web='', address='')
        fn = i.first_name.strip()
        ln = i.last_name.strip()
        em = yaml.dump(sepnorm(i.email, as_string=False))
        ph = yaml.dump(sepnorm(i.phone, as_string=False))
        fx = yaml.dump(sepnorm(i.fax, as_string=False))
        ww = yaml.dump(sepnorm(i.web, as_string=False))
        ad = i.address.strip()
        r = db.update('ms_user', where='id=$id', first_name=fn, last_name=ln, email=em, 
            phone=ph, fax=fx, web=ww, address=ad, log_id=sess.log, vars={'id': sess.u})
        if r:
            sess.msg = ['ok', msgs['msg_profile_updated']]
        raise web.seeother('/profile')
        
        
class admin_fs:
    def GET(self):
        max = res['max_file_size']/1024
        data = {'files': dfs(), 'max_file_size_kb': nf(max), 'error_message': smget()}
        t = tpl('admin_fs')
        ttl = msgs['title_fs'].capitalize()
        o = t.admin_fs(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_fs_del:
    def GET(self):
        raise web.seeother('/admin/fs')
    
    def POST(self):
        i = web.input(id=0, api=0)
        try:
            iid = int(i.id)
        except:
            return 'error'
        #
        r = db.select('ms_file', what='name', where='id=$id', vars={'id':iid})
        if not r:
            return 'error'
        #
        r = db.delete('ms_file', where='id=$id', vars={'id':iid})
        if r:
            return 'ok'
        #
        return 'error'

        
class admin_fs_upload:
    def GET(self):
        raise web.seeother('/admin/fs')
    
    def POST(self):
        i = web.input(userfile={}, api=0)
        iname = i.userfile.filename
        #
        if not iname.strip():
            raise web.seeother('/admin/fs')
        #
        name_add = ''
        q = 'select  max(abs(cast(name_add as integer)))+1 as max from ms_file where name=$name'
        a = {'name':iname}
        r_check = query(q, a)
        if r_check and r_check[0].max > 0:
            name_add= str(r_check[0].max)
        #
        icontent = i.userfile.value
        size = len(icontent)
        if size > res['max_file_size']:
            size = nf(size/1024)
            sess.msg = ['ok', '%s (%s: %s KB)' %(msgs['msg_fs_error_upload_file_too_big'], iname, size)]
            raise web.seeother('/admin/fs')
        #
        itype = i.userfile.type
        itype_opt = yaml.dump(i.userfile.type_options)
        idisposition = i.userfile.disposition
        idisposition_opt = yaml.dump(i.userfile.disposition_options)
        date_file = now()
        #
        headers = {}
        for j in i.userfile.headers.keys():
            headers[j] = i.userfile.headers[j]
        iheaders = yaml.dump(headers)
        #
        r = db.insert('ms_file', log_id=sess.log, name=iname, name_add=name_add, size=size, type=itype, 
            type_options=itype_opt, disposition=idisposition, 
            disposition_options=idisposition_opt, content=sqlite3.Binary(icontent), date_file=date_file,
            headers=iheaders)
        if r:
            raise web.seeother('/admin/fs')
        #
        return 'error'


class admin_fs_view:
    def GET(self, id):
        f = dfs(id)
        if not f:
            raise web.seeother('/admin/fs')
        #
        t = tpl('admin_fs_view')
        ttl = msgs['title_fs_view'].capitalize()
        o = t.admin_fs_view(title(ttl), f[0])
        o = tplb(o)
        return o
        

    def POST(self):
        raise web.seeother('/')


class admin_system:
    def GET(self):
        t = tpl('admin_system')
        ttl = msgs['title_system'].capitalize()
        #
        data = {}
        data['site_description'] = ypget('site_description')
        data['extra_info'] = ypget('extra_info')
        data['cart'] = res['cart']
        data['use_cart'] = ucart()
        data['cart_check_stock'] = pget('cart_check_stock')
        data['invoice_extra_info'] = ypget('invoice_extra_info')
        data['offline'] = pget('offline')
        data['currency'] = pget('currency', callback=dcur)
        data['all_currency'] = dcur()
        data['template'] = pget('template')
        data['all_template'] = atpl()
        data['logo_file'] = int(pget('logo_file', default=0))
        data['all_files'] = dfs(filter=['image','flash'])
        data['keywords'] = pget('site_keywords', default='')
        data['news_max'] = pget('news_max')
        data['message'] = smget() 
        data['expose_time'] = pget('expose_time')
        data['promote'] = pget('promote')
        data['max_product_category'] = pget('max_product_category')
        data['max_product'] = pget('max_product')
        data['max_file_size'] = pget('max_file_size')
        data['max_files'] = pget('max_files')
        data['mail_smtp'] = pget('mail_smtp')
        data['mail_user'] = pget('mail_user')
        data['mail_pass'] = pget('mail_pass')
        data['mail_default'] = pget('mail_default')
        data['homepage'] = pget('homepage')
        data['font_dir'] = pget('font_dir')
        data['payments'] = pget('payments')
        data['lang'] = pget('lang')
        #
        o = t.admin_system(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        i = web.input(api=0,
                site_desc='',
                extra_info='',
                use_cart='',
                cart_check_stock='',
                invoice_extra_info='',
                site_offline='',
                currency='',
                template=TEMPLATE_DEFAULT,
                logo_file='',
                keywords='',
                news_max='',
                expose_time='',
                promote='',
                payments='',
                max_product_category='',
                max_product='',
                max_file_size='',
                max_files='',
                mail_smtp='',
                mail_user='',
                mail_pass='',
                mail_default='',
                homepage='',
                font_dir='',
                lang='',
            )
        #
        site_desc = mlset(i, 'site_desc')
        extra_info = mlset(i, 'extra_info')
        use_cart = i.use_cart
        cart_check_stock = i.cart_check_stock
        invoice_extra_info = mlset(i, 'invoice_extra_info')
        site_offline = i.site_offline
        currency = i.currency
        template = i.template
        logo_file = i.logo_file
        keywords = i.keywords
        news_max = i.news_max
        expose_time= i.expose_time
        promote= i.promote
        payments= i.payments
        max_product_category= i.max_product_category
        max_product= i.max_product
        max_file_size= i.max_file_size
        max_files= i.max_files
        mail_smtp= i.mail_smtp
        mail_user= i.mail_user
        mail_pass= i.mail_pass
        mail_default= i.mail_default
        homepage= i.homepage
        font_dir= i.font_dir
        lang = i.lang
        #
        tpinfo = tinfo(template)
        if not tpinfo:
            template = TEMPLATE_DEFAULT
        else:
            try:
                owner = tpinfo['general']['owner']
            except:
                owner = ''
            if owner and DOMAIN.lower() not in owner:
                template = TEMPLATE_DEFAULT
        #
        config = {
            'site_description'  : site_desc,
            'extra_info'        : extra_info,
            'use_cart'          : use_cart,
            'invoice_extra_info': invoice_extra_info,
            'offline'           : site_offline,
            'currency'          : currency,
            'template'          : template,
            'cart_check_stock'  : cart_check_stock,
            'logo_file'         : logo_file,
            'site_keywords'     : keywords,
            'news_max'          : news_max,
            'expose_time'  : expose_time,
            'promote'  : promote,
            'payments'  : payments,
            'max_product_category'  : max_product_category,
            'max_product'  : max_product,
            'max_file_size'  : max_file_size,
            'max_files'  : max_files,
            'mail_smtp'  : mail_smtp,
            'mail_user'  : mail_user,
            'mail_pass'  : mail_pass,
            'mail_default'  : mail_default,
            'homepage'  : homepage,
            'font_dir'  : font_dir,
            'lang'      : lang,
        }
        for i in config.keys():
            r = db.update('ms_config', value=config[i], where='param=$param', log_id=sess.log, vars={'param': i})
        #
        sess.msg = ['ok', msgs['msg_sys_saved']]
        raise web.seeother('/admin/system')


class admin_product:
    def GET(self):
        t = tpl('admin_product')
        ttl = msgs['title_admin_product'].capitalize()
        data = dadmin(section=['admin.product'])
        o = t.admin_product(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_product_category:
    def GET(self):
        t = tpl('admin_product_category')
        ttl = msgs['title_admin_product_category'].capitalize()
        data = {}
        data['category'] = dpro_category()
        data['message'] = smget()
        o = t.admin_product_category(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_product_category_del:
    def GET(self):
        raise web.seeother('/admin/product/category')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        cat = dpro_category(iid)
        if not cat:
            return 'error'
        #
        q = 'update ms_category set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        return 'ok'        


class admin_product_category_save: 
    def GET(self):
        raise web.seeother('/admin/product/category')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        if i.type == 'edit':        
            allid = [c.id for c in dpro_category(field='id')]
        elif i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            try:
                ipriority = int(  siget(i, 'priority', str(a))  )
            except:
                ipriority = 0        
            #
            m = mlset(i, str(a))
            #
            if disblank(m, True):
                sess.msg = ['error', msgs['msg_product_category_error_required']]
                raise web.seeother('/admin/product/category')
            else:
                if i.type == 'edit':
                    q = 'update ms_category set name=$name, active=1, priority=$priority, log_id=$logid where id=$id'
                    a = {'id': a, 'name': m, 'priority': ipriority, 'logid': sess.log}
                    r = query(q, a)
                    sess.msg = ['ok', msgs['msg_product_category_saved']]
                elif i.type == 'add':
                    cat = dpro_category()
                    if len(cat) >= res['max_product_category']:
                        sess.msg = ['error', msgs['msg_product_category_error_max']]
                        raise web.seeother('/admin/product/category')
                    #
                    q = 'insert into ms_category (name,active, priority,log_id) values($name, 1, $priority, $logid)'
                    a = {'name': m, 'priority': ipriority, 'logid': sess.log}
                    r = query(q, a)
                    sess.msg = ['ok', msgs['msg_product_category_added']]
        #
        raise web.seeother('/admin/product/category')

            
class admin_product_group:
    def GET(self):
        t = tpl('admin_product_group')
        ttl = msgs['title_admin_product_group'].capitalize()
        data = {}
        data['category'] = dpro_category(field='id,name')
        data['group'] = dpro_group()
        data['message'] = smget()
        data['files'] = dfs(filter=['image','flash'])
        o = t.admin_product_group(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_product_group_del:
    def GET(self):
        raise web.seeother('/admin/product/group')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        grp = dpro_group(id=iid)
        if not grp:
            return 'error'
        #
        q = 'update ms_product set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        return 'ok'        


class admin_product_group_save:
    def GET(self):
        raise web.seeother('/admin/product/group')
        
    def POST(self):
        i = web.input(api=0, type='add', id=0, file_id=0)
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        try:
            iid = int(i.id)
            icategory_id = int(i.category_id)
            ifile_id = int(i.file_id)
        except:
            sess.msg = ['error', msgs['msg_product_group_error_required']]
            raise web.seeother('/admin/product/group')
        #
        cat = [x.id for x in dpro_category(field='id')]
        files = [x.id for x in dfs(filter=['image','flash'])]
        if (not icategory_id in cat) or (not ifile_id in files and ifile_id != 0): #illegal
            raise web.internalerror()
        #
        try:
            ipriority = int(i.priority)
        except:
            ipriority = 0
        iname = mlset(i, 'name')
        idesc = mlset(i, 'description')
        ifull = mlset(i, 'fullinfo')
        #
        if disblank(iname, True):
            sess.msg = ['error', msgs['msg_product_group_error_required']]
        else:
            if i.type == 'add':
                grp = dpro_group()
                if len(grp) >= res['max_product']:
                    sess.msg = ['error', msgs['msg_product_group_error_max']]
                    raise web.seeother('/admin/product/group')
                #
                r = db.insert('ms_product', category_id=icategory_id, active=1, file_id=ifile_id,
                    name=iname, description=idesc, full_info=ifull, priority=ipriority, log_id=sess.log)
                if r:
                    sess.msg = ['ok', msgs['msg_product_group_added']]
            elif i.type == 'edit':
                r = db.update('ms_product', category_id=icategory_id, active=1, file_id=ifile_id,
                    name=iname, description=idesc, full_info=ifull, priority=ipriority, log_id=sess.log, where='id=$id', 
                    vars={'id': iid})
                if r:
                    sess.msg = ['ok', msgs['msg_product_group_saved']]
                
        #
        if i.type == 'edit':
            raise web.seeother('/admin/product/group/edit/%s' %(iid))
        else:
            raise web.seeother('/admin/product/group')


class admin_product_group_edit:
    def GET(self, id):
        t = tpl('admin_product_group_edit')
        ttl = msgs['title_admin_product_group'].capitalize()
        data = {}
        data['category'] = dpro_category(field='id,name')
        data['group'] = dpro_group()
        data['detail'] = dpro_group(id=id) 
        data['message'] = smget()
        data['files'] = dfs(filter=['image','flash'])
        o = t.admin_product_group_edit(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        #handled by admin_product_group_save
        raise web.seeother('/')        


class admin_product_item:
    def GET(self):
        t = tpl('admin_product_item')
        ttl = msgs['title_admin_product_item'].capitalize()
        data = {}
        data['group'] = dpro_group(field='id,name')
        data['message'] = smget()
        data['item'] = dpro_item()
        data['cart_check_stock'] = pget('cart_check_stock')
        data['files'] = dfs()
        o = t.admin_product_item(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_product_item_del:
    def GET(self):
        raise web.seeother('/admin/product/item')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        items = dpro_item(id=iid)
        if not items:
            return 'error'
        #
        q = 'update ms_product_variant set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        return 'ok'        


class admin_product_item_save: 
    def GET(self):
        raise web.seeother('/admin/product/item')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        if i.type == 'edit':
            allid = [c.id for c in dpro_item(field='id')]
        elif i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            try:
                ivfid = int(  siget(i, 'vfile_id', str(a))  )
            except:
                ivfid = 0  
            files = [x.id for x in dfs()]
            if not ivfid in files: ivfid = 0
            #
            try:
                ipid = int(  siget(i, 'product_id', str(a))  )
            except:
                ipid = 0        
            #
            try:
                istock = int(  siget(i, 'stock', str(a))  )
            except:
                istock = 0        
            #
            try:
                iprice = nrfloat(  siget(i, 'price', str(a))  )
            except:
                iprice = 0        
            #
            try:
                itaxratio = nrfloat(  siget(i, 'taxratio', str(a))  )
                itaxratio = nlimit(itaxratio, decimal.Decimal('0.0'), decimal.Decimal('1.0'))
            except:
                itaxratio = 0        
            #
            m = mlset(i, str(a))
            #
            if disblank(m, True) or ipid == 0:
                sess.msg = ['error', msgs['msg_product_item_error_required']]
                raise web.seeother('/admin/product/item')
            else:
                if i.type == 'edit':
                    q = 'update ms_product_variant set name=$name, active=1, product_id=$ipid, stock=$istock, price=$iprice, taxratio=$itaxratio, variant_file_id=$variant_file_id, log_id=$logid where id=$id'
                    a = {'id': a, 'name': m, 'ipid': ipid, 'istock': istock, 'iprice': float(iprice), 'itaxratio': float(itaxratio), 'variant_file_id': ivfid, 'logid': sess.log}
                    r = query(q, a)
                    sess.msg = ['ok', msgs['msg_product_item_saved']]
                elif i.type == 'add':
                    r = db.insert('ms_product_variant', active=1, product_id=ipid, stock=istock, price=float(iprice), 
                    taxratio=float(itaxratio), name=m, variant_file_id=ivfid, log_id=sess.log)
                    if r:
                        sess.msg = ['ok', msgs['msg_product_item_added']]
        #
        raise web.seeother('/admin/product/item')


class admin_bank:
    def GET(self):
        t = tpl('admin_bank')
        ttl = msgs['title_admin_bank'].capitalize()
        data = {}
        data['all_currency'] = dcur()
        data['message'] = smget()
        data['bank'] = dbank()
        o = t.admin_bank(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_bank_del:
    def GET(self):
        raise web.seeother('/admin/bank')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        bank = dbank(id=iid)
        if not bank:
            return 'error'
        #
        q = 'update ms_bank set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        #
        return 'ok'        


class admin_bank_save: 
    def GET(self):
        raise web.seeother('/admin/bank')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        if i.type == 'edit':
            allid = [c.id for c in dbank(field='id')]
        elif i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            try:
                icur = int(  siget(i, 'currency_id', str(a))  )
            except:
                icur = 0        
            #
            name = siget(i, 'name', str(a))
            holder = siget(i, 'holder', str(a))
            account = siget(i, 'account', str(a))
            branch = siget(i, 'branch', str(a))
            address = siget(i, 'address', str(a))
            country = siget(i, 'country', str(a))
            swift = siget(i, 'swift', str(a))
            #
            if not name or not holder or not account:
                sess.msg = ['error', msgs['msg_bank_error_required']]
                raise web.seeother('/admin/bank')
            else:
                if i.type == 'edit':
                    q = 'update ms_bank set name=$name, active=1, holder=$holder, account=$account, branch=$branch, address=$address, country=$country, swift=$swift, currency_id=$icur, log_id=$logid where id=$id'
                    a = {'id': a, 'name': name, 'icur': icur, 'holder':holder, 'account':account, 'branch':branch, 'address':address, 'country':country, 'swift':swift, 'logid': sess.log}
                    r = query(q, a)
                    sess.msg = ['ok', msgs['msg_bank_saved']]
                elif i.type == 'add':
                    r = db.insert('ms_bank', name=name, active=1, holder=holder, account=account, branch=branch, address=address, country=country, swift=swift, currency_id=icur, log_id=sess.log)
                    if r:
                        sess.msg = ['ok', msgs['msg_bank_added']]
        #
        raise web.seeother('/admin/bank')


class admin_paypal:
    def GET(self):
        t = tpl('admin_paypal')
        ttl = msgs['title_admin_paypal'].capitalize()
        data = {}
        data['paypal'] = dpaypal()
        data['message'] = smget()
        o = t.admin_paypal(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_paypal_del:
    def GET(self):
        raise web.seeother('/admin/paypal')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        paypal = dpaypal(iid)
        if not paypal:
            return 'error'
        #
        q = 'update ms_paypal set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        return 'ok'        


class admin_paypal_save: 
    def GET(self):
        raise web.seeother('/admin/paypal')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add']:
            raise web.internalerror()
        #
        allid = []
        if i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            account = siget(i, 'account', str(a)).lower()
            if not account:
                sess.msg = ['error', msgs['msg_paypal_error_required']]
                raise web.seeother('/admin/paypal')
            else:
                if i.type == 'add':
                    paypal = [x.account.lower() for x in dpaypal()]
                    if account in paypal:
                        sess.msg = ['error', msgs['msg_paypal_error_exists']]
                        raise web.seeother('/admin/paypal')
                    else:
                        r = db.insert('ms_paypal', active=1, account=account, log_id=sess.log)
                        if r:
                            sess.msg = ['ok', msgs['msg_paypal_added']]
        #
        raise web.seeother('/admin/paypal')


class admin_yahoo:
    def GET(self):
        t = tpl('admin_yahoo')
        ttl = msgs['title_admin_yahoo'].capitalize()
        data = {}
        data['yahoo'] = dyahoo()
        data['message'] = smget()
        o = t.admin_yahoo(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_yahoo_del:
    def GET(self):
        raise web.seeother('/admin/yahoo')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        yahoo = dyahoo(iid)
        if not yahoo:
            return 'error'
        #
        q = 'delete from ms_yahoo where id=$id'
        a = {'id': iid}
        r = query(q, a)
        return 'ok'        


class admin_yahoo_save: 
    def GET(self):
        raise web.seeother('/admin/yahoo')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add']:
            raise web.internalerror()
        #
        allid = []
        if i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            account = siget(i, 'account', str(a)).lower()
            if not account:
                sess.msg = ['error', msgs['msg_yahoo_error_required']]
                raise web.seeother('/admin/yahoo')
            else:
                if i.type == 'add':
                    yahoo = [x.account[0].lower() for x in dyahoo()]
                    if account in yahoo:
                        sess.msg = ['error', msgs['msg_yahoo_error_exists']]
                        raise web.seeother('/admin/yahoo')
                    else:
                        r = db.insert('ms_yahoo', account=account, log_id=sess.log)
                        if r:
                            sess.msg = ['ok', msgs['msg_yahoo_added']]
        #
        raise web.seeother('/admin/yahoo')


class admin_link:
    def GET(self):
        t = tpl('admin_link')
        ttl = msgs['title_admin_link'].capitalize()
        data = {}
        data['link'] = dlink()
        data['message'] = smget()
        o = t.admin_link(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_link_del:
    def GET(self):
        raise web.seeother('/admin/link')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        link = dlink(iid)
        if not link:
            return 'error'
        #
        q = 'delete from ms_link where id=$id'
        a = {'id': iid}
        r = query(q, a)
        return 'ok'        


class admin_link_save: 
    def GET(self):
        raise web.seeother('/admin/link')
        
    def POST(self):
        i = web.input(api=0, id=0, type='add')
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        allid = []
        if i.type == 'add':
            allid = ['new']
        elif i.type == 'edit':
            allid = [x.id for x in dlink(field='id')]
        #
        for a in allid:
            try:
                iid = int ( siget(i, 'id', str(a)) )
            except:
                iid = 0
            code = siget(i, 'code', str(a)).lower()
            if not code:
                sess.msg = ['error', msgs['msg_link_error_required']]
                raise web.seeother('/admin/link')
            else:
                if i.type == 'add':
                    r = db.insert('ms_link', code=code, log_id=sess.log)
                    if r:
                        sess.msg = ['ok', msgs['msg_link_added']]
                elif i.type == 'edit':
                    r = db.update('ms_link', code=code, log_id=sess.log, where='id=$id', vars={'id': iid})
                    if r:
                        sess.msg = ['ok', msgs['msg_link_updated']]
        #
        raise web.seeother('/admin/link')


class admin_news:
    def GET(self):
        t = tpl('admin_news')
        ttl = msgs['title_admin_news'].capitalize()
        data = {}
        data['news'] = dnews(read_session=False)
        data['message'] = smget()
        data['files'] = dfs(filter=['image','flash'])
        o = t.admin_news(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_news_del:
    def GET(self):
        raise web.seeother('/admin/news')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        news = dnews(id=iid, read_session=False)
        if not news:
            return 'error'
        #
        q = 'delete from tr_news where id=$id'
        a = {'id': iid}
        r = query(q, a)
        return 'ok'        


class admin_news_save:
    def GET(self):
        raise web.seeother('/admin/news')
        
    def POST(self):
        i = web.input(api=0, type='add', id=0, file_id=0)
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        try:
            iid = int(i.id)
            ifile_id = int(i.file_id)
        except:
            sess.msg = ['error', msgs['msg_news_error_required']]
            raise web.seeother('/admin/news')
        #
        files = [x.id for x in dfs(filter=['image','flash'])]
        if (not ifile_id in files and ifile_id != 0): #illegal
            raise web.internalerror()
        #
        ititle = mlset(i, 'title')
        idesc = mlset(i, 'description')
        inews = mlset(i, 'news')
        #
        if not i.has_key('date'):
            date = now()
        else:
            date = i.date()
        #
        if disblank(ititle, True):
            sess.msg = ['error', msgs['msg_news_error_required']]
        else:
            if i.type == 'add':
                r = db.insert('tr_news', date_news=date, title=ititle, description=idesc, news=inews, file_id=ifile_id, log_id=sess.log)
                if r:
                    sess.msg = ['ok', msgs['msg_news_added']]
            elif i.type == 'edit':
                r = db.update('tr_news', title=ititle, description=idesc, news=inews, file_id=ifile_id, log_id=sess.log, 
                    where='id=$id', vars={'id': iid})
                if r:
                    sess.msg = ['ok', msgs['msg_news_saved']]
                
        #
        if i.type == 'edit':
            raise web.seeother('/admin/news/edit/%s' %(iid))
        else:
            raise web.seeother('/admin/news')


class admin_news_edit:
    def GET(self, id):
        t = tpl('admin_news_edit')
        ttl = msgs['title_admin_news'].capitalize()
        data = {}
        data['detail'] = dnews(id=id, read_session=False) 
        data['message'] = smget()
        data['files'] = dfs(filter=['image','flash'])
        o = t.admin_news_edit(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        #handled by admin_news_save
        raise web.seeother('/')        


class admin_faq:
    def GET(self):
        t = tpl('admin_faq')
        ttl = msgs['title_admin_faq'].capitalize()
        data = {}
        data['faq'] = dfaq()
        data['message'] = smget()
        data['files'] = dfs()
        o = t.admin_faq(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_faq_del:
    def GET(self):
        raise web.seeother('/admin/faq')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        faq = dfaq(id=iid)
        if not faq:
            return 'error'
        #
        q = 'delete from tr_faq where id=$id'
        a = {'id': iid}
        r = query(q, a)
        return 'ok'        


class admin_faq_save:
    def GET(self):
        raise web.seeother('/admin/faq')
        
    def POST(self):
        i = web.input(api=0, type='add', id=0, file_id=0)
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        try:
            iid = int(i.id)
            ifile_id = int(i.file_id)
        except:
            sess.msg = ['error', msgs['msg_faq_error_required']]
            raise web.seeother('/admin/faq')
        #
        files = [x.id for x in dfs()]
        if (not ifile_id in files and ifile_id != 0): #illegal
            raise web.internalerror()
        #
        icat = mlset(i, 'category')
        iq = mlset(i, 'question')
        ia = mlset(i, 'answer')
        #
        if disblank(icat, True) or disblank(iq, True) or disblank(ia, True):
            sess.msg = ['error', msgs['msg_faq_error_required']]
        else:
            if i.type == 'add':
                r = db.insert('tr_faq', category=icat, question=iq, answer=ia, file_id=ifile_id, log_id=sess.log)
                if r:
                    sess.msg = ['ok', msgs['msg_faq_added']]
            elif i.type == 'edit':
                r = db.update('tr_faq', category=icat, question=iq, answer=ia, file_id=ifile_id, log_id=sess.log, 
                    where='id=$id', vars={'id': iid})
                if r:
                    sess.msg = ['ok', msgs['msg_faq_saved']]
                
        #
        if i.type == 'edit':
            raise web.seeother('/admin/faq/edit/%s' %(iid))
        else:
            raise web.seeother('/admin/faq')


class admin_faq_edit:
    def GET(self, id):
        t = tpl('admin_faq_edit')
        ttl = msgs['title_admin_faq'].capitalize()
        data = {}
        data['detail'] = dfaq(id=id) 
        data['message'] = smget()
        data['files'] = dfs()
        o = t.admin_faq_edit(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        #handled by admin_faq_save
        raise web.seeother('/')        


class admin_invoice:
    def GET(self):
        t = tpl('admin_invoice')
        ttl = msgs['title_admin_invoice'].capitalize()
        data = {}
        data['date_from'] = ''
        data['date_to'] = ''
        data['closed'] = '0'
        data['invoice'] = None
        data['message'] = smget()
        o = t.admin_invoice(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        i = web.input(date_from='', date_to='', closed='0')
        try:
            iclosed = int(i.closed)
        except:
            iclosed = 0
        #
        t = tpl('admin_invoice')
        ttl = msgs['title_admin_invoice'].capitalize()
        data = {}
        data['date_from'] = i.date_from
        data['date_to'] = i.date_to
        data['closed'] = i.closed
        data['invoice'] = dinvoice(date_from=i.date_from, date_to=i.date_to, closed=iclosed)
        if not data['invoice']:
            sess.msg = ['ok', msgs['msg_invoice_empty']]
        data['message'] = smget()
        o = t.admin_invoice(title(ttl), data)
        o = tplb(o)
        return o


class admin_invoice_view:
    def GET(self, id):
        t = tpl('admin_invoice_view')
        ttl = msgs['title_admin_invoice_view'].capitalize()
        data = {}
        data['invoice'] = dinvoice(id)
        if not data['invoice']:
            raise web.internalerror()
        #
        data['message'] = smget()
        o = t.admin_invoice_view(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_invoice_approval:
    def GET(self, id):
        raise web.seeother('/')

    def POST(self):
        i = web.input(type='', id=0, api=0)
        if not i.type in ['approve', 'disapprove']:
            return 'error'
        #
        try:
            iid = int(i.id)
        except:
            return 'error'
        #
        inv = dinvoice(id=iid, all_confirm=True)
        confirm = rget(inv, 'confirm_info', default=[], to_yaml=True)
        if i.type == 'approve':
            try:
                if confirm and confirm[-1]['date']:
                    r = db.update('tr_invoice_header', log_id=sess.log, where='id=$id', done=True,
                        date_paid=confirm[-1]['date'], vars={'id':iid})
                    if r:
                        return 'ok'
            except:
                return 'error'
        elif i.type == 'disapprove':
            if not inv[0].done:
                confirm.append('')
                r = db.update('tr_invoice_header', log_id=sess.log, where='id=$id', confirm_info=yaml.dump(confirm),
                    vars={'id':iid})
                if r:
                    return 'ok'
        #
        return 'error'


class admin_stat:
    def GET(self):
        t = tpl('admin_stat')
        ttl = msgs['title_admin_stat'].capitalize()
        data = {}
        data['date_from'] = ''
        data['date_to'] = ''
        data['stat'] = None
        data['message'] = smget()
        o = t.admin_stat(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        i = web.input(date_from='', date_to='')
        t = tpl('admin_stat')
        ttl = msgs['title_admin_stat'].capitalize()
        data = {}
        data['date_from'] = i.date_from
        data['date_to'] = i.date_to
        data['stat'] = dstat(date_from=i.date_from, date_to=i.date_to)
        if not data['stat']:
            sess.msg = ['ok', msgs['msg_stat_empty']]
        data['message'] = smget()
        o = t.admin_stat(title(ttl), data)
        o = tplb(o)
        return o


class admin_doc:
    def GET(self):
        f = DOC_ADMIN
        if not f or not os.path.exists(f):
            raise web.seeother('/admin')
        else:
            disposition = 'attachment; filename=' + os.path.basename(f)
            web.header('Content-Type', 'text/plain')
            web.header('Content-Length', os.path.getsize(f))
            web.header('Content-Disposition', disposition)
            return open(f).read()

    def POST(self):
        raise web.seeother('/')


class admin_redir:
    def GET(self):
        t = tpl('admin_redir')
        ttl = msgs['title_admin_redir'].capitalize()
        data = {}
        data['redir'] = dredir()
        data['message'] = smget()
        o = t.admin_redir(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_redir_del:
    def GET(self):
        raise web.seeother('/admin/redir')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        redirs = dredir(id=iid)
        if not redirs:
            return 'error'
        #
        q = 'delete from ms_redirect where id=$id'
        a = {'id': iid}
        r = query(q, a)
        return 'ok'        


class admin_redir_save: 
    def GET(self):
        raise web.seeother('/admin/redir')
        
    def POST(self):
        i = web.input(api=0, type='add')
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        if i.type == 'edit':
            allid = [c.id for c in dredir(field='id')]
        elif i.type == 'add':
            allid = ['new']
        #
        for a in allid:
            iurl = siget(i, 'url', str(a)).lower() 
            iurl = iurl.lstrip('/')
            iurl = iurl.strip()
            itarget = siget(i, 'target', str(a)).lower()
            itarget = itarget.strip()
            #
            if not iurl or not itarget:
                sess.msg = ['error', msgs['msg_admin_redir_error_required']]
                raise web.seeother('/admin/redir')
            else:
                check = [x.url for x in dredir() if x.id != a]
                if iurl in check:
                    sess.msg = ['error', '%s: %s' %(msgs['msg_admin_redir_error_exists'], iurl)]
                    raise web.seeother('/admin/redir')
                #
                used = []
                for u in range(len(URLS)):
                    if u % 2 == 0:
                        u2 = URLS[u].split('/')
                        used.append(u2[1])
                iurl2 = iurl.split('/')
                try:
                    iurl_sys = iurl2[0]
                except:
                    iurl_sys = iurl
                if iurl_sys in used:
                    sess.msg = ['error', '%s: %s' %(msgs['msg_admin_redir_error_used_system'], iurl)]
                    raise web.seeother('/admin/redir')
                #
                parsed = urlparse.urlparse(itarget)
                parsed_dom_split = parsed[1].split('.')
                raw_dom_len = len(DOMAIN.split('.'))
                if len(parsed_dom_split) > raw_dom_len:
                    parsed_dom_start = len(parsed_dom_split) - raw_dom_len
                else:
                    parsed_dom_start = 0
                parsed_dom = '.'.join(parsed_dom_split[parsed_dom_start:])
                if itarget == iurl or (parsed_dom == DOMAIN and parsed[2] == ub('/' + iurl)):
                    sess.msg = ['error', '%s: %s' %(msgs['msg_admin_redir_error_same'], iurl)]
                    raise web.seeother('/admin/redir')                    
                #
                if i.type == 'edit':
                    q = 'update ms_redirect set url=$url, target=$target, log_id=$logid where id=$id'
                    a = {'id': a,  'logid': sess.log, 'url': iurl, 'target': itarget}
                    r = query(q, a)
                    sess.msg = ['ok', msgs['msg_admin_redir_saved']]
                elif i.type == 'add':
                    r = db.insert('ms_redirect', log_id=sess.log, url=iurl, target=itarget)
                    if r:
                        sess.msg = ['ok', msgs['msg_admin_redir_added']]
        #
        raise web.seeother('/admin/redir')


class admin_go:
    def GET(self):
        t = tpl('admin_go')
        ttl = msgs['title_admin_go'].capitalize()
        data = {}
        data['go'] = dgo()
        data['message'] = smget()
        o = t.admin_go(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        raise web.seeother('/')


class admin_go_del:
    def GET(self):
        raise web.seeother('/admin/go')
        
    def POST(self):
        i = web.input(api=0, id=0)
        try:
            iid = i.id
        except:
            return 'error'
        #
        gos = dgo(id=iid)
        if not gos:
            return 'error'
        #
        q = 'update ms_user_content set active=0,log_id=$logid where id=$id'
        a = {'id': iid, 'logid': sess.log}
        r = query(q, a)
        return 'ok'        


class admin_go_save:
    def GET(self):
        raise web.seeother('/admin/go')
        
    def POST(self):
        i = web.input(api=0, type='add', id=0)
        #
        if not i.type in ['add', 'edit']:
            raise web.internalerror()
        #
        try:
            iid = int(i.id)
        except:
            sess.msg = ['error', msgs['msg_go_error_required']]
            raise web.seeother('/admin/go')
        #
        try:
            ipriority = int(i.priority)
        except:
            ipriority = 10000
        #
        try:
            ishow = int(i.show_in_menu)
        except:
            ishow = 0
        #
        ipage = mlset(i, 'page')
        icontent = mlset(i, 'content')
        #
        if disblank(ipage, True) or disblank(icontent, True):
            sess.msg = ['error', msgs['msg_go_error_required']]
        else:
            if i.type == 'add':
                r = db.insert('ms_user_content', page=ipage, active=1, content=icontent, show_in_menu=ishow,
                    priority=ipriority, log_id=sess.log)
                if r:
                    sess.msg = ['ok', msgs['msg_go_added']]
            elif i.type == 'edit':
                r = db.update('ms_user_content', page=ipage, active=1, content=icontent, show_in_menu=ishow,
                    priority=ipriority, log_id=sess.log, where='id=$id', 
                    vars={'id': iid})
                if r:
                    sess.msg = ['ok', msgs['msg_go_saved']]
                
        #
        if i.type == 'edit':
            raise web.seeother('/admin/go/edit/%s' %(iid))
        else:
            raise web.seeother('/admin/go')


class admin_go_edit:
    def GET(self, id):
        t = tpl('admin_go_edit')
        ttl = msgs['title_admin_go'].capitalize()
        data = {}
        data['go'] = dgo(id=id) 
        data['message'] = smget()
        o = t.admin_go_edit(title(ttl), data)
        o = tplb(o)
        return o

    def POST(self):
        #handled by admin_go_save
        raise web.seeother('/')        

