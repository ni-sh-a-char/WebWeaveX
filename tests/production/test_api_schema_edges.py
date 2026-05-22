import pytest

from webweavex.api.schemas import validate_request, validate_response


def test_validate_request_errors():
    with pytest.raises(ValueError):
        validate_request("not dict")
    with pytest.raises(ValueError):
        validate_request({"input": 1})
    with pytest.raises(ValueError):
        validate_request({"input": "  "})


def test_validate_response_errors():
    with pytest.raises(RuntimeError):
        validate_response({})
    with pytest.raises(RuntimeError):
        validate_response(
            {
                "structured_data": {},
                "confidence": "bad",
                "source": "x",
                "version": "2",
            }
        )
