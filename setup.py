"""Setup."""

from setuptools import setup, find_packages

# Runtime requirements.
inst_reqs = ["mercantile", "rio-tiler"]

extra_reqs = {}

setup(
    name="rio-tiler-bench",
    version="0.0.1",
    description=u"Benchmark rio-tiler",
    long_description="Benchmark rio-tiler",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COGEO CloudOptimized Geotiff rasterio",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.com",
    license="BSD-3",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
