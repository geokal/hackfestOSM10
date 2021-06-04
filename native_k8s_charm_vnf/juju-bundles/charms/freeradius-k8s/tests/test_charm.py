# Copyright 2021 root
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import Mock

from charm import FreeradiusK8SCharm
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(FreeradiusK8SCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_action(self):
        action_event = Mock()
        self.harness.charm._on_custom_action(action_event)
