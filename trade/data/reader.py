import os
import pandas as pd
from trade.data import ColumnName, Dataset


class Reader(object):
    def read(self, ticker, columns):
        raise NotImplementedError

    def read_column(self, tickers, column):
        df = pd.DataFrame()
        for ticker in tickers:
            if ticker in df.columns:
                continue
            df_temp = self.read(ticker, [column])
            df_temp = df_temp.rename(columns={column: ticker})
            df = df.join(df_temp, how="outer")
        return df

    def read_dataset(self, tickers, columns):
        ds = Dataset()
        for column in columns:
            ds.columns[column] = self.read_column(tickers, column)
        return ds


class CsvReader(Reader):
    def __init__(self, root="data"):
        self.root = root

    def _ticker_cvs_path(self, ticker):
        return os.path.join(self.root, "{}.csv".format(str(ticker)))

    def read(self, ticker, columns):
        if ColumnName.DATE not in columns:
            columns += [ColumnName.DATE]

        file_path = self._ticker_cvs_path(ticker)
        return pd.read_csv(
            file_path,
            parse_dates=True,
            index_col=ColumnName.DATE,
            usecols=columns,
            na_values=["nan"])
