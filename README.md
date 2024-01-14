# scripts

Various scripts

## Installation

```console
poetry install
```

## Keepass to pass
First initialize pass on your computer, then export keepass data to csv and run:
```console
poetry run scripts-keepass_csv_to_pass <path to csv file>
```

This will create pass entries with the following format:
```
<Password>
username: <Username>
account: <Account>
website: <Website>
notes: <Notes>
```
Note: Any missing fields will be omitted from the entry.

