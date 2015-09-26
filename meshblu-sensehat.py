from sense_hat import SenseHat
import meshblu, json, time

def processTweets():
  flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'
  log = open('/tmp/meshblu-sensehat.log', 'w+', 1)

  ts = time.strftime("%c")
  m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
  status = m.getStatus()
  print >>log, '\n\n' + ts + ' ## attempting connection to Meshblu'
  print >>log, ts + '\n'  + json.dumps(status, sort_keys=True, indent=2, separators=(',', ': '))

  sense = SenseHat()
  print >>log, ts + ' ## initializing SenseHat'

  dev = m.addDevice({'type':'device', 'id':'sensehat'})
  print >>log, ts + ' ## registering a new device'
  print >>log, ts + '\n' + json.dumps(dev, sort_keys=True, indent=2, separators=(',', ': '))
  m.setCredentials(dev['uuid'], dev['token'])

  ts = time.strftime("%c")
  print >>log, ts + ' ## analyzing tweets'
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

        print >>log, ts + '\n' + json.dumps(s, sort_keys=True, indent=2, separators=(',', ': '))
        print >>log, ts + ' ## ' + sn + ': ' + twt + ': ' + color
        if (twt.startswith("shutdown") and "#octoblu" in twt and "#makerfaire" in twt):
          print >>log, ts + ' ## shutting down'
          sense.clear([255,0,255])
          time.sleep(3)
          sense.clear()
          exit()
        elif ("red" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,0,0])
        elif ("yellow" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[255,255,0])
        elif ("green" in color):
          sense.show_message(sn + ": " + twt, scroll_speed=0.05, text_colour=[0,255,0])
      elif ('device-status' in s['topic']):
        ts = time.strftime("%c")
        if (s['payload']['online']):
          print >>log, ts + ' ## flow came online'
          sense.show_message(' ## flow came online', scroll_speed=0.05, text_colour=[128,128,128])
        else:
          print >>log, ts + ' ## flow went offline'
          sense.show_message(' ## flow went offline', scroll_speed=0.05, text_colour=[128,128,128])
    else:
      ts = time.strftime("%c")
      print >>log, ts + ' ## bad/no data received'
      sense.clear([255,0,0])
      time.sleep(3)
      sense.clear()

def main():
    processTweets()

if __name__ == "__main__":
    main()
