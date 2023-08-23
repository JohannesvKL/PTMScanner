# This Dockerfile builds OpenMS, the TOPP tools, pyOpenMS and thidparty tools.
# It also adds a basic streamlit server that serves a pyOpenMS-based app.
# hints:
# build image and give it a name (here: streamlitapp) with: docker build --no-cache -t streamlitapp:latest . 2>&1 | tee build.log 
# check if image was build: docker image ls
# run container: docker run -p 8501:8501 streamlitappsimple:latest
# debug container after build (comment out ENTRYPOINT) and run container with interactive /bin/bash shell
# prune unused images/etc. to free disc space (e.g. might be needed on gitpod). Use with care.: docker system prune --all --force

FROM ubuntu:22.04 AS setup-build-system
ARG OPENMS_REPO=https://github.com/OpenMS/OpenMS.git
ARG OPENMS_BRANCH=develop
ARG PORT=8501
USER root

# Install required Ubuntu packages.
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends --no-install-suggests g++ autoconf automake patch libtool make git gpg wget ca-certificates curl libgtk2.0-dev openjdk-8-jdk
RUN update-ca-certificates
RUN apt-get install -y --no-install-recommends --no-install-suggests libsvm-dev libeigen3-dev coinor-libcbc-dev libglpk-dev libzip-dev zlib1g-dev libxerces-c-dev libbz2-dev libomp-dev libhdf5-dev
RUN apt-get install -y --no-install-recommends --no-install-suggests libboost-date-time1.74-dev \
                                                                     libboost-iostreams1.74-dev \
                                                                     libboost-regex1.74-dev \
                                                                     libboost-math1.74-dev \
                                                                     libboost-random1.74-dev
RUN apt-get install -y --no-install-recommends --no-install-suggests qtbase5-dev libqt5svg5-dev libqt5opengl5-dev

# Download and install mamba.
ENV PATH="/root/mambaforge/bin:${PATH}"
RUN wget -q \
    https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh \
    && bash Mambaforge-Linux-x86_64.sh -b \
    && rm -f Mambaforge-Linux-x86_64.sh
RUN mamba --version

# Setup mamba environment.
COPY environment.yml ./environment.yml
RUN mamba env create -f environment.yml
RUN echo "mamba activate streamlit-env" >> ~/.bashrc
SHELL ["/bin/bash", "--rcfile", "~/.bashrc"]
SHELL ["mamba", "run", "-n", "streamlit-env", "/bin/bash", "-c"]

# Install up-to-date cmake via mamba and packages for pyOpenMS build.
RUN mamba install cmake
RUN pip install --upgrade pip && python -m pip install -U setuptools nose Cython autowrap pandas numpy pytest

# Clone OpenMS branch and the associcated contrib+thirdparties+pyOpenMS-doc submodules.
RUN git clone --recursive --depth=1 -b ${OPENMS_BRANCH} --single-branch ${OPENMS_REPO} && cd /OpenMS

# Pull Linux compatible third-party dependencies and store them in directory thirdparty.
WORKDIR /OpenMS
RUN mkdir /thirdparty && \
    git submodule update --init THIRDPARTY && \
    cp -r THIRDPARTY/All/* /thirdparty && \
    cp -r THIRDPARTY/Linux/64bit/* /thirdparty && \
    chmod -R +x /thirdparty
ENV PATH="/thirdparty/LuciPHOr2:/thirdparty/MSGFPlus:/thirdparty/Sirius:/thirdparty/ThermoRawFileParser:/thirdparty/Comet:/thirdparty/Fido:/thirdparty/MaRaCluster:/thirdparty/MyriMatch:/thirdparty/OMSSA:/thirdparty/Percolator:/thirdparty/SpectraST:/thirdparty/XTandem:/thirdparty/crux:${PATH}"

# Build OpenMS and pyOpenMS.
FROM setup-build-system AS compile-openms
WORKDIR /

# Set up build directory.
RUN mkdir /openms-build
WORKDIR /openms-build

# Configure.
RUN /bin/bash -c "cmake -DCMAKE_BUILD_TYPE='Release' -DCMAKE_PREFIX_PATH='/OpenMS/contrib-build/;/usr/;/usr/local' -DHAS_XSERVER=OFF -DBOOST_USE_STATIC=OFF -DPYOPENMS=ON ../OpenMS -DPY_MEMLEAK_DISABLE=On"

# Build TOPP tools, clean up and add to PATH.
RUN make -j4 TOPP
RUN rm -rf src doc CMakeFiles
ENV PATH="/openms-build/bin/:${PATH}"

# Build pyOpenMS wheels and install via pip.
RUN make -j4 pyopenms
WORKDIR /openms-build/pyOpenMS
RUN pip install dist/*.whl


# Copy share folder and remove source directory.
WORKDIR /
RUN mkdir app
RUN cp -r OpenMS/share/OpenMS /app/openms-share
RUN rm -rf OpenMS

# Copy TOPP tools bin directory and remove build directory.
RUN cp -r openms-build/bin app/openms-bin
RUN rm -rf openms-build

# Prepare and run streamlit app.
FROM compile-openms AS run-app
# Create workdir and copy over all streamlit related files/folders.

# note: specifying folder with slash as suffix and repeating the folder name seems important to preserve directory structure
WORKDIR /app
COPY app.py /app/app.py 
COPY src/ /app/src
COPY assets/ /app/assets
COPY example-data/ /app/example-data
COPY pages/ /app/pages

# TODO install cron (TODO: think about automatic clean up of temporary files and workspaces)
# RUN apt-get install -y cron

# Run app as container entrypoint.
EXPOSE $PORT
ENTRYPOINT ["mamba", "run", "--no-capture-output", "-n", "streamlit-env", "streamlit", "run", "app.py"]
