# Dumbo Scopus

Simple CLI to search on Scopus and obtain the results in a XLSX file.


# Prerequisites

- Python 3.10
- An API key from http://dev.elsevier.com


# Install

```bash
$ pip install dumbo-scopus
```


# Usage

Use the following command line:
```bash
$ python -m dumbo_scopus "TITLE(magic sets)" --api-key=YOUR-API-KEY
```

A file `scopus.xlsx` with the results will be produced.
Add `--help` to see more options.

Check `https://dev.elsevier.com/sc_search_tips.html` for the format of the query.
Additionally, if the API key is authorized to access the [Citation Overview API](https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl), citations of an article can be obtained by using "CITATIONS(2-s2.0-scopus-id-here)" as query.
