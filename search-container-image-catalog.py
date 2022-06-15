#!/usr/bin/env python3

import argparse
import requests

# Red Hat's public API url
pyxis_url="https://catalog.redhat.com/api/containers/v1"

# Get arguments from command line
parser = argparse.ArgumentParser(
    description='Script to search Red Hat catalog for container images matching a given criteria. \
    All filters default to false, and when set will do substring match.')
parser.add_argument('--namespace', required=False, default=None,
    help='Filter by Namespace, such as rhosp-rhel8 (rhosp16), rhosp13, openshift3, openshift4, etc.')
parser.add_argument('--provider', required=False, default=None,
    help='Filter by vendor provider, such as "redhat", "ibm" or "cisco".')
parser.add_argument('--registry', required=False, default=None,
    help='Filter by registry, such as "registry.connect.redhat.com".')
parser.add_argument('--repository', required=False, default=None,
    help='Filter by repository, such as "nova".')
parser.add_argument('--sortby', required=False, default='repository',
    help='Key to sort results by. Defaults to "repository", but could be one of [repository, namespace, vendor_label]')
parser.add_argument('--pagesize', required=False, default=200,
    help='Results paging size request when searching the catalog. Defaults to 200.')
args = parser.parse_args()

# Repositories API url plus basic paging and sorting
repositories_url = pyxis_url + "/repositories?sort_by=" + args.sortby + "&page_size=" + str(args.pagesize)

if args.namespace or args.provider or args.registry:
    repositories_url = repositories_url + "&filter="
    if args.registry:
        repositories_url = repositories_url + "registry~%3D" + args.registry
        if args.namespace or args.provider:
            repositories_url = repositories_url + "%20and%20"
    if args.namespace:
        repositories_url = repositories_url + "namespace~%3D" + args.namespace
        if args.provider:
            repositories_url = repositories_url + "%20and%20"
    if args.provider:
        repositories_url = repositories_url + "vendor_label~%3D" + args.provider

response = requests.get(repositories_url)
repo_list = response.json()['data']

page = 0
while len(repo_list) > 0:
    for x in repo_list:
        if args.repository:
            if args.repository in x['repository'].split('/')[-1]:
                print(x['registry'] + "/" + x['repository'])    
        else:
            print(x['registry'] + "/" + x['repository'])

    page += 1
    response = requests.get(repositories_url + "&page=" + str(page))
    repo_list = response.json()['data']
