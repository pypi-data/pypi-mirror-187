#!/usr/bin/env python3
"""Check if a package is present in a python package repo"""
import sys
from typing import Optional, List

from pypi_simple import PyPISimple, PYPI_SIMPLE_ENDPOINT, DistributionPackage
from pypi_simple.client import NoSuchProjectError
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--index", "-i", type=str, metavar="INDEX", default=PYPI_SIMPLE_ENDPOINT,
                    help="Python package index URL")
parser.add_argument("PACKAGE", type=str,
                    help="name of the package, eg 'requests'")
parser.add_argument("VERSION", type=str, nargs="?", default=None,
                    help="Version to check for (optional)")

def run(args=None):
    opts = parser.parse_args(args)
    server = opts.index
    if "/simple" not in server:
        server = f"{server}/simple"

    print(f"Getting packages named: {opts.PACKAGE} on {server}:", file=sys.stderr)
    if opts.VERSION:
        print(f"Limiting to {opts.PACKAGE} {opts.VERSION}", file=sys.stderr)
    sys.stderr.flush()
    packages = list_package(opts.PACKAGE,
                            exact_version=opts.VERSION,
                            index_url=server)
    for package in packages:
        print(f"{package.filename} {package.version} type={package.package_type} url={package.url}")

def list_package(name: str,
                 exact_version: Optional[str] = None,
                 index_url: Optional[str] = None) -> List[DistributionPackage]:
    """Return all versions of the named package on a pypi simple index server"""
    if index_url is None:
        index_url = PYPI_SIMPLE_ENDPOINT

    with PyPISimple(endpoint=index_url) as client:
        try:
            project = client.get_project_page(name)
        except NoSuchProjectError:
            return []

        found = []
        for package in project.packages:
            if not package.is_yanked:
                if exact_version is None or exact_version == package.version:
                    found.append(package)
        return found


if __name__ == "__main__":
    run()
