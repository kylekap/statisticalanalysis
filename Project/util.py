import datetime
import os
import pandas as pd
import platform  # For getting the operating system name
import subprocess  # For executing a shell command


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Building the command. Ex: "ping -c 1 google.com"
    command = ["ping", param, "1", host]

    return subprocess.call(command) == 0


def clear_empty_df(df_list):
    return [df for df in df_list if not df.empty]


def prepend(the_list, the_str):
    """Add string to the front of each item in a list

    Args:
        list (list): List of values
        str (string): string to prepend
    """

    the_str += "{0}"
    the_list = [the_str.format(i) for i in the_list]
    return the_list


def createStrTime(the_date_time):
    """Takes a datetime type and returns as a formatted string

    theDateTime: datetime.datetime value

    Return: string datetime in the format %m/%d/%Y, %H:%M:%S
    """

    if the_date_time == None:
        the_date_time = datetime.now()
    elif type(the_date_time) == type(1.0):
        the_date_time = datetime.datetime.fromtimestamp(the_date_time)
    return the_date_time.strftime("%m/%d/%Y, %H:%M:%S")


def createDatetime(the_date_str):
    """Takes a string date type and returns as a datetime

    theDate: string date value formatted %m/%d/%Y, %H:%M:%S

    Return: datetime formatted date.
    """

    if the_date_str is None:
        date_time_value = datetime.now()
    else:
        date_time_value = the_date_str
    return datetime.strptime(date_time_value, "%m/%d/%Y, %H:%M:%S")


def createDateRange(startDate, endDate):
    """Takes a starting & ending date as strings, and returns a monthly interval between them

    theDateTime: datetime.datetime value

    Return: string datetime in the format %m/%d/%Y, %H:%M:%S
    """

    return (
        pd.date_range(startDate, endDate, freq="MS")
        .strftime("%m/%d/%Y, %H:%M:%S")
        .tolist()
    )


def fileNeedCreate(srcpath, fname):
    """Checks if a file exists in the srcpath folder. Will create srcpath if it doesn't exist.

    srcpath: source folder (i.e. "H://FOLDER)

    fname: file name to check (i.e. "A.CSV")
    """
    if not os.path.exists(srcpath):  # if the file directory doesn't exist, create it
        os.makedirs(srcpath)
    return not os.path.exists(os.path.join(srcpath, fname))


def createStrDate(theDatetime):
    """Creates a YYYY_M formatted string from a datetime"""
    return theDatetime.strftime("%Y_%m")


def asset_fill(df):
    """[summary]

    Args:
        df_asset ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Reindex to minute by minute
    rng = pd.date_range(df_asset.index.min(), df_asset.index.max(), freq="T")
    df_asset.reindex(rng)
    # subset?
    df_asset = df_asset.apply(pd.to_numeric, errors="ignore")
    df_asset.ffill(inplace=True)
    df_asset.bfill(inplace=True)
    # remove common string from all column names
    # df_asset.columns = list(map(lambda x: x.replace(asset_name, ""), df_asset.columns))
    return df_asset
