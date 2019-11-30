# rio-tiler benchmarking

[![CircleCI](https://circleci.com/gh/vincentsarago/rio-tiler-bench.svg?style=svg)](https://circleci.com/gh/vincentsarago/rio-tiler-bench)

Benchmark of rio-tiler with GDAL 2.4 and GDAL 3.0

This was created mostly to investigate https://github.com/RemotePixel/amazonlinux/issues/10

# Results

```
$ docker-compose run gdal2
$ docker-compose run gdal3
```


--- | GDAL 2.4 (gdalwarp) | GDAL 3.0 (gdalwarp) | GDAL 2.4 (rio-tiler) | GDAL 3.0 (rio-tiler)
--- | ---                 | ---                 | ---                  | ---     
Canada | | | | |
**Time** | 0.19 | 0.20 | 0.18 | 0.17 
**Overview level** | 1 | 1 | 1 | 1
**HTTP call** | 4 | 4 | 4 |  4
**Bytes transfered** | 79921 | 79921 |  79921 | 98612
--- | ---                 | ---                 | ---                  | ---     
France | | | | |
**Time** | 0.19 | 0.23 | 0.06 | 0.08
**Overview level** | 1 | 1 | 1 | 1
**HTTP call** | 6 | 6 | 6 | 6
**Bytes transfered** | 554897 | 554897 |  554897 | 554897
--- | ---                 | ---                 | ---                  | ---     
Chile | | | | |
**Time** | 0.19 | 0.23 | 0.06 | 0.08
**Overview level** | 1 | 1 | 1 | 1
**HTTP call** | 5 | 5 | 5 | 5
**Bytes transfered** | 517705 | 517705 |  517705 | 533409
--- | ---                 | ---                 | ---                  | ---     
Brazil | | | | |
**Time** | 0.31 | 0.23 | 0.05 | 0.08
**Overview level** | 2 | 2 | 2 | 2
**HTTP call** | 4 | 4 | 4 | 4
**Bytes transfered** | 293305 | 293305 |  293305 | 301337
--- | ---                 | ---                 | ---                  | ---     
NewZealand | | | | |
**Time** | 0.20 | 0.23 | 0.06 | 0.08 
**Overview level** | 1 | 1 | 1 | 1
**HTTP call** | 7 | 7 | 7 | 7
**Bytes transfered** | 705004 | 705004 |  705004 | 705004
--- | ---                 | ---                 | ---                  | ---     
Antartica | | | | |
**Time** | 0.16 | 0.21 | 0.02 | 0.06 
**Overview level** | 0 | 0 | 0 | 0
**HTTP call** | 4 | 4 | 4 | 4
**Bytes transfered** | 49512 | 65792 | 65844 | 65844
--- | ---                 | ---                 | ---                  | ---     
Australia | | | | |
**Time** | 0.18 | 0.21 | 0.04 | 0.07 
**Overview level** | 2 | 2 | 2 | 2
**HTTP call** | 5 | 5 | 5 | 5
**Bytes transfered** | 454481 | 454481 |  400119 | 400119

# Profile
function | new rio-tiler | old rio-tiler
--- | --- | ---
GDAL 2 | 
WarpedVRTReaderBase | 0.264 |  0.213
calculate_default_transform | 0.003 | 0.008
GET | 4 | 4 
Data | 79 921 | 79 921
--- | --- | ---
GDAL 3 | 
WarpedVRTReaderBase | 0.213 |  **3.180**
calculate_default_transform | 1.022 | 1.030
GET | 4 | 4 
Data | 98 612 | 98 612