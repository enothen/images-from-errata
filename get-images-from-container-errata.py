#!/usr/bin/env python3

import argparse
import requests

# Red Hat's public API url
pyxis_url="https://catalog.redhat.com/api/containers/v1"

# Get arguments from command line
parser = argparse.ArgumentParser(description='Get images that were released as part of an Errata')
parser.add_argument('--architecture', required=False, default='amd64',
    help='Only list images matching a specific architecture, such as amd64 (default) ppc64le, or otherwise "all"')
parser.add_argument('--imagename', required=False, default=False, help='List only images matching exactly imagename')
parser.add_argument('--errata', required=True, help='Errata to search for, such as RHBA-2022:0333')
parser.add_argument('--namespace', required=True,
    help='Namespace to use when searching for image names, such as rhosp-rhel8 (rhosp16), rhosp13, openshift3 or openshift4')
args = parser.parse_args()

# Get list of images
response = requests.get(pyxis_url + "/repositories?page_size=200&page=0&sort_by=repository&filter=namespace%3D%3D" + args.namespace)
image_list = response.json()['data']

print("Searching for images with image_advisory_id =",args.errata)
for x in image_list:
    errata_found = False
    if args.imagename and args.namespace+"/"+args.imagename != x['repository']:
        continue
    header = {'accept': 'application/json'}
    response = requests.get(pyxis_url + "/repositories/registry/registry.access.redhat.com/repository/" + x['repository'] + "/images?page_size=200&page=0&sort_by=last_update_date%5Bdesc%5D", headers=header)
    image_versions = response.json()['data']

    for image in image_versions:
        if errata_found or args.architecture not in [ "all", image['architecture'] ]:
            continue
        for repo in image['repositories']:
            if 'image_advisory_id' in repo and repo['image_advisory_id'] == args.errata:
                if args.architecture != "all":
                    errata_found = True
                print(repo['registry']+"/"+repo['repository']+"@"+repo['manifest_schema2_digest']+" ("+image['architecture']+")")
                continue

