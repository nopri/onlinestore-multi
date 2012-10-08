#!/usr/bin/env python

import sys

toplevels = [
'biz', 
'com',
'info',
'name',
'net',
'org',
'pro',
'aero',
'asia',
'cat',
'coop',
'edu',
'gov',
'int',
'jobs',
'mil',
'mobi',
'museum',
'tel',
'travel',
]

user_allowed = '-_.%+'
host_allowed = '-_.'

def is_valid_email(email, tld=toplevels):
    #too short
    if len(email) < 6:
        return False
    #
    
    #split by @
    try:
        user, domain = email.rsplit('@', 1)
        host, tl = domain.rsplit('.', 1)
    except:
        return False
    #
    
    #check for country code and toplevel
    if len(tl) != 2 and tl not in tld:
        return False
    #

    #remove char in user allowed
    for i in user_allowed:
        user = user.replace(i, '')
    #
    #remove char in host allowed
    for i in host_allowed:
        host = host.replace(i, '')
    #

    #should contain only alpha numeric
    if user.isalnum() and host.isalnum():
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        email = sys.argv[1]
    except:
        email = ''
    #
    if not email:
        print 'usage: %s <email_address>' %(sys.argv[0])
    else:
        print is_valid_email(email)
