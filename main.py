#!/usr/bin/env python

import argparse
import os
import yaml
import time
from jenkinsapi.jenkins import Jenkins
from jenkinsapi import custom_exceptions
from terminaltables import AsciiTable

COLORS = {
    "red": "\033[1;31m",
    "blue": "\033[1;34m",
    "yellow": "\033[1;43m",
    "cyan": "\033[1;36m",
    "green": "\033[0;32m",
    "bold": "\033[;1m",
    "reverse": "\033[;7m",
    "reset": "\033[0;0m",
}

parser = argparse.ArgumentParser(prog='Jenkins handler',
                                 description='Handle jobs on Jenkins servers.')

subparsers = parser.add_subparsers(dest='action')

parser_a = subparsers.add_parser('list')
parser_b = subparsers.add_parser('details')
parser_b.add_argument(
    '-j', '--job_name', dest='job_name', help='Name of the job to get info of')

parser.add_argument('-c', '--config', dest='filename', required=True,
                    type=lambda x: is_valid_file(parser, x),
                    help='path of the configuration file')


def job_list(config, params=None):
    print('%sFetching job list for %s %s...' % (COLORS["blue"], config['url'], COLORS['reset']))
    server = Jenkins(config['url'], timeout=2000, username=config['login'], password=config['password'])
    table_data = [
        ['Name', 'Status', 'Url']
    ]
    count = 0
    start = time.time()
    for job_name, job_instance in server.get_jobs():
        count += 1
        if count >= 10:
            break
        table_data.append([
            job_instance.name,
            COLORS["yellow"] + 'RUNNING' + COLORS["reset"] if job_instance.is_running() else
            COLORS["red"] + 'STOPPED' + COLORS["reset"],
            job_instance.url
        ])

    print(time.time() - start)
    table = AsciiTable(table_data)
    print(table.table)
    print("Jobs found: ", len(server.get_jobs_list()))


def job_details(config, job_name):
    print('%sGetting details for job %s on server %s %s...'
          % (COLORS["blue"], job_name, str(config['url']), COLORS['reset']))
    server = Jenkins(config['url'])  # , username=config['login'], password=config['password']
    try:
        job = server.get_job(job_name)
        print('Got Job %s. Running: %s. Enabled: %s' % (job, job.is_running(), job.is_enabled()))
    except custom_exceptions.UnknownJob:
        print('No job found : %s' % job_name)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def main():
    kwargs = vars(parser.parse_args())
    configs = yaml.load(kwargs.pop('filename'))
    for config in configs:
        globals()["job_%s" % kwargs.pop('action')](config['server'], **kwargs)


if __name__ == "__main__":
    # execute only if run as a script
    main()
