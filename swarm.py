"""
Swarm cluster manager module that provides functionality to schedule services as well as
manage their state in the cluster.
"""

from argparse import ArgumentParser
import docker


class SwarmManager(object):

    def __init__(self):
        parser = ArgumentParser(description='Manage a swarm cluster')

        parser.add_argument("-i", "--info", action="store_true",
                            help="get swarm cluster info")
        self.parser = parser
        self.docker_client = None

    def _get_docker_client(self, options_filepath=None):
        """
        Internal method to get a docker client connected to remote or local docker deamon.
        """
        if options_filepath==None:
            self.docker_client = docker.from_env()
        else:
            options = {}
            with open(options_filepath, 'r') as options_file:
                options = json.load(options_file)
            if base_url in options:
                self.docker_client = docker.DockerClient(base_url=options.base_url)

    def get_info(self):
        """
        Get the Swarm's state info.
        """
        print("Working!")

    def run(self, args=None):
        """
        Parse the arguments passed to the manager and perform the appropriate action.
        """
        options = self.parser.parse_args(args)
        if options.info:
            self.get_info()

        self.args = options




# ENTRYPOINT
if __name__ == "__main__":
    manager = SwarmManager()
    manager.run()


