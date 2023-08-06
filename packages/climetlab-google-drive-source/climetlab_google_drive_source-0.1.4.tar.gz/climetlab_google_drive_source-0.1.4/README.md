## climetlab-google_drive_source

A source plugin for climetlab for the source google-drive.


Features
--------

In this README is a description of how to use the source provided by the python package google_drive_source.

## Source description

Read a publicly accessible file from google drive as if it was local (i.e. cache the file locally).

## Using climetlab to access the data

See the [demo notebooks](https://github.com/ecmwf-lab/climetlab-google-drive-source/tree/main/notebooks)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-lab/climetlab-google-drive-source/main?urlpath=lab)


- [demo.ipynb](https://github.com/ecmwf-lab/climetlab-google-drive-source/tree/main/notebooks/demo.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-google-drive-source/blob/main/notebooks/demo.ipynb) 
[![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ecmwf-lab/climetlab-google-drive-source/blob/main/notebooks/demo.ipynb) 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-lab/climetlab-google-drive-source/main?filepath=notebooks/demo.ipynb)
[<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/ecmwf-lab/climetlab-google-drive-source/tree/main/notebooks/demo.ipynb)



The climetlab python package allows easy access to the data with a few lines of code such as:
``` python

!pip install climetlab climetlab-google-drive-source
import climetlab as cml
ds = cml.load_source("google-drive", file_id="...")
# use ds as you would use cml.load("file", filename)
```

Todo
----

Add authentification support. Perhaps using the package pydrive2?


Support and contributing
------------------------

Open a issue on github or a pull request.

LICENSE
-------

See the LICENSE file.
(C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation
nor does it submit to any jurisdiction.

Authors
-------

Florian Pinault and al.

See also the CONTRIBUTORS.md file.
