#!/usr/bin/python
import httplib
import urllib
import re
import smtplib
import ConfigParser
from email.mime.text import MIMEText

def getip():
    url = "ip.taobao.com"
    params = urllib.urlencode({'ip':'myip'})
    headers = {'Host':'ip.taobao.com','Content-Type': 'application/x-www-form-urlencoded'}
    conn = httplib.HTTPConnection(url)
    conn.request("POST", "/service/getIpInfo2.php", params, headers)
    resp = conn.getresponse().read()

    ip = re.search(r'\d+\.\d+\.\d+\.\d+', resp).group(0)
    conn.close()
    return ip

def sendmail(sender, passwd, to, msg):
    try:
        to = to.split(',')
        s = smtplib.SMTP('smtp.163.com')
        s.login(sender, passwd)
        s.sendmail(sender, to, msg.as_string())
        s.close()
    except smtplib.SMTPDataError, e:
        print e
    except smtplib.SMTPAuthenticationError, e:
        print e

if __name__ == '__main__':
    fd = open('/proc/uptime')
    uptime = fd.readline().split()[0]
    fd.close()
    if float(uptime) - 1000 > 0:
        exit()
    configparser = ConfigParser.ConfigParser()
    configparser.read('/home/script/profile')
    sender = configparser.get('EMAIL', 'USER')
    passwd = configparser.get('EMAIL', 'PASSWORD')
    to = configparser.get('EMAIL', 'TO')
    ip = getip()
    msg = MIMEText('%s' % ip)
    msg['Subject'] = 'AUTOSEND: home ip'
    msg['From'] = sender
    sendmail(sender, passwd, to, msg)
