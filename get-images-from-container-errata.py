#!/usr/bin/env python3

import argparse
import urllib.request
import json

# Red Hat's public API url
pyxis_url="https://catalog.redhat.com/api/containers/v1"

# Get arguments from command line
parser = argparse.ArgumentParser(description='Get images that were released as part of an Errata.')
parser.add_argument('--architecture', required=False, default='amd64',
    help='Only list images matching a specific architecture, such as amd64 (default) or ppc64le')
parser.add_argument('--errata', required=True, help='Errata to search for, such as RHBA-2022:0333')
parser.add_argument('--namespace', required=True, help='Namespace to use when searching for image names, use rhosp-rhel8 (rhosp16) or rhosp13')
args = parser.parse_args()

# Get list of images
response = urllib.request.urlopen(pyxis_url + "/repositories?page_size=200&page=0&sort_by=repository&filter=namespace%3D%3D" + args.namespace)
image_list = json.load(response)['data']

print("Searching for images with image_advisory_id =",args.errata)
for x in image_list:
    errata_found = False
    image_versions = json.load(urllib.request.urlopen(pyxis_url + "/repositories/registry/registry.access.redhat.com/repository/" + x['repository'] + "/images?page_size=100&page=0&sort_by=creation_date%5Bdesc%5D"))['data']

    for image in image_versions:
        if errata_found or image['architecture'] != args.architecture:
            continue
        for repo in image['repositories']:
            if 'image_advisory_id' in repo and repo['image_advisory_id'] == args.errata:
                errata_found = True
                print(repo['registry']+"/"+repo['repository']+"@"+repo['manifest_schema2_digest'])
                continue

