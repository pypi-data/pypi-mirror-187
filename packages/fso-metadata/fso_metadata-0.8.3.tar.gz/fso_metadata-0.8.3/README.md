# Metadata Auto

## Introduction

This repository aims to simplify the access to the [Swiss Federal Statistical Office](https://www.bfs.admin.ch/bfs/en/home.html) metadata. 
Following the implementation in the [interoperability platform](https://www.i14y.admin.ch) and the [SIS portal](https://sharepoint.admin.ch/edi/bfs/fr-ch/News/Pages/go-life-neues-sis-portals.aspx), the APIs are made available here in python.
This public library is made available for the internal FSO staff, the federal administration and for external actors.

## Installation

You can install the library with
```
pip install fso_metadata
```

then at the beginning of your python script, you will need to 
```
import fso_metadata
```

## Functionnalities
Based on the metadata that you want, you will call certain functions and parameters. 
In the first part, we describe the API available from everywhere, then we describe the API available only from within the confederation network.

### Available everywhere with the interoperability plateform (i14y)
#### Codelists
1. Export a codelist based on an identifier
```
response = get_codelist(
    identifier, 
    export_format="SDMX-ML", 
    version_format=2.1, 
    annotations=False
)
```

    Parameters:
        - identifier (str): the codelist's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - export_format (str, default="SDMX-ML"): the export's format. 
            Available are CSV, XLSX, SDMX-ML or SDMX-JSON.
        - version_format (float, default=2.1): the export format's version 
            (2.0 or 2.1 when format is SDMX-ML).
        - annotations (bool, default=False): flag to include annotations
    Returns:
        - response (pd.DataFrame or dict) based on the export format
            - a pd.DataFrame if export_format was CSV or XLSX
            - a dictionnary if export_format was SDMX-ML or SDMX-JSON.


#### Nomenclatures
   
1. Export one level of a nomenclature
```
response = get_nomenclature_one_level(
    identifier, 
    level_number, 
    filters={}, 
    language='fr', 
    annotations=False
)
```

    Parameters:
        - identifier (str): nomenclature's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - level_number (int): level to export
        - filter (default={}): additionnal filters
        - language (str, default='fr'): response data's language 
            Available are 'fr', 'de', 'it', 'en'.
        - annotations (bool, default=False): flag to include annotations
    Returns:
        - response (pd.DataFrame): dataframe with 3 columns 
            (Code, Parent and Name in the selected language)


2. Export multiple levels of a nomenclature (from `level_from` to `level_to`)
```
response = get_nomenclature_multiple_levels(
    identifier, 
    level_from, 
    level_to, 
    filters={}, 
    language='fr', 
    annotations=False
)
```

    Parameters:
        - identifier (str): nomenclature's identifier
        - environment (str, default="PRD"): environment to call
            Available are 'PRD', 'ABN', 'TEST', 'QA' and 'DEV'.
        - level_from (int): the 1st level to include
        - level_to (int): the last level to include
        - filter (default={}): additionnal filters
        - language (str, default='fr'): response data's language 
            Available are 'fr', 'de', 'it', 'en'.
        - annotations (bool, default=False): flag to include annotations
        - post_processing (bool, default=False): flag to post-process
    Returns:
        - response (pd.DataFrame): dataframe columns from `level_from` to `level_to` codes


As the APIs continue to be implemented, further functionnalities will be added.

## Background
All the APIs made available in this library are also documented in Swagger UI should you want to do more experiments through a UI. See [here](https://www.i14y.admin.ch/api/index.html) for APIs of the interoperability platform (public).

## Example

Examples for each API are provided in the notebook [examples.ipynb](https://renkulab.io/gitlab/dscc/meatadata-auto/-/blob/master/examples.ipynb).