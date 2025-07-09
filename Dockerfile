// Dockerfile
FROM continuumio/miniconda3

COPY environment.yml .

RUN conda env create -f environment.yml && conda clean -a

SHELL ["/bin/bash", "-c"]

ENV PATH /opt/conda/envs/mtb_refgen_env/bin:$PATH

WORKDIR /pipeline

COPY . .

ENTRYPOINT ["nextflow"]
