#!/usr/bin/env python3
# Copyright 2021 root
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging
import subprocess

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import (
    ActiveStatus,
    MaintenanceStatus,
)

logger = logging.getLogger(__name__)


class FreeradiusK8SCharm(CharmBase):
    """Charm the service."""

    state = StoredState()
    mysql = "localhost"

    def __init__(self, *args):
        super().__init__(*args)
        self.state.set_default(spec=None)

        # Basic hooks
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

        # Action hooks
        self.framework.observe(self.on.custom_action, self._on_custom_action)
        self.framework.observe(self.on.adduser_action, self._on_adduser_action)

        # Relation hooks
        self.framework.observe(self.on.mysql_relation_changed, self._on_mysql_relation_changed)

    
    def _on_mysql_relation_changed(self, event):
        # TODO
        #self.mysql = event.params["host"]
        
        self.model.unit.status = MaintenanceStatus("Receiving DB IP")
        self.mysql = event.relation.data[event.unit].get("host")
        
        if(self.mysql != None):
            self._apply_spec()
            self.model.unit.status = ActiveStatus(f"Received DB IP:{self.mysql}")
    
    def _apply_spec(self):
        # Only apply the spec if this unit is a leader.
        if not self.framework.model.unit.is_leader():
            return
        new_spec = self.make_pod_spec()
        if new_spec == self.state.spec:
            return
        self.framework.model.pod.set_spec(new_spec)
        self.state.spec = new_spec

    def make_pod_spec(self):
        config = self.framework.model.config

        ports = [
            {
                "name": "port-1",
                "containerPort": config["port-1"],
                "protocol": "UDP",
            },
            {
                "name": "port-2",
                "containerPort": config["port-2"],
                "protocol": "UDP",
            }
        ]

        spec = {
            "version": 3,
            "containers": [
                {
                    "name": self.framework.model.app.name,
                    "image": "{}".format(config["image"]),
                    "ports": ports,
                    "envConfig": { # Environment variables that wil be passed to the container
                        "RADIUS_DB_HOST": self.mysql,
                        "RADIUS_DB_PORT": "3306",
                        "RADIUS_DB_USERNAME": "root",
                        "RADIUS_DB_PASSWORD": "root",
                        "RADIUS_SQL": "true",
                        "RADIUS_DB_NAME": "database",
                    }
                }
            ],
        }

        return spec

    def _on_config_changed(self, event):
        """Handle changes in configuration"""
        unit = self.model.unit
        unit.status = MaintenanceStatus("Applying new pod spec")
        self._apply_spec()
        unit.status = ActiveStatus("Ready")

    def _on_start(self, event):
        """Called when the charm is being installed"""
        unit = self.model.unit
        unit.status = MaintenanceStatus("Applying pod spec")
        self._apply_spec()
        unit.status = ActiveStatus("Ready")

    def _on_upgrade_charm(self, event):
        """Upgrade the charm."""
        unit = self.model.unit
        unit.status = MaintenanceStatus("Upgrading charm")
        self.on_start(event)

    def _on_custom_action(self, event):
        """Define an action"""
        # TODO
        filename = event.params["customparam"]
        cmd = 'touch '+str(filename)
        try:
            #subprocess.run(cmd, shell=True)
            subprocess.run(["touch", filename], cwd="/root")
            event.set_results({
                    "output": f"File {filename} created successfully"
                    })
        except Exception as e:
            event.fail(f"Touch action failed with the following exception: {e}")

    def _on_adduser_action(self, event):
        username = event.params["username"]
        password = event.params["password"]
        cmd1 = f"echo '{username} Cleartext-Password := \"{password}\"' >> /etc/freeradius/users"
        try:
            subprocess.run(cmd1, shell=True)
            event.set_results({
            "output": f"User {username} created successfully"
            })
        except Exception as e:
            event.fail(f"Touch action failed with the following exception: {e}")


if __name__ == "__main__":
    main(FreeradiusK8SCharm)
