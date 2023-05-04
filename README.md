# GitHub_Coursera
Test Repo for Coursera Github Training
I am editing the README file. Adding some more details about the project description.

## Local Development Environment Setup
* [Install the CloudSDK](https://docs.google.com/document/d/1u17vPzBI7j_vl63ibgjltc0hsKodM8EOU9jp_rJ8iq0/edit) - Link to Documentation
  * In PowerShell
    * `$env:CLOUDSDK_PROXY_TYPE='http'`
    * `$env:CLOUDSDK_PROXY_ADDRESS='proxy.ec.equifax.com'`
    * `$env:CLOUDSDK_PROXY_PORT=18717`
    * `$env:CLOUDSDK_PROXY_USERNAME=’username’`
    * `$env:CLOUDSDK_PROXY_PASSWORD=’password’`
    * `(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe") & $env:Temp\GoogleCloudSDKInstaller.exe`
* Open new installed application, **Cloud Tools for PowerShell**
  * In Cloud Tools for Powershell, run the following commands
    * `gcloud config unset proxy/type`
    * `gcloud config unset proxy/address`
    * `gcloud auth application-default login`
    * `gcloud auth login`
  * Test Access - Try to run one of the following in Cloud Tools for Powershell
    * `gsutil ls` - Will return a list of all GCS buckets in default environment
    * ``bq query --nouse_legacy_sql 'SELECT COUNT(*) FROM `corpsvc-fint-edh1-prd-de9f.corpsvc_fint_prd_ews_datasources.dim_calendar`'``
      * Will return a count of total number of records in dim_calendar
* Pycharm Setup
  * Download [Pycharm Community Edition](https://www.jetbrains.com/pycharm/download/#section=windows)
* Local Development Setup
  * Setup access to Github - [Creating a user in Github](https://equifax.atlassian.net/wiki/spaces/GCIC/pages/584716445/Creating+a+user+in+Github)
    * Add new users to [csa-edh-ewsbi-maintain](https://github.com/orgs/Equifax/teams/csa-edh-ewsbi-maintain) group
    * Add new users to [csa-edh-ewsbi-write](https://github.com/orgs/Equifax/teams/csa-edh-ewsbi-write) group
  * Download [Github Desktop](https://desktop.github.com/)
  * Clone the ews-fin-bi-reporting repo down to your local machine
  * Set up a new PyCharm project in the newly cloned repo using the following
    *  New Virtualenv using Python 3.9 (you may need to install from [python.org](https://www.python.org/downloads/release/python-3910/))
  * In PyCharm, go to `Settings -> Tools -> Terminals`
    * Set `Shell path` from `powershell.exe` to `cmd.exe`
  * Run the following in the PyCharm Terminal
    * `pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org`
    * If the above errors, try running the following individually:
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org apache-airflow`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org apache-airflow-providers-google`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pytest`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pandas`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org google-cloud-storage`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org gcsfs`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org google-cloud-bigquery`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyspark`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org xlrd`
      * `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org googlemaps`
    * If additional errors occur, let data team know for troubleshooting
    * If everything is installed correctly, any errors for package imports should disappear, and it should now be possible to run the below
      * Terminal - Run `pytest` - This will kick off the current tests

## Adding a new DAG
* Run the script **create_new_dag_directory.py** using the following terminal command:
  * `python ews_bi\dags\utils\python\create_new_dag_directory.py <pipeline_name> <template_to_copy>` - Acceptable values are template_pipeline, template_file_drop_pipeline, template_file_ingest_pipeline
  * This will create all the needed initial template files for the DAG, markdown, and a SQL directory / file
* Build your DAG
  * Coding Standards - See `template_pipeline` for additional details. These are largely naming conventions as the tasks portions are laid out in the template_pipeline
    * Naming Conventions
      * SQL Files - Should mirror the name of the task 
        * Example - `'load_calendar_data.sql'`
      * default_args - Keys should strip off the .sql from the name of the sql file and add query for clarity
        * Example - `'load_calendar_data_query': 'load_calendar_data.sql'`
      * params - Keys should indicate whether the params will create a view or table.
        * Example - `'load_calendar_data_table': 'dim_calendar',`
      * Task Names / IDs - Names / IDs should simply strip off the _query, _view, or _table
        * Example - `load_calendar_data = BigQueryExecuteQueryOperator(task_id='load_calendar_data',`
* Test your SQL using `python ews_bi\dags\utils\python\execute_dry_run_query.py <directory_name> <sql_file>`
  * This executes a dry run against BQ to see if the SQL will process anything
  * Successful SQL will return total bytes to be processed
* Once complete, parameterize the SQL using **sql_parameterizer.py** as follows for each SQL file:
  * `python ews_bi\dags\utils\python\sql_parameterizer.py <pipeline_directory> <sql_file>.sql params`
  * Note: This process can also be reversed to get SQL by switching **params** to **sql** in the above

## Repo Structure
* ews_bi/dags
  * DAG Directory - Repeated for all unique DAGs
    * <file_dag.py> - Must have _dag.py or will not be deployed
    * .md - Markdown file detailing the DAG / data flow
    * sql
      * <sql_file.sql> - All files with .sql will be deployed to Composer
  * utils
    * dataproc_scripts - Folder containing scripts that utilize Dataproc
    * default_args - Folder containing default arguments for DAG, Can be overwritten
      * default-args-environ.json - Proper default arguments are dynamically loaded on DAG run
    * params - Folder containing default params for queries like projects, datasets, etc,
      * params-envrion.json - Proper params are dynamically loaded on DAG run
    * python - Folder containing Python holder functions
      * create_new_dag_directory.py - Setup a new DAG / pipeline directory
        * Args - <directory_name> <template_to_copy> - Acceptable values are template_pipeline, template_file_drop_pipeline, template_file_ingest_pipeline
      * find_usage.py - Find string in SQL files to determine usage
        * Args - <string to search for in SQL>
      * local_helpers.py - Class / functions to help with local debugging
      * read_configs.py - Class / functions for loading default arguments and params
      * sql_parameterizer.py - Convert a .SQL file from SQL to params and params to SQL
        * Args - <directory_name> <sql_file> <params or sql>
      * execute_dry_run_query.py - Run a de-parameterized query as a dry run against BQ to ensure it works
        * Args - <directory_name> <sql_file>
    * sql - Folder containing generic SQL statements
      * create_repalce_view.sql - SQL function to generate view on top of landed table
* scm - This folder houses the Jenkins build options - DO NOT CHANGE
* tests - contains Pytests to be run before creating a PR / merge
  * Current Tests
    * test_unique_file_names.py - Ensure all SQL files have unique names
    * test_valid_json.py - Ensures default_args and params are valid json
  * In Progress
    * test_vailid_dags.py - Test that a DAG will run in Airflow - NOT IN USE
* pom.xml - This file contains build options - DO NOT CHANGE

## GCS / Composer Structure
* GCS Bucket Structure
  * | GCS Bucket/
    * dags/
      * ews_bi/
        * Any file in a directory tagged as `_dag.py` will be loaded here
        * sql/
          * Any file in directory/sql ending with `.sql` will be loaded here
          * There is a pytest to check for name uniqueness
        * default_args/
          * Files in the utils/default_args directory will be loaded here to determine which runtime variables are needed
        * params/
          * Files in the utils/params directory will be loaded here to ensure the proper SQL is run
        * utils/
          * dataproc_scripts - Folder containing scripts that utilize Dataproc - Can be .py or zipped files for scripts with multiple .py files to be called
          * python - Files in utils/python ending with `.py` will be loaded here
            * read_configs.py - This file utilizes the `GCS_BUCKET` environment variable to determine dev / qa / test / prod and load the proper parameters and configurations
        * markdown/
          * Markdown files for DAGs

## Other GCS Buckets of Note
* [corpsvc-fint-edh1-prd-us-ews-bi-artifacts](https://console.cloud.google.com/storage/browser/corpsvc-fint-edh1-prd-us-ews-bi-artifacts;tab=objects?forceOnBucketsSortingFiltering=false&project=corpsvc-fint-edh1-prd-de9f&prefix=&forceOnObjectsSortingFiltering=false) - Bucket to drop data files for consumption elsewhere
* [corpsvc-fint-edh1-prd-us-ews-bi-file-ingestion](https://console.cloud.google.com/storage/browser/corpsvc-fint-edh1-prd-us-ews-bi-file-ingestion;tab=objects?forceOnBucketsSortingFiltering=false&project=corpsvc-fint-edh1-prd-de9f&prefix=&forceOnObjectsSortingFiltering=false) - Bucket for manual file ingestion 
* [corpsvc-fint-edh1-prd-us-ews-bi-dataproc-temp](https://console.cloud.google.com/storage/browser/corpsvc-fint-edh1-prd-us-ews-bi-dataproc-temp;tab=objects?forceOnBucketsSortingFiltering=true&project=corpsvc-fint-edh1-prd-de9f&prefix=&forceOnObjectsSortingFiltering=false) - Cloud Dataproc temp bucket
* [corpsvc-fint-edh1-prd-us-ews-bi-dataproc-staging](https://console.cloud.google.com/storage/browser/corpsvc-fint-edh1-prd-us-ews-bi-dataproc-staging;tab=objects?forceOnBucketsSortingFiltering=true&project=corpsvc-fint-edh1-prd-de9f&prefix=&forceOnObjectsSortingFiltering=false) - Cloud Dataproc Staging Bucket

## CI/CD Pipeline Notes
* [Jenkins](https://cicd-tools.us.equifax.com/corpsvcs-edh-jenkins/) is utilized for our CI/CD process to promote code through dev / qa / uat / prod
  * For Jenkins issues with Jenkins deploys
    * [EDH Front Door Requests](https://equifax.atlassian.net/jira/core/projects/WMEDH/form/40)
    * Once you get the automated email for ticket creation, reach out to Dinesh Kumar / Nischay Lakshminarayan
* Triggers
  * Dev Environment - `corpsvc-fintech-edh1-npe-3ae9` - Create a branch with the word `devd`
    * Composer Instance Name - `edh-platform-dev-npe-us-east1`
    * [Cloud Composer Dev](https://fe2b24ca15ba50a05p-tp.appspot.com/home)
      * Savyint Entitlement - corpsvc-fintech-edh1-npe~#~ Composer User
    * GCS Bucket - `us-east1-edh-platform-dev-n-a6567e35-bucket`
    * Folder - `dags/ews_bi`
  * QA Environment - `corpsvc-fintech-edh2-npe-5cf8` - Open a PR from any `feature-<something>` to `develop` branch
    * Composer Instance Name - `edh-platform-dev-qa-us-east1`
    * [Cloud Composer QA](https://ldbc4a0c3022a62c2p-tp.appspot.com/home)
      * Savyint Entitlement - corpsvc-fintech-edh2-npe~#~ Composer User
    * GCS Bucket - `us-east1-edh-platform-qa-np-c9f87810-bucket`
    * Folder - `dags/ews_bi`
  * UAT Environment - `corpsvc-fint-edh1-uat-prd-3f67` - Open a PR from a `release-<something>`` branch to `main`
    * Composer Instance Name - `edh-platform-uat-prod-us-east1`
    * [Cloud Composer UAT](https://j1d2a5accdbe23411p-tp.appspot.com/home)
      * Savyint Entitlement - corpsvc-fint-edh1-uat-prd~#~ Composer User
    * GCS Bucket - `us-east1-edh-platform-uat-p-7e57c3e2-bucket`
    * Folder - `dags/ews_bi`
  * Prod Environment - `corpsvc-fint-edh1-prd-de9f` - Any merge to `main`
    * Composer Instance Name - `edh-platform-prod-us-east1`
    * [Cloud Composer Prod](https://p87bd6f625fc66636p-tp.appspot.com/home)
      * Savyint Entitlement - corpsvc-fint-edh1-prd~#~ Composer User
    * GCS Bucket - `us-east1-edh-platform-prod--c4e7f121-bucket`
    * Folder - `dags/ews_bi`

## GChat Integration for Alerts
* DAGs will now alert a Google Space, [EWS Finance BI Pipeline Alerts](https://mail.google.com/chat/u/0/#chat/space/AAAAU_N6uiU), in the event of failure
