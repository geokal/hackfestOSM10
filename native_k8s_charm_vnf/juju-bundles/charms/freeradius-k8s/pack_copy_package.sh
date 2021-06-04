#!/bin/bash

echo "Packaging the charm and copying the files in ../juju-bundles/charms/freeradius-k8s"
sudo charmcraft pack && rm -rf ../juju-bundles/charms/freeradius-k8s/* && cp -r ./build/* ../juju-bundles/charms/freeradius-k8s
echo "Done!"