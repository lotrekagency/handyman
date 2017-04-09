import os
import paramiko
from datetime import datetime

from django.conf import settings


class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project, server, username, password, script, backup_archive):

    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(server, username=username, password=password)
    print (script.split('\n'))
    stdin, stdout, stderr = ssh.exec_commands(*script.split('\r\n'))
    exit_status = stderr.channel.recv_exit_status()
    print (exit_status)
    stderr=stderr.readlines()
    print (stderr)

    sftp = ssh.open_sftp()
    backuptime = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
    archive_file = os.path.join(
        settings.BACKUP_PATH,
        '{0}-{1}-backup.zip'.format(project, backuptime)
    )
    sftp.get(backup_archive, archive_file)
    sftp.close()
    ssh.close()
