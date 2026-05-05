from .db import init_db
from .web import app
from . import streamer_proxy_routes  # noqa: F401


@app.on_event('startup')
async def startup() -> None:
    await init_db()
