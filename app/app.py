from requests import Request
from fastapi import FastAPI
from .controllers.users import router as user_router  # <- use full path!
from .controllers.auth import router as auth_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .connections.db import check_db_connection

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.on_event("startup")
async def startup_db():
    await check_db_connection()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = err["loc"]
        field = ".".join(str(l) for l in loc if l != "body")
        message = err["msg"]
        errors.append({"field": field, "error": message})

    return JSONResponse(
        status_code=422,
        content={
            "status": "fail",
            "message": "Validation error",
            "errors": errors,  # You can customize the format here
        },
    )


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
