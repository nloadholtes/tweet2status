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
import xmpp

def updateStatus(config, status):
    print(status)

def main(configfilename='config.cfg'):
    config = ConfigParser.RawConfigParser()
    config.readfp(codecs.open(configfilename, "r", "utf8"))

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
    updateStatus(config, status)

if __name__ == "__main__":
    main()
