import click
import json

import traw

pass_client = click.make_pass_decorator(traw.Client)


class IntOrEmailParamType(click.ParamType):
    name = 'int-or-email'

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except ValueError:
            pass

        if '@' in value:
            return value
        else:
            self.fail('%s is not a valid integer or email address' % value, param, ctx)


INT_OR_EMAIL = IntOrEmailParamType()


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


@get.command('project')
@click.argument('project-id', type=int)
@pass_client
def get_project(client, project_id):
    """Return information about a specific project

    i.e. `traw get project 4`
    """
    project = client.project(project_id)._content
    click.echo(json.dumps(project, indent=4, sort_keys=True))


@get.command('projects')
@click.option('--complete/--not-complete', default=None)
@pass_client
def get_projects(client, complete):
    """Return information about projects"""
    if complete is True:
        kwargs = {'completed_only': True}
    elif complete is False:
        kwargs = {'active_only': True}
    else:
        kwargs = dict()

    projects = [p._content for p in client.projects(**kwargs)]
    click.echo(json.dumps(projects, indent=4, sort_keys=True))


@get.command('run')
@click.argument('run-id', type=int)
@pass_client
def get_run(client, run_id):
    """Return information about a specific run

    i.e. `traw get run 556`
    """
    run = client.run(run_id)._content
    click.echo(json.dumps(run, indent=4, sort_keys=True))


@get.command('runs')
@click.argument('project-id', type=int)
@pass_client
def get_runs(client, project_id):
    """Return information about runs for a given project"""
    runs = [r._content for r in client.runs(project_id)]
    click.echo(json.dumps(runs, indent=4, sort_keys=True))


@get.command('user')
@click.argument('user-id-or-email', type=INT_OR_EMAIL)
@pass_client
def get_user(client, user_id_or_email):
    """Return information about a specific user

    i.e. `traw get user 16` or  `traw get user foo-name@bar.com`
    """
    user = client.user(user_id_or_email)._content
    click.echo(json.dumps(user, indent=4, sort_keys=True))


@get.command('users')
@pass_client
def get_users(client):
    """Return information about users"""
    users = [u._content for u in client.users()]
    click.echo(json.dumps(users, indent=4, sort_keys=True))
