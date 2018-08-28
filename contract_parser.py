"""
Module for parsing the completed contracts dataframe with duration and spending
calculations data returned from the calculations module.  It filters the
dataframe to generate separate excel workbooks for each division using agency
contracts and creates sheets in each for the key watchlists for managing
contracts:  contracts expiring by a certain date and heavily spent contracts.

It creates a temporary workbook folder and pushes any returned files there to
support functions for managing storage from longterm use of the program and the
generated watchlist files.
"""

from datetime import datetime as dt
import os
import pandas as pd
# custom module for running DGS contract management formulas
from calculations import contracts

def generate_watchlist_workbooks():
    """
    Function creates a folder labeled 'temporary_workbooks_folder' and saves
    excel workbooks for each division using contracts. Each workbook contains
    separate named sheets for high burning contracts, contracts expiring in 3
    months and contracts expiring in 6 months for each division if, there are
    contracts meeting those conditions.

    Where conditions are not met and there are no contracts meeting a particular
    category no sheet is added to the workbook for that criteria.  Files are
    generated with the following naming convention indicating the division and
    the program run date:

            division-blankets-month-day-year.xlsx
            example:
                facilities-blankets-05-15-18.xlsx

    Function returns a list of the filenames created enabling the function call
    to be used to open, attach or access the files generated for each division.
    """
    # generate excel files & writers dynamically based on divisions using contracts
    excel_writers = {}
    filenames = []
    for div in contracts['division'].unique():
        key = '{}'.format(div)

        # create temp directory for holding program generated files in order
        # to delete sent files and catch and retain files for emails that
        # failed to send in messenger.py
        filepath = 'temporary_workbooks_folder'
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filenames.append(os.path.join(filepath,
                                     '{}-blankets-{}.xlsx'.format(key.lower(),dt.today().strftime('%m-%d-%y'))))

        excel_writers[key] = pd.ExcelWriter(os.path.join(filepath,'{}-blankets-{}.xlsx'.format(key.lower(),dt.today().strftime('%m-%d-%y'))))

        if len(contracts[(contracts['division']==div)&(contracts['burn_status']=='high')]) < 1:
            pass
        else:
            contracts[(contracts['division']==div)&\
                      (contracts['burn_status']=='high')].to_excel(excel_writers[div],'high burn rate')

        # parse contracts dataframe based on 3 month and 6 month expirations
        for trigger in [3,6]:
            if trigger == 3:
                if len(contracts[(contracts['months_left']<=trigger)&(contracts['division']==div)]) < 1:
                    pass
                else:
                    contracts[(contracts['months_left']<=trigger)&\
                              (contracts['division']==div)].to_excel(excel_writers[div],'expire 90 days')

            else:
                if len(contracts[(contracts['months_left']<=trigger)&(contracts['division']==div)]) < 1:
                    pass
                else:
                    contracts[(contracts['months_left']<=trigger)&\
                              (contracts['division']==div)].to_excel(excel_writers[div],'expire 180 days')

        excel_writers[div].save()

    return filenames

if __name__ == '__main__':
    generate_watchlist_workbooks()
