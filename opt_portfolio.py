import argparse

import trade.type
import trade.common


def run():
    parser = argparse.ArgumentParser(description='Create optimal portfolio.')
    parser.add_argument('tickers', metavar='T', type=str, nargs='+',
                        help='ticker to include in portfolio')
    parser.add_argument('-b', '--baseline', default="SPY", type=str,
                        help='baseline ticker')
    parser.add_argument('-s', '--start', required=True, type=trade.type.date,
                        help="Evaluation start date")
    parser.add_argument('-e', '--end', required=True, type=trade.type.date,
                        help="Evaluation end date")
    parser.add_argument('-c', '--cost', default=1, type=int,
                        help="Total portfolio cost")
    parser.add_argument('--short', action='store_true',
                        help="Allow shorting")
    parser.add_argument('--stat', action='store_true',
                        help="Show statistics")
    parser.add_argument('--json', type=str,
                        help="File to save optimized portfolio")
    args = parser.parse_args()

    trade.common.optimize(
        args.tickers,
        args.baseline,
        args.start,
        args.end,
        args.cost,
        args.short,
        args.stat,
        args.json
    )


if __name__ == "__main__":
    run()
