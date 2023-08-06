# collabutils

[![Build Status](https://github.com/dlce-eva/collabutils/workflows/tests/badge.svg)](https://github.com/dlce-eva/collabutils/actions?query=workflow%3Atests)
[![Documentation Status](https://readthedocs.org/projects/collabutils/badge/?version=latest)](https://collabutils.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/collabutils.svg)](https://pypi.org/project/collabutils)


Utilities for collaborative curation of data - in particular for curating cross-linguistic data via
[cldfbench](https://github.com/cldf/cldfbench).


## Installation

Install via
```shell
pip install collabutils
```

Note that some modules have "extra" requirements, thus can only be used when these extras are
installed as well. Refer to the docs linked below for details.


## Curating tabular data

In a `cldfbench`-enabled curation workflow, it is often required to curate the
"configuration data", i.e. data in a dataset's `etc/` directory collaboratively -
or even share it (e.g. language lists) across multiple datasets.

Thus, curating this data in collaborative spreadsheet apps, and only pulling it into
the dataset repository when `cldfbench download` is run, can be a solution.

`collabutils` provides functionality to do this easily

- [from Google Sheets](https://collabutils.readthedocs.io/en/latest/googlesheets.html)
- [from OwnCloud installations](https://collabutils.readthedocs.io/en/latest/oc.html)


## Curating lexical data

While simple wordlists are somewhat easy to maintain as single table, this gets
considerably trickier when cognate codings are added. Thus, curating lexical
data with cognate codings can profit from specialized apps.

`collabutils` provides functionality to pull down lexical data curated

- [in EDICTOR](https://collabutils.readthedocs.io/en/latest/edictor.html)


## Curating bibliographies

Sources referenced in datasets are another type of data, that may be better curated
with tools tailored to bibliographical data.

`collabutils` provides functionality to sync bibliographies between a dataset's
sources file and

- [Zotero](https://collabutils.readthedocs.io/en/latest/zotero.html)
- Overleaf: coming soon!

