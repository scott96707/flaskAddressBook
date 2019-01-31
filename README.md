To setup dev environment:
pip install -e .
. venv/bin/activate
flask init-db
flask run


Deploy production:
pip install wheel
python setup.py bdist_wheel
pip install flaskr-1.0.0-py3-none-any.whl
export FLASK_APP=flaskr
flask init-db
# installed to venv/var/flaskr/instance
