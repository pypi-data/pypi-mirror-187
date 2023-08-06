# hitfactorpy_sqlalchemy

[![Main](https://github.com/cahna/hitfactorpy_sqlalchemy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/hitfactorpy_sqlalchemy/actions/workflows/main.yaml)

Manage practical match reports with SQLAlchemy

## Status

**Work in progress...**

## Usage

1. Run migrations on a database to create tables and types:
    ```console
    $ hitfactorpy-sqlalchemy migrate up
    ```
2. Verify DB status:
    ```console
    $ hitfactorpy-sqlalchemy migrate check
    ```
3. Import a match report from a text file:
    ```console
    $ hitfactorpy-sqlalchemy import match-report ./report.txt
    ```
4. Bulk import match reports:
    ```console
    $ find reports/ -type f -name "*.txt" | xargs hitfactorpy-sqlalchemy import match-report
    ```
