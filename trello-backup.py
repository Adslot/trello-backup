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
ORGANIZATION_IDS = ""
ORGANIZATION_NAMES = ""
log_level = "INFO"


def get_organization_ids(ORGANIZATION_NAMES, api_key, token):
    """
    Translates Org Name to ID
    """
    selected_organizations = []
    for organization in ORGANIZATION_NAMES.split(","):
        selected_organizations.append(organization.strip())
    ORGANIZATION_IDS = []

    # Parameters to get a list of organizations
    organizations_payload = {
        'key': '{}'.format(api_key),
        'token': '{}'.format(token),
    }

    organizations = requests.get(API_URL + "members/me/organizations", params=organizations_payload)
    if len(organizations.json()) <= 0:
        logger.error("No organizations found.")
    else:
        logger.info("Finding all Organizations.")
        for organization in organizations.json():
            if organization["name"].lower() in selected_organizations:
                ORGANIZATION_IDS.append(organization["id"])
                logger.debug("Org Added: {}".format(organization["id"]))
    return ORGANIZATION_IDS

if __name__ == "__main__":

    # parse args
    parser = argparse.ArgumentParser(description="Trello Backup")
    parser.add_argument("-d", "--directory", required=True,
                        help="Directory to save JSON files, created if it does not exist")
    parser.add_argument("-a", "--app-name", required=True, help="Trello App Name")
    parser.add_argument("-k", "--key", help="Trello API Key")
    parser.add_argument("-t", "--oauth-token", help="Trello OAuth Token")
    parser.add_argument("-l", "--log", help="Logging level - info|INFO|WARNING|ERROR|CRITICAL")
    parser.add_argument("-o", "--org-id", help="Organisation by ID to backup. ")
    parser.add_argument("-n", "--org-name", help="Organisation by Name to backup")

    args = parser.parse_args()

    api_key = args.key
    token = args.oauth_token
    output_directory = args.directory
    app_name = args.app_name
    if args.org_id:
        ORGANIZATION_IDS = args.org_id.lower()
    if args.org_name:
        ORGANIZATION_NAMES = args.org_name.lower()

    if args.log is not None:
        log_level = args.log.upper()

    # Create our logger
    logger = logging.getLogger("root")
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if not api_key:
        logger.error("You need an API key to run this app.")
        logger.error("Visit this url: https://trello.com/1/appKey/generate, and re-run script")
        sys.exit(1)

    if not token:
        logger.error("You need a token to run this app.")
        logger.error("Visit this url: {0}connect?key={1}&name={2}&response_type=token&expiration={3}".format(
            API_URL,
            api_key,
            app_name,
            "never"))
        logger.error("Then re-run script")
        sys.exit(1)

    if ORGANIZATION_NAMES and not ORGANIZATION_IDS:
        ORGANIZATION_IDS = get_organization_ids(ORGANIZATION_NAMES, api_key, token)
        if len(ORGANIZATION_IDS) < 1:
            logger.error("Finding Org ID failed.")
            sys.exit(1)

    # Parameters to get list of boards
    boards_payload = {
        'key': '{}'.format(api_key),
        'token': '{}'.format(token),
        'filter': 'open',
        'lists': 'open',
    }
    # Parameters to get board contents
    board_payload = {
        'key': '{}'.format(api_key),
        'token': '{}'.format(token),
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
        boards = requests.get(API_URL + "organizations/" + org_id + "/boards", params=boards_payload)
        try:
            if len(boards.json()) <= 0:
                logger.info("No boards found under Organisation ID: {}".format(org_id))
        except ValueError:
            logger.error("Unable to access your boards. Check your key and token.")
            sys.exit(1)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        logger.info("Backing up boards:")
        epoch_time = str(int(time.time()))

        for board in boards.json():
            if ORGANIZATION_IDS and (not board["idOrganization"] or not board["idOrganization"] in ORGANIZATION_IDS):
                continue

            logger.info(" {0} ({1})".format(board["name"], board["id"]))
            boardContents = requests.get(API_URL + "boards/" + board["id"], params=board_payload)
            with io.open(output_directory + "/{0}_".format(board["name"].replace("/", "-")) + epoch_time + ".json",
                         "w", encoding="utf8") as file:
                args = dict(sort_keys=True, indent=4)
                data = json.dumps(boardContents.json(), ensure_ascii=False, **args)
                file.write(data)
