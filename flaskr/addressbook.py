from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask import current_app, jsonify

from flaskr.auth import login_required
from flaskr.db import get_db

import requests
import xml.etree.ElementTree as ET
import json

bp = Blueprint('addressbook', __name__)
USERID="829SGCOM5266"

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, entryname, entryaddress, entrycity, entrystate, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('addressbook/index.html', posts=posts)

@bp.route('/zipcheck', methods=['POST'])
@login_required
def zipcheck():

    data = request.get_json()
    zipNum = data.get("zip")

    addressurl = '''http://production.shippingapis.com/ShippingAPITest.dll?API=CityStateLookup
        &XML=<CityStateLookupRequest USERID="''' + USERID + '''"><ZipCode ID="5">
        <Zip5>''' + zipNum + '''</Zip5></ZipCode></CityStateLookupRequest>'''

    try:
        res = requests.get(addressurl)
    except Exception as exc:
        res = exc

    root = ET.fromstring(res.text)
    outputCity = root[0][1].text
    outputState = root[0][2].text
    output = {
        'city': outputCity, 
        'state': outputState
        }
    return json.dumps(output)

@bp.route('/addresscheck', methods=['POST'])
@login_required
def addresscheck():

    data = request.get_json()
    address = data.get("address")
    city = data.get("city")
    state = data.get("state")

    zipUrl = '''http://production.shippingapis.com/ShippingAPITest.dll?API=ZipCodeLookup
        &XML=<ZipCodeLookupRequest USERID="''' + USERID +'''"><Address ID="0">
        <Address1></Address1><Address2>''' + address + '''</Address2>
        <City>''' + city + '''</City><State>''' + state + '''</State></Address>
        </ZipCodeLookupRequest>'''

    try:
        res = requests.get(zipUrl)
    except Exception as exc:
        res = exc

    root = ET.fromstring(res.text)
    output = root[0][3].text + ' - ' + root[0][4].text

    return jsonify(output=output)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        entryname = request.form['entryname']
        entryaddress = request.form['entryaddress']
        entrycity = request.form['entrycity']
        entrystate = request.form['entrystate']
        entryzip = request.form['entryzip']
        error = None

        if not entryname:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (entryname, entryaddress, entrycity, entrystate, entryzip, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (entryname, entryaddress, entrycity, entrystate, entryzip, g.user['id'])
            )
            db.commit()
            return redirect(url_for('addressbook.index'))

    return render_template('addressbook/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, entryname, entryaddress, entrycity, entrystate, entryzip, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        entryname = request.form['entryname']
        entryaddress = request.form['entryaddress']
        entrycity = request.form['entrycity']
        entrystate = request.form['entrystate']
        entryzip = request.form['entryzip']

        error = None

        if not entryname:
            error = 'Name is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET entryname = ?, entryaddress = ?, entrycity = ?, entrystate = ?, entryzip = ?'
                ' WHERE id = ?',
                (entryname, entryaddress, entrycity, entrystate, entryzip, id)
            )
            db.commit()
            return redirect(url_for('addressbook.index'))

    return render_template('addressbook/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('addressbook.index'))