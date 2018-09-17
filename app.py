import contract_parser,messenger


if __name__ == '__main__':
    deliver_reports = messenger.send_emails()
    create_memos = contract_parser.generate_pdfs()
    try:
        deliver_reports
        create_memos
    except:
        pass
