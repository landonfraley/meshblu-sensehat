#! /usr/bin/env python
# -*- coding: utf-8
from sense_hat import SenseHat
import meshblu, json, time, codecs

def tracing(message):
  ts = time.strftime("%c")
  log = codecs.open('/tmp/msb.log', 'a', 'utf-8')
  log.write(ts + ' :: ' + message + '\n')
  log.close()

def processTweets():
  # UUID for _your_ Twitter Sentiment Banner flow
  flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'

  tracing('attempting connection to Meshblu')
  m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
  status = m.getStatus()
  tracing(json.dumps(status, sort_keys=True, indent=2, separators=(',', ': ')))

  tracing('initializing SenseHat')
  sense = SenseHat()

  tracing('registering a new device')
  dev = m.addDevice({'type':'device', 'id':'sensehat'})
  tracing(json.dumps(dev, sort_keys=True, indent=2, separators=(',', ': ')))
  m.setCredentials(dev['uuid'], dev['token'])

  tracing('analyzing tweets')
  sense.clear([0,255,0])
  time.sleep(3)
  sense.clear()
  while (1):
    s = m.subscribeUuid(flow, dev['uuid'], dev['token'])
    if (s):
      tracing(json.dumps(s, sort_keys=True, indent=2, separators=(',', ': ')))
      if ('meshblu-sensehat-banner' in s['topic']):
        sn = s['screen_name']
        color = s['color']
        twt = s['tweet']
        tracing(sn + ': ' + twt + ' - ' + color)
        if ("red" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,0,0])
        elif ("yellow" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,255,0])
        elif ("green" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[0,255,0])
        else:
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,255,25])
      elif ('device-status' in s['topic']):
        if (s['payload']['online']):
          tracing('flow came online')
          sense.show_message('flow came online', scroll_speed=0.05, text_colour=[128,128,255])
        else:
          tracing('flow went offline')
          sense.show_message('flow went offline', scroll_speed=0.05, text_colour=[128,128,255])
      else:
        tracing('unknown topic')
        sense.show_message('unknown topic', scroll_speed=0.05, text_colour=[255,0,255])
    else:
      tracing('no data received')
      sense.clear([255,0,0])
      time.sleep(3)
      sense.clear()

def main():
    processTweets()

if __name__ == "__main__":
    main()
