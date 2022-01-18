import io
import pandas as pd
import requests

from typing import Dict, Iterable, List


def fetch_data(url : str) -> pd.DataFrame :
    """
    Fetches the data from a given url and returns it in the form of a Pandas DataFrame.
    Data must be semicolon-separated CSV.

    :param url: the url to fetch the data from
    :return: the generated dataframe
    """

    # Fetch data
    response = requests.request("GET", url)

    # Convert to dataframe
    raw_csv = response.content.decode("utf-8")
    data = pd.read_csv(io.StringIO(raw_csv), sep = ";", low_memory = False)

    return data


def get_region_data(data : pd.DataFrame,
                    regions : Iterable[str]) -> Dict[str, pd.DataFrame] :
    """
    Returns the regional data from a general dataset.

    :param data: the general dataset
    :param regions: the regions to select
    :return: a dictionary containing all the separate dataframes
    """

    to_remove = ["dep", "jour", "cl_age90", "pop"]

    reg_data = {}

    for region in regions :
        tmp : pd.DataFrame = data.loc[data.dep == region]
        tmp.set_index(pd.to_datetime(tmp.jour), inplace = True)
        tmp = tmp.drop(columns = to_remove)
        tmp = tmp.groupby(level = "jour").sum()
        tmp = tmp.sort_index()
        tmp = tmp.asfreq("D")

        reg_data[region] = tmp

    return reg_data




