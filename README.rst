Docker Registry Purger
======================

A simple cleaner for private docker-registries.

Installation
------------

.. code-block:: console

    $ pip install docker-registry-purger

Usage
-----

Clean registry using standard options (i.e keep at less 7 versions, drop only
packages older than 180 days, developement packages older than 30 days and rc
packages older than 90 days).

.. code-block:: console

    $ docker-registry-purger 'https://[username]:[password]@[your_repository]'
    $ # OR if you have your credentials in ``.netrc``
    $ docker-registry-purger 'https://[your_repository]'

This script only drops references to blobs, the blobs themself are not deleted,
to remove them you have to follow the procedure describe on
https://docs.docker.com/registry/garbage-collection/#run-garbage-collection.

You can test this script with the ``dry-run`` option:

.. code-block:: console

    $ docker-registry-purger --dry-run 'https://[username]:[password]@[your_repository]'
