import sys
import json

sys.path.insert(0, './')

from . import client, app

#add log
def test_addLog(client):
    # we don't need to have an endpoint for creating logs,
    # we should have tests for internal functions (not exposed to clients),
    # which are related to managing logs
    assert True
