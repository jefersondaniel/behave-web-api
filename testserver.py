import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.datastructures import UploadFile
import uvicorn


app = FastAPI()


@app.api_route("/requests/echo", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def echo(request: Request):
    try:
        body_bytes = await request.body()
        body = body_bytes.decode("utf-8")
    except Exception:
        body = None

    print(request.headers.get("Content-Type"))

    if request.headers.get("Content-Type") == "application/json":
        try:
            body = json.loads(body)
        except Exception:
            pass

    files = []
    form = await request.form()
    for key, value in form.multi_items():
        if isinstance(value, UploadFile):
            files.append({"key": key, "name": value.filename})

    result = {
        "method": request.method,
        "headers": {k.title(): v for k, v in request.headers.items()},
        "body": body,
        "files": files,
    }

    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)

