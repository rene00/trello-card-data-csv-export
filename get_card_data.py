#!/usr/bin/python -tt

""" Export Trello Card data to CSV for a given List. """

import argparse
import csv
import re
import sys
from trello import TrelloApi


def parse_args():
    """ Parse arguments. """

    parser = argparse.ArgumentParser()
    parser.add_argument('--list-id', dest='list_id', help='Trello list id',
                        required=True)
    parser.add_argument('--trello-key', dest='trello_key', help='Trello key',
                        required=True)
    parser.add_argument('--trello-token', dest='trello_token',
                        help='Trello token',
                        required=True)

    return parser.parse_args()

def main():
    """ Export Trello ard data to CSV for a given List. """

    args = parse_args()

    trello = TrelloApi(args.trello_key)
    trello.set_token(args.trello_token)
    list_items = trello.lists.get_card(args.list_id)

    for card in list_items:
        card_data = {}
        for key, value in card.iteritems():
            if unicode(key) == 'closed' and value:
                continue

            if unicode(key) == 'name':
                try:
                    match = re.match("^\((.*)\)\s(.*)$", unicode(value))
                    card_data['estimate'] = unicode(match.group(1))
                    card_data['name'] = unicode(match.group(2)) \
                                                .encode('ascii','ignore')
                except AttributeError:
                    pass

            if unicode(key) == 'shortUrl':
                card_data['short_url'] = unicode(value)

        csv_filename = "{0}.csv".format(args.list_id)
        with open(csv_filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, card_data.keys())
            csv_writer.writerow(card_data)

    return True

if __name__ == '__main__':
    sys.exit(main())
