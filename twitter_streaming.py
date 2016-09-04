from TwitterAPI import TwitterAPI
import random

def twitterpush(imagefile, name):
    #Variables that contains the user credentials to access Twitter API 

    messages = ['Wunderbar! {0} schwimmt gerade hier vorbei.',
                'Oha. Was schippert denn da vorbei? Wenn das mal nicht die {0} ist.',
                'Schaut mal wir haben die {0} gesichtet.']

    keys = {}
    with open("twitter_access.txt") as f:
        for line in f:
           (key, val) = line.split()
           keys[key] = val

    api = TwitterAPI(
                keys['consumer_key'], keys['consumer_secret'], 
                keys['access_token'], keys['access_token_secret']
                )
    # without image:
    #api.update_status('Updating using OAuth authentication via Tweepy!')
    file = open(imagefile, 'rb')
    data = file.read()
    status = random.choice(messages).format(name)
    print("Tweeting status: {0}".format(status))
    #r = api.request('statuses/update_with_media', {'status': status, {'media[]':data})
    #print(r.status_code)
    return
