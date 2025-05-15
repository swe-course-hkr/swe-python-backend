import json
from flask import Response
from app.util import successResponse, errorResponse


def test_successResponse():
    resp, code = successResponse()

    assert type(code) is int
    assert code == 200

    assert type(resp.data) is bytes

    responseData = json.loads(resp.data)
    assert type(responseData) is dict

    assert "data" in responseData
    assert "error" in responseData

    assert responseData.get("data") is None
    assert responseData.get("error") is None


def test_successResponse_with_data_and_code():
    response, code = successResponse(
        data = { "somekey": "somevalue" },
        statusCode = 202
    )

    assert type(code) is int
    assert code == 202

    assert type(response.data) is bytes

    responseData = json.loads(response.data)
    assert type(responseData) is dict

    assert "data" in responseData
    assert "error" in responseData
    assert type(responseData.get("data")) is dict
    assert responseData.get("error") is None

    assert "somekey" in responseData.get("data")
    assert responseData["data"]["somekey"] == "somevalue"


def test_errorResponse():
    response, code = errorResponse()

    assert type(code) is int
    assert code == 401

    assert type(response.data) is bytes

    responseData = json.loads(response.data)
    assert type(responseData) is dict

    assert "data" in responseData
    assert "error" in responseData

    assert responseData.get("data") is None

    assert type(responseData.get("error")) is dict

    assert "message" in responseData.get("error")
    assert "code" in responseData.get("error")

    assert responseData.get("error").get("message") is None
    assert responseData.get("error").get("code") == 401


def test_errorResponse_with_message_and_code():
    response, code = errorResponse("not allowed", 403)

    assert type(code) is int
    assert code == 403

    assert type(response.data) is bytes

    responseData = json.loads(response.data)
    assert type(responseData) is dict

    assert "data" in responseData
    assert "error" in responseData

    assert responseData.get("data") is None

    assert type(responseData.get("error")) is dict

    assert "message" in responseData.get("error")
    assert "code" in responseData.get("error")

    assert responseData.get("error").get("message") == "not allowed"
    assert responseData.get("error").get("code") == 403