# Copyright (c) 2020, Riverbank Computing Limited
# All rights reserved.
#
# This copy of SIP is licensed for use under the terms of the SIP License
# Agreement.  See the file LICENSE for more details.
#
# This copy of SIP may also used under the terms of the GNU General Public
# License v2 or v3 as published by the Free Software Foundation which can be
# found in the files LICENSE-GPL2 and LICENSE-GPL3 included in this package.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
from packaging.version import parse

from ..exceptions import UserException


# The directory containing the different module implementations.
_module_source_dir = os.path.join(os.path.dirname(__file__), 'source')


def get_module_source_dir(abi_version):
    """ Return the name of the directory containing the latest source of the
    sip module that implements the given ABI version.
    """

    return os.path.join(_module_source_dir, abi_version)


def get_sip_module_version(abi_version):
    """ Return the version number of the latest implementation of the sip
    module with the given ABI as a string.
    """

    # Read the version from the header file shared with the code generator.
    with open(os.path.join(get_module_source_dir(abi_version), 'sip.h.in')) as vf:
        for line in vf:
            parts = line.strip().split()
            if len(parts) == 3 and parts[0] == '#define':
                name = parts[1]
                value = parts[2]

                if name == 'SIP_MODULE_PATCH_VERSION':
                    patch_version = value
                    break
        else:
            # This is an internal error and should never happen.
            raise ValueError(
                    "'SIP_MODULE_PATCH_VERSION' not found for ABI {0}".format(
                            abi_version))

    return abi_version + '.' + patch_version


def resolve_abi_version(abi_version):
    """ Return a valid ABI version or the latest if none was given. """

    if abi_version:
        # See if a complete version number was given.
        if '.' in abi_version:
            if not os.path.isdir(get_module_source_dir(abi_version)):
                raise UserException(
                        "'{0}' is not a supported ABI version".format(
                                abi_version))
        else:
            # Only the major version was given.
            major = abi_version + '.'
            versions = sorted(os.listdir(_module_source_dir), key=parse,
                    reverse=True)

            for version in versions:
                if version.startswith(major):
                    abi_version = version
                    break
            else:
                raise UserException(
                        "'{0}' is not a supported ABI major version".format(
                                abi_version))
    else:
        abi_version = sorted(os.listdir(_module_source_dir), key=parse)[-1]

    return abi_version
