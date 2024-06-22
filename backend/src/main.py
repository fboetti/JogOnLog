from fastapi import FastAPI

# -- Backend Package Imports -- #
from src.core import (
    BackendSettings,
    get_settings,
)

settings: BackendSettings = get_settings()

app = FastAPI(
    title="JogOnLog FASTAPI Backend",
    docs_url="/docs",
)


@app.get("/")
def read_root():
    print(settings)
    return {"Hello": "World"}
