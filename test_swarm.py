import unittest
from swarm import SwarmManager
import json
import docker


class SwarmManagerTests(unittest.TestCase):
    """
    Test the SwarmManager's methods
    """

    @classmethod
    def setUpClass(cls):
        # initialize a single-node swarm
        cls.client = docker.from_env()
        cls.client.swarm.init()

    @classmethod
    def tearDownClass(cls):
        cls.client.swarm.leave(True)

    def setUp(self):
        self.manager = SwarmManager()
        self.service_name = 'simple_service'

    def test_schedule(self):
        image_name = 'fnndsc/pl-simplefsapp'
        command = 'python simplefsapp --help'
        self.manager.schedule(image_name, command, self.service_name)
        self.docker_client.services.get(name)


if __name__ == '__main__':
    unittest.main()
