#!/usr/bin/python

import sys,nntplib,syslog,email,smtplib
from email import policy

smtp_host = 'smtp-server-goes-here'
smtp_user   = 'smtp-username-goes-here'
smtp_passwd = 'smtp-password-goes-here'

mailgroups = {
    'gmane.comp.foobar.users': 'foobar-list@foobar.invalid',
}

syslog.openlog('inews')

def logerr(s):
    syslog.syslog(s)
    sys.stderr.write(s)

def loginf(s):    
    syslog.syslog(s)

status = 0

article = sys.stdin.buffer.read()
msg = email.message_from_bytes(article, policy=policy.SMTP)
group = msg['Newsgroups']

if group not in mailgroups:
    # post using NNTP
    try:
        s = nntplib.NNTP('news.gmane.io')
    except Exception as e:
        logerr("Error connecting to news.gmane.io: %s" % str(e))
        sys.exit(1)
        
    try:
        s.post(article)
        loginf("NNTP post to %s OK" % group)
    except Exception as e:
        logerr("NNTP post to %s failed: %s" % (group,str(e)))
        status = 1
    s.quit()
else:
    # send as e-mail
    toaddr = mailgroups[group]
    msg['To'] = toaddr
    del msg['Newsgroups']

    try:
        s = smtplib.SMTP_SSL(smtp_host)
    except Exception as e:
        logerr('Error connecting to %s: %s' % (smtp_host, str(e)))
        sys.exit(1)

    try:                  
        s.login(smtp_user,smtp_passwd)
        if 0:
            s.send_message(msg) # bug in send_message does from mangling when it should not
        else:
            s.sendmail(msg['From'], toaddr, msg.as_bytes())
        loginf('SMTP send to %s OK' % toaddr)
    except Exception as e:
        logerr('SMTP send to %s failed: %s' % (toaddr, str(e)))
        status = 1
    s.close()
    
sys.exit(status)

    

