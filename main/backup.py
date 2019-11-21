import os
import paramiko
import time

from datetime import datetime
from django.conf import settings
from .exceptions import BackupException


class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project):

    project_slug = project.slug
    server = project.machine.server_address
    username = project.machine.ssh_username
    password = project.machine.ssh_password
    script = project.backup_script
    backup_archive = project.backup_archive
    sync_folders = project.backup_sync_folders

    sftp = None
    ssh = None

    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        if password:
            ssh.connect(server, username=username, password=password)
        else:
            key_path = os.path.expanduser(os.path.join("~", ".ssh", "id_rsa"))
            key = paramiko.RSAKey.from_private_key_file(key_path, os.getenv('RSA_KEY_PASSPHRASE'))
            ssh.connect(server, username=username, pkey=key)
        print (script.split('\r\n'))
        stdin, stdout, stderr = ssh.exec_commands(*script.split('\r\n'))
        exit_status = stderr.channel.recv_exit_status()

        print (exit_status)

        if exit_status != 0:
            stderr = '\n'.join(stderr.readlines())
            print (stderr)
            ssh.close()
            error_reporting = 'Error code: {0}\n{1}'.format(
                exit_status, stderr
            )
            raise BackupException(error_reporting)

        sftp = ssh.open_sftp()
        backuptime = datetime.now().strftime("%Y-%m-%d[%H_%M_%S]")
        os.makedirs(os.path.join(settings.BACKUP_PATH, project_slug), exist_ok=True)
        archive_file = os.path.join(
            settings.BACKUP_PATH,
            project_slug,
            '{0}-{1}-backup.zip'.format(project_slug, backuptime)
        )
        if backup_archive:
            sftp.get(backup_archive, archive_file)
        if ssh:
            ssh.close()
            ssh = None
        time.sleep(2)
        if sync_folders:
            for folder in sync_folders.split('\r\n'):
                if password:
                    command_sync = 'sshpass -p "{0}" rsync -avv {1}@{2}:{3} {4}'.format(
                        password, username, server, folder,
                        os.path.join(settings.BACKUP_PATH, project_slug)
                    )
                else:
                    command_sync = 'sshpass -P passphrase -p "{0}" rsync -avv {1}@{2}:{3} {4}'.format(
                        os.getenv('RSA_KEY_PASSPHRASE'), username, server, folder,
                        os.path.join(settings.BACKUP_PATH, project_slug)
                    )
                os.system(command_sync)

    except Exception as ex:
        raise BackupException(ex)
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()

    # Delete old backup files
    backup_directory = os.path.join(settings.BACKUP_PATH, project_slug)
    for file in os.listdir(backup_directory):
        path = os.path.join(backup_directory, file)
        if os.path.isfile(path):
            time_old = datetime.now() - datetime.fromtimestamp(os.stat(path).st_mtime)
            if time_old.days > settings.FILE_DAYS_OLD_TO_REMOVE:
                os.remove(path)
