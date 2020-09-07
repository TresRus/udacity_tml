import os
import pandas as pd
import storage

class Reader(object):
    def read(self, ticker, columns):
        raise NotImplementedError

    def read_column(self, tickers, column):
        c = storage.Column(column)
        for ticker in tickers:
            df_temp = self.read(ticker, [column])
            df_temp = df_temp.rename(columns={column: ticker})
            c.df = c.df.join(df_temp, how="outer")
        return c

    def read_stock(self, tickers, columns):
        s = storage.Stock()
        for column in columns:
            s.data[column] = self.read_column(tickers, column)
        return s


class CsvReader(Reader):
    def __init__(self, root="data"):
        self.root = root

    def _ticker_cvs_path(self, ticker):
        return os.path.join(self.root, "{}.csv".format(str(ticker)))

    def read(self, ticker, columns):
        if storage.Column.Name.DATE not in columns:
            columns += [storage.Column.Name.DATE]

        file_path = self._ticker_cvs_path(ticker)
        return pd.read_csv(
            file_path,
            parse_dates=True,
            index_col=storage.Column.Name.DATE,
            usecols=columns,
            na_values=["nan"])


