import os
import sys

import pandas as pd

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from zeno import get_server, zeno, ZenoParameters  # type: ignore


def command_line():
    app = FastAPI(title="Frontend API")
    api_app = FastAPI(title="Backend API")

    @api_app.get("/test")
    def test():
        return {"test": "test"}

    # from zeno import get_server, zeno

    df = pd.read_csv("./data/adult.csv")

    configA = ZenoParameters(metadata=df.head(10), serve=False)
    configB = ZenoParameters(metadata=df.head(100), serve=False)

    zenoA = zeno(configA)
    if zenoA is None:
        sys.exit(1)
    serverA = get_server(zenoA)
    zenoA.start_processing()
    app.mount("/zenoA", serverA)

    zenoB = zeno(configB)
    if zenoB is None:
        sys.exit(1)
    serverB = get_server(zenoB)
    zenoB.start_processing()
    app.mount("/zenoB", serverB)

    app.mount("/api", api_app)

    app.mount(
        "/",
        StaticFiles(
            directory=os.path.dirname(os.path.realpath(__file__)) + "/frontend",
            html=True,
        ),
        name="base",
    )

    print("Running server")

    port = 8000
    port_arg = os.getenv("PORT")
    if port_arg is not None:
        port = int(port_arg)

    uvicorn.run(app, host="localhost", port=port)
