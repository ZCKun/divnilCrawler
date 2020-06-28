import requests
import sys
import os

from multiprocessing import Pool
from bs4 import BeautifulSoup


class Divnil:

    def __init__(self):
        self.head = "https://divnil.com/wallpaper/iphone8/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        }

    def fetch(self, url: str) -> requests.Response:
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != requests.codes.OK:
            raise requests.RequestException(f"Request Error, Code: {resp.status_code}")
        return resp

    def parser(self, resp):
        soup = BeautifulSoup(resp.text, "html.parser")

        contents = soup.find("div", id="contents")
        wallpapers = contents.findAll("a", rel="wallpaper")

        self.links = []
        for wallpaper in wallpapers:
            self.links.append(wallpaper['href'])

        pages = soup.find("ul", class_="pages")
        self.nextPage = pages.find("li", class_="btn_next")  # 获取下一页按钮的dom

    def get_image_info_url(self, url):
        resp = self.fetch(url)
        self.parser(resp)

    def download_image(self, url):

        resp = requests.get(f"{self.head}{url}", headers=self.headers)
        if resp.status_code != requests.codes.OK:
            raise requests.RequestException("URL: %s REQUESTS ERROR. CODE: %d" % (url, resp.status_code))

        soup = BeautifulSoup(resp.text, "html.parser")

        img = soup.find("div", id="contents").find("img", id="main_content")
        img_url = self.head + img['original'].replace("../", "")
        img_name = img['alt']

        print("start download %s ..." % img_url)

        resp = requests.get(img_url, headers=self.headers)
        if resp.status_code != requests.codes.OK:
            raise requests.RequestException("IMAGE %s DOWNLOAD FAILED." % img_name)

        if '/' in img_name:
            img_name = img_name.split('/')[1]

        with open("./Divnil/" + img_name + ".jpg", "wb") as f:
            f.write(resp.content)

    def run(self):

        if os.path.exists("./Divnil") != True:
            os.mkdir("./Divnil")

        url = "https://divnil.com/wallpaper/iphone8/%E3%82%A2%E3%83%8B%E3%83%A1%E3%81%AE%E5%A3%81%E7%B4%99.html"
        self.get_image_info_url(url)

        with Pool() as pool:
            while True:
                for url in self.links:
                    pool.apply_async(self.download_image, args=(url, ))

                # 如果 nextPage 为空，也就是没有下一页了
                if self.nextPage == None:
                    break

                page = self.nextPage.find("a")
                # 这里再次判断是因为我也不知道最后一页是什么样，加上保险
                if page == None:
                    break

                self.get_image_info_url(self.head + page['href'])

            pool.close()
            pool.join()


if __name__ == "__main__":
    divnil = Divnil()
    divnil.run()

