import os

import pytest

pytestmark = pytest.mark.skipif(not os.environ.get("WEBWEAVEX_RUN_NETWORK_TESTS"), reason="opt-in")
