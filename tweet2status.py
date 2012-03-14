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
import logging

log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

def updateStatus(config, newstatus):
    print(newstatus)
    jid = xmpp.protocol.JID(config.get('gtalk', 'gtalkname'))
    cl = xmpp.Client(jid.getDomain(),debug=[])
    if not cl.connect(('talk.google.com',5222)):
        log.error('Can not connect to server.')
        return
    if not cl.auth(jid.getNode(), config.get('gtalk', 'gtalkpassword')):
        log.error('Can not auth with server')
        return

    iq = xmpp.Iq()
    iq.setType('get')
    iq.setTo(config.get('gtalk', 'gtalkname'))
    node = xmpp.Node()
    node.setName('query')
    node.setAttr('xmlns', 'google:shared-status')
    iq.addChild(node=node)
    cl.RegisterHandler('iq', handler)
    cl.send(iq)
    cl.Process(1)
    cl.disconnect()


def handler(conn, node):
    node0 = node.getChildren()[0]
    node0.delAttr('status-list-max')
    node0.delAttr('status-max')
    node0.delAttr('status-list-contents-max')
    status = node0.getChildren()[0]
    if status.getData() == "BLAH":
        return
    status.setData("BLAH")
    node.setType('set')
    conn.send(node)

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
