import csv
import sys
import os

# def new_recipient_gmail(row, domains, recipients):
#     return row['Recipient address'] not in recipients \
#             and any(d in row['Recipient address'] for d in domains) \
#             and "journal" not in row['Recipient address']

def new_recipient_outlook(row, domains, recipients):
    return row['Recipients'] not in recipients \
            and any(d in row['Recipients'] for d in domains) \
            and "journal" not in row['Recipients']

def outlook_incoming(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

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

def new_outlook_target(row, domains, responders):
    to_ignore = ["automatic reply", "away", "out of office"]
    return row['Sender address'] not in responders \
            and any(d in row['Sender address'] for d in domains) \
            and not any (s in row['Subject'].lower() for s in to_ignore)

def outlook_outgoing(filename, domains):
    csv_file = open(filename, 'r')
    reader = csv.DictReader(csv_file)

    responders = []
    for row in reader:
        # Count unique responders
        if new_outlook_target(row, domains, responders):
            responders.append(row['Sender address'])

            # Print details so we can notify each victim
            print(f"{row['Sender address']}\t\t"
                  f"{row['Recipients']}\t\t{row['Subject']}")

    print(f'Total: {len(responders)}')

    csv_file.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: ./analyze_logs.py logs_dir domains.txt")
        sys.exit()

    path = sys.argv[1]
    contents = os.listdir(path)
    fps = {}
    for name in contents:
        full_path = os.path.join(path, name)
        if not os.path.isfile(full_path) and full_path[-4:] == ".csv":
            continue
        if "outlook" in full_path and "in" in full_path:
            fps['outlook_infile'] = full_path
        elif "outlook" in full_path and "out" in full_path:
            fps['outlook_outfile'] = full_path
        elif "gmail" in full_path and "in" in full_path:
            fps['gmail_infile'] = full_path
        elif "gmail" in full_path and "out" in full_path:
            fps['gmail_outfile'] = full_path

    domains_file = open(sys.argv[2], 'r')
    domains = [d.strip() for d in domains_file.readlines()]
    
    # Outlook incoming: recipients, received to inbox
    print(f"========= OUTLOOK INCOMING ({fps['outlook_infile']})")
    outlook_incoming(fps["outlook_infile"], domains)

    # Outlook outgoing: number of replies
    print(f"========= OUTLOOK OUTGOING ({fps['outlook_outfile']})")
    outlook_outgoing(fps["outlook_outfile"], domains)

    # Gmail incoming: recipients, received to inbox
    print(f"========= GMAIL INCOMING ({fps['gmail_infile']})")
    
    # Gmail outgoing: number of replies
    print(f"========= GMAIL OUTGOING ({fps['gmail_outfile']})")
    
if __name__ == "__main__":
    main()