# images-from-errata

As of this writing, Red Hat container images errata has no details of the images they update (name and checksum). This is an issue for example on OpenStack, where there are over 100 possible images, but a single errata may update just a handful of them.

This script uses [Red Hat public endpoints](https://catalog.redhat.com/api/containers/v1/ui/#/) to figure out which images have the image_advisory_id field set to a particular errata. You need to know the namespace of the images and, of course, the errata. Some of the most popular namespaces are:

- rhosp-rhel8 (Red Hat OpenStack Platform 16.x)
- rhosp13 (Red Hat OpenStack Platform 13)
- openshift3
- openshift4

~~~
$ ./get-images-from-container-errata.py --errata RHBA-2022:0238 --namespace rhosp-rhel8
Searching for images with image_advisory_id = RHBA-2022:0238
registry.access.redhat.com/rhosp-rhel8/openstack-etcd@sha256:c186750b2eaf94ab7adc35cedd6ed17701dced1aa253fed1652b04bed1fd927c
registry.access.redhat.com/rhosp-rhel8/openstack-nova-compute@sha256:48ad99d42c04d8d41dfdd9d817a48b1c94dda2b0596fd33bd5099bffb25ff744
registry.access.redhat.com/rhosp-rhel8/openstack-nova-compute-ironic@sha256:3e5ad3adf30b8b5fd1527e0b9fe7ceaa3705685455b4ef8df303ffb715a87a8a
registry.access.redhat.com/rhosp-rhel8/openstack-nova-libvirt@sha256:8bc5107e0c1b6e3b5ca8f4c10b3c6229ea853bebb384c9c74c51aa93b5cda07b
~~~
