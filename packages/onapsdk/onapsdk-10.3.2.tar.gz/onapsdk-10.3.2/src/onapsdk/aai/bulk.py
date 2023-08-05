"""A&AI bulk module."""
#   Copyright 2022 Orange, Deutsche Telekom AG
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

from dataclasses import dataclass
from typing import Any, Dict, Iterable

from more_itertools import chunked

from onapsdk.configuration import settings
from onapsdk.utils.jinja import jinja_env

from .aai_element import AaiElement


@dataclass
class AaiBulkRequest:
    """Class to store information about a request to be sent in A&AI bulk request."""

    action: str
    uri: str
    body: Dict[Any, Any]


@dataclass
class AaiBulkResponse:
    """Class to store A&AI bulk response."""

    action: str
    uri: str
    status_code: int
    body: str


class AaiBulk(AaiElement):
    """A&AI bulk class.

    Use it to send bulk request to A&AI. With bulk request you can send
        multiple requests at once.
    """

    @property
    def url(self) -> str:
        """Bulk url.

        Returns:
            str: A&AI bulk API url.

        """
        return f"{self.base_url}{self.api_version}/bulk"

    @classmethod
    def single_transaction(cls, aai_requests: Iterable[AaiBulkRequest])\
        -> Iterable[AaiBulkResponse]:
        """Singe transaction bulk request.

        Args:
            aai_requests (Iterable[AaiBulkRequest]): Iterable object of requests to be sent
                as a bulk request.

        Yields:
            Iterator[Iterable[AaiBulkResponse]]: Bulk request responses. Each object
                correspond to the sent request.

        """
        for requests_chunk in chunked(aai_requests, settings.AAI_BULK_CHUNK):
            for response in cls.send_message_json(\
                "POST",\
                "Send bulk A&AI request",\
                f"{cls.base_url}{cls.api_version}/bulk/single-transaction",\
                data=jinja_env().get_template(\
                    "aai_bulk.json.j2").render(operations=requests_chunk)\
            )["operation-responses"]:
                yield AaiBulkResponse(
                    action=response["action"],
                    uri=response["uri"],
                    status_code=response["response-status-code"],
                    body=response["response-body"]
                )
