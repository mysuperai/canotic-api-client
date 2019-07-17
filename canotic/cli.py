import json
import os
import signal
import sys

from botocore.exceptions import ClientError
from warrant import Cognito
from canotic.config import BASE_FOLDER, COGNITO_USERPOOL_ID, COGNITO_CLIENT_ID, COGNITO_REGION
from canotic.client import Client
import click


def _signal_handler(s, f):
    sys.exit(1)


def save_api_key(api_key: str):
    api_key_file = os.path.expanduser(f'{BASE_FOLDER}/apikey')
    if not os.path.exists(os.path.dirname(api_key_file)):
        os.makedirs(os.path.dirname(api_key_file))
    with open(api_key_file, 'w') as f:
        f.write(api_key)


@click.group()
def cli():
    pass


def load_api_key() -> str:
    api_key_file = os.path.expanduser(f'{BASE_FOLDER}/apikey')
    with open(api_key_file) as f:
        api_key = f.readline()
    return api_key


@cli.group()
@click.pass_context
def client(ctx):
    """
    Canotic API operations
    """
    api_key = ''
    try:
        api_key = load_api_key()
    except Exception as e:
        pass
    if len(api_key) == 0:
        print('User needs to login or set api key')
        exit()
    ctx.obj = {}
    ctx.obj['client'] = Client(api_key=api_key)


@client.command(name='create_job')
@click.option('--app_id', '-a', help='Application id', required=True)
@click.option('--callback_url', '-c', help='Callback URL for post when jobs finish')
@click.option('--inputs', '-i', help='Json list with inputs')
@click.option('--inputs_file', '-if', help='URL pointing to JSON file')
@click.pass_context
def create_job(ctx, app_id: str, callback_url: str, inputs: str, inputs_file: str):
    """
    Submit a job
    """
    client = ctx.obj['client']
    print("Submitting job")
    json_inputs = None
    if inputs is not None:
        try:
            json_inputs = json.loads(inputs)
        except:
            print("Couldn't read json inputs")
            exit()
    print(client.create_job(app_id, callback_url, json_inputs, inputs_file))


@client.command(name='fetch_job')
@click.option('--job_id', '-j', help='Job id', required=True)
@click.pass_context
def fetch_job(ctx, job_id: str):
    """
    Get Job given job id
    """
    client = ctx.obj['client']
    print(f'Fetching job {job_id}')
    print(client.fetch_job(job_id))


@client.command(name='cancel_job')
@click.option('--job_id', '-j', help='Job id', required=True)
@click.pass_context
def cancel_job(ctx, job_id: str):
    """
    Cancel a job given job id. Only for jobs in SCHEDULED, IN_PROGRESS or SUSPENDED state.
    """
    client = ctx.obj['client']
    print(f'Cancelling job {job_id}')
    print(client.cancel_job(job_id))


@client.command(name='list_jobs')
@click.option('--app_id', '-a', help='Application id', required=True)
@click.option('--page', '-p', help='Page number', type=int)
@click.option('--size', '-s', help='Size of page', type=int)
@click.pass_context
def list_jobs(ctx, app_id: str, page: int, size: int):
    """
    Get a paginated list of jobs given an application id
    """
    client = ctx.obj['client']
    print(f'Fetching jobs per application {app_id}')
    print(client.list_jobs(app_id, page, size))


@cli.command()
@click.option('--api-key', help='Your Canotic API KEY', required=True)
def config(api_key):
    """
    Set api key.
    """
    save_api_key(api_key)


@cli.command()
@click.option('--username', '-u', help='Canotic Username', required=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """
    Use username and password to get Canotic api key.
    """
    user = Cognito(user_pool_id=COGNITO_USERPOOL_ID, client_id=COGNITO_CLIENT_ID,
                   user_pool_region=COGNITO_REGION, username=username)
    try:
        user.authenticate(password)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException' or e.response['Error'][
            'Code'] == 'NotAuthorizedException':
            print("Incorrect username or password")
            return
        else:
            print(f"Unexpected error: {e}")
            return

    client = Client(auth_token=user.access_token)
    api_keys = client.get_apikeys()
    if len(api_keys) > 0:
        save_api_key(api_keys[0])
        print(f'Api key {api_keys[0]} was set')
    else:
        print(f'User {username} doesn\'t have any api keys')


@cli.command()
def logout():
    """
    Remove stored api key
    """
    save_api_key('')
    print('Stored api key was removed')


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    sys.exit(cli())


if __name__ == '__main__':
    main()
