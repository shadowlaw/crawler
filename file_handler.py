import os


def new_file(filename):
    with open(filename, 'w'):
        pass


def rename_file(source, destination):
    os.rename(source, destination)


def set_to_file(data, filename):
    with open(filename, 'w') as file_ptr:
        for item in data:
            file_ptr.write(str(item)+'\n')


def initialize(project_name, base_url):
    project_name = project_name

    queue_file = project_name+"/queue.txt"
    crawled_file = project_name + "/crawled.txt"

    if not os.path.isdir(project_name):
        os.makedirs(project_name)

    if not os.path.isfile(queue_file):
        new_file(queue_file)
        set_to_file([base_url], queue_file)

    if not os.path.isfile(crawled_file):
        new_file(crawled_file)


def file_to_set(filename):
    new_set = set()

    try:
        with open(filename, 'r') as file_ptr:
            for line in file_ptr:
                new_set.add(line.replace('\n', ''))
    except Exception as e:
        print(str(e))

    return new_set
