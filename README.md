# hackfestOSM11

## Description

A freeradius-k8s VNF with Juju Charms for doing various actions

## Usage

TODO: Provide high-level usage, such as required config or relations
git clone from the repo

Onboard your VNF 

```sh
cd hackfestOSM11
osm vnfpkg-create native_k8s_charm_vnf/
osm vnfpkg-create native_k8s_charm_ns/
```
## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
