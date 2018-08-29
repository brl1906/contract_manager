"""
Module for documenting and running the calcultations
necessary to perform the contract management responsiblities
for duration based as well as spending or burn rate based
indicators for DGS contracts.
"""
import pandas as pd
import numpy as np
from datetime import datetime as dt
# custom module for preparing and returning relevant DGS dataframes
import fetcher

# Perform the calculations required for contract management tracking
def run_duration_formulas(df):
    """
    """
    df['duration_months'] = round((df['mb_end'] - df.index) / np.timedelta64(1,'M')).astype(int)
    df['months_left'] = [np.ceil(mos).astype(int)
                     for mos in (df['mb_end'] - dt.now()) / np.timedelta64(1,'M')]

    # calculate months passed on contract by taking the floor if above 1/2 month
    # passed and returning 1 month if not to be proactive and catch potential early
    # burner contracts that have extreme spending in initial months
    df['months_passed'] = [np.floor(mos).astype(int) if np.floor(mos) >= 1
                           else np.floor(mos).astype(int) + 1
                           for mos in  ((dt.now() - df.index) / np.timedelta64(1,'M'))]
    return df

def run_spending_formulas(df):
    """
    """
    estimated_months_before_limit_reached = [0 if np.isinf(np.floor(mos)) else
                                             np.floor(mos).astype(int)
                                             for mos in  df['mb_$_limit'] /(df['mb_$_spent']/df['months_passed'])]

    df['pct_spent'] = (df['mb_$_spent'] / df['mb_$_limit']) * 100
    df['desired_burn_rate'] = ((df['mb_$_limit'] / df['duration_months']) / df['mb_$_limit']) * 100
    df['burn_rate'] = ((df['mb_$_spent'] / df['months_passed']) / df['mb_$_limit']) * 100
    df['burn_status'] = np.where(df['burn_rate'] >= df['desired_burn_rate'],'high',
                        np.where(df['burn_rate'] <= df['desired_burn_rate']/3,'low','medium'))

    projected_limit_date = []
    for start,months in zip(df.index,estimated_months_before_limit_reached):
        projected_limit_date.append(start + pd.DateOffset(months=months))

    df['projected_limit_date'] = projected_limit_date
    df['watch_list_75%_spent'] = np.where(df['pct_spent'] >=75,'watch','safe')

    return df

def get_management_dataframe():
    """
    Function returns complete dataframe with contract management formulas
    run for both relevant measures of duration and spending levels. It
    first calls the duration formula function upon which the calculation of
    key spending formulas is dependent.

    The duration function returns a dataframe with columns providing data on
    remaining months, months since contract start and, contract duraton. The
    spending formula function is called on the returned dataframe and uses
    duration elements like duration or months passed to calculate indicators
    for desired burn rate, current burn rate and the estimated number of
    months remaining before a contract spending limit is reached.
    """
    return run_spending_formulas(run_duration_formulas(df))

# Get and prepare the necessary data
df = fetcher.create_contractmgmt_dataframe('data/Contract List.xlsx')
df = fetcher.fiscal_year(df)
df = fetcher.format_column_names(df)
# filter dataframe for active contracts
df = df[df['mb_end'] > dt.now()]
contracts = get_management_dataframe()
