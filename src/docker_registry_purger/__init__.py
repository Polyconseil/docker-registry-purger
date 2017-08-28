#!/usr/bin/env python
import datetime
import json
import logging
import urllib.parse as urlparse

import click
import daiquiri
import isodate
import requests

logger = daiquiri.getLogger(__name__)


class Registry:
    def __init__(self, url):
        self.base_url = urlparse.urljoin(url, '/v2/')

    def _request(self, method, path, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return requests.request(
            method=method,
            url=urlparse.urljoin(self.base_url, path),
            **kwargs,
        )

    def _get(self, path, **kwargs):
        return self._request('get', path, **kwargs)

    def _delete(self, path, **kwargs):
        return self._request('delete', path, **kwargs)

    def list_repositories(self):
        return self._get('_catalog').json()['repositories']

    def list_tags(self, repository):
        return self._get('{}/tags/list'.format(repository)).json()['tags'] or []

    def delete_digest(self, repository, digest):
        return self._delete('{}/manifests/{}'.format(repository, digest))

    def get_tag(self, repository, tag):
        response = self._get('{}/manifests/{}'.format(repository, tag))
        return response.json(), response.headers.get('Docker-Content-Digest')

    def delete_tag(self, repository, tag):
        _, digest = self.get_tag(repository, tag)
        return self.delete_digest(repository, digest)


def tag_info(registry, repository, tag):
    today = datetime.date.today()
    info, digest = registry.get_tag(repository, tag)

    # Retrieve tag age
    dates = [json.loads(line['v1Compatibility']).get('created') for line in info.get('history', [])]
    last_update = isodate.parse_date(max(dates)) if dates else today
    age = (today - last_update).days

    return tag, digest, age


def setup_logging(verbosity):
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]
    verbosity = min(max(0, verbosity), len(levels) - 1)
    daiquiri.setup(level=levels[verbosity])


def execute(dry_run, fct, *args, **kwargs):
    """Only execute function on non dry run mode"""
    if not dry_run:
        return fct(*args, **kwargs)


@click.command()
@click.argument('registry-url')
@click.option(
    '--min-kept', default=7, type=click.INT,
    help='Minimal tags to keep', show_default=True,
)
@click.option(
    '--max-age', default=6 * 30, type=click.INT,
    help='Maximum age (in days) of tag', show_default=True,
)
@click.option(
    '--max-dev-age', default=1 * 30, type=click.INT,
    help='Maximum age (in days) of dev tag', show_default=True,
)
@click.option(
    '--max-rc-age', default=3 * 30, type=click.INT,
    help='Maximum age (in days) of rc tag', show_default=True,
)
@click.option('--dry-run/--no-dry-run', default=False, help='Dry run')
@click.option('-v', '--verbose', count=True, help='Be verbose')
@click.option('-q', '--quiet', count=True, help='Be quiet')
def main(registry_url, min_kept, max_age, max_dev_age, max_rc_age, dry_run, verbose, quiet):
    setup_logging(1 + quiet - verbose)

    registry = Registry(registry_url)
    for repository in registry.list_repositories():
        logger.info('Checking <%s> repository', repository)
        tags = sorted(
            [tag_info(registry, repository, tag) for tag in registry.list_tags(repository)],
            key=lambda x: x[2],
        )
        counter = [
            0 if 'dev' in tag or 'rc' in tag or not digest else 1
            for tag, digest, age in tags
        ]
        for index, (tag, digest, age) in enumerate(tags, start=1):
            logger.info('. %s', tag)

            if sum(counter[:index]) <= min_kept:
                continue

            if not digest:
                logger.warning('%s:%s already deleted', repository, tag)
                continue  # image already deleted

            if 'dev' in tag and age > max_dev_age:
                logger.warning('Deleting %s:%s [dev: %s]', repository, tag, age)
                execute(dry_run, registry.delete_digest, repository, digest)

            elif 'rc' in tag and age > max_rc_age:
                logger.warning('Deleting %s:%s [rc: %s]', repository, tag, age)
                execute(dry_run, registry.delete_digest, repository, digest)

            elif age > max_age:
                logger.warning('Deleting %s:%s [old: %s]', repository, tag, age)
                execute(dry_run, registry.delete_digest, repository, digest)


if __name__ == '__main__':
    daiquiri.setup(level=logging.INFO)
    main()
