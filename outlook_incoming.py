import csv
import sys

'''
./outlook_incoming.py from_scammer.csv domains.txt

This script reads Outlook data (CSV) and counts up unique email addresses in our
domains who received messages from a particular scammer.

from_scammer.csv: a CSV downloaded from Outlook Threat Explorer, containing all
emails our organization received from a particular scammer

domains.txt: a text file containing our domains, separated by newlines
'''

def new_recipient(row, domains, recipients):
    return row['Recipients'] not in recipients \
            and any(d in row['Recipients'] for d in domains) \
            and "journal" not in row['Recipients']

def main():
    if len(sys.argv) != 3:
        print("Usage: ./outlook_incoming.py from_scammer.csv domains.txt")
        sys.exit()

    csv_file = open(sys.argv[1], 'r')
    reader = csv.DictReader(csv_file)

    domains_file = open(sys.argv[2], 'r')
    domains = [d.strip() for d in domains_file.readlines()]

    recipients = []
    inbox_count = 0
    for row in reader:
        # Count unique recipients
        if new_recipient(row, domains, recipients):
            recipients.append(row['Recipients'])

            if "Inbox" in row['Latest delivery location']:
                inbox_count += 1

    print(f"Unique recipients:\t{len(recipients)}")
    print(f"Sent to inbox:\t\t{inbox_count}")

    csv_file.close()
    domains_file.close()

if __name__ == "__main__":
    main()
