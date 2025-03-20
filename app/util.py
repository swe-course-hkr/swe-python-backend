from flask import jsonify


def successResponse(data=None, statusCode=200):
    return jsonify({
        "data": data,
        "error": None
    }), statusCode


def errorResponse(error=None, statusCode=401):
    return jsonify({
        "data": None,
        "error": {
            "message": error,
            "code": statusCode
        }
    }), statusCode
