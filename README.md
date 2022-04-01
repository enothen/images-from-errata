# images-from-errata

As of this writing, Red Hat container images errata has no details of the images they update (name and checksum). This is an issue for example on OpenStack, where there are over 100 possible images, but a single errata may update just a handful of them.

This script uses [Red Hat public endpoints](https://catalog.redhat.com/api/containers/v1/ui/#/) to figure out which images have the image_advisory_id field set to a particular errata. You need to know the namespace of the images and, of course, the errata. Some of the most popular namespaces are:

- rhosp-rhel8 (Red Hat OpenStack Platform 16.x)
- rhosp13 (Red Hat OpenStack Platform 13)
- openshift3
- openshift4

## Usage examples
List amd64 images (default) updated by an errata on the OpenStack 16.x namespace:
~~~
$ ./get-images-from-container-errata.py --errata RHBA-2022:0238 --namespace rhosp-rhel8
Searching for images with image_advisory_id = RHBA-2022:0238
registry.access.redhat.com/rhosp-rhel8/openstack-etcd@sha256:c186750b2eaf94ab7adc35cedd6ed17701dced1aa253fed1652b04bed1fd927c
registry.access.redhat.com/rhosp-rhel8/openstack-nova-compute@sha256:48ad99d42c04d8d41dfdd9d817a48b1c94dda2b0596fd33bd5099bffb25ff744
registry.access.redhat.com/rhosp-rhel8/openstack-nova-compute-ironic@sha256:3e5ad3adf30b8b5fd1527e0b9fe7ceaa3705685455b4ef8df303ffb715a87a8a
registry.access.redhat.com/rhosp-rhel8/openstack-nova-libvirt@sha256:8bc5107e0c1b6e3b5ca8f4c10b3c6229ea853bebb384c9c74c51aa93b5cda07b
~~~

List all images (multiple architectures) updated by an errata on the OpenStack 13 namespace:
~~~
$ ./get-images-from-container-errata.py --namespace rhosp13 --errata RHBA-2022:0425 --architecture all
Searching for images with image_advisory_id = RHBA-2022:0425
registry.access.redhat.com/rhosp13/openstack-cinder-backup@sha256:07e9d469ace2171afaab3e43ac98eb57b001d416da5504e2992544a6459517bd (amd64)
registry.access.redhat.com/rhosp13/openstack-cinder-backup@sha256:689f0858264151a046176cb5210309abfb974a2edc605ab3eebbdc696a1cd1f2 (ppc64le)
registry.access.redhat.com/rhosp13/openstack-cinder-volume@sha256:c6bc1f6821e507f4e65ddfe2e34e7fc2b4e58e7a7885a3c0fba6b74fe3da27cd (ppc64le)
registry.access.redhat.com/rhosp13/openstack-cinder-volume@sha256:f0dcb019c6af1fcca00044f6f88cf591946ca5a02d6095ab5745b8ade55eb4b2 (amd64)
registry.access.redhat.com/rhosp13/openstack-haproxy@sha256:c37f79aa6d3a0ec8a9b71058db8f36f27ad0b3e4f8f47289fd002481118c6d0e (amd64)
registry.access.redhat.com/rhosp13/openstack-manila-share@sha256:199ec222ed628983e45ef2b361d52782e9fa6884305f069ef0fd323acdb40dc0 (amd64)
registry.access.redhat.com/rhosp13/openstack-mariadb@sha256:fe7b815f387a799ba73527243e65c170719531352935e7444f0a46c286981f85 (amd64)
registry.access.redhat.com/rhosp13/openstack-ovn-northd@sha256:17ef3ba4628cf2acf4a1c951dc9dd4f8716f6056984c3d3dcb867e956ec46360 (amd64)
registry.access.redhat.com/rhosp13/openstack-rabbitmq@sha256:1758ed9b8ff235058be71f5da1f049f0dbde05d84afad71185e820a52ad44c04 (amd64)
registry.access.redhat.com/rhosp13/openstack-redis@sha256:c4f2cc4e05406e29acb1c7a82eb21162185844ef677a890d3d1528da7ddf0b86 (amd64)
~~~

Filter images named "ose-elasticsearch-operator" on all architectures, updated by an errata on the OpenShift 4 namespace:
~~~
$ ./get-images-from-container-errata.py --namespace openshift4 --errata RHBA-2020:3459 --architecture all --imagename ose-elasticsearch-operator
Searching for images with image_advisory_id = RHBA-2020:3459
registry.access.redhat.com/openshift4/ose-elasticsearch-operator@sha256:c67e45ef1ce2c8514d69573fc075e5b9feef9b9627965cae42f9976a2e0ce8ec (s390x)
registry.access.redhat.com/openshift4/ose-elasticsearch-operator@sha256:70e2107e6bd92bafaa03c438640245be63808bd7bb1db670c9af70fe30ef608f (ppc64le)
registry.access.redhat.com/openshift4/ose-elasticsearch-operator@sha256:ed8acd5a10f669da72a98eddac6a4905b554fecd132b9f17e5212a9933dd5dd9 (amd64)
~~~