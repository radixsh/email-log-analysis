import csv
import sys

'''
./gmail_incoming.py from_scammer.csv domains.txt

This script reads Gmail log data (CSV) and identifies email addresses in our
domains who responded to a particular scammer.

from_scammer.csv: a CSV downloaded from Gmail Log Search, containing all
outgoing emails from our organization to a particular scammer

domains.txt: a text file containing our domains, separated by newlines

Expected format of from_scammer.csv:
Message ID,Start date,End date,Sender,Message size,Subject,Direction,Attachments,Recipient address,Event target,Event date,Event status,Event target IP address,Has encryption,Event SMTP reply code,Event description,Client Type,Device User Session ID
'''

def new_recipient(row, domains, recipients):
    return row['Recipient address'] not in recipients \
            and any(d in row['Recipient address'] for d in domains) \
            and "journal" not in row['Recipient address']

def main():
    if len(sys.argv) != 3:
        print("Usage: ./gmail_incoming.py from_scammer.csv domains.txt")
        sys.exit()

    csv_file = open(sys.argv[1], 'r')
    reader = csv.DictReader(csv_file)

    domains_file = open(sys.argv[2], 'r')
    domains = [d.strip() for d in domains_file.readlines()]

    recipients = []
    inbox_count = 0
    for row in reader:
        # Lots of duplicate logs
        if "SMTP_" in row['Event target']:
            continue

        # Count unique recipients
        if new_recipient(row, domains, recipients):
            recipients.append(row['Recipient address'])

            if "GMAIL_INBOX" in row['Event target']:
                inbox_count += 1

    print(f"Unique recipients:\t{len(recipients)}")
    print(f"Sent to Gmail inbox:\t{inbox_count}")

    csv_file.close()
    domains_file.close()

if __name__ == "__main__":
    main()
