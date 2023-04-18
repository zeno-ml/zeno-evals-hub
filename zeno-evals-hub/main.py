import os
import sys

import uvicorn
import yaml  # type: ignore
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from zeno import get_server, zeno  # type: ignore
from zeno_evals import generate_zeno_config  # type: ignore


def command_line():
    app = FastAPI(title="Frontend API")

    args = []
    with open(sys.argv[1], "r") as f:
        args = yaml.safe_load(f)

    @app.get("/args")
    def get_args():
        return args

    os.chdir(os.path.dirname(sys.argv[1]))

    zeno_objs = []
    for entry in args:
        name = list(entry.keys())[0]
        params = entry[name]
        # TODO: handle not having a second results or functions file
        config = generate_zeno_config(
            params["results-file"],
            params["second-results-file"],
            params["functions-file"],
        )
        config.serve = False
        zeno_obj = zeno(config)
        if zeno_obj is None:
            sys.exit(1)
        server = get_server(zeno_obj)
        zeno_obj.start_processing()
        zeno_objs.append(zeno_obj)
        app.mount("/" + name, server)

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
