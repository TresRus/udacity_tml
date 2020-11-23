import json
import argparse

import trade.common
import trade.type


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('file', metavar='F', type=str,
                        help='portfolio json file')
    parser.add_argument('-d', '--date', type=trade.type.date,
                        help="Calculation date")
    args = parser.parse_args()

    with open(args.file) as json_file:
        data = json.load(json_file)
        allocation_set = trade.type.AllocationSet([])
        allocation_set.data = data
        trade.common.value(allocation_set, args.date)


if __name__ == "__main__":
    run()
