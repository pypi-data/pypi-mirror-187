"""Base VES module."""
#   Copyright 2022 Orange, Deutsche Telekom AG, Nokia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService


class VesService(OnapService):
    """Base VES class.

    Stores url to VES API (edit if you want to use other) and authentication tuple
    (username, password).
    """

    _url: str = settings.VES_URL
