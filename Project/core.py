import time
import datetime

import pandas as pd
from matplotlib import cm
import matplotlib.pyplot as plt

import config as config
import util as util


class ExampleClass:
    def __init__(self, df, shared_idx=[]):
        self.start_time = time.time()
        self.data = self.get_data()
        if shared_idx != []:
            self.idx = shared_idx
        self.results = []
        self.final = pd.DataFrame()
        return None

    def get_data(self):
        results = pd.DataFrame()
        return results

    def pivot(self, df, vals="Temp", rename_dict={}, agg="last"):
        result = pd.pivot_table(df, values=vals, index=self.idx, aggfunc=agg)
        result.rename(columns=rename_dict, inplace=True)
        return result

    def concat_pivots(self, li, save_name="Results/concat.csv", group=True):
        a = pd.concat(
            [df for df in util.clear_empty_df(li)], axis=1, join="outer"
        ).reset_index()
        if group:
            a = a.groupby(level=0, axis=1).sum()
        if save_name != "":
            a.to_csv(save_name)
        return a

    def spread(self, df, spread_vals, spread_name):
        df["Min" + spread_name] = df[spread_vals].min(axis=1)
        df["Max" + spread_name] = df[spread_vals].max(axis=1)
        df["Spread" + spread_name] = abs(
            df["Max" + spread_name] - df["Min" + spread_name]
        )
        df.drop(spread_vals, axis=1, inplace=True)
        return df

    def lambda_ex(self, df, vals, lim, type=">", rename_dict={}):
        if type == ">":
            agg = lambda x: (x > lim).sum()
        elif type == "<":
            agg = lambda x: (x < lim).sum()
        else:
            agg = lambda x: (x == lim).sum()

        result = pd.pivot_table(df, values=vals, index=self.idx, aggfunc=agg)
        result.rename(columns=rename_dict, inplace=True)
        return result

    def output(self, file_name="Results/result.csv"):
        result = self.concat_pivots(self.results, save_name=file_name)
        return result

    def graph(self, df, xname, yname, filename="", plttype="scatter", lims={}):
        if xname == "index":
            df.plot(use_index=True, y=yname, kind=plttype, colormap=cm.Dark2)
        else:
            df.plot(x=xname, y=yname, kind=plttype, colormap=cm.Dark2)

        if lims != {}:
            for key, val in lims.items():
                plt.axhline(y=val, color="r", linestyle="-", label=key)

        if filename != "":
            plt.savefig(rf"Results/{filename}")
        return None

    def print_time_taken(self):
        print(
            "Start Time",
            util.createStrTime(datetime.datetime.fromtimestamp(self.start_time)),
            "",
            "End Time",
            util.createStrTime(datetime.datetime.fromtimestamp(time.time())),
            "Total Time Taken",
            round(time.time() - self.start_time, 2),
        )


def main():
    """Main function used to run the program."""
    T = ExampleClass(
        df=pd.DataFrame,
    )
    T.print_time_taken()


if __name__ == "__main__":
    """[summary]"""
    main()
