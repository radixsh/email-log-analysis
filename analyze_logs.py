import csv
import sys
import os

permissible_replies = ["automatic reply", "away", "out of office"]

def outlook_incoming(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

    def new_recipient_outlook(row, domains, recipients):
        # The gmx things will be counted in new_recipient_gmail(), so don't
        # double-count them here
        to_ignore = ["journal", "gmx"]
        return row["Recipients"] not in recipients \
                and any(d in row["Recipients"] for d in domains) \
                and not any(word in row["Recipients"] for word in to_ignore)

    recipients = []
    inbox_count = 0
    for row in reader:
        # Count unique recipients
        if new_recipient_outlook(row, domains, recipients):
            recipients.append(row['Recipients'])

            if "Inbox" in row['Latest delivery location']:
                inbox_count += 1

    print(f"Unique recipients:\t{len(recipients)}")
    print(f"Sent to inbox:\t\t{inbox_count}")

    csv_file.close()

def outlook_outgoing(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

    def new_responder_outlook(row, domains, responders):
        return row['Sender address'] not in responders \
                and any(d in row['Sender address'] for d in domains) \
                and not any (s in row['Subject'].lower() for s in permissible_replies)

    responders = []
    for row in reader:
        # Count unique responders
        if new_responder_outlook(row, domains, responders):
            responders.append(row['Sender address'])

            # Print details so we can notify each victim
            print(f"{row['Sender address']}\t\t"
                  f"{row['Recipients']}\t\t{row['Subject']}")

    print(f'Total: {len(responders)}')
    csv_file.close()

def gmail_incoming(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

    def new_recipient_gmail(row, domains, recipients):
        return row["Recipient address"] not in recipients \
                and any(d in row["Recipient address"] for d in domains) \
                and "journal" not in row["Recipient address"]

    recipients = []
    subjects = []
    inbox_count = 0
    for row in reader:
        # Lots of duplicate logs
        if "SMTP_" in row['Event target']:
            continue

        # Count unique recipients
        if new_recipient_gmail(row, domains, recipients):
            recipients.append(row['Recipient address'])

            if row['Subject'] not in subjects:
                subjects.append(row['Subject'])

            if "GMAIL_INBOX" in row['Event target']:
                inbox_count += 1

    print(f"Unique recipients:\t{len(recipients)}")
    print(f"Sent to Gmail inbox:\t{inbox_count}")
    print(f"Subject lines:\t\t{','.join(subjects)}")

    csv_file.close()

def gmail_outgoing(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

    def new_responder_gmail(row, domains, responders):
        return row['Sender'] not in responders \
                and any(d in row['Sender'] for d in domains) \
                and not any(s in row['Subject'].lower() for s in permissible_replies)

    responders = []
    for row in reader:
        # Count unique responders
        if new_responder_gmail(row, domains, responders):
            responders.append(row['Sender'])

            # Print details so we can notify each victim
            print(f"{row['Sender']}\t\t"
                  f"{row['Recipient address']}\t\t{row['Subject']}")

    print(f"Total: {len(responders)}")
    csv_file.close()

def main():
    if len(sys.argv) < 3:
        print("Usage: ./analyze_logs.py subdir domains.txt")
        sys.exit()

    path = sys.argv[1]
    contents = os.listdir(path)
    filenames = {}
    for name in contents:
        full_path = os.path.join(path, name)
        if not os.path.isfile(full_path):
            print(f"Skipping {full_path}")
            continue

        if "outlook" in full_path and "incoming" in full_path:
            filenames["outlook_infile"] = full_path
        elif "outlook" in full_path and "outgoing" in full_path:
            filenames["outlook_outfile"] = full_path
        elif "gmail" in full_path and "incoming" in full_path:
            filenames["gmail_infile"] = full_path
        elif "gmail" in full_path and "outgoing" in full_path:
            filenames["gmail_outfile"] = full_path

    domains_file = open(sys.argv[2], 'r')
    domains = [d.strip() for d in domains_file.readlines()]

    # Do it this way to control the order of output
    if "outlook_infile" in filenames.keys():
        # Outlook incoming: recipients, received to inbox
        print(f"========= OUTLOOK INCOMING ({filenames['outlook_infile']})")
        outlook_incoming(filenames["outlook_infile"], domains)

    if "outlook_outfile" in filenames.keys():
        # Outlook outgoing: number of replies
        print(f"========= OUTLOOK OUTGOING ({filenames['outlook_outfile']})")
        outlook_outgoing(filenames["outlook_outfile"], domains)

    if "gmail_infile" in filenames.keys():
        # Gmail incoming: recipients, received to inbox
        print(f"========= GMAIL INCOMING ({filenames['gmail_infile']})")
        gmail_incoming(filenames["gmail_infile"], domains)

    if "gmail_outfile" in filenames.keys():
        # Gmail outgoing: number of replies
        print(f"========= GMAIL OUTGOING ({filenames['gmail_outfile']})")
        gmail_outgoing(filenames["gmail_outfile"], domains)

if __name__ == "__main__":
    main()
