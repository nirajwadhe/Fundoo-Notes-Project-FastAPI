from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

def base_exception_handler(request:Request,exception:Exception):
    return JSONResponse(status_code=500,content={"message":str(exception),"status":500}) 

def create_app(name,dependencies=None):
    if not dependencies:
        routes = FastAPI(title=name,dependencies=dependencies)
    else:
        routes=FastAPI(title=name,dependencies=dependencies)
    routes.add_exception_handler(Exception,base_exception_handler)
    return routes


