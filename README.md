# Domain Web Crawler
Simple optional multi-threaded python code that gathers all links from a specified domain.

## Components
* domain_finder - returns domain of the provided url.
* file_handler - handles crawler file management (creation, deletion, reading and writing).
* link_compiler - finds and returns all links to a web page.
* crawler - traverses provided web-site.


## Instructions
#### Usage:
          ```crawler.py <project name> <homepage url> [options]
          
          eg. 
          * crawler google https://www.google.com -t 2
          * crawler google https://www.google.com```
          

#### Options:
          ```-h or --help:	Displays help page
          -t <number_of_threads>:	Enables threading, creating <number_of_threads> threads.```

## Compatibility
only tested with python 3.x on unix

