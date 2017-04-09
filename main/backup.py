import os
import paramiko
from datetime import datetime

from django.conf import settings

from .exceptions import BackupException


class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project, server, username, password, script, backup_archive):

    try:
        ssh = SSHClient()
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
    except SSHException as ex:
        raise BackupException(ex)
    finally:
        sftp.close()
        ssh.close()
