from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask import current_app

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('addressbook', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, entryname, entryaddress, entrycity, entrystate, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('addressbook/index.html', posts=posts)

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