# Email log analysis scripts
These are some scripts I wrote at work for gleaning phishing campaign data from
Outlook Threat Explorer and Gmail Log Search data.

Each script can be run like this:
```./script.py data.csv domains.txt```

The first argument, `data.csv`, is data downloaded via the GUIs of Microsoft
Threat Explorer and Gmail Log Search, within the admin portals of each.

The second argument, `domains.txt`, is a text file containing domains (or
subdomains) separated by newlines. These domains are the domains we care about:
that is, we don't care if someone @gmail.com responds to an external phishing
threat, but we do care if someone @example.com (if we are an organization called
Example) responds to a phishing attempt.

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

## Running the scripts
```sh
$ ./{gmail,outlook}_{incoming,outgoing}.py data.csv domains.txt```
