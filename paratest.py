import os
import paramiko
from datetime import datetime

class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project, server, username, password, script, backup_archive):

    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(server, username=username, password=password)
    print (script.split('\n'))
    stdin, stdout, stderr = ssh.exec_commands(*script.split('\n'))
    exit_status = stderr.channel.recv_exit_status()
    print (exit_status)
    stderr=stderr.readlines()
    print (stderr)

    sftp = ssh.open_sftp()
    backuptime = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")
    sftp.get(
        backup_archive,
        'backup/{0}-{1}-backup.zip'.format(project, backuptime)
    )
    sftp.close()
    ssh.close()


username = 'root'
password = 'F4E51El4'
server = '213.32.70.154'

backup_archive = '/home/lotrektest/new.lotrek.it.lotrek.it/new-lotrek/backup.zip'

script = """
cd /home/lotrektest/new.lotrek.it.lotrek.it/new-lotrek/
rm -f backup.zip
rm -rf backup
mkdir backup
zip -r backup/media.zip media
. venv/bin/activate
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > backup/database.json
zip -r backup.zip backup
"""

execute_backup(
    'new_lotrek', server, username,
    password, script, backup_archive
)


