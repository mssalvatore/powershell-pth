import click
from pypsrp.client import Client
from pypsrp.powershell import PowerShell, RunspacePool


DUMMY_HASH = "00000000000000000000000000000000"


@click.command()
@click.option("--cmd", required=True)
@click.option("--host", required=True)
@click.option("--username", required=True)
@click.option("--lm_hash", default=DUMMY_HASH)
@click.option("--nt_hash", default=DUMMY_HASH)
@click.option("--use_ssl", default=False)
@click.option("--timeout", default=3, type=int)
def run_remote_cmd(
    cmd,
    host,
    username,
    lm_hash=DUMMY_HASH,
    nt_hash=DUMMY_HASH,
    use_ssl=True,
    timeout=3,
):
    formatted_credentials = (
        f"Username: {username}, LM Hash: {lm_hash}, NT Hash: {nt_hash}"
    )

    try:
        client = connect(host, username, lm_hash, nt_hash, use_ssl, timeout)
        print(f"Authentication succeeded -- {formatted_credentials}")
    except Exception as ex:
        print(f"Authentication failed -- {formatted_credentials}")
        print(ex)
    else:
        execute_cmd(cmd, client)


def connect(host, username, lm_hash, nt_hash, use_ssl=True, timeout=3):
    # The pypsrp library requires LM or NT hashes to be formatted like "LM_HASH:NT_HASH"
    #
    # Example:
    # If your LM hash is 1ec78eb5f6edd379351858c437fc3e4e and your NT hash is
    # 79a760336ad8c808fee32aa96985a305, then you would pass
    # "1ec78eb5f6edd379351858c437fc3e4e:79a760336ad8c808fee32aa96985a305" as the
    # `password` parameter to pypsrp.
    #
    # pypsrp will parse this string and automatically use the appropriate hash
    # for NTLM authentication.
    # 
    # If you only have one of the two hashes, this script will automatically
    # populate the other hash with zeros.
    formatted_ntlm_hashes = f"{lm_hash}:{nt_hash}"

    client = Client(
        host,
        username=username,
        password=formatted_ntlm_hashes,
        cert_validation=False,
        ssl=use_ssl,
        auth="ntlm",
        encryption="auto",
        connection_timeout=timeout,
    )

    # Execute a command to validate that authentication was actually successful. This
    # will raise an exception if authentication failed.
    client.execute_cmd("dir")

    return client


def execute_cmd(cmd, client):
    # SECURITY: Watch out! No attempt is made to protect against command
    # injection.
    print(f"Running command: {cmd}")
    stdout, stderr, rc = client.execute_cmd(cmd)
    print(f"STDOUT:\n{stdout}\n\n")
    print(f"STDERR:\n{stderr}\n\n")
    print(f"RETURN CODE: {rc}")


if __name__ == "__main__":
    run_remote_cmd()
