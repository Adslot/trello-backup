#!/usr/bin/env python -u
from __future__ import unicode_literals
import os
import sys
import json
import requests
import time
import io
import logging
import argparse

API_URL = "https://api.trello.com/1/"


def get_organization_ids(ORGANIZATION_NAMES, API_KEY, TOKEN):
    """
    Translates Org Name to ID
    """
    selected_organizations = []
    for organization in ORGANIZATION_NAMES.split(','):
        selected_organizations.append(organization.strip())
    organization_ids = []

    # Parameters to get a list of organizations
    organizationsPayload = {
        'key': '{}'.format(API_KEY),
        'token': '{}'.format(TOKEN),
    }

    organizations = requests.get(API_URL + "members/me/organizations", params=organizationsPayload)
    if len(organizations.json()) <= 0:
        logger.error('No organizations found.')
    else:
        logger.info('Finding all Organizations.')
        for organization in organizations.json():
            if organization["name"].lower() in selected_organizations:
                organization_ids.append(organization["id"])
                logger.debug('Org Added: {}'.format(organization["id"]))
    return organization_ids

if __name__ == "__main__":

    # parse args
    parser = argparse.ArgumentParser(description="Trello Backup")
    parser.add_argument("-k", "--key", help="Trello API Key")
    parser.add_argument("-t", "--oauth-token", help="Trello OAuth Token")
    parser.add_argument("-d", "--directory", required=True, help="Directory to save JSON files, created if non exist")
    parser.add_argument("-l", "--log", help="Logging level - info|INFO|WARNING|ERROR|CRITICAL")
    parser.add_argument("-a", "--appname", required=True, help="Trello App Name")
    parser.add_argument("-o", "--orgid", help="Organisation by ID to backup. ")
    parser.add_argument("-n", "--orgname", help="Organisation by Name to backup")

    args = parser.parse_args()

    API_KEY = args.key
    TOKEN = args.oauth_token
    OUTPUT_DIRECTORY = args.directory
    APP_NAME = args.appname
    ORGANIZATION_IDS = ""
    ORGANIZATION_NAMES = ""
    if args.orgid:
        ORGANIZATION_IDS = args.orgid.lower()
    if args.orgname:
        ORGANIZATION_NAMES = args.orgname.lower()
    PRETTY_PRINT = 'yes'

    if args.log is not None:
        log_level = args.log.upper()
    else:
        log_level = "INFO"
    # Create our logger
    logger = logging.getLogger('root')
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if not API_KEY:
        logger.error('You need an API key to run this app.')
        logger.error('Visit this url: https://trello.com/1/appKey/generate, and re-run script')
        sys.exit(1)

    if not TOKEN:
        logger.error('You need a token to run this app.')
        logger.error("Visit this url: {0}connect?key={1}&name={2}&response_type=token&expiration={3}".format(
            API_URL,
            API_KEY,
            APP_NAME,
            "never"))
        logger.error("Then re-run script")
        sys.exit(1)

    if ORGANIZATION_NAMES and not ORGANIZATION_IDS:
        ORGANIZATION_IDS = get_organization_ids(ORGANIZATION_NAMES, API_KEY, TOKEN)
        if len(ORGANIZATION_IDS) < 1:
            logger.error('Finding Org ID failed.')
            sys.exit(1)

    # Parameters to get list of boards
    boardsPayload = {
        'key': '{}'.format(API_KEY),
        'token': '{}'.format(TOKEN),
        'filter': 'open',
        'lists': 'open',
    }
    # Parameters to get board contents
    boardPayload = {
        'key': '{}'.format(API_KEY),
        'token': '{}'.format(TOKEN),
        'lists': 'open',
        'fields': 'all',
        'actions': 'all',
        'action_fields': 'all',
        'actions_limit': '1000',
        'cards': 'all',
        'card_fields': 'all',
        'card_attachments': 'true',
        'lists': 'all',
        'list_fields': 'all',
        'members': 'all',
        'member_fields': 'all',
        'checklists': 'all',
        'checklist_fields': 'all',
        'organization': 'false',
    }

    for org_id in ORGANIZATION_IDS:
        boards = requests.get(API_URL + "organizations/" + org_id + "/boards", params=boardsPayload)
        try:
            if len(boards.json()) <= 0:
                logger.info('No boards found under Organisation ID: {}'.format(org_id))
        except ValueError:
            logger.error('Unable to access your boards. Check your key and token.')
            sys.exit(1)
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)

        logger.info('Backing up boards:')
        epoch_time = str(int(time.time()))

        for board in boards.json():
            if ORGANIZATION_IDS and (not board["idOrganization"] or not board["idOrganization"] in ORGANIZATION_IDS):
                continue

            logger.info(" {0} ({1})".format(board["name"], board["id"]))
            boardContents = requests.get(API_URL + "boards/" + board["id"], params=boardPayload)
            with io.open(OUTPUT_DIRECTORY + '/{0}_'.format(board["name"].replace("/", "-")) + epoch_time + '.json',
                         'w', encoding='utf8') as file:
                args = dict(sort_keys=True, indent=4) if PRETTY_PRINT else dict()
                data = json.dumps(boardContents.json(), ensure_ascii=False, **args)
                file.write(data)
