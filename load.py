import requests

def main():
    currencies = {
        'ETH': 'ethereum',
        'XRP': 'ripple'
    }

    for name, full in currencies.iteritems():
        url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=20090101&end=20180109' % (full)
        req = requests.get(url)
        with open('htmls/%s.html' % name, 'w') as out:
            out.write(req.text.encode(req.encoding))


if __name__ == "__main__":
    main()

