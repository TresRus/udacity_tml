import json
import argparse

import trade.type
import trade.common


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('file', metavar='F', type=str,
                        help='portfolio json file')
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    parser.add_argument('-t', '--topup', default=0, type=int,
                        help="Total portfolio cost")
    parser.add_argument('--short', action='store_true',
                        help="Allow shorting")
    parser.add_argument('--stat', action='store_true',
                        help="Show statistics")
    args = parser.parse_args()

    with open(args.file) as json_file:
        data = json.load(json_file)

    allocation_set = trade.type.AllocationSet([])
    allocation_set.data = data
    print("Portfolio before:")
    print(allocation_set)
    cost = trade.common.value(allocation_set, args.end) + args.topup

    trade.common.optimize(
        data.keys(),
        args.baseline,
        args.start,
        args.end,
        cost,
        args.short,
        args.stat,
        args.file
    )


if __name__ == "__main__":
    run()
