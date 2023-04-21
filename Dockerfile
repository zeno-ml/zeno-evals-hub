# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9

RUN useradd -m -u 1000 user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH \
    PORT=7860
WORKDIR $HOME/app
# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app
# ADD --chown=user ./.zeno_cache $HOME/app/.zeno_cache
RUN chown user:user -R $HOME/app

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install .


CMD ["python" "-m" "zeno-evals-hub" "evals/evals.yaml"]