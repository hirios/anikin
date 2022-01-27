from collections import OrderedDict
import requests
import lxml.html
import random


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
]


def default_headers() -> OrderedDict:
    DEFAULT_USER_AGENT = random.choice(USER_AGENTS)
    DEFAULT_HEADERS = OrderedDict(
        (
            ("Host", None),
            ("Connection", "keep-alive"),
            ("Upgrade-Insecure-Requests", "1"),
            ("User-Agent", DEFAULT_USER_AGENT),
            (
                "Accept",
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            ),
            ("Accept-Language", "en-US,en;q=0.9"),
            ("Accept-Encoding", "gzip, deflate"),
        )
    )

    return DEFAULT_HEADERS


class Mangas():
    def __init__(self):
        self.search_url = 'https://mangahost4.com/find/'
        
    
    def search(self, anime_name: str) -> dict:
        anime_name = "+".join(anime_name.split())
        DEFAULT_HEADERS = default_headers()

        response = requests.get(self.search_url + anime_name, headers=DEFAULT_HEADERS)
        parser = lxml.html.fromstring(response.text)
        elements = parser.xpath('//h4[@class="entry-title"]/a')
        img = parser.xpath('//td/a/picture/source/img/@src')
        anime_list = []

        cont = 0
        for html in elements:
            title = html.get('title')
            href = html.get('href')
            anime_list.append({'title': title, 'href': href, 'img': img[cont]})
            cont += 1
            
        return {'Mangas': anime_list}
        

    # anime_url -> https://mangahost4.com/manga/fullmetal-alchemist-mh36553
    def get_last_chapter(self, anime_url: str) -> list[str]: 
        """ Retorna uma string com o numero do último capítlo disponível """
        
        DEFAULT_HEADERS = default_headers()
        response = requests.get(anime_url, headers=DEFAULT_HEADERS)
        parser = lxml.html.fromstring(response.text)
        last_chapter = parser.xpath('//a[@class="btn-caps w-button"]/text()')
        return last_chapter


    # anime_url_chapters -> https://mangahost4.com/manga/fullmetal-alchemist-mh36553/5
    def get_pages(self, anime_url_chapter: str) -> list[str]:
        DEFAULT_HEADERS = default_headers()
        response = requests.get(anime_url_chapter, headers=DEFAULT_HEADERS)  
        parser = lxml.html.fromstring(response.text) 
        pages = parser.xpath('//a/picture/source/img/@src')
        
        if not pages:
            pages = parser.xpath('//div[@id="slider"]/a/img/@src') 

        return pages