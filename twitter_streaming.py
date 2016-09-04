from TwitterAPI import TwitterAPI

def twitterpush(imagefile, name):
    #Variables that contains the user credentials to access Twitter API 
    

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
    r = api.request('statuses/update_with_media', {'status':'Wunderbar! {0} schwimmt gerade hier vorbei.'.format(name)}, {'media[]':data})
    print(r.status_code)
    return
