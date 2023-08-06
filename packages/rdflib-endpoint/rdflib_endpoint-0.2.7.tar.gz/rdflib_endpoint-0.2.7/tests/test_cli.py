import time
from multiprocessing import Process

import pkg_resources
import pytest
import requests
from click.testing import CliRunner

from rdflib_endpoint.__main__ import cli


def run_cli():
    runner = CliRunner()
    return runner.invoke(
        cli,
        [
            "serve",
            pkg_resources.resource_filename("tests", "resources/test.nq"),
            pkg_resources.resource_filename("tests", "resources/test2.ttl"),
            pkg_resources.resource_filename("tests", "resources/another.jsonld"),
        ],
    )


@pytest.fixture
def server(scope="module"):
    proc = Process(target=run_cli, args=(), daemon=True)
    proc.start()
    time.sleep(1)
    yield proc
    proc.kill()


def test_query_cli(server):
    resp = requests.get(
        "http://localhost:8000/sparql?query=" + select_all_query,
        headers={"accept": "application/json"},
        timeout=600,
    )
    assert len(resp.json()["results"]["bindings"]) > 2


select_all_query = """SELECT * WHERE {
    ?s ?p ?o .
}"""
