#!/usr/bin/env python3

import argparse
import requests

# Red Hat's public API url
pyxis_url="https://catalog.redhat.com/api/containers/v1"

# Get arguments from command line
parser = argparse.ArgumentParser(description='Helper script to get the current health index of images')
parser.add_argument('--tag', required=True, help="Minor release or z-stream to search for")
parser.add_argument('--architecture', required=False, default='amd64',
    help='Only list images matching a specific architecture, such as amd64 (default) ppc64le, or otherwise "all"')
parser.add_argument('--imagename', required=False, default=False, help='List only images matching exactly imagename')
parser.add_argument('--namespace', required=True,
    help='Namespace to use when searching for image names, such as rhosp-rhel8 (rhosp16), rhosp13, openshift3 or openshift4')
#parser.add_argument('--date', required=False, help='Print the date when the image was ')
parser.add_argument('--parseable', action='store_true', required=False, default=False, help="Whether to print parseable output")
args = parser.parse_args()

# Get list of images
response = requests.get(pyxis_url + "/repositories?page_size=200&page=0&sort_by=repository&filter=namespace%3D%3D" + args.namespace)
image_list = response.json()['data']

if args.parseable:
    print ('Image Name:Tag,CurrentGrade,FutureGrades(From[|To])[;...]')
else:
    print_format="{:<38}{:<22}{:<7}{:<22}{:<22}"
    print (print_format.format('Image Name' ,'Tag','Grade', 'From', 'To'))

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
                    if tag['name'] != 'latest':
                        max_tag = str(max(max_tag, tag['name']))
                if args.parseable:
                    print(repo['repository'] + "," + max_tag + "," + image['freshness_grades'][0]['grade'] + ",", end='')
                    for x in range(1, len(image['freshness_grades'])-1):
                        print (image['freshness_grades'][x]['grade'] + "(" + image['freshness_grades'][x]['start_date'] + "|" + image['freshness_grades'][x]['end_date'] + ");", end='')
                    print (image['freshness_grades'][-1]['grade'] + "(" + image['freshness_grades'][-1]['start_date'] + ")")
                else:
                    x = image['freshness_grades'][0]
                    if len(image['freshness_grades']) == 1:
                        print (print_format.format(repo['repository'].split("/")[-1], max_tag, x['grade'], x['start_date'].split("+")[0], ''))
                    else:
                        print (print_format.format(repo['repository'].split("/")[-1], max_tag, x['grade'], x['start_date'].split("+")[0], x['end_date'].split("+")[0]))
                        for x in range(1, len(image['freshness_grades'])-1):
                            print (print_format.format('', '', image['freshness_grades'][x]['grade'], image['freshness_grades'][x]['start_date'].split("+")[0], image['freshness_grades'][x]['end_date'].split("+")[0]))
                        print (print_format.format('', '', image['freshness_grades'][-1]['grade'], image['freshness_grades'][-1]['start_date'].split("+")[0], ''))
