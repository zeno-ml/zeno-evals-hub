import json
import os
import sys

import uvicorn
import yaml  # type: ignore
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from zeno import get_server, zeno, ZenoParameters  # type: ignore
from zeno_evals import generate_zeno_config  # type: ignore


# parse information in spec
def prepare_spec(params, second_exists):
    res = {}

    data = []
    with open(params["results-file"]) as f:
        for index, line in enumerate(f):
            data.append(json.loads(line))
            if index == 1:
                break
    data2 = []
    if second_exists:
        with open(params["second-results-file"]) as f:
            for index, line in enumerate(f):
                data2.append(json.loads(line))
                if index == 1:
                    break

    res["accuracy"] = [
        data[1]["final_report"]["accuracy"],
        data2[1]["final_report"]["accuracy"] if second_exists else "",
    ]
    return res


def prepare_zeno_params(config: ZenoParameters):
    res = {}
    res["models"] = config.models
    res["view"] = config.view
    res["data_column"] = config.data_column
    res["id_column"] = config.id_column
    res["batch_size"] = config.batch_size
    res["samples"] = config.samples
    return res


# handle not having a second results or functions file
def prepare_zeno_config(params, second_exits, function_exists) -> ZenoParameters:
    if second_exits and function_exists:
        return generate_zeno_config(
            params["results-file"],
            params["second-results-file"],
            params["functions-file"],
        )
    elif second_exits:
        return generate_zeno_config(
            params["results-file"],
            params["second-results-file"],
        )
    elif function_exists:
        return generate_zeno_config(
            params["results-file"],
            params["functions-file"],
        )
    else:
        return generate_zeno_config(
            params["results-file"],
        )


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
        second_exists = True if "second-results-file" in params else False
        function_exists = True if "function-results" in params else False
        config = prepare_zeno_config(params, second_exists, function_exists)
        params["spec"] = prepare_spec(params, second_exists)
        params["zeno"] = prepare_zeno_params(config)
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
