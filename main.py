#!/usr/bin/env python

import argparse
import os
import yaml
from jenkins import JenkinsHandler


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def main():
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

    kwargs = vars(parser.parse_args())
    configs = yaml.load(kwargs.pop('filename'))
    for config in configs:
        server = JenkinsHandler(config['server']['url'], config['server']['login'], config['server']['password'])
        server.__getattribute__("job_%s" % kwargs.pop('action'))(**kwargs)


if __name__ == "__main__":
    main()
