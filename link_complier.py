from html.parser import HTMLParser
from urllib import parse
from domain_finder import *


class LinkFinder(HTMLParser):

    def __init__(self, base_url, domain):
        super(LinkFinder, self).__init__()
        self.base_url = base_url
        self.domain = domain
        self.links = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    if get_domain_name(url) == self.domain:
                        self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        print(message)
