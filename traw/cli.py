import click
import json
from pprint import pformat

import traw

pass_client = click.make_pass_decorator(traw.Client)


@click.group()
@click.version_option()
@click.option('-u', '--username', 'username', envvar='TRAW_USERNAME', help='TestRail username')
@click.option('-p', '--password', 'password', envvar='TRAW_PASSWORD', help='TestRail password')
@click.option('-a', '--api-key', 'user_api_key', envvar='TRAW_USER_API_KEY', help='TestRail user api key')
@click.option('--url', 'url', envvar='TRAW_URL', help='TestRail instance URL')
@click.pass_context
def cli(ctx, **kwargs):
    """TestRail Api Wrapper CLI
    """
    ctx.obj = traw.Client(**kwargs)


@cli.group()
def get():
    """Get information about a given TestRail object type"""


@get.command('projects')
@pass_client
def get_projects(client):
    """Return information about projects"""
    projects = [p._content for p in client.projects()]
    click.echo(json.dumps(projects, indent=4))


@get.command('project')
@click.argument('project-id', type=int)
@pass_client
def get_projects(client, project_id):
    """Return information about a specific project
   
    i.e. `traw get project 4`
    """
    project = client.project(project_id)._content
    click.echo(json.dumps(project, indent=4))


@get.command('runs')
@click.argument('project-id', type=int)
@pass_client
def get_runs(client, project_id):
    """Return information about runs for a given project"""
    runs = [r._content for r in client.runs(project_id)]
    click.echo(json.dumps(runs, indent=4))


@get.command('run')
@click.argument('run-id', type=int)
@pass_client
def get_projects(client, run_id):
    """Return information about a specific run
   
    i.e. `traw get run 556`
    """
    run = client.run(run_id)._content
    click.echo(json.dumps(run, indent=4))
