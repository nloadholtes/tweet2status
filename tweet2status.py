#! /usr/bin/env python
#
# tweet2statuss.py
# Nick Loadholtes <nick@ironboundsoftware.com>
# March 13, 2012
#

import urllib2
import json
import ConfigParser
import codecs
from xmpp import *
import warnings

warnings.filterwarnings("ignore") # silence DeprecationWarning messages

def updateStatus(config, newstatus):
    # Code based on: http://blog.thecybershadow.net/2010/05/08/setting-shared-google-talk-gmail-status-programmatically
    cl=Client(server='gmail.com',debug=[])

    # T'would be better if this was oauth.
    #
    if not cl.connect(server=('talk.google.com',5222)):
        raise IOError('Can not connect to server.')

    if not cl.auth(config.get('gtalk', 'gtalkname'), config.get('gtalk', 'gtalkpassword'), 'gmail.com'):
        raise IOError('Can not auth with server.')
    cl.send(Iq('set','google:shared-status', payload=[
        Node('show',payload=["default"]),
        Node('status',payload=[newstatus])
    ]))
    cl.disconnect()

def getTweet(config):
    url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name='
    url += config.get('twitter', 'username')
    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    response = f.read()
    tweets = json.loads(response)
    status = ''
    for tweet in tweets:
        if tweet['text'][0] == '@':
            continue
        status = tweet['text']
        break
    return status


def main(configfilename='config.cfg'):
    config = ConfigParser.RawConfigParser()
    config.readfp(codecs.open(configfilename, "r", "utf8"))
    status = getTweet(config)
    updateStatus(config, status)

if __name__ == "__main__":
    main()
