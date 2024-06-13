from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException,RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

def http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.detail, "status": exception.status_code}
    )

def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation Error", "details": exception.errors(), "status": 422}
    )

def database_exception_handler(request: Request, exception: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Database Error", "status": 500}
    )

def base_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error", "status": 500}
    )

def create_app(name,dependencies=None):
    routes=FastAPI(title=name,dependencies=dependencies)
    routes.add_exception_handler(HTTPException, http_exception_handler)
    routes.add_exception_handler(RequestValidationError, validation_exception_handler)
    routes.add_exception_handler(SQLAlchemyError, database_exception_handler)
    routes.add_exception_handler(Exception, base_exception_handler)
    return routes


