#!/usr/bin/env python3

import argparse
import requests

# Red Hat's public API url
pyxis_url="https://catalog.redhat.com/api/containers/v1"

# Get arguments from command line
parser = argparse.ArgumentParser(description='Get the latest list of images that are part of a z-stream')
parser.add_argument('--tag', required=True, help="z-stream to search for")
parser.add_argument('--architecture', required=False, default='amd64',
    help='Only list images matching a specific architecture, such as amd64 (default) ppc64le, or otherwise "all"')
parser.add_argument('--imagename', required=False, default=False, help='List only images matching exactly imagename')
parser.add_argument('--namespace', required=True,
    help='Namespace to use when searching for image names, such as rhosp-rhel8 (rhosp16), rhosp13, openshift3 or openshift4')
parser.add_argument('--parseable', action='store_true', required=False, default=False, help="Whether to print parseable output")
args = parser.parse_args()

# Get list of images
response = requests.get(pyxis_url + "/repositories?page_size=200&page=0&sort_by=repository&filter=namespace%3D%3D" + args.namespace)
image_list = response.json()['data']

if args.parseable:
    print("ImageName,Tag,Digest")
else:
    print("Searching for images with tag", args.tag)

for x in image_list:
    if args.imagename and args.namespace+"/"+args.imagename != x['repository']:
        continue
    header = {'accept': 'application/json'}
    response = requests.get(pyxis_url + "/repositories/registry/registry.access.redhat.com/repository/" + x['repository'] + "/tag/" + args.tag, headers=header)
    image_list_by_tag = response.json()['data']

    for image in image_list_by_tag:
        if args.architecture not in [ "all", image['architecture'] ]:
            continue
        for repo in image['repositories']:
            if 'tags' in repo:
                max_tag = ''
                for tag in repo['tags']:
                    max_tag = str(max(max_tag, tag['name']))
                if args.parseable:
                    print(repo['registry']+"/"+repo['repository']+","+max_tag + "," + repo['manifest_schema2_digest'])
                else:
                    print(repo['registry']+"/"+repo['repository']+":"+max_tag + " " + repo['manifest_schema2_digest'])
