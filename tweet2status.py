#! /usr/bin/env python
#
# tweet2statuss.py
# Nick Loadholtes <nick@ironboundsoftware.com>
# March 13, 2012
#

import urllib2
import json

def main(configfilename='config.cfg'):
    config = ConfigParser.RawConfigParser()
    config.readfp(codecs.open(configfilename, "r", "utf8"))

    url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name='
    req = urllib2.open(url)
    

if __name__ == "__main__":
    main()
