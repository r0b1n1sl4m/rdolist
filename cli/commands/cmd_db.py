import click

from app import create_app
from app.extensions import db
from seeds.base_seeder import BaseSeeder

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """
    Manage database seeding, resetting etc.
    """

    # Prevent command if config is set to production
    if app.config['MODE'] == 'production':
        click.echo('You cant perform this action in production.')
        raise click.Abort()


@click.command()
def init():
    """
    Initialize the database.
    """

    click.echo('Dropping tables')
    db.drop_all()

    click.echo('Creating database tables')
    db.create_all()


@click.command()
@click.argument('seeder_name', required=False)
def seed(seeder_name):
    """
    Seed the database from BaseSeeder.

    :type seeder_name: Specific seeder name
    """

    # Run the seeder base class
    click.echo('Running database seeder')

    seeder = BaseSeeder(seeder_name)
    seeder.run()


@click.command()
@click.pass_context
def reset(ctx):
    """
    Init and seed automatically.
    """

    # Init and seed database
    ctx.invoke(init)
    ctx.invoke(seed)


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
