# Dockerfile for a STEGOWIPP image made by Nicolas Issa
# Comment using the # symbol to debug any lines of code
# (Ctrl + /) comments/uncomments all highlighted lines of code
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Create working directory to be /app/STEGOWIPP
WORKDIR /app
RUN mkdir STEGOWIPP
WORKDIR /app/STEGOWIPP

# Default Environmental Variables
# PRCMODE can be either linear or cluster
ENV ROOTDIR="/app/STEGOWIPP/"
ENV SRCDIR="/app/STEGOWIPP/src/"
ENV RESULTS="/app/STEGOWIPP/src/videos/processed/"
ENV TEMPIMG="/app/STEGOWIPP/src/videos/tempimages/"

ENV VIDEO="/app/STEGOWIPP/src/videos/ARC_Video.MOV"
ENV PRCMODE="linear"

COPY . /app/STEGOWIPP

# Set default shell to Bash and add 'conda' command to the PATH env variable
SHELL ["/bin/bash", "--login", "-c"]
ENV PATH /opt/conda/bin:$PATH

# Update conda to the latest version
RUN conda update conda

# Install git
RUN apt-get update && \
    apt-get install -y git

# Install cython and pydensecrf
RUN pip install cython && \
    conda install -c conda-forge pydensecrf

# Create the stegowipp environment and activate it
RUN conda env create -f environment.yml

RUN conda init bash && \
    source ~/.bashrc

RUN source activate stegowipp

# Run STEGO_WIPP.py when container is run
# Curr DIR is /app/STEGOWIPP/
CMD ["python", "/app/STEGOWIPP/src/STEGO_WIPP.py"]
