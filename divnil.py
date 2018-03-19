import requests
from bs4 import BeautifulSoup
import sys
import os


class Divnil:

	def __init__(self):
		#self.url = "https://divnil.com/wallpaper/iphone8/%E3%82%A2%E3%83%8B%E3%83%A1%E3%81%AE%E5%A3%81%E7%B4%99.html"
		self.head = "https://divnil.com/wallpaper/iphone8/"
		self.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
		}
	

	def getImageInfoUrl(self,url):

		resp = requests.get(url, headers=self.headers)
		if resp.status_code != requests.codes.OK:
			print("Request Error, Code: %d"% resp.status_code)
			sys.exit()

		soup = BeautifulSoup(resp.text, "html.parser")
		
		contents = soup.find("div", id="contents")
		wallpapers = contents.findAll("a", rel="wallpaper")
		
		self.links = []
		for wallpaper in wallpapers:
			self.links.append(wallpaper['href'])
			
		pages = soup.find("ul", class_="pages")
		self.nextPage = pages.find("li", class_="btn_next")
		

	
	def downloadImage(self):

		if os.path.exists("./Divnil") != True:
			os.mkdir("./Divnil")
		
		url = "https://divnil.com/wallpaper/iphone8/%E3%82%A2%E3%83%8B%E3%83%A1%E3%81%AE%E5%A3%81%E7%B4%99.html"
		self.getImageInfoUrl(url)
		
		while True:

			for url in self.links:
				
				url = self.head + url
				
				resp = requests.get(url, headers=self.headers)
				if  resp.status_code != requests.codes.OK:
					print("URL: %s REQUESTS ERROR. CODE: %d" % (url, resp.status_code))
					continue
				
				soup = BeautifulSoup(resp.text, "html.parser")
				
				img = soup.find("div", id="contents").find("img", id="main_content")
				img_url = self.head + img['original'].replace("../", "")
				img_name = img['alt']
				
				print("start download %s ..." % img_url)

				resp = requests.get(img_url, headers=self.headers)
				if resp.status_code != requests.codes.OK:
					print("IMAGE %s DOWNLOAD FAILED." % img_name)
					continue

				if '/' in img_name:
					img_name = img_name.split('/')[1]

				with open("./Divnil/" + img_name + ".jpg", "wb") as f:
					f.write(resp.content)
					
			if self.nextPage == None:
				break
				
			page = self.nextPage.find("a")
			if page == None:
				break
			
			self.getImageInfoUrl(self.head + page['href'])


	def main(self):
		self.downloadImage()


if __name__ == "__main__":
	divnil = Divnil()
	divnil.main()
