# Development

Below you will find basic setup and deployment instructions for the Health
Assessment Workspace Collaborative project.  To begin you should have the
following applications installed on your local development system:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) == 3.9
- [Node.js](https://nodejs.org)
- [Yarn](https://yarnpkg.com/)
- [PostgreSQL](https://www.postgresql.org/) == 12

When writing code for HAWC, there are a few requirements for code acceptance. We have built-in CI using github actions for enforcement:

- Python code must comply with code formatters and linters: black, flake8, and isort
- Javascript code must comply with eslint formatters
- All unit-test (currently in python-only) must pass; please write test when contributing new code

See the `Useful utilities` below for more details on how to automatically lint/format your code.

## Environment setup


HAWC can be developed both on Windows and and Linux/Mac. Development on Mac/Linux is preferred as it is more similar to the deployment environments, and things are a little more out of the box. Instructions are provided below for both environments.

```bash title="Mac/Linux"
# clone repository; we'll put in ~/dev but you can put anywhere
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/shapiromatron/hawc.git

# create virtual environment and install requirements
cd ~/dev/hawc
python -m venv venv

# activate the environment
source ./venv/bin/activate

# install requirements
./venv/bin/pip install -r ./requirements/dev.txt

# create a PostgreSQL database and superuser
createuser --superuser --no-password hawc
createdb -E UTF-8 -U hawc hawc
```

For Windows, use anaconda or miniconda to get requirements can be used to get dependencies:

```batch title="Windows"
:: create a conda environment with our hard to get dependencies
conda create --name hawc
conda activate hawc
conda install python=3.9 postgresql=12
conda install -c conda-forge nodejs
conda install -c conda-forge yarn

:: clone repository; we'll put in dev but you can put anywhere
mkdir %HOMEPATH%\dev
cd %HOMEPATH%\dev
git clone https://github.com/shapiromatron/hawc.git

:: install python requirements
cd %HOMEPATH%\dev\hawc
python -m pip install --upgrade pip
pip install -r requirements\dev.txt

:: setup and start PostgreSQL; in this example we'll put it in dev
cd %HOMEPATH%\dev
mkdir pgdata
pg_ctl -D pgdata initdb
mkdir pgdata\logs
pg_ctl -D pgdata -l pgdata\logs\logfile start

:: create our superuser and main/test databases
createuser --superuser --no-password hawc
createdb -T template0 -E UTF8 hawc
createdb -T template0 -E UTF8 hawc-test
```

## Running the application

After installing hawc above, you can access the hawc application management commands using the `manage` command in your terminal. You can also use `manage.py` on mac or linux; this was done to mirror the django [manage.py](https://docs.djangoproject.com/en/4.1/ref/django-admin/) convention.

### Linux/Mac

In the first terminal, let's create our database and then run the python webserver:

```bash title="Terminal #1"
# active python virtual environment
cd ~/dev/hawc
source ./venv/bin/activate

# update python/js packages; sync app state with database
make sync-dev

# run development webserver
manage runserver
```

In a second terminal, run the node development webserver for javascript:

```bash title="Terminal #2"
# navigate to frontend folder
cd ~/dev/hawc/frontend

# install javascript dependencies
yarn install

# start node hot-reloading server
npm start
```

If you navigate to [localhost](http://127.0.0.1:8000/) and see a website, you're ready to begin coding!

### Windows

In the first terminal, let's create our database and then run the python webserver:

```batch title="Terminal #1"
:: activate our environment
conda activate hawc

:: start the postgres database (if not already started)
pg_ctl -D %HOMEPATH%\dev\pgdata -l %HOMEPATH%\dev\pgdata\logs\logfile start

:: update python/js packages; sync app state with database
make sync-dev

:: run development webserver
manage runserver
```

In a second terminal, run the node development webserver for javascript:

```batch title="Terminal #2"
:: activate our environment
conda activate hawc

:: navigate to frontend folder
cd %HOMEPATH%\dev\hawc\frontend

:: install javascript dependencies
yarn install

:: start node hot-reloading server
npm start
```

If you navigate to [localhost](http://127.0.0.1:8000/) and see a website, you're ready to begin coding!

### Useful utilities

There are a number of helpful utility commands available from the command line.
A full list of these commands is located in the ``Makefile`` or ``make.bat`` (depending on the OS), but they are called using the same commands.

```bash
# run unit tests
make test
make test-js

# run integration tests
make test-integration

# run integration tests with a visible chrome window and debugger
make test-integration-debug

# lint code (show changes required) - all, javascript-only, or python-only
make lint
make lint-js
make lint-py

# format code (try to make changes) - all,  javascript-only, or python-only
make format
make format-js
make format-py
```

On Mac/Linux; if you have [tmux](https://github.com/tmux/tmux/wiki) installed, there's a one-line command to start the environment

```bash
# use the bundled dev `tmux` dev environment
make dev
```

On Windows; if you created the pgdata folder in %HOMEPATH%\dev, there's a short command to start the database

```bash
# start postgres db (if pgdata folder is located in %HOMEPATH%\dev)
make startdb
```

## Local Settings
### Django settings inheritance

HAWC settings are structured according to the django settings framework. Within ``hawc/main/settings``, there are a number of settings files that inherit using the following pattern:

```text
            -------------------
            |  HAWC SETTINGS  |
            -------------------
                    |
                    |
                -----------
                | base.py |
                -----------
                /        \
                /          \
    --------------       ----------        ------------
    | staging.py |       | dev.py |  <---  | local.py |
    --------------       ----------        ------------
            |                  |             (applied to dev.py,
            |                  |                 if file exists)
    -----------------    ---------------
    | production.py |    | unittest.py |
    -----------------    ---------------
```

To make changes to your local environment, create (and then modify) ``hawc/main/settings/local.py``. This file is not created by default (and is not tracked in git), but a template can be copied and renamed from ``hawc/main/settings/local.example.py`` as a starting point. You can make changes to this file to configure your local environment, such as which database is used or the "flavor" of HAWC (see "More Settings").


## Testing HAWC

### The test database

A test database is automatically loaded each time you run the unit tests; it contains simplistic data for every model in HAWC.

This makes the test database useful when writing new features. There are multiple users you can use, each with their own global and assessment-level permissions. If you have the test database loaded in, you can log in using the credentials below:

 Role                | Email                    | Password
---------------------|--------------------------|----------
 **Administrator**   | admin@hawcproject.org    | pw
 **Project manager** | pm@hawcproject.org       | pw
 **Team member**     | team@hawcproject.org     | pw
 **Reviewer**        | reviewer@hawcproject.org | pw

As new features are added, adding and changing content in the test database will be required to test these features. Instructions for loading and dumping are described below.

#### Generating the test database

Follow the instructions below to generate a test database.

```bash title="Mac/Linux"
# specify that we're using the unit-test settings
export "DJANGO_SETTINGS_MODULE=hawc.main.settings.unittest"

# load existing test
createdb hawc-fixture
manage load_test_db

# now make edits to the database using the GUI or via command line

# export database
manage dump_test_db
```

```batch title="Windows"
:: specify that we're using the unit-test settings
set DJANGO_SETTINGS_MODULE=hawc.main.settings.unittest

:: load existing test
createdb -T template0 -E UTF8 hawc-fixture
manage load_test_db

:: now make edits to the database using the GUI or via command line

:: export database
manage dump_test_db
```

If tests aren't working after the database has changed (ie., migrated); try dropping the test-database with the command ``dropdb hawc-test``.

Some tests compare large exports on disk to ensure the generated output is the same as expected. In some cases, these export files should changes. Therefore, you can set a flag in the `tests/conftest.py` to set `rewrite_data_files` to True. This will rewrite all saved files, so please review the changes to ensure they're expected. A test is in CI to ensure that `rewrite_data_files` is False.


### Loading a database dump

If you have a database dump saved locally, you can load that in instead. If you have multiple databases, you can switch them on the fly in your local.py settings (see Django Settings Inheritance above).

```bash

# add hawc superuser
createuser hawc --superuser --no-password

# create new database owned by a hawc user
createdb -O hawc hawc

# load gzipped database
gunzip -c "db_dump.sql.gz" | psql -U hawc -d hawc
```

### Creating a database dump

Here's how to create a database dump:

```bash
# anonymize data
manage scrub_db

# dump in gzipped format
pg_dump -U hawc hawc | gzip > db_dump.sql.gz
```


### Mocking external resources in tests

When writing tests for code that accesses external resources (e.g., data from PubMed API endpoints), the ``vcr`` python package is used to save "cassettes" of expected responses for faster tests and stability in case external resources are intermittently offline. These cassettes can be rebuilt by running ``make test-refresh``, which will delete the ``cassettes`` directory and run the python test suite, which will recreate the cassettes based on actual responses.

If a test uses an external resource, ensure that it is decorated with ``@pytest.mark.vcr`` to generate a cassette; see our current tests suite for examples.

To run tests without using the cassettes and making the network requests, use:

```bash
py.test --disable-vcr
```

### Testing celery application

The following requires ``redis-cli`` and ``docker-compose``.

To test asynchronous functionality in development, modify your ``hawc/main/settings/local.py``:

```python
CELERY_BROKER_URL = "redis://:default-password@localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://:default-password@localhost:6379/2"
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False
```

Then, create the example docker container and start a celery worker instance:

```bash
# build container
docker-compose -f compose/dc-build.yml --project-directory . build redis
docker-compose -f compose/dc-build.yml --project-directory . up -d redis

# check redis is up and can be pinged successfully
redis-cli -h localhost -a default-password ping

# start workers
celery --app=hawc.main.celery worker --loglevel=INFO
celery --app=hawc.main.celery beat --loglevel=INFO

# stop redis when you're done
docker-compose -f compose/dc-build.yml --project-directory . down
```

Asynchronous tasks will not be executed by celery workers instead of the main thread.

### Integration tests

While the standard tests check that the backend views and models interact as designed, integration testing checks whether the frontend of HAWC functions in a browser as intended. These tests use [playwright](https://playwright.dev/python/). By default, integration tests are skipped when running pytest locally by default, but are always executed in github actions. To run:

```bash title="Mac/Linux"
# to run all
make test-integration-debug

# or a custom method to run a single test
export INTEGRATION_TESTS=1
py.test -sv tests/integration/test_login.py --pdb
```

```batch title="Windows"
:: to run all
make test-integration-debug

:: or a custom method to run a single test
set INTEGRATION_TESTS=1
py.test -sv tests/integration/ --pdb
```

By default, the integration tests run in "headless" mode, or without a browser being shown. When editing integration tests, use the interactive mode to capture user operations:

```bash
make test-integration-debug

# use set instead of export on windows
export INTEGRATION_TESTS=1
export PWDEBUG=1
py.test -sv tests/integration/test_login.py --pdb
```


## More settings

### Visual Studio Code

[Visual Studio Code]( https://code.visualstudio.com/) is the recommended editor for this project. Recommended extensions include:

- [Python for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Eslint for VS Code](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

When using the recommended settings below, your python and javascript code should automatically format whenever you save to fix most, but not all requirements. In addition, you should have pretty good autocompletion. Python type annotations are enabled with warnings, but not enforced; this may change as we continue to annotate the existing codebase. You can add these settings to your overall VSCode settings.json file, or create a [workspace](https://code.visualstudio.com/docs/editor/workspaces) for HAWC and add it to the workspace settings.json file.

```json
{
    "[dockerfile]": {
        "editor.formatOnSave": false
    },
    "[javascript]": {
        "editor.formatOnSave": false,
    },
    "[markdown]": {
        "editor.wordWrap": "bounded",
        "editor.quickSuggestions": false
    },
    "[python]": {
        "editor.formatOnPaste": false,
    },
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },
    "editor.formatOnPaste": true,
    "editor.formatOnSave": false,
    "editor.rulers": [100, 120],
    "editor.tabSize": 4,
    "eslint.format.enable": true,
    "files.eol": "\n",
    "files.exclude": {
        "**/*.pytest_cache": true,
        "**/__pycache__": true
    },
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnknownMemberType": "information",
    },
    "python.analysis.typeCheckingMode": "basic",
    "python.autoUpdateLanguageServer": true,
    "python.formatting.provider": "black",
    "python.languageServer": "Pylance",
    "python.linting.flake8Enabled": true,
    "search.exclude": {
        "**/node_modules": true,
        "**/.git": true,
    },
}
```

### HAWC flavors

Currently HAWC has two possible application "flavors", where the application is slightly different depending on which flavor is selected. To change, modify the ``HAWC_FLAVOR`` variable at ``hawc/main/settings/local.py``.

Possible values include:

- PRIME (default application; as hosted at <https://hawcproject.org>)
- EPA (EPA application; as hosted at EPA)


### Materialized views

HAWC is in essence two different systems with very different data requirements:

1. It is a content-management capture system for data used in systematic reviews
2. It is a data visualization and summarization system of these data

To facilitate #2, materialized views have been added and other caching systems to precompute views
of the data frequently used for generate data visuals and other insights. In production, materialized
views are refreshed daily via a persistent celery task, as well as up to every five minutes if a
flag for updating the data is set.

In development however, we generally do not run the celery task service in the backend. Thus, to
trigger a materialized view rest, you can use a `manage` command:

```bash
manage refresh_views
```

You may need to do this periodically if your data is stale.

### Lines of code

To generate a report on the lines of code, install [cloc](https://github.com/AlDanial/cloc) and then run the make command:

```bash
make loc
```