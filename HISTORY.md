# History
## 0.9.1 (2025-06-25)
* Moves to python 3.12
* Updates dependencies
  
## 0.8.2 (2022-10-19) - Explicit JSONSerializable
* Adds JSONSerializable class for more explicit inheritance, improves CLI
* Adds mixin for dicom -> json dataset conversion

## 0.8.1 (2022-10-17) - Add cli
* Adds single cli method to convert DICOM to annotated JSON (#13)
* Adds tag decription to annotated JSON (AnnotatedDataset)

## 0.7.1 (2022-10-13) - Pypi info fix
* Adds missing readme, license, repo to project description

## 0.7.0 (2022-10-13) - More dusting, AnnotatedDataset
* Replaces readthedocs with simple markup readme
* Renames and refactors code, removes outdated and disused code
* Adds AnnotatedDataset, a json representation of a Dataset, with annotations per tag. No docs yet, sorry, alpha!

## 0.6.0 (2022-10-12) - Dust off code
* Moves to PEP517-consistent poetry package management
* Adds flake and mypy checks
* Lints all code flake8 and mypy
* Removes python 3.7 support

## 0.1.0 (2019-12-31)
* First release on PyPI.
