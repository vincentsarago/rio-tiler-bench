# rio-tiler benchmarking

[![CircleCI](https://circleci.com/gh/vincentsarago/rio-tiler-bench.svg?style=svg)](https://circleci.com/gh/vincentsarago/rio-tiler-bench)


pds | GDAL 2.4 (gdalwarp) | GDAL 3.0 (gdalwarp) | GDAL 2.4 (rio-tiler) | GDAL 3.0 (rio-tiler)
--- | --- | ---    | ---              | ---         | ---        
Canada | | | | |
**Time** | 1.11 | - | 1.13 | - 
**Overview level** | 1 | - | 1 | -
**HTTP call** | 5 | 5 | 5 | 5 
**Bytes transfered** | 79920 | - |  79920 | -
| | | | |
France | | | | |
**Time** | 1.00 | - | 1.06 | - 
**Overview level** | 1 | - | 1 | -
**HTTP call** | 7 | - | 7 | -
**Bytes transfered** | 554896 | - |  554896 | -
| | | | |
Chile | | | | |
**Time** | 1.22 | - | 0.93 | - 
**Overview level** | 1 | - | 1 | -
**HTTP call** | 6 | - | 6 | -
**Bytes transfered** | 517704 | - |  517704 | -
| | | | |
Brazil | | | | |
**Time** | 0.94 | - | 0.82 | - 
**Overview level** | 2 | - | 2 | -
**HTTP call** | 5 | - | 5 | -
**Bytes transfered** | 293304 | - |  293304 | -
| | | | |
NewZealand | | | | |
**Time** | 1.13 | - | 1.06 | - 
**Overview level** | 2 | - | 2 | -
**HTTP call** | 8 | - | 8 | -
**Bytes transfered** | 705003 | - |  705003 | -
| | | | |
Antartica | | | | |
**Time** | 1.23 | - | 0.63 | - 
**Overview level** | 0 | - | 0 | -
**HTTP call** | 5 | - | 5 | -
**Bytes transfered** | 49511 | - |  54843 | -
| | | | |
Australia | | | | |
**Time** | 0.93 | - | 1.00 | - 
**Overview level** | 2 | - | 2 | -
**HTTP call** | 6 | - | 6 | -
**Bytes transfered** | 454480 | - |  400118 | -