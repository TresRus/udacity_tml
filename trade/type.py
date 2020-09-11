import datetime
import argparse

class Allocation(object):
    def __init__(self, ticker, number):
        self.ticker = ticker
        self.number = number

    @staticmethod
    def argparse(value):
        parts = value.split(":")
        if len(parts) != 2 or int(parts[1]) <= 0:
            raise argparse.ArgumentTypeError("Invalide format: {}. Allocator should have format: <ticker>:<number> (example: SPY:40)".format(value))
        return Allocation(parts[0], int(parts[1]))

def date(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError("Not a valid date: {}. Should be in forman YYYY-MM-DD (example: 2020-09-05).".format(value))
