import requests
import datetime
import csv
import os
from lxml import html


def load_dict(currencies, from_date, to_date):
    for name, full in currencies.iteritems():
        load_currency(name, full, from_date, to_date)


def load_currency(name, full, from_date, to_date, save_html=False):
    url = 'https://coinmarketcap.com/currencies/%s/historical-data/?start=%04d%02d%02d&end=%04d%02d%02d' % (
        full, from_date.year, from_date.month, from_date.day, to_date.year, to_date.month, to_date.day)
    req = requests.get(url)
    if save_html:
        if not os.path.exists('htmls'):
            os.makedirs('htmls')

        with open('htmls/%s.html' % name, 'w') as out:
            out.write(req.text.encode(req.encoding))

    if not os.path.exists('cc_data'):
        os.makedirs('cc_data')

    with open('cc_data/%s.csv' % name, 'w') as out:
        csv_wr = csv.writer(out)
        tree = html.fromstring(req.text.encode(req.encoding))
        history = tree.xpath('//div[@id = "historical-data"]')[0]
        head = history.xpath('.//thead/tr')[0]
        hr = ()
        for he in head.xpath('.//th/text()'):
            hr = hr + (he,)

        csv_wr.writerow(hr)

        for row in history.xpath('.//tbody/tr'):
            rd = ()
            for re in row.xpath('.//td/text()'):
                if not rd:
                    d = datetime.datetime.strptime(re, '%b %d, %Y')
                    rd = rd + (d.strftime('%Y-%m-%d'),)
                else:
                    rd = rd + (re.replace(',', '').replace('-', '0'),)
            csv_wr.writerow(rd)


def main():
    currencies = {
        'ETH': 'ethereum',
        'XRP': 'ripple'
    }

    start = datetime.date(2009, 1, 1)

    now = datetime.datetime.now()
    begin = now - datetime.timedelta(days=5)

    load_dict(currencies, begin, now)


if __name__ == "__main__":
    main()
