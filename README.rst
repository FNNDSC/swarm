#####
Swarm
#####

A swarm cluster manager based on the Python docker API

.. image:: https://travis-ci.org/FNNDSC/swarm.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/swarm

The docker image can be run from a swarm manager to schedule a service:

.. code-block:: bash

  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock fnndsc/swarm swarm.py -s test -i alpine -c "echo test"

This will schedule the ``test`` service that runs command:

.. code-block:: bash

  echo test

using the ``Alpine`` image


The same thing can be accomplished from ``Python`` code:

.. code-block:: python

  client = docker.from_env()
  # 'remove' option automatically remove container when finished
  byte_str = client.containers.run('fnndsc/swarm',  'swarm.py -s test -i alpine -c "echo test"',
                                   volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}},
                                   remove=True)


To remove the ``test`` service:

.. code-block:: bash

  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock fnndsc/swarm swarm.py --remove test

or from ``Python``:

.. code-block:: python

  byte_str = client.containers.run('fnndsc/swarm',  'swarm.py --remove test',
                                   volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}},
                                   remove=True)

