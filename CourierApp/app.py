from api.courier_api.router import courier_router
from api.order_api.router import order_router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(courier_router)
    application.include_router(order_router)
    return application

app = get_application()
