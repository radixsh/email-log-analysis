import csv
import sys

'''
./outlook_outgoing.py to_scammer.csv domains.txt

This script reads Outlook data (CSV) and identifies email addresses in our
domains who responded to a particular scammer.

to_scammer.csv: a CSV downloaded from Outlook Threat Explorer, containing all
outgoing emails from our organization to a particular scammer

domains.txt: a text file containing our domains, separated by newlines
'''

def new_victim(row, domains, responders):
    to_ignore = ["automatic reply", "away", "out of office"]
    return row['Sender address'] not in responders \
            and any(d in row['Sender address'] for d in domains) \
            and not any (s in row['Subject'].lower() for s in to_ignore)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./outlook_outgoing.py to_scammer.csv domains.txt")
        sys.exit()

    csv_file = open(sys.argv[1], 'r')
    reader = csv.DictReader(csv_file)

    domains_file = open(sys.argv[2], 'r')
    domains = [d.strip() for d in domains_file.readlines()]

    responders = []
    for row in reader:
        # Count unique responders
        if new_victim(row, domains, responders):
            responders.append(row['Sender address'])

            # Print details so we can notify each victim
            print(f"{row['Sender address']}\t\t{row['Recipients']}\t\t{row['Subject']}")

    print(f'Total: {len(responders)}')

    csv_file.close()
    domains_file.close()

if __name__ == "__main__":
    main()
