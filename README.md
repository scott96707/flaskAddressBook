# Setup and deployment

## To setup dev environment

python3 -m venv venv  
. venv/bin/activate  
pip install -e .  
pip install python-dotenv  
flask init-db  
export FLASK_APP=flaskr  
export FLASK_ENV=development  
flask run  

## Setup distribution file

pip install wheel  
python setup.py bdist_wheel  

## Deploy production

pip install flaskr-1.0.0-py3-none-any.whl  
export FLASK_APP=flaskr  
(set FLASK_APP=flaskr) <-- for windows  
(pip install python-dotenv) <-- may need to install for db  
flask init-db  

installed to venv/var/flaskr/instance  

## Run Production Server

pip install waitress  
waitress-serve --call 'flaskr:create_app'  
