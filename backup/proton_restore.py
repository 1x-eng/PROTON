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
import datetime
import dropbox
import io
import zipfile
from backup_utilities import Utilities
from datetime import date

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class RestoreProductionStack(Utilities):

    def __init__(self):
        super(RestoreProductionStack, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--proton_backup_env_token')
        self.parser.add_argument('--proton_backup_pg_token')
        self.parser.add_argument('--proton_backup_redis_token')
        self.parser.add_argument('--proton_backup_sqlite_token')
        self.parser.add_argument('--env_mount_path')
        self.parser.add_argument('--sqlite_mount_path')
        self.parser.add_argument('--pg_mount_path')
        self.parser.add_argument('--redis_mount_path')
        self.proton_restore_args = self.parser.parse_args()
        self.proton_restore_map = {
            'env': {
                'token': self.proton_restore_args.proton_backup_env_token,
                'remote_path': '.env',
                'stopwatch_message': 'downloading of proton platform config',
                'job_name': 'Platform Config Restore',
                'mount_path': self.proton_restore_args.env_mount_path
            },
            'pg': {
                'token': self.proton_restore_args.proton_backup_pg_token,
                'remote_path': 'proton_pg.zip',
                'stopwatch_message': 'downloading of proton postgres database',
                'job_name': 'Postgres DB Restore',
                'mount_path': self.proton_restore_args.pg_mount_path
            },
            'redis': {
                'token': self.proton_restore_args.proton_backup_redis_token,
                'remote_path': 'proton_redis.zip',
                'stopwatch_message': 'downloading of proton redis database',
                'job_name': 'Redis DB Restore',
                'mount_path': self.proton_restore_args.redis_mount_path
            },
            'sqlite': {
                'token': self.proton_restore_args.proton_backup_sqlite_token,
                'remote_path': 'proton_sqlite.zip',
                'stopwatch_message': 'downloading of proton sqlite database',
                'job_name': 'Sqlite DB Restore',
                'mount_path': self.proton_restore_args.sqlite_mount_path
            }
        }

    def process_restore(self, proton_restore_type):
        if self.proton_restore_map[proton_restore_type]['mount_path'] is not None:
            with self.stopwatch('./reports/restore', proton_restore_type,
                                self.proton_restore_map[proton_restore_type]['stopwatch_message']):
                try:
                    dbx = dropbox.Dropbox(self.proton_restore_map[proton_restore_type]['token'])
                    folders = dbx.files_list_folder('')
                except Exception as err:
                    print('[PROTON Restore]-[{}] - '
                          'API Error\n'.format(self.proton_restore_map[proton_restore_type]['job_name']), err)
                else:
                    try:
                        list_of_folders = []
                        for folder in folders.entries:
                            list_of_folders.append(folder.name)
                        sorted(list_of_folders, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
                        most_recent_folder = list_of_folders[-1]
                        md, res = dbx.files_download('/{}/{}'.format(most_recent_folder,
                                                                     self.proton_restore_map[proton_restore_type][
                                                                         'remote_path']))
                        if proton_restore_type != 'env':
                            z = zipfile.ZipFile(io.BytesIO(res.content))
                            z.extractall(self.proton_restore_map[proton_restore_type]['mount_path'])
                        else:
                            with open('{}/.env'.format(self.proton_restore_map[proton_restore_type]['mount_path']),
                                      'wb') as env_file:
                                env_file.write(res.content)
                        with open('./reports/restore/{}.txt'.format(proton_restore_type), 'a') as writer:
                            writer.write('Successfully downloaded PROTON type '
                                         '- {} from remote folder -{} to '
                                         'this '
                                         'location - {}.\n'.format(proton_restore_type, most_recent_folder,
                                                                   self.proton_restore_map[proton_restore_type][
                                                                       'mount_path']))
                            writer.write('Date & time of execution: '
                                         '{} @ {}\n'.format(str(date.today()),
                                                            datetime.datetime.now().strftime("%H:%M:%S")))

                    except Exception as e:
                        print('[PROTON Restore]-[{}] - '
                              'Download error. '.format(self.proton_restore_map[proton_restore_type]['job_name']), e)
        else:
            print('PROTON restore cannot proceed without valid mount path.')


if __name__ == '__main__':
    proton_restore = RestoreProductionStack()
    proton_restore.process_restore('env')
    proton_restore.process_restore('pg')
    proton_restore.process_restore('redis')
    proton_restore.process_restore('sqlite')
