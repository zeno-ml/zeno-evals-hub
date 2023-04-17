import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# from zeno import get_server, zeno

# create zeno object
# create second zeno object

# create fastapi for both zeno objects

# serve

# get_server()


def command_line():
    app = FastAPI(title="Frontend API")
    api_app = FastAPI(title="Backend API")

    @api_app.get("/test")
    def test():
        return {"test": "test"}

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
    uvicorn.run(app)


if __name__ == "__main__":
    command_line()
