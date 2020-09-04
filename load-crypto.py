import requests
import datetime
import csv
import os
import json
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


def load_top100(save_html=False):
    url = 'https://coinmarketcap.com/'
    req = requests.get(url)
    if save_html:
        if not os.path.exists('htmls'):
            os.makedirs('htmls')

        with open('htmls/top100.html' % name, 'w') as out:
            out.write(req.text.encode(req.encoding))

    tree = html.fromstring(req.text.encode(req.encoding))
    table = tree.xpath('//tbody')[0]
    res = {}
    for row in table.xpath('.//tr'):
        currency = row.xpath('.//td')[1]
        data = currency.xpath('./span/a')[0]
        name = data.text
        link = data.get("href")[12:-1]
        res[name] = link

    with open('top100.json', 'w') as jf:
        json.dump(res, jf)

def run():
    load_top100()
    load_currencies = json.load(open('top100.json'))

    begin = datetime.date(2009, 1, 1)
    end = datetime.datetime.now()

    load_dict(load_currencies, begin, end)


if __name__ == "__main__":
    run()
