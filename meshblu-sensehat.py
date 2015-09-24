from sense_hat import SenseHat
import meshblu
import json

def processTweets():
    flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'

    print "## attempting connection to Meshblu"
    m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
    s = m.getStatus()
    print json.dumps(s, sort_keys=True, indent=2, separators=(',', ': '))
    
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
        if (color == "red"):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,0,0])
        elif (color == "yellow"):
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[255,255,0])
        else:
          sense.show_message(screen_name + ": " + tweet, scroll_speed=0.05, text_colour=[0,255,0])
        if (tweet.startswith("shutdown") and "#octoblu" in tweet and "#makerfaire" in tweet):
          print "## shutting down"
          exit()

def main():
    processTweets()

if __name__ == "__main__":
    main()
