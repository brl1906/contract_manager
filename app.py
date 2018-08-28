import messenger


if __name__ == '__main__':
    deliver_reports = messenger.send_emails()
    try:
        deliver_reports
    except:
        pass
