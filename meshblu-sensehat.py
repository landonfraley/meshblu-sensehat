from sense_hat import SenseHat
import meshblu
import json
import time

def processTweets():
    flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'

    print "## attempting connection to Meshblu"
    m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
    status = m.getStatus()
    print json.dumps(status, sort_keys=True, indent=2, separators=(',', ': '))
    
    print "## initializing SenseHat"
    sense = SenseHat()
   
    print "## registering a new device"
    dev = m.addDevice({'type':'device', 'id':'sensehat'})
    print json.dumps(dev, sort_keys=True, indent=2, separators=(',', ': '))
    m.setCredentials(dev['uuid'], dev['token'])

    print "## analyzing tweets"
    while (1):
        s = m.subscribeUuid(flow, dev['uuid'], dev['token'])
        screen_name = s['screen_name']
        color = s['color']
        tweet = s['tweet']
        print(screen_name + ": " + tweet + ": " + color)
        if (tweet.startswith("shutdown") and "#octoblu" in tweet and "#makerfaire" in tweet):
          print "## shutting down"
          sense.clear([255,0,0])
          time.sleep(1)
          sense.clear([255,255,255])
          time.sleep(1)
          sense.clear([255,0,0])
          time.sleep(1)
          sense.clear()
          exit()
        elif ("red" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,0,0])
        elif ("yellow" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,255,0])
        elif ("green" in color):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[0,255,0])
        else:
          print "## bad/no data received"
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,255,255])
          sense.clear([255,0,0])
          time.sleep(1)
          sense.clear()

def main():
    processTweets()

if __name__ == "__main__":
    main()
