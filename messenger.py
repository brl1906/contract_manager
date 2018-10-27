"""
Module for sending email with attachments for spreadsheets
of contracts requiring attention for each division. Module
also includes a method for cleaning a temporary folder
for the reports.
"""
import configparser
import os
import smtplib
import sys

from datetime import datetime as dt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import contract_parser # custom module for parsing target crieteria
import wiper # module for cleaning sucessfully emailed files from temp folder

def send_emails():
    """
    Function uses an SMTP connection to send an email with Gmail secured via TLS
    for each of the divisions using contracts and attaches a separate excel
    workbook file with contract management watchlist spreadhseets for: high
    burning contracts, contracts expiring in 3 months and, contracts expiring in
    6 months for each division.

    It performs 3 main tasks:
        1. emails the target reports from their location in temporary folder
        2. returns a list of all files sucessfully attached and emailed
        3. deletes sucessfully sent files from temporary folder

    The email recipient is set as a default value in the make_email() function.
    It can be changed by passing a valid email address to the recipient
    parameter.

    It relies upon the make_email() function to generate the template for each
    email and relies upon the contract_parser module which evaluates each active
    contract to determine if they meet the above watchlist criteria and returns
    excel workbook files for each division. The make_email() function takes
    advantage of the naming convention for generating files in the
    contract_parser module's generate_watchlist_workbooks() method to indicate
    the relevant division in the email subject line and to provide access to the
    list of files generated for each division as return value of the function.
    """
    sent_files = []
    config = configparser.ConfigParser()
    config.read('configuration/config.ini')

    def make_email(file, division, recipient=config['Email']['email_address']):
        """
        Function takes 2 parameters, the name of the file to be sent as an attachment
        and the name of the division using the contracts in the file.

        It constructs an email notifying which contracts require action due to having
        a high burn rate and or approaching expiration and attaches the relevant
        excel file.  The email is built using Gmail
        """
        sender = config['Email']['email_address']
        password = config['Email']['password']

        msg = MIMEMultipart()
        # change recipient to AP contract manager
        msg['To'] =  recipient
        msg['From'] = sender
        msg['Subject'] = '{} Contract Management Watchlist {}'.format(division,
            dt.today().strftime('%m-%d-%y'))
        body = MIMEText(
    'Attached please find the contract management report for \
your division indicating those contracts requiring your attention due to:\n\
\t1) a high burn rate, and or\n\t2) approaching contract expiration.')
        msg.attach(body)

        with open(file, 'rb') as f:
            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(f.read())
            encoders.encode_base64(payload) # encode into base64
            payload.add_header('Content-Disposition',
                              'attachment; filename={}'.format(file.split('/')[1]))
            msg.attach(payload) # attach payload MIMEBase instance to the message

        smtpObj = smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.sendmail(msg['From'],msg['To'],msg.as_string())
        smtpObj.quit()
        print('{} message sent'.format(division))
        sent_files.append(file) # add sucessfully sent files to list

    try:
        for workbook in contract_parser.generate_watchlist_workbooks():
            make_email(file=workbook, division=workbook.split('/')[1].split('-')[0].capitalize())
    except Exception as e:
        # for help debugging
        e_type,e_obj,e_traceback = sys.exc_info()
        print('***{} is causing problems***'.format(str(e_traceback.tb_frame.f_code).split()[2]))

        print('Failure in object: {}\n'.format(e_traceback.tb_frame.f_code))
        print('Error type: {}\nError Message: {}\nError Location: line {}'.format(
            str(e_type).split("'")[1], e_obj, e_traceback.tb_lineno))

    # wipe files from sucessfully sent messages & track files failing to send
    clean_folder = wiper.clean_temporary_folder(outbound_files=sent_files)
    clean_folder

    # simple testing logic on performance of wiping folder clean
    if len(sent_files) == clean_folder:
        print('okay:: number of deleleted files is equal to files sent.')
    else:
        print('problem:: {} files sent but {} cleaned'.format(len(sent_files),clean_folder))

    return sent_files
