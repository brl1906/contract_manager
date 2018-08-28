"""
Module for managing file and storage size of
the temporary folder for longterm use of the program
and easily identifying which contract management
watchlists failed to send to target divisions.
"""
import os

def clean_temporary_folder(outbound_files):
    """
    Function removes files from the temporary folder if they have been
    sent via email. Primary purposes of this function are to:
        1. manage memory utilization of program generated files
        2. provide a capture for files that were not sent due to problematic
        email addresses so it is easy to identify the intended recipient,
        date and file

    The program checks for and deletes sucessfully sent excel workbooks from
    'temporary_workbooks_folder'
    """
    before = len(os.listdir('temporary_workbooks_folder/'))
    for item in os.listdir('temporary_workbooks_folder/'):
        # keep non-file objects like .files
        if os.path.isfile('temporary_workbooks_folder/{}'.format(item)) == False:
            pass
        else:
            if 'temporary_workbooks_folder/{}'.format(item) in outbound_files:
                os.remove('temporary_workbooks_folder/{}'.format(item))

    after = len(os.listdir('temporary_workbooks_folder/'))
    print('{} files deleted'.format(before - after))

    return (before - after)
