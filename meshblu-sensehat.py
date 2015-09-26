from sense_hat import SenseHat
import meshblu
import json
import time

def processTweets():
  flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'
  log = open('/tmp/meshblu-sensehat.log', 'w+', 1)

  print >>log, '\n\n## attempting connection to Meshblu'
  m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
  status = m.getStatus()
  print >>log, json.dumps(status, sort_keys=True, indent=2, separators=(',', ': '))
    
  print >>log, '## initializing SenseHat'
  sense = SenseHat()
 
  print >>log, '## registering a new device'
  dev = m.addDevice({'type':'device', 'id':'sensehat'})
  print >>log, json.dumps(dev, sort_keys=True, indent=2, separators=(',', ': '))
  m.setCredentials(dev['uuid'], dev['token'])

  print >>log, '## analyzing tweets'
  while (1):
    sense.clear([0,255,0])
    time.sleep(3)
    sense.clear()
    s = m.subscribeUuid(flow, dev['uuid'], dev['token'])
    if (s):
      if ('makerfaire-octoblu' in s['topic']):
        print >>log, json.dumps(s, sort_keys=True, indent=2, separators=(',', ': '))
        screen_name = s['screen_name']
        color = s['color']
        tweet = s['tweet']
        print >>log, screen_name + ': ' + tweet + ': ' + color
        if (tweet.startswith("shutdown") and "#octoblu" in tweet and "#makerfaire" in tweet):
          print >>log, '## shutting down'
          sense.clear([255,0,0])
          time.sleep(3)
          sense.clear()
          exit()
        elif ("red" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,0,0])
        elif ("yellow" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,255,0])
        elif ("green" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[0,255,0])
      elif ('device-status' in s['topic']):
        print >>log, '## flow status change' + s['payload']['online']
      else:
        print >>log, '## bad/no data received'

def main():
    processTweets()

if __name__ == "__main__":
    main()
