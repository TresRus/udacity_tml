import load
import datetime


def main():
    currencies = {
        'ETH': 'ethereum',
        'XRP': 'ripple'
    }

    start = datetime.date(2009, 1, 1)
    now = datetime.datetime.now()

    load.load_dict(currencies, start, now)


if __name__ == "__main__":
    main()
