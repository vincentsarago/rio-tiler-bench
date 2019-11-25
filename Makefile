
SHELL = /bin/bash

################################################################################
# BUILD
gdal2:
	docker build --build-arg GDAL_VERSION=2.4 --tag img:latest  .

gdal3:
	docker build --build-arg GDAL_VERSION=3.0 --tag img:latest  .

run:
	docker run \
		--name bench \
		--volume $(shell pwd):/local \
		--env CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.tif \
		--env GDAL_CACHEMAX=25% \
		--env GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR \
		--env GDAL_HTTP_MERGE_CONSECUTIVE_RANGES=YES \
      	--env GDAL_HTTP_MULTIPLEX=YES \
		--env GDAL_HTTP_MULTIRANGE=YES \
      	--env GDAL_HTTP_VERSION=2 \
		--env VSI_CACHE=TRUE \
		--env VSI_CACHE_SIZE=536870912 \
		-itd img:latest /bin/bash

################################################################################
# TESTS
test2: gdal2 run
	docker exec -it bench bash -c 'python -m rio_tiler_bench > /local/gdal2.4_results.json'
	docker stop bench
	docker rm bench


test3: gdal3 run
	docker exec -it bench bash -c 'python -m rio_tiler_bench > /local/gdal3.0_results.json'
	docker stop bench
	docker rm bench


################################################################################
clean:
	docker stop bench
	docker rm bench
