Trello Backup
=============

This simple app backs up your Trello boards as JSON files to a local directory.

## Setup

- Copy `trello-backup.config.sample` to `trello-backup.config` and edit accordingly
- run `trello-backup.py -c trello-backup.config -d directory_to_save_json` and follow the prompts to Generate a Trello API Key and OAuth Token

All arguments can be overridden by parameters via commandline

**Note**: The user must be added to the organisation(s)


## Usage: 

```
usage: trello-backup.py [-h] [-c CONFIG] [-d OUTPUT_DIRECTORY] [-a APP_NAME]
                        [-k API_KEY] [-t TOKEN] [-e TOKEN_EXPIRATION]
                        [-l LOG_LEVEL] [-o ORGANIZATION_IDS]
                        [-n ORGANIZATION_NAMES]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify Config File
  -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Directory to save JSON files, created if it does not
                        exist
  -a APP_NAME, --app_name APP_NAME
                        Trello App Name
  -k API_KEY, --api_key API_KEY
                        Trello API Key
  -t TOKEN, --token TOKEN
                        Trello OAuth Token
  -e TOKEN_EXPIRATION, --token_expiration TOKEN_EXPIRATION
                        Trello Token Expiration
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        Logging level - info|INFO|WARNING|ERROR|CRITICAL
  -o ORGANIZATION_IDS, --organization_ids ORGANIZATION_IDS
                        Organisation by ID(s) to backup.
  -n ORGANIZATION_NAMES, --organization_names ORGANIZATION_NAMES
                        Organisation by Name(s) to backup

```
