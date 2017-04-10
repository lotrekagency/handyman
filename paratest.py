import os
import paramiko
from datetime import datetime

class SSHClient(paramiko.SSHClient):

    def exec_commands(self, *commands):
        command = ';'.join(commands)
        return self.exec_command(command.strip(';'))


def execute_backup(project, server, username, password, script, backup_archive):

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    known_host_file = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
    print (known_host_file)
    ssh.load_host_keys(known_host_file)
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


username = 'tvl'
password = 'tvl$2017'
server = '158.255.193.27'

backup_archive = '/var/www/html/core/backup.zip'

script = """
echo 'tvl$2017' | sudo -S ls
cd /var/www/html/core
echo 'tvl$2017' | sudo -S rm -f backup.zip
echo 'tvl$2017' | sudo -S rm -rf backup
echo 'tvl$2017' | sudo -S mkdir backup
echo 'tvl$2017' | sudo -S chmod -R 777 backup
. venv/bin/activate
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > backup/database.json
echo 'tvl$2017' | sudo -S zip -r backup.zip backup
"""

execute_backup(
    'tvl', server,
    username, password,
    script, backup_archive
)


