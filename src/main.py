# -*- coding: utf-8 -*-
import json
import os

import cli
import menu_parser

import util
from entities import Week


def get_menu_parsing_strategy(location):
    parser = None

    # set parsing strategy based on location
    if location == "mensa-garching":
        parser = menu_parser.StudentenwerkMenuParser()

    return parser


def jsonify(weeks, directory):
    # iterate through weeks
    for calendar_week in weeks:
        # get Week object
        week = weeks[calendar_week]
        # get year of calendar week
        year = week.year

        # create dir: <year>/
        json_dir = "%s/%s" % (str(directory), str(year))
        if not os.path.exists(json_dir):
            os.makedirs("%s/%s" % (str(directory), str(year)))

        # convert Week object to JSON
        week_json = week.to_json()
        # write JSON to file: <year>/<calendar_week>.json
        with open("%s/%s.json" % (str(json_dir), str(calendar_week).zfill(2)), 'w') as outfile:
            json.dump(json.loads(week_json), outfile, indent=4, ensure_ascii=False)


def main():
    # get command line args
    args = cli.parse_cli_args()

    # get location from args
    location = args.location
    # get required parser
    parser = get_menu_parsing_strategy(location)
    if parser is None:
        print("The selected location '%s' does not exist." % location)

    # parse menu
    menus = parser.parse(location)

    # if date has been explicitly specified, try to parse it
    menu_date = None
    if args.date is not None:
        try:
            menu_date = util.parse_date(args.date)
        except ValueError as e:
            print("Error during parsing date from command line: %s" % args.date)
            print("Required format: %s" % util.cli_date_format)
            return

    # print menu
    if menus is None:
        print("Error. Could not retrieve menu(s)")
    # jsonify argument is set
    elif args.jsonify is not None:
        weeks = Week.to_weeks(menus)
        if not os.path.exists(args.jsonify):
            os.makedirs(args.jsonify)
        jsonify(weeks, args.jsonify)
    # date argument is set
    elif args.date is not None:
        if menu_date not in menus:
            print("There is no menu for '%s' on %s!" % (location, menu_date))
            return
        menu = menus[menu_date]
        print(menu)
    # else, print weeks
    else:
        weeks = Week.to_weeks(menus)
        for calendar_week in weeks:
            print(weeks[calendar_week])


if __name__ == "__main__":
    main()
