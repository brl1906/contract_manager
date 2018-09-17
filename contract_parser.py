"""
Module for parsing the completed contracts dataframe with duration and spending
calculations data returned from the calculations module.  It does 2 things:
1) First, it filters the dataframe to generate separate excel workbooks for each
division using agency contracts and creates sheets in each for the key
watchlists for managing contracts:  contracts expiring by a certain date and
heavily spent contracts. In doing this it creates a temporary workbook folder
and pushes any returned files there to support functions for managing storage
from longterm use of the program and the generated watchlist files.

2) Secondly, it generates parses the contracts to determine which ones require
a change order memo and generates a PDF file of change order memo for each of
the contracts that has a high burn rate and is in danger of exceeding the limit.
In doing this it creates a chageorder_memos folder and pushes the memos there.
Each PDF file for change order memo is generated with the naming convention of:
po_number-changeorder-Month-Day-Year.pdf   for example:
    >> P12246-changeorder-09-12-18.pdf
"""

from datetime import datetime as dt
from fpdf import FPDF
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


class PDF(FPDF):
    """
    Create pdf memo document with City seal header and page number footer.
    """
    def header(self):
        """
        Create header for pdf page.
        ---------------------------
        default settings include image file of city seal saved
        in project folder and Arial bold, size 15 font.
        """
        self.image('images/from_head.png',w=190, h=40 )
        self.set_font('Arial', 'B', 15)
        self.cell(55) # shift right roughly center
        #self.cell(85, 10, 'INTERAGENCY MEMORANDUM', 1, 0, 'C')
        self.ln(2)

    def footer(self):
        """
        Create footer for pdf page.
        ---------------------------
        default settings include Arial italicized, size 8 font and
        centered page numbers.
        """
        self.set_y(-15) # set footer 1.5 cm from bottom
        self.set_font('Arial', 'I', 8)
        # page number
        self.cell(0, 10, 'page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def memo(recipient,months_remaining,pct_spent,description,amount,
                limit,po_number,expiration,division=''):
    """
    Generate pdf file of change order memo for a contract.
    ------------------------------------------------------
    required argments:
        recipient        --> string
        months_remaining --> integer
        pct_spent        --> float
        description      --> string
        amount           --> float
        limit            --> float
        po_number        --> string
        expiration       --> datetime timestamp object

    optional argument:
        division         --> string

        example function call:
                memo(recipient='michael b jordan', months_remaining=8,
                            pct_spent=89, description='Description of Contract..',
                            amount=12345.67, limit=70000, po_number='P1224',
                            expiration=pd.to_datetime('2019-06-24 00:00:00'),
                            division='Fleet')

        >>> P1224-changeorder-amount-09-12-18.pdf
    """

    recipient_address = ['Office of Procurement','7 East Redwood Sreet, 10th flr',
                        'Baltimore, MD 21202']
    pdf = PDF() # instantiate PDF class object
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font(family='Times',style='B',size=16)
    pdf.set_text_color(r=153,g=153,b=0)
    pdf.cell(w=10,h=5,txt='TO',border=0,ln=0)
    pdf.set_text_color(r=0,b=0,g=0)
    pdf.set_font(family='Times',style='',size=12)
    pdf.cell(w=20,h=5,txt='{}'.format(' '.join([part.capitalize() for part in recipient.split()])),border=0,ln=0)

    pdf.cell(w=100,h=5,txt='',ln=0)
    pdf.set_font(family='Times',style='B',size=16)
    pdf.set_text_color(r=153,g=153,b=0)
    pdf.cell(w=10,h=5,txt='DATE:',border=0,ln=0)
    pdf.set_font(family='Times',style='',size=12)
    pdf.cell(w=10,h=5,txt='',ln=0)
    pdf.set_text_color(r=0,b=0,g=0)
    pdf.cell(w=10,h=5,txt=dt.today().strftime('%B %d, %Y'),ln=1)
    pdf.cell(w=10,h=5,txt='',ln=0)

    for ln,text in enumerate(recipient_address):
        pdf.cell(100,5,text,ln=ln+.25)
    [pdf.ln() for i in range(2)]
    pdf.multi_cell(600,5,
                   txt = """
We are writing you to request a change order be issued in the amount of ${:,.2f}\
 to increase funding for \ncontract ________, Master Blanket Purchase Order {}.\
   This contract has {} months remaining and is \ndue to expire on {}. The total \
amount of ${:,.2f} is needed to continue to provide services\nthroughout the \
remainder of the contract life cycle and gaurd against potentially harmful \
gaps in service.\n\nThe description of the contract and relevant budget \
account number are below: \nDescription: "{}"\nBudget Account Number: \
2029-000000-1982-709500-_______ \n\nThis is an increase to the above \
referenced contract from ${:,.2f} to ${:,.2f}.  If you have any\nquestions \
whatsoever regarding the above, please contact __________. Thank you in \
advance for your thorough\nand celeritious response to this request.\n\n\n\n
cc: {} \n{}\n{}""".format(
                        amount, po_number, months_remaining,
                        '{} {}, {}'.format(expiration.strftime('%B'),expiration.day,expiration.year),
                        amount, description, limit, limit+amount,'Berke Attila',
                        division+' Division Chief', division+' Deputy Chief')
                  )

    [pdf.ln() for i in range(3)]
    pdf.image('images/signature.png',w=50,h=40)
    pdf.ln()
    pdf.cell(10,5,'AP Supervisor')
    # save to file
    filepath = 'changeorder_memos'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    pdf.output(os.path.join(filepath,'{}-changeorder-{}.pdf'.format(po_number,dt.today().strftime('%m-%d-%y'))))



def generate_pdfs(rcpnt='marcia diggs',percent_of_limit=10):
    """
    Generate change order memo as pdf for each high burning contract
    -----------------------------------------------------------------
    optional arguments:
        rcpnt              --> string   (default value for memo recpient)
        percent_of_limit   --> int      (default vaule for amount of request as
                                         a percentage of the blanket limit)

    """
    high_df = contracts[contracts['burn_status']=='high']
    for index,row in high_df.iterrows():
        memo(recipient=rcpnt,
                months_remaining=row['months_left'],
                pct_spent=row['pct_spent'],
                description=row['description'],
                amount=(row['mb_$_limit']/ percent_of_limit),
                limit=row['mb_$_limit'],
                po_number=row['po'],
                expiration=row['mb_end'],
                division=row['division'])
    print('generate_pdfs function run complete.')


if __name__ == '__main__':
    generate_watchlist_workbooks()
    generate_pdfs()
