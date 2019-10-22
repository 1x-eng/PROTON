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
from backup_utilities import Utilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class CleanupProtonRemoteBackup(Utilities):

    def __init__(self):
        super(CleanupProtonRemoteBackup, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--proton_backup_env_token')
        self.parser.add_argument('--proton_backup_pg_token')
        self.parser.add_argument('--proton_backup_redis_token')
        self.parser.add_argument('--proton_backup_sqlite_token')
        self.parser.add_argument('--date')
        self.parser.add_argument('--time')
        self.proton_cleanup_args = self.parser.parse_args()
        self.proton_cleanup_map = {
            'env': {
                'token': self.proton_cleanup_args.proton_backup_env_token,
                'stopwatch_message': 'cleanup of proton platform config',
                'job_name': 'Platform Config Cleanup',
            },
            'pg': {
                'token': self.proton_cleanup_args.proton_backup_pg_token,
                'stopwatch_message': 'cleanup of proton postgres database',
                'job_name': 'Postgres DB Cleanup',
            },
            'redis': {
                'token': self.proton_cleanup_args.proton_backup_redis_token,
                'stopwatch_message': 'cleanup of proton postgres database',
                'job_name': 'Redis DB Cleanup',
            },
            'sqlite': {
                'token': self.proton_cleanup_args.proton_backup_sqlite_token,
                'stopwatch_message': 'cleanup of proton postgres database',
                'job_name': 'Sqlite DB Cleanup',
            }
        }

    def process_cleanup(self, proton_remote_cleanup_type):

        if self.proton_cleanup_args.date is not None and self.proton_cleanup_args.time is not None:
            with self.stopwatch('./reports/cleanup', proton_remote_cleanup_type,
                                self.proton_cleanup_map[proton_remote_cleanup_type]['stopwatch_message']):
                try:
                    dbx = dropbox.Dropbox(self.proton_cleanup_map[proton_remote_cleanup_type]['token'])
                    folders = dbx.files_list_folder('')
                except Exception as err:
                    print('[PROTON Cleanup]-[{}] - '
                          'API Error\n'.format(self.proton_cleanup_map[proton_remote_cleanup_type]['job_name']), err)
                else:
                    try:
                        list_of_folders = []
                        deletion_metadata = []
                        for folder in folders.entries:
                            list_of_folders.append(folder.name)
                        sorted(list_of_folders, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), reverse=True)
                        if len(list_of_folders) > 5:
                            folders_to_delete = list_of_folders[0:4]
                            for folder in folders_to_delete:
                                deletion_metadata.append(dbx.files_delete('/{}'.format(folder)))

                        with open('./reports/cleanup/{}.txt'.format(proton_remote_cleanup_type), 'a') as writer:
                            for md in deletion_metadata:
                                writer.write('Successfully deleted '
                                             '- {} as part of '
                                             '{}\n'.format(md.name,
                                                           self.proton_cleanup_map[proton_remote_cleanup_type][
                                                               'job_name']))
                                writer.write('Date & time of execution: {} @ '
                                             '{}\n'.format(self.proton_cleanup_args.date,
                                                           self.proton_cleanup_args.time))

                    except Exception as e:
                        print('[PROTON Cleanup]-[{}] - '
                              'Cleanup error. '
                              ''.format(self.proton_cleanup_map[proton_remote_cleanup_type]['job_name']), e)
        else:
            print('PROTON remote cleanup cannot proceed unless key arguments date and time are available.')


if __name__ == '__main__':
    cleanup = CleanupProtonRemoteBackup()
    cleanup.process_cleanup('env')
    cleanup.process_cleanup('pg')
    cleanup.process_cleanup('redis')
    cleanup.process_cleanup('sqlite')
