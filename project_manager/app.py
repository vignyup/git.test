import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g
import click
from flask.cli import with_appcontext

app = Flask(__name__)
DATABASE = 'project_manager/tasks.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)

def add_task(title, description):
    db = get_db()
    db.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
               [title, description, 'Open'])
    db.commit()

def get_all_tasks():
    db = get_db()
    cur = db.execute('SELECT id, title, description, status FROM tasks ORDER BY id DESC')
    tasks = cur.fetchall()
    return tasks

@app.route('/')
def index():
    all_tasks = get_all_tasks()
    return render_template('index.html', tasks=all_tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task_route():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title and description: # Basic validation
            add_task(title, description)
            return redirect(url_for('index'))
        else:
            # Optional: Add some error handling or message here
            return "Error: Title and description are required.", 400
    return render_template('add_task.html')

if __name__ == '__main__':
    app.run(debug=True)
