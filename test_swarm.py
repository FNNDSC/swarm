import unittest
from swarm import SwarmManager
import docker


class SwarmManagerTests(unittest.TestCase):
    """
    Test the SwarmManager's methods
    """

    @classmethod
    def setUpClass(cls):
        # initialize a single-node swarm
        cls.docker_client = docker.from_env()
        cls.docker_client.swarm.init()

    @classmethod
    def tearDownClass(cls):
        cls.docker_client.swarm.leave(True)

    def setUp(self):
        self.manager = SwarmManager()
        self.manager.get_docker_client()
        self.service_name = 'simple_service'
        self.image = 'alpine'
        self.command = 'echo test'

    def test_schedule(self):
        self.manager.schedule(self.image, self.command, self.service_name)
        service = self.docker_client.services.get(self.service_name)
        self.assertIsInstance(service, docker.models.services.Service)
        service.remove()

    def test_get_service(self):
        service = self.docker_client.services.create(self.image, self.command, name=self.service_name)
        service1 = self.manager.get_service(self.service_name)
        self.assertEqual(service, service1)
        service.remove()

    def test_get_service_container(self):
        service = self.docker_client.services.create(self.image, self.command, name=self.service_name)
        container = self.manager.get_service_container(self.service_name)
        self.assertEqual(container['ServiceID'], service.id)
        service.remove()

    def test_remove(self):
        self.docker_client.services.create(self.image, self.command, name=self.service_name)
        self.assertEqual(len(self.docker_client.services.list()), 1)
        self.manager.remove(self.service_name)
        self.assertEqual(len(self.docker_client.services.list()), 0)

if __name__ == '__main__':
    unittest.main()
