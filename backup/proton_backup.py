#!/usr/bin/env python

# BSD 3-Clause License
#
# Copyright (c) 2018, Pruthvi Kumar All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import dropbox
from backup_utilities import Utilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class BackupProductionStack(Utilities):

    def __init__(self):
        super(BackupProductionStack, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--proton_backup_env_token')
        self.parser.add_argument('--proton_backup_pg_token')
        self.parser.add_argument('--proton_backup_redis_token')
        self.parser.add_argument('--proton_backup_sqlite_token')
        self.parser.add_argument('--sqlite_mount_path')
        self.parser.add_argument('--pg_mount_path')
        self.parser.add_argument('--redis_mount_path')
        self.parser.add_argument('--date')
        self.parser.add_argument('--time')
        self.proton_backup_args = self.parser.parse_args()
        self.proton_backup_map = {
            'env': {
                'token': self.proton_backup_args.proton_backup_env_token,
                'path': './../.env',
                'stopwatch_message': 'uploading of proton platform config',
                'upload_file_name': '.env',
                'job_name': 'Platform Config Backup'
            },
            'pg': {
                'token': self.proton_backup_args.proton_backup_pg_token,
                'path': self.proton_backup_args.pg_mount_path,
                'stopwatch_message': 'uploading of proton postgres database',
                'upload_file_name': 'proton_pg.zip',
                'job_name': 'Postgres DB Backup'
            },
            'redis': {
                'token': self.proton_backup_args.proton_backup_redis_token,
                'path': self.proton_backup_args.redis_mount_path,
                'stopwatch_message': 'uploading of proton redis database',
                'upload_file_name': 'proton_redis.zip',
                'job_name': 'Redis DB Backup'
            },
            'sqlite': {
                'token': self.proton_backup_args.proton_backup_sqlite_token,
                'path': self.proton_backup_args.sqlite_mount_path,
                'stopwatch_message': 'uploading of proton sqlite database',
                'upload_file_name': 'proton_sqlite.zip',
                'job_name': 'Sqlite DB Backup'
            }
        }

    def process_backup(self, proton_backup_type):
        if self.proton_backup_args.date is not None and self.proton_backup_args.time is not None:
            dbx = dropbox.Dropbox(self.proton_backup_map[proton_backup_type]['token'])
            with open(self.proton_backup_map[proton_backup_type]['path'], 'rb') as proton_backup_file_read_handle:
                proton_backup_load = proton_backup_file_read_handle.read()

            with self.stopwatch('./reports/backup', proton_backup_type,
                                self.proton_backup_map[proton_backup_type]['stopwatch_message']):
                try:
                    res = dbx.files_upload(proton_backup_load,
                                           '/{}/{}'.format(self.proton_backup_args.date,
                                                           self.proton_backup_map[proton_backup_type]['upload_file_name']),
                                           dropbox.files.WriteMode.overwrite)
                except Exception as err:
                    print('[PROTON Backup]-[{}] - '
                          'API error\n'.format(self.proton_backup_map[proton_backup_type]['job_name']), err)
                    return None
                with open('./reports/backup/{}.txt'.format(proton_backup_type), 'a') as writer:
                    writer.write('{} successful\n'.format(self.proton_backup_map[proton_backup_type]['job_name']))
                    writer.write('Date & time of execution: {} @ {}\n'.format(self.proton_backup_args.date,
                                                                              self.proton_backup_args.time))
                # TODO: email res to PK.
                return res
        else:
            print('Backup process missing key date and time arguments. Backup cannot proceed.')


if __name__ == '__main__':
    backup = BackupProductionStack()
    backup.process_backup('env')
    backup.process_backup('pg')
    backup.process_backup('redis')
    backup.process_backup('sqlite')



