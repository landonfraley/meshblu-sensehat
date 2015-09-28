#! /usr/bin/env python
# -*- coding: utf-8
from sense_hat import SenseHat
import meshblu, json, time, codecs

def tracing(message):
  log = codecs.open('/tmp/msb.log', 'a', 'utf-8')
  log.write(message)
  log.close()

def processTweets():
  # UUID for Octoblu Flow
  flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'

  ts = time.strftime("%c")
  m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
  status = m.getStatus()
  tracing(ts + ' ## attempting connection to Meshblu\n')
  tracing(ts + ' - '  + json.dumps(status, sort_keys=True, indent=2, separators=(',', ': ')) + '\n')

  sense = SenseHat()
  tracing(ts + ' ## initializing SenseHat\n')

  dev = m.addDevice({'type':'device', 'id':'sensehat'})
  tracing(ts + ' ## registering a new device\n')
  tracing(ts + ' - ' + json.dumps(dev, sort_keys=True, indent=2, separators=(',', ': ')) + '\n')
  m.setCredentials(dev['uuid'], dev['token'])

  ts = time.strftime("%c")
  tracing(ts + ' ## analyzing tweets\n')
  sense.clear([0,255,0])
  time.sleep(3)
  sense.clear()
  while (1):
    s = m.subscribeUuid(flow, dev['uuid'], dev['token'])
    if (s):
      if ('makerfaire-octoblu' in s['topic']):
        ts = time.strftime("%c")
        sn = s['screen_name']
        color = s['color']
        twt = s['tweet']

        tracing(ts + ' - ' + json.dumps(s, sort_keys=True, indent=2, separators=(',', ': ')) + '\n')
        tracing(ts + ' ## ' + sn + ': ' + twt + ': ' + color + '\n')
        if ("red" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,0,0])
        elif ("yellow" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,255,0])
        elif ("green" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[0,255,0])
      elif ('device-status' in s['topic']):
        ts = time.strftime("%c")
        if (s['payload']['online']):
          tracing(ts + ' ## flow came online\n')
          sense.show_message(' ## flow came online', scroll_speed=0.05, text_colour=[128,128,128])
        else:
          tracing(ts + ' ## flow went offline\n')
          sense.show_message(' ## flow went offline', scroll_speed=0.05, text_colour=[128,128,128])
    else:
      ts = time.strftime("%c")
      tracing(ts + ' ## bad/no data received\n')
      sense.clear([255,0,0])
      time.sleep(3)
      sense.clear()

def main():
    processTweets()

if __name__ == "__main__":
    main()
