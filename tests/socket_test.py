# -----------------------------------------------------------------
# pytest
# -----------------------------------------------------------------

from falcon import testing
import pytest

import app.main as app


# Depending on your testing strategy and how your application
# manages state, you may be able to broaden the fixture scope
# beyond the default 'function' scope used in this example.

@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.App` instance.
    return testing.TestClient(app)


def test_get_message(client):
    doc = {'message': 'Hello world!'}

    result = client.simulate_get('/v1/users')
    assert result.json == doc
