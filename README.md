# Email log analysis scripts
This is a script I wrote at work for gleaning phishing campaign data from
Outlook Threat Explorer and Gmail Log Search data. Run the script with
`./analyze_logs.py data_dir domains.txt`.

The first argument, `data_dir`, is the name of a folder containing data from the
admin portal GUIs of Microsoft Threat Explorer and Gmail Log Search.

The second argument, `domains.txt`, is a text file containing domains (or
subdomains) separated by newlines. These domains are the domains we care about.
For instance, we could write the line `example.com`. This would tell our script
to look for phishing emails received by (or responded to by) people whose email
addresses end in "@example.com".

## How to get the logs from the admin portal GUIs
### Outlook Threat Explorer
- Set search scope to the last month or so
- Search for messages where the sender is a particular scammer. Download this
data, and call it `outlook_incoming.csv`.
	- This is largely tolerable because example.com will always be a target of
	phishing attempts and spam.
- Search for messages where the recipient is a particular scammer. Download this
data, and call it `outlook_outgoing.csv`.
	- These are all the Outlook people at our organization who fell for this scam :(

### Gmail Log Search
- Set search scope to the last month or so
- Search for messages where the sender is a particular scammer. Download this
data, and call it `gmail_incoming.csv`.
	- Again, this is fine; we're only downloading this to log some statistics
	internally
- Search for messages where the recipient is a particular scammer. Download this
data, and call it `gmail_outgoing.csv`.
	- These are all the phishing victims at the Example organization whose email
	accounts are managed by Google
