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

from configuration import ProtonConfig
from nucleus.db.connection_manager import ConnectionManager
from nucleus.metagen import MetaGen
from sqlalchemy import MetaData, Table, Column, Integer, DateTime, String, ForeignKey
from unittest import TestCase

__author__ = "Pooja Pruthvi, pooja.pruthvikumar@gmail.com"
__copyright__ = "Copyright (C) 2018 Pooja Pruthvi"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class TestMetaGen(TestCase):

    def test_metagen(self):
        metagen_object = MetaGen()
        assert str(type(metagen_object.metagen_logger)) == "<class 'logging.Logger'>"
        assert metagen_object._MetaGen__models_root == '{}/mic/models'.format(metagen_object.ROOT_DIR)
        assert metagen_object._MetaGen__controllers_root == '{}/mic/controllers'.format(metagen_object.ROOT_DIR)
        assert metagen_object._MetaGen__main_executable == '{}/main.py'.format(metagen_object.ROOT_DIR)
        assert str(type(metagen_object._MetaGen__jinja_env)) == "<class 'jinja2.environment.Environment'>"
        assert str(type(metagen_object._MetaGen__models_template)) == "<class 'jinja2.environment.Template'>"
        assert str(type(metagen_object._MetaGen__controllers_template)) == "<class 'jinja2.environment.Template'>"
        assert str(type(metagen_object.bootstrap_sqlite)) == "<class 'method'>"
        assert str(type(metagen_object.new_mic)) == "<class 'method'>"
        