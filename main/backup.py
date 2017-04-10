import os
import paramiko

from datetime import datetime
from django.conf import settings
from .exceptions import BackupException


class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project, server, username, password, script, backup_archive, sync_folders):

    try:
        sftp = None
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=password)
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
            '{0}-{1}-backup.zip'.format(project, backuptime)
        )
        sftp.get(backup_archive, archive_file)
        if sync_folders:
            for folder in sync_folders.split('\r\n'):
                command_sync = 'sshpass -p "{0}" rsync -avz {1}@{2}:{3} {4}'.format(
                    password, username, server, folder,
                    os.path.join(settings.BACKUP_PATH, project)
                )
                os.system(command_sync)

    except paramiko.SSHException as ex:
        raise BackupException(ex)
    except OSError as ex:
        raise BackupException(ex)
    finally:
        if sftp:
            sftp.close()
        ssh.close()
