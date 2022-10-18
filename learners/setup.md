---
title: Setup
---

## Setup

Please perform this setup before you start with the first episode.

## Data Sets

Download the [data zip file](data/data.zip) and unzip it to your Desktop

## Software Setup

### MUSCLE3

Installing MUSCLE3 on Python will install all the Python-based components of the system, i.e. the Python version of libmuscle, the YMMSL Python library, and the MUSCLE Manager. This requires at least Python 3.6.

MUSCLE3 is on PyPI as an ordinary Python package, so it can be installed via Pip in the usual way. It’s normally a good idea to make a virtual environment (virtualenv), if you don’t yet have one:

```bash
python3 -m venv muscle3_venv
. muscle3_venv/bin/activate
pip install -U pip setuptools wheel
pip install muscle3
```

This will create a Python virtualenv in a directory named muscle3_venv in your home directory, and then activate it. This means that when you run Python, it will use the version of Python in the virtual environment, and see the packages you have installed there. Of course, you can put it wherever you want it.

Next, we upgrade pip, the Python package installer (most systems have an old version, and old versions sometimes give problems), setuptools (same thing) and we install wheel (which can cause packages to fail to install if it’s not there).

Having made a good environment, we can then install MUSCLE3 inside of it. Once that’s done, you can use MUSCLE3 whenever you have the virtualenv activated. This will also install the Python YMMSL library, and any required dependencies.
