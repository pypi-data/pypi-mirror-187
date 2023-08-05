from __future__ import annotations

from datetime import datetime

import click
import isolate_cloud.auth as auth
from isolate_cloud import sdk
from rich.console import Console
from rich.table import Table

DEFAULT_HOST = "alpha.fal.ai"
DEFAULT_PORT = "443"

console = Console()


@click.group()
def cli():
    pass


###### Auth group ######
@cli.group("auth")
def auth_cli():
    pass


@auth_cli.command(name="login")
def auth_login():
    auth.login()


@auth_cli.command(name="logout")
def auth_logout():
    auth.logout()


@auth_cli.command(name="hello", hidden=True)
def auth_test():
    """
    To test auth.
    """
    print(f"Hello, {auth.USER.info['name']}")


###### Key group ######
@cli.group("key")
@click.option("--host", default=DEFAULT_HOST)
@click.option("--port", default=DEFAULT_PORT, hidden=True)
@click.pass_context
def key_cli(ctx, host: str, port: str):
    ctx.obj = sdk.FalCloudClient(f"{host}:{port}")


@key_cli.command(name="generate")
@click.pass_obj
def key_generate(client: sdk.FalCloudClient):
    with client.connect() as connection:
        result = connection.create_user_key()
        print(
            "Generated key id and key secret.\n"
            "This is the only time the secret will be visible.\n"
            "You will need to generate a new key pair if you lose access to this secret."
        )
        print(f"KEY_ID='{result[1]}'\nKEY_SECRET='{result[0]}'")


@key_cli.command(name="list")
@click.pass_obj
def key_list(client: sdk.FalCloudClient):
    with client.connect() as connection:
        keys = connection.list_user_keys()
        for key in keys:
            print(f"KEY_ID='{key.key_id}' @ {key.created_at.ToDatetime()}")
        else:
            print("No more keys.")


@key_cli.command(name="revoke")
@click.argument("key-id", required=True)
@click.pass_obj
def key_revoke(client: sdk.FalCloudClient, key_id: str):
    with client.connect() as connection:
        connection.revoke_user_key(key_id)


###### Scheduled group ######
@cli.group("scheduled")
@click.option("--host", default=DEFAULT_HOST)
@click.option("--port", default=DEFAULT_PORT, hidden=True)
@click.pass_context
def scheduled_cli(ctx, host: str, port: str):
    ctx.obj = sdk.FalCloudClient(f"{host}:{port}")


@scheduled_cli.command(name="list")
@click.pass_obj
def list_scheduled(client: sdk.FalCloudClient):
    table = Table(title="Scheduled jobs")
    table.add_column("Job ID")
    table.add_column("State")
    table.add_column("Cron")

    with client.connect() as connection:
        for cron in connection.list_scheduled_runs():
            table.add_row(cron.run_id, cron.state.name, cron.cron)

    console.print(table)


@scheduled_cli.command(name="activations")
@click.argument("job-id", required=True)
@click.argument("limit", default=15)
@click.pass_obj
def list_activations(client: sdk.FalCloudClient, job_id: str, limit: int = 15):
    table = Table(title="Job activations")
    table.add_column("Job ID")
    table.add_column("Activation ID")
    table.add_column("Activation Date")

    with client.connect() as connection:
        for cron in connection.list_run_activations(job_id)[-limit:]:
            table.add_row(
                cron.run_id,
                cron.activation_id,
                str(datetime.fromtimestamp(int(cron.activation_id))),
            )

    console.print(table)


@scheduled_cli.command(name="logs")
@click.argument("job-id", required=True)
@click.argument("activation-id", required=True)
@click.pass_obj
def print_logs(client: sdk.FalCloudClient, job_id: str, activation_id: str):
    with client.connect() as connection:
        raw_logs = connection.get_activation_logs(
            sdk.ScheduledRunActivation(job_id, activation_id)
        )
        console.print(raw_logs.decode(errors="ignore"), highlight=False)


@scheduled_cli.command("cancel")
@click.argument("job-id", required=True)
@click.pass_obj
def cancel_scheduled(client: sdk.FalCloudClient, job_id: str):
    with client.connect() as connection:
        connection.cancel_scheduled_run(job_id)
        console.print("Cancelled", repr(job_id))


cli.add_command(auth_cli, name="auth")
cli.add_command(key_cli, name="key")
cli.add_command(scheduled_cli, name="scheduled")

if __name__ == "__main__":
    cli()
