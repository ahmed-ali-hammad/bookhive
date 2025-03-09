import click
import uvicorn
from src.main import app


def run_service():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


@click.group()
def cli():
    pass


@cli.command()
def run_webapp():
    run_service()


if __name__ == "__main__":
    cli()
