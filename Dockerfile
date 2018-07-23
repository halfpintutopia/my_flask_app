FROM continuumio/miniconda:latest

RUN apt-get update && apt-get install -y wget bzip2
# make sure that it runs in the image Run and then copy
RUN mkdir -p /app | \
    mkdir -p /run
# have file in docker image, new image with configuration
COPY ./app/requirements.yml /app/requirements.yml
# every time it runs, it creates new, every time your commit - it will not execute it again if you have not made any changes, it will take from cache
RUN /opt/conda/bin/conda env create -f /app/requirements.yml
# short config - all executables are in the bin
ENV PATH /opt/conda/envs/app/bin:$PATH

COPY ./app /app

COPY ./scripts/* app/scripts/
RUN chmod +x /app/scripts/*
# change mode - chmod'ed to executable, +x means execute

WORKDIR /app
