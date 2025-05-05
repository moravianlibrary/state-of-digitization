# State of Digitization

## Overview

This repository provides a Python library and a simple Streamlit-based client for checking the digitization status of bibliographic records using the RDcz (Registr digitalizace) API and, in the future, the Kramerius registry.

## Library

The core library offers multiple methods to check the digitization state of records. Currently, it supports querying RDcz and is structured to support Kramerius in the future.

#### Supported Methods

- `find_by_identifiers` - find the digitization status based on selected identifiers (e.g., sysno, barcode) (Implemented). 
- `find_by_marc_record` - intended to support digitization lookups using a full MARC record (Not implemented yet).
- `find_by_marc_issue` - intended for digitization status lookups using MARC data along with issue-specific details (e.g., volume, year) (Not implemented yet).

**Note**: Kramerius registry integration is planned but not yet implemented.

## Client

A basic web client built with [Streamlit](https://streamlit.io/) is included in this repository. It provides a user-friendly interface for using the digitization-checking library.
