# -- Pure Python Imports -- #
import typing
import inspect
# -- Backend Requirements Imports -- #
from fastapi import (
    FastAPI,
    APIRouter,
)
# -- Backend Package Imports -- #
from src.core import (
    get_settings,
    BackendSettings,
)
import src.api.controllers as all_controllers

settings: BackendSettings = get_settings()

# Get all the controllers from the controllers package, except for the "create_standard_controller" controller.
controllers: typing.List[APIRouter] = [
    controller
    for controller_name, controller in inspect.getmembers(all_controllers)
    if isinstance(controller, APIRouter) and controller_name != "create_standard_controller"
]


app = FastAPI(
    title="JogOnLog FASTAPI Backend",
    docs_url="/docs",
)

# Add all the controllers to the app.
for controller in controllers:
    app.include_router(controller)


@app.get("/")
def read_root():
    return {"Hello": "World"}
