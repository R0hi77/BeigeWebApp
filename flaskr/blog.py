""" 
Management of the blog posts
"""


from flask import( 
    Blueprint, render_template, redirect,
    url_for, request,g, flash, abort

)

from .db import get_db
from .auth import login_required


bp =  Blueprint('blog', __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        'SELECT  p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template("blog/index.html",posts=posts)



@bp.route("/create", methods=('GET','POST'))
@login_required
def create():
    if request.method=="POST":
        title = request.form['title']
        body= request.form['body']
        error = None

        if not title:
            error = " title is required"
        elif not body:
            error = "Insert a post body " 

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute('INSERT INTO post(title, body, author_id) VALUES (?,?,?)' ,(title,body,g.user["id"]))
            db.commit()
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html')



def get_post(id, check_author=True):
    """
    retrieves post id from the database
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id =?', (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doestnt exist.")

    if check_author and post["author_id"] != g.user['id']:
        abort(403)
    return post

@bp.route("/<int:id>/update", methods=('GET','POST'))
@login_required

def update(id):
    post = get_post(id)
    if request.method=="POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = " title required"

    # elif not body:
    #     error = "Insert a post body" 

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body =?'
                ' WHERE id = ?', (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)



@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))