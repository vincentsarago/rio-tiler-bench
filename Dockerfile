ARG GDAL_VERSION
FROM remotepixel/amazonlinux:gdal${GDAL_VERSION}-py3.7-cogeo

COPY rio_tiler_bench rio_tiler_bench
COPY setup.py setup.py

RUN pip3 install .
RUN pip3 install git+https://github.com/cogeotiff/rio-tiler.git@e01078881d3e924d44556d94e7f10c73d4448b9c -U
RUN rm -rf rio_tiler_bench setup.py
