# A Python library for Rule-Based reference parsing

refparse is an effective tool designed to extract structured data from unformatted reference strings. It is capable of parsing reference strings from **Web of Science, Scopus and CSSCI**.

## Install
Ensure Python 3.9 or higher is installed on your device.

```console
$ pip install refparse
```

## Basic Usage
```python
>>> import refparse
>>> source = "scopus"
>>> ref = "LeCun Y., Bengio Y., Hinton G., Deep learning, Nature, 521, pp. 436-444, (2015)"
>>> print(refparse.parse(ref, source))

{'author': 'LeCun Y., Bengio Y., Hinton G.',
 'title': 'Deep learning',
 'source': 'Nature',
 'volume': '521',
 'issue': None,
 'page': '436-444',
 'year': '2015'}
```

## Return Fields

|        | Web of Science | Scopus  | CSSCI*  |
| :---:  | :---:          | :---:   | :---:   |
| author | &check;        | &check; |         |
| title  |                | &check; |         |
| source | &check;        | &check; |         |
| volume | &check;        | &check; |         |
| issue  |                | &check; |         |
| page   | &check;        | &check; |         |
| year   | &check;        | &check; |         |
| doi    | &check;        |         |         |
| identifier except doi | |         | &check; |

\* CSSCI will return differently depending on reference type.
