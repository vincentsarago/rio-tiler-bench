ARG GDAL_VERSION
FROM remotepixel/amazonlinux:gdal${GDAL_VERSION}-py3.7-cogeo

COPY bench_tiler bench_tiler
COPY setup.py setup.py

RUN pip3 install .
RUN pip3 install git+https://github.com/cogeotiff/rio-tiler.git@2f4ef42cdc78c74599c21be3c6e4d89bc6474753 -U
RUN rm -rf bench_tiler setup.py