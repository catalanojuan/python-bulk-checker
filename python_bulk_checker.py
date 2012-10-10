# -*- encoding: utf8 -*-
#!/usr/bin/env python

import csv

import requests
import yaml

DEFAULTS = {
    'base_url': 'http://localhost:8000/',
    'to_strip': 'http://somedomain.com/',
    'urls_file': 'urls.csv',
}
FAIL = '\033[91m'
ENDC = '\033[0m'


def read_options():
    try:
        f = open('options.yml', 'r')
        return yaml.load(f.read())
    except IOError as e:
        if e.errno == 2:
            return {}
        raise e


def prepare_url(url, options=DEFAULTS):
    ret = url
    if 'to_strip' in options and url.startswith(options['to_strip']):
        slug = url[len(options['to_strip']):]
        ret = options['base_url'] + slug
    return ret


def print_fail(msg):
    print FAIL + msg + ENDC


def main():
    options = read_options() or DEFAULTS
    urls_reader = csv.reader(open(options['urls_file'], 'r'), delimiter=',',
                            quotechar='"')

    for row in urls_reader:
        url = row[0]
        prepared_url = prepare_url(url, options)
        response = requests.head(prepared_url)

        if response.status_code == 200:
            print 'Request to: %s. OK.' % prepared_url
        elif response.status_code == 301:
            print 'Request to %s. Redirected.' % prepared_url
        elif response.status_code == 404:
            print_fail('Request to %s. Not Found.' % prepared_url)
        else:
            print 'Request to %s. Error. Status code: %d' (prepared_url,\
                                                           response.status_code)


if __name__ == '__main__':
	main()
