Trello Backup
=============

This simple app backs up your Trello boards as JSON files to a local directory.

Setup
-----
- run `trello-backup.py -a "AppName" -d directory_to_save_json` and follow the prompts to Generate a Trello API Key and OAuth Token


```
usage: trello-backup.py [-h] [-k KEY] [-t OAUTH_TOKEN] -d DIRECTORY [-l LOG]
                        -a APPNAME [-o ORGID] [-n ORGNAME]

Trello Backup

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Trello API Key
  -t OAUTH_TOKEN, --oauth-token OAUTH_TOKEN
                        Trello OAuth Token
  -d DIRECTORY, --directory DIRECTORY
                        Directory to save JSON files, created if non exist
  -l LOG, --log LOG     Logging level - info|INFO|WARNING|ERROR|CRITICAL
  -a APPNAME, --appname APPNAME
                        Trello App Name
  -o ORGID, --orgid ORGID
                        Organisation by ID to backup.
  -n ORGNAME, --orgname ORGNAME
                        Organisation by Name to backup

```
