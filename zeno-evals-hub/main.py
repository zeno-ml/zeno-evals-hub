import json
import os
import sys

import uvicorn
import yaml  # type: ignore
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from zeno import ZenoParameters, get_server, zeno  # type: ignore
from zeno_evals import ZenoEvals  # type: ignore


# parse information in spec
def prepare_spec(file_path):
    res = {}
    data = []
    accuracy = 0
    with open(file_path) as f:
        for line in f:
            json_entry = json.loads(line)
            if "final_report" in json_entry:
                accuracy = json_entry["final_report"]["accuracy"]
            data.append(json_entry)

    res["models"] = data[0]["spec"]["completion_fns"][0]
    res["accuracy"] = accuracy * 100
    res["events"] = len(data) - 2
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

        res_spec = prepare_spec(params["results-file"])
        params["models"] = [res_spec["models"]]
        params["accuracy"] = [res_spec["accuracy"]]
        params["events"] = [res_spec["events"]]
        params["link"] = [params["link"]]
        params["description"] = [params["description"]]

        if second_exists:
            sec_res_spec = prepare_spec(params["second-results-file"])
            params["models"].append(sec_res_spec["models"])
            params["accuracy"].append(sec_res_spec["accuracy"])
            params["events"].append(sec_res_spec["events"])

        zeno_eval = ZenoEvals(
            params.get("results-file"),
            params.get("second-results-file"),
            params.get("functions-file"),
        )
        config = zeno_eval.generate_zeno_config()

        config.serve = False
        config.cache_path = "./.zeno_cache_" + name
        config.multiprocessing = False
        config.batch_size = 2000
        port_arg = os.getenv("PORT")
        if port_arg is not None:
            config.editable = False

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
    host = "localhost"
    port_arg = os.getenv("PORT")
    if port_arg is not None:
        port = int(port_arg)
        host = "0.0.0.0"

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    command_line()
