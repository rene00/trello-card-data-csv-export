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
    parser.add_argument('--mode', dest='mode', metavar='MODE',
                        choices=['csv','burndown'], default='burndown',
                        help='csv or burndown', required=False) 
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
    list_data = {}

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

            if unicode(key) == 'dateLastActivity':
                match = re.match("^(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}\.\d{3}Z", unicode(value))
                card_data['last_activity_timestamp'] = unicode(match.group(1))

            if unicode(key) == 'shortUrl':
                card_data['short_url'] = unicode(value)

        if args.mode == 'csv':
            csv_filename = "{0}.csv".format(args.list_id)
            with open(csv_filename, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, card_data.keys())
                csv_writer.writerow(card_data)
        elif args.mode == 'burndown':
            if 'estimate' in  card_data:
                if card_data['last_activity_timestamp'] in list_data:
                    list_data[card_data['last_activity_timestamp']].append(float(card_data['estimate']))
                else:
                    list_data[card_data['last_activity_timestamp']] = [float(card_data['estimate'])]

    if args.mode == 'burndown':
        for date in list_data.keys():
            print "{0}:{1}".format(date, sum(list_data[date]))

    return True

if __name__ == '__main__':
    sys.exit(main())
