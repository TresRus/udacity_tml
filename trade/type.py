import datetime
import argparse


class Allocation(object):
    def __init__(self, ticker, number):
        self.ticker = ticker
        self.number = number

    def __str__(self):
        return "{} - {}".format(self.ticker, self.number)

    @staticmethod
    def argparse(value):
        parts = value.split(":")
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(
                "Invalide format: {}. Allocator should have format: <ticker>:<number> (example: SPY:40)".format(value))
        return Allocation(parts[0], int(parts[1]))


class AllocationSet(object):
    def __init__(self, allocations):
        self.data = {}
        for allocation in allocations:
            self.data[allocation.ticker] = int(allocation.number)

    def get_list(self):
        return [Allocation(ticker, number) for ticker, number in self.data.items()]

    def __str__(self):
        return "\n".join([str(a) for a in self.get_list()])


def date(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Not a valid date: {}. Should be in forman YYYY-MM-DD (example: 2020-09-05).".format(value))
