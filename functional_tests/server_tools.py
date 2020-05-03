from fabric.context_managers import shell_env, settings
from fabric.operations import run


def create_server_pre_auth_server(host, email):
    manage_command = f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"
    env_lines = run(f"cat ~/sites/{host}/.env").splitlines()
    env = dict(l.split("=") for l in env_lines if l)
    with settings(host_string=f'dima@{host}'):
        with shell_env(**env):
            session_key = run(f"{manage_command} create_session {email}")
            return session_key.strip()


def reset_database(host):
    manage_command = f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"
    with settings(host_string=f'dima@{host}'):
        run(f"{manage_command} flush --noinput")
