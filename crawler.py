from urllib.request import urlopen
from domain_finder import *
from file_handler import *
from link_complier import LinkFinder
import sys


def request_get_links(url):
    html_string = ''
    try:
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
        finder = LinkFinder(base_url, url)
        finder.feed(html_string)
    except Exception as e:
        print(str(e))
        return set()
    return finder.page_links()


def add_to_queue(link_set):
    for item in link_set:
        if item in queue_set or item in crawled_set or domain_name not in item:
            continue
        queue_set.add(item)


def file_update(queue, crawled):
    set_to_file(queue['queue_set'], queue['queue_file'])
    set_to_file(crawled['crawled_set'], crawled['crawled_file'])


def help():
    print('Usage:\n\
          crawler.py <project name> <homepage url>\n')
    print('Options:\n\
          -h or --help')


if __name__ == '__main__':

    if len(sys.argv) < 3 or len(sys.argv) > 4 or '-h' in sys.argv or '--help' in sys.argv:
        help()
        sys.exit(0)

    project_name = sys.argv[1]
    base_url = sys.argv[2]
    queue_file = project_name + '/queue.txt'
    crawled_file = project_name + '/crawled.txt'
    result_file = project_name+'/result.txt'
    domain_name = get_domain_name(base_url)
    initialize(project_name, base_url)
    queue_set = file_to_set(queue_file)
    crawled_set = file_to_set(crawled_file)

    while len(queue_set) > 0:
        url = queue_set.pop()
        print('Processing url: '+ url)
        print(str(len(queue_set))+' left in queue.')

        add_to_queue(request_get_links(url))
        crawled_set.add(url)

        file_update({'queue_set':queue_set, 'queue_file':queue_file}, {"crawled_set":crawled_set, 'crawled_file': crawled_file})
        print('{0} crawled. {1} crawled'.format(url, len(crawled_set)))

        queue_set = file_to_set(queue_file)
        crawled_set = file_to_set(crawled_file)

    rename_file(crawled_file, result_file)