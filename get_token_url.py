#!/usr/bin/python -tt

""" Grab Trello Token Url for a given key. """

import argparse
import sys
from trello import TrelloApi

def parse_args():
    """ Parse arguments. """

    parser = argparse.ArgumentParser()
    parser.add_argument('--trello-key', dest='trello_key', required=True,
                        help='Trello key')
    parser.add_argument('--prog-name', dest='prog_name', required=True,
                        help='Program name')
    parser.add_argument('--expires', dest='expires', default='30days',
                        help='Program name')
    parser.add_argument('--write-access', dest='write_access', default=False,
                        help='Enable ')

    return parser.parse_args()

def main():
    """ Grab Trello Token Url for a given key. """

    args = parse_args()
    trello = TrelloApi(args.trello_key)

    return trello.get_token_url(args.prog_name, expires=args.expires,
                                write_access=False)

if __name__ == '__main__':
    sys.exit(main())
