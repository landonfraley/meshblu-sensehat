from sense_hat import SenseHat
import meshblu
import json

def helloWorld():
    flow = '0a603b74-bb62-4eda-bac8-7c823cc63b03'

    m = meshblu.MeshbluRestClient('http://meshblu.octoblu.com')
    sense = SenseHat()
    dev = m.addDevice({'type':'device', 'id':'sensehat'})
    m.setCredentials(dev['uuid'], dev['token'])
    while (1):
        s = m.subscribeUuid(flow, dev['uuid'], dev['token'])
        msg = s['payload']['message']
        print(msg)
        sense.show_message(msg)
        if (msg == "landonf: shutdown test #sensehat"):
          exit()

def main():
    helloWorld()

if __name__ == "__main__":
    main()
