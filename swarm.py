"""
Swarm cluster manager module that provides functionality to schedule services as well as
manage their state in the cluster.
"""

from argparse import ArgumentParser
import configparser
import json
import docker


class SwarmManager(object):

    def __init__(self):
        parser = ArgumentParser(description='Manage a swarm cluster')

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-s", "--schedule", help="schedule a new service",
                           metavar='name')
        group.add_argument("-r", "--remove", help="remove a previously scheduled service",
                           metavar='name')
        group.add_argument("--state", help="print state of scheduled service",
                           metavar='name')
        parser.add_argument("--conffile", help="swarm cluster configuration file")
        parser.add_argument("-i", "--image",
                            help="docker image for the scheduled service container")
        parser.add_argument("-c", "--command",
                            help="command to be run inside scheduled service container")
        parser.add_argument("-p", "--restart-policy",
                            help="restart policy on scheduled jobs",
                            metavar='restart',
                            default='on-failure')
        parser.add_argument("-m", "--mount", help="mount directory in the cluster",
                            metavar='dir')
        self.parser = parser
        self.docker_client = None

    def get_docker_client(self, conf_filepath=None):
        """
        Method to get a docker client connected to remote or local docker deamon.
        """
        if conf_filepath is None:
            self.docker_client = docker.from_env()
        else:
            conf = configparser.ConfigParser()
            conf.read(conf_filepath)
            conf_dict = conf['DEFAULT']
            base_url = 'unix://var/run/docker.sock'
            if 'base_url' in conf_dict:
                base_url = conf_dict.base_url
            self.docker_client = docker.DockerClient(base_url=base_url)

    def schedule(self, image, command, name, restart_policy, mountdir=None):
        """
        Schedule a new service and returns the service object.
        """
        # 'on-failure' restart_policy ensures that the service will not be rescheduled
        # when it completes
        restart_policy = docker.types.RestartPolicy(condition=restart_policy)
        mounts = []
        if mountdir is not None:
            mounts.append('%s:/share:rw' % mountdir)
        return self.docker_client.services.create(image, command, name=name, mounts=mounts,
                                                  restart_policy=restart_policy)

    def get_service(self, name):
        """
        Get a previously scheduled service object.
        """
        return self.docker_client.services.get(name)

    def get_service_container(self, name):
        """
        Get docker container for a previously scheduled service object.
        """
        return self.get_service(name).tasks()[0]

    def remove(self, name):
        """
        Remove a previously scheduled service.
        """
        service = self.get_service(name)
        service.remove()

    def parse(self, args=None):
        """
        Parse the arguments passed to the manager and perform the appropriate action.
        """
        # parse argument options
        options = self.parser.parse_args(args)

        # get the docker client
        if options.conffile:
            self.get_docker_client(options.conffile)
        else:
            self.get_docker_client()

        if options.schedule:
            if not (options.image and options.command):
                self.parser.error("-s/--schedule requires -i/--image and -c/--command")
            self.schedule(options.image, options.command, options.schedule, options.restart
                          options.mount)

        if options.remove:
            self.remove(options.remove)

        if options.state:
            container = self.get_service_container(options.state)
            print(json.dumps(container))


# ENTRYPOINT
if __name__ == "__main__":
    manager = SwarmManager()
    manager.parse()


