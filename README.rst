Docker Registry Purger
======================

A simple cleaner for private docker-registries.

Usage::

    python src/docker_registry_purger/__init__.py 'https://[username]:[password]@[your_repository]'

You can test this script with the ``dry-run`` option::
    
    python src/docker_registry_purger/__init__.py --dry-run 'https://[username]:[password]@[your_repository]'
