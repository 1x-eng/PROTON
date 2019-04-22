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

import binascii
import hashlib
import os

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class PasswordManager:

    def __init__(self):
        super(PasswordManager, self).__init__()

    def hash_password(self, password):
        """
        Encodes a provided password in a way that is safe to store on a database or file

        hash_password actually does multiple things; it doesn’t just hash the password.

        The first thing it does is generate some random salt that should be added to the password.
        That’s just the sha256 hash of some random bytes read from os.urandom . It then extracts a string
        representation of the hashed salt as a set of hexadecimal numbers ( hexdigest).

        The salt is then provided to pbkdf2_hmac together with the password itself to hash the password in a randomized
        way. As pbkdf2_hmac  requires bytes as its input, the two strings (password and salt) are previously encoded
        in pure bytes. The salt is encoded as plain ASCII, as the hexadecimal representation of a hash will only
        contain the 0-9 and A-F characters. While the password is encoded as utf-8 , it could contain any character.
        (Is there anyone with emojis in their passwords?)

        The resulting pbkdf2 is a bunch of bytes, as you want to store it into a database; you use binascii.hexlify
        to convert the bunch of bytes into their hexadecimal representation in a string format.
        Hexlify is a convenient way to convert bytes to strings without losing data. It just prints all the bytes as
        two hexadecimal digits, so the resulting data will be twice as big as the original data, but apart from this,
        it’s exactly the same as the converted data.

        In the end, the function joins together the hash with its salt. As you know that the hexdigest of a sha256
        hash (the salt) is always 64 characters long, by joining them together, you can grab back the salt by reading
        the first 64 characters of the resulting string.

        :param password: Actual password.
        :return: Hashed password.
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        """
        Given an encoded password and a plain text one is provided by the user, it verifies whether the provided
        password matches the encoded (and thus saved) one

        The first thing verify_password does is extract the salt from the hashed password (remember, you placed it as
        the first 64 characters of the string resulting from hash_password).

        The extracted salt and the password candidate are then provided to pbkdf2_hmac  to compute their hash and then
        convert it into a string with binascii.hexlify . If the resulting hash matches with the hash part of the
        previously stored password (the characters after the salt), it means that the two passwords match.

        If the resulting hash doesn’t match, it means that the provided password is wrong. As you can see, it’s very
        important that you make the salt and the password available together, because you’ll need it to be able to
        verify the password and a different salt would result in a different hash and thus you’d never be able to
        verify the password.

        :param stored_password: Hashed password stored in the database
        :param provided_password: Actual password provided by user.
        :return: Boolean - Password match or does not match.
        """
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
