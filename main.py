import argparse
import os
import yaml


def list_jobs():
    print('LIST JOBS')


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
    print('hello, opening file : ', args.filename)
    config = yaml.load(args.filename)
    print("config", config)
    print('action', args.action)
    if args.action not in AVAILABLE_ACTIONS:
        parser.error("The action %s does not exist" % args.action)
    AVAILABLE_ACTIONS[args.action]()


if __name__ == "__main__":
    # execute only if run as a script
    main()
