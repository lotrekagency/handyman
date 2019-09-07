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

    print ('HELLO')

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
        ssh.connect(server, username=username, password=password)
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
        backuptime = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
        archive_file = os.path.join(
            settings.BACKUP_PATH,
            project_slug,
            '{0}-{1}-backup.zip'.format(project_slug, backuptime)
        )
        sftp.get(backup_archive, archive_file)
        if ssh:
            ssh.close()
            ssh = None
        time.sleep(2)
        if sync_folders:
            for folder in sync_folders.split('\r\n'):
                command_sync = 'sshpass -p "{0}" rsync -avv {1}@{2}:{3} {4}'.format(
                    password, username, server, folder,
                    os.path.join(settings.BACKUP_PATH, project_slug)
                )
                os.system(command_sync)

        command_zip_folder = 'zip -r {0}.zip {1}'.format(
            os.path.join(settings.BACKUP_PATH, project_slug),
            os.path.join(settings.BACKUP_PATH, project_slug)
        )
        os.system(command_zip_folder)

    except Exception as ex:
        raise BackupException(ex)
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
