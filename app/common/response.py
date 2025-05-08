def Response(data, message):
    if isinstance(data, dict) and "_id" in data:
        data["_id"] = str(data["_id"])
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
