from quart import Quart, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Quart(__name__)
app.config['SECRET_KEY'] = 'ThIs v3ry S3crat'


@app.route('/')
async def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return await render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
async def post(post_id):
    post = get_post(post_id)
    return await render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
async def create():
    if request.method == 'POST':
        form = await request.form
        title = form['title']
        content = form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return await render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
async def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        form = await request.form
        title = form['title']
        content = form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return await render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
async def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return await redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
