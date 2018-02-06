import argparse
import os
import yaml
from jenkinsapi.jenkins import Jenkins
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


def list_jobs(config):
    print('%sJobs list for %s %s' % (COLORS["blue"], config['url'], COLORS['reset']))
    server = Jenkins(config['url'])  # , username=config['login'], password=config['password']
    table_data = [
        ['Name', 'Status', 'Url']
    ]
    rows = 0
    for job_name, job_instance in server.get_jobs():
        rows += 1
        if rows == 4:
            break
        table_data.append([
            job_instance.name if job_instance.is_enabled() else COLORS["red"] + job_instance.name + COLORS["reset"],
            COLORS["yellow"] + 'RUNNING' + COLORS["reset"] if job_instance.is_running() else
            COLORS["red"] + 'STOPPED' + COLORS["reset"],
            job_instance.url
        ])

    table = AsciiTable(table_data)

    print(table.table)


def job_info():
    print('JOB INFO')


AVAILABLE_ACTIONS = {
    "list": list_jobs,
    "info": job_info
}


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def main():
    parser = argparse.ArgumentParser(prog='Jenkins handler',
                                     description='Handle jobs on Jenkins servers.')
    parser.add_argument('action', metavar='ACTION',
                        help='The action to perform on the jenkins servers')
    parser.add_argument('--config', dest="filename", required=True,
                        type=lambda x: is_valid_file(parser, x),
                        help='path of the configuration file')

    args = parser.parse_args()
    config = yaml.load(args.filename)
    if args.action not in AVAILABLE_ACTIONS:
        parser.error("The action %s does not exist" % args.action)
    for server in config:
        AVAILABLE_ACTIONS[args.action](server['server'])


if __name__ == "__main__":
    # execute only if run as a script
    main()
