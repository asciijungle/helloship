from lxml import html
import requests

class ImageFetcher():
	def __init__(self, event):
		self.event = event
		self.userid = event['userid']
		pass

	def getVTUrl(self):
		if self.event['imo'] is not 0:
			image_url = str('http://www.vesseltracker.com/en/Ships/'+ str(self.event['imo']) +'.html')
		if self.event['imo'] is 0:
			image_url = 'no image url'
		return image_url
        
	def getImage(self):
		url = self.getVTUrl()
		if url != 'no image url':
			page = requests.get(url)
			tree = html.fromstring(page.text)
			imageurl = tree.xpath('//*[@id="bigImage"]')
			if len(imageurl) is not 0:
				print('Downloading Image for ship with ID: {0}'.format(str(self.userid)))
				r = requests.get(imageurl[0].values()[0])
				if r.status_code == 200:
					with open(str(self.userid) + '.jpg', 'wb') as f:
						for chunk in r:
							f.write(chunk)
		else:
			print('There is no image for this ship')
		return

# zum ausführen:
#imagefetcher = ImageFetcher(event=event)
#imagefetcher.getImage()
