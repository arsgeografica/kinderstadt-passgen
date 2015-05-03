from celery.bin.celery import main as celery_main
import click
from kinderstadt_passgen.app import factory
from kinderstadt_passgen.tasks import celery


@click.group()
@click.option('--debug/--no-debug', default=True)
@click.option('--config', default='kinderstadt_passgen.config.development')
@click.pass_context
def cli(ctx, debug, config):
    """
    Passgen Command Line Interface.
    """
    ctx.obj['DEBUG'] = debug
    ctx.obj['CONFIG'] = config


@cli.command()
@click.pass_context
def server(ctx):
    """
    Run the flask development server.
    """
    app = factory(ctx.obj['CONFIG'])
    app.run(debug=ctx.obj['DEBUG'])


@cli.command()
@click.pass_context
def worker(ctx):
    """
    Run the celery worker service
    """
    app = factory(ctx.obj['CONFIG'])
    celery_args = ['celery', 'worker']
    with app.app_context():
        return celery_main(celery_args)


def main():
    """
    setuptools console_script entrypoint.
    """
    cli(obj={})


if __name__ == '__main__':
    main()
