# Dockerfile for a STEGO image made by Nicolas Issa
# Comment using the # symbol to debug any lines of code
# (Ctrl + /) comments/uncomments all highlighted lines of code
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

# Environmental Variables
ENV ROOTDIR=/STEGOWIPP
ENV VIDEODIR=/STEGOWIPP/src/videos
ENV SRCDIR=/STEGOWIPP/src

COPY . ./

# RUN conda install python=3.8.16 && \
#     conda remove python=3.10

# Downgrade to conda 4.8 since it doesn't freeze on solving environment
# RUN conda install conda=4.10
RUN conda update conda

# Install mamba
RUN conda install -c conda-forge mamba

# Create the stegowipp environment and activate it
RUN mamba env create -f environment.yml
RUN conda activate stegowipp


CMD [ "python", "./STEGOWIPP/src/STEGO_WIPP.py" ]












# # Open port 8888
# EXPOSE 8888

# # Install anaconda
# RUN apt-get update && \
#     apt-get install -y wget bzip2 git && \
#     rm -rf /var/lib/apt/lists/*

# RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh -O ~/anaconda.sh && \
#     /bin/bash ~/anaconda.sh -b -p /opt/conda && \
#     rm ~/anaconda.sh

# # Downgrade to conda 4.8 since it doesn't freeze on solving environment
# # RUN conda install conda=4.8

# ENV PATH /opt/conda/bin:$PATH

# # Prereqs for pytorch build from source
# RUN conda install cmake ninja

# RUN git clone --recursive https://github.com/pytorch/pytorch.git && \
#     cd pytorch && \
#     git checkout tags/v2.0.0 -b v2.0.0

# WORKDIR /pytorch
# RUN make -f docker.Makefile

# # # Build pytorch from source
# # RUN apt-get update && \
# #     apt-get install -y git cmake ninja && \
# #     pip install numpy
# #
# # RUN git clone --recursive https://github.com/pytorch/pytorch.git && \
# #     cd pytorch && \
# #     git checkout tags/v2.0.0 -b v2.0.0
# #
# # RUN pip install -r requirements.txt
# #
# # # Linux dependencies
# # RUN conda install mkl mkl-include && \
# #     conda install -c pytorch magma-cuda117
# #
# # RUN cd pytorch && \
# #     export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"} && \
# #     python setup.py develop
# #
# # RUN python -c 'import torch; print(torch.__version__)'
