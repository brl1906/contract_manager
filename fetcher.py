"""
Module for getting, cleaning and returning formatted
data for the contract management program
"""
import pandas as pd
import numpy as np

def create_contractmgmt_dataframe(filepath, sheet='master', idx_col='MB START',
                                cols=['PO','BUYER','MB START','MB END',
                                'DESCRIPTION','VENDOR','MB $ LIMIT','MB $ SPENT',
                                'Division','Options Remaining','Option (Y/N)',
                                'Comments','Spending Comments']):
    """
    Function creates a dataframe indexed to the master blanket start
    date for the contract management excel workbook. It drops all pre-
    calculated columns for transparancy and uses 13 select columns by
    default. Additional columns can be included or excluded by changing the
    cols variable to include or exclude desired columns if they exist in
    the workbook.
    """
    df = pd.read_excel(filepath,sheet_name=sheet,index_col=idx_col,usecols=cols)
    return df

def fiscal_year(df):
    """
    Function takes a dataframe with a DateTimeIndex and
    returns dataframe with corresponding fiscal year as a
    four digit year for each date on the index of the dataframe.
    It drops any rows that do not have a pandas timestamp as
    its index to match size of dataframe index and the fiscal
    year list object which is added to dataframe as pandas series.

    The function is based on the Maryland Govt fiscal year which
    runs from July 1st to June 30th.
    """
    for i,idx in enumerate(df.index):
    # drop rows if observation is not a timestamp
        if isinstance(idx, pd._libs.tslib.NaTType):
            df.drop(df.index[i],axis=0,inplace=True)

    fiscal_year = np.where(df.index.month >= 7,df.index.year+1,df.index.year)
    df['fiscal_year'] = fiscal_year
    return df


def format_column_names(df):
    """
    Function takes dataframe and changes column headers to
    lower case, replaces spaces with underscores, and drops any
    columns that are not strings or don't have a lower case
    attribute."""
    cols = []
    for col in df.columns:
        try:
            col.lower()
            cols.append(col.lower().replace(' ','_'))
        except:
            df.drop(col,axis=1,inplace=True)

    df.columns = cols
    return df
