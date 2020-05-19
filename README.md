Longhorn Python Adapter Template
=========================

## Overview
This template can be used to create a python based adapter.
The template is written in Python.


### Notes
Template has three actions:
1. hello_world
2. create_template
3. run_script
There is also one action which is supposed to be by default in every adapter, verify_target.
Usually verify_target action is used to verify connection and credentials to the target during its creation in UI.


### Run adapter locally
Run adapter locally
1. Install required packages: python-dotenv, six, requests.
2. Create self-signed certificates in the custom python adapter project folder:
    Run "make create-certs" - this will create all needed certificates to run adapter https service  locally

After running certificate creation commands you will have the following files created:
    "secrets/ssl/cert/certificate.pem"
    "secrets/ssl/cert/private_key.pem"

If you want to use your own certificates, then add following environment variables:
    export CERTFILE=path_to_certificate.pem
    export PKEYFILE=path_to_private_key.pem
    export CAFILE=path_to_ca_certificate.pem

3.  Prepare JAIL environment.

Download Jailkit package and follow the INSTALL.TXT instructions.

Here are common commands to install Jail environment:
    wget http://olivier.sessink.nl/jailkit/jailkit-2.20.tar.gz
    tar -xzvf jailkit-2.20.tar.gz
    cd jailkit-2.20;./configure && make && make install
    mkdir /jail (or use some other directory)
    jk_init -j /jail jk_lsh
    PYTHON_PATH=$(which python)
    PYTHON_LIB_PATH=$(python -c "import os, inspect; print os.path.dirname(inspect.getfile(inspect))")
    jk_cp -j /jail $PYTHON_PATH
    jk_cp -j /jail $PYTHON_LIB_PATH
    groupadd script_executer
    adduser script_executer -G script_executer
    jk_jailuser -n -j /jail script_executer

Export environment variables needed to run the adapter:
    export JAIL_DIR=/jail
    export JAIL_USERNAME=script_executer
    export JAIL_GROUPNAME=script_executer

4. Add the custom adapter project directory to PYTHONPATH using the following command: export PYTHONPATH=PathToCustomPythonAdapterProject

5. Run adapter:  python worker/activities-worker

(worker/activities-worker is the main entry point to run the adapter)

Worker URL for requests - http://localhost:8082/api/v1/function

### Files
1. setup.py, setup.cfg,requires.txt - are used for building python package
2. Dockerfile - used to create adapter docker container
Example commands:
cd 'cloned adapter repo folder'
python setup.py bdist_wheel
docker build -t ad-template ( ad-template - container name for the adapter)

3. Jenkinsfile, Jenkinsfile-lambda - used in jenkins jobs
4. event-json - contains sample api calls to run each action


### activities_python Folders

Actions folder contains three template actions and sample test files:
1. Hello World - represents an action to demonstrate input and output parameters.
2. Create Template - represents an action with api POST request. BasicConstants.ACTIVITY_2_URL is api relative URL for the action2.
3. Run Script - represents an action to run python script in jail env.
4. Verify Target - represents an action for verifying target.

common folder - is a common adapter library.

constants folder files: You can change the values of these constants to customize your adapter.

events/event_resolver.py : Type resolver for incoming requests. We have four event types with corresponding actions.

pythonutils - contains different models used in actions.


Other folders/files:
--------------------

functions/lambda_function_name/handler.py is used to run adapter as aws lambda function. The name 'lambda_function_name' should be the same as name in adapter lambda schema.

schemas/generate_schemes.py - is used to generate schemes for current template adapter. you can simply run it in python.
If you want to make your own changes in schemes please refer to the schemes documentation.

scripts/run_test.sh - script is used in build to run tests

worker/activities-worker - is used to run adapter as microservice
