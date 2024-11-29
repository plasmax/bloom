import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Task, File

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')