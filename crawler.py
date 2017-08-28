from urllib.request import urlopen
from domain_finder import *
from file_handler import *
from link_complier import LinkFinder

import sys
import threading


def request_get_links(url):
    html_string = ''
    try:
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
        finder = LinkFinder(base_url, domain_name)
        finder.feed(html_string)
    except Exception as e:
        print(str(e))
        return set()
    return finder.page_links()


def add_to_queue(link_set):
    for item in link_set:
        if item in queue_set or item in crawled_set:
            continue
        queue_set.add(item)


def file_update(queue, crawled):
    set_to_file(queue['queue_set'], queue['queue_file'])
    set_to_file(crawled['crawled_set'], crawled['crawled_file'])


def crawl():
    global queue_set, queue_file
    global crawled_set, crawled_file

    thread_lock.acquire()
    while len(queue_set) > 0:
        url = queue_set.pop()
        thread_lock.release()

        print('{0} processing url: {1}'.format(threading.current_thread().getName(), url))
        print(str(len(queue_set))+' left in queue.')

        thread_lock.acquire()
        add_to_queue(request_get_links(url))
        crawled_set.add(url)

        file_update({'queue_set':queue_set, 'queue_file':queue_file}, {"crawled_set":crawled_set, 'crawled_file': crawled_file})
        print('{0} crawled. {1} crawled'.format(url, len(crawled_set)))

        queue_set = file_to_set(queue_file)
        crawled_set = file_to_set(crawled_file)

    thread_lock.release()

    print('Message from {0}.'.format(threading.current_thread().getName()))
    print('Thread {0} Terminated.'.format(threading.current_thread().getName()))
    print('{0} active Threads left.'.format(threading.active_count()))


def help():
    print('Usage:\n\
          crawler.py <project name> <homepage url> [options]\n')
    print('Options:\n\
          -h or --help:\tDisplays help page\n\
          -t <number_of_threads>:\tEnables threading, creating <number_of_threads> threads.')


if __name__ == '__main__':

    if len(sys.argv) < 3 or len(sys.argv) > 6 or '-h' in sys.argv or '--help' in sys.argv:
        help()
        sys.exit(0)

    project_name = 'projects/'+sys.argv[1]
    base_url = sys.argv[2]
    queue_file = project_name + '/queue.txt'
    crawled_file = project_name + '/crawled.txt'
    domain_name = get_domain_name(base_url)
    initialize(project_name, base_url)
    queue_set = file_to_set(queue_file)
    crawled_set = file_to_set(crawled_file)
    thread_lock = threading.RLock()

    if '-t' in sys.argv:
        counter = 0
        threads = []

        number_of_threads = int(float(sys.argv[sys.argv.index('-t')+1]))

        while counter < number_of_threads:
            threads.append(threading.Thread(target=crawl))
            counter += 1

        print('{0} threads created.'.format(len(threads)))

        counter = 1

        while counter < number_of_threads:
            try:
                threads[counter].start()
                counter += 1
            except Exception as e:
                print(e)

        crawl()

        print('{0} threads started.'.format(len(threads)))
    else:
        crawl()