# -*- coding: utf-8 -*-
"""Generic Communication Interface. Defines the syntax of the communication functions.
Abstract methods must be implemented by child class (e.g. Ethernet Com IF)
:author:     R. Mueller
"""
from abc import abstractmethod, ABC

from tmtccmd.tm import TelemetryListT


class ComInterface(ABC):
    """Generic form of a communication interface to separate communication logic from
    the underlying interface.
    """

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def initialize(self, args: any = None) -> any:
        """Perform initializations step which can not be done in constructor or which require
        returnvalues.
        """

    @abstractmethod
    def open(self, args: any = None) -> None:
        """Opens the communication interface to allow communication.

        :return:
        """

    @abstractmethod
    def is_open(self) -> bool:
        """Can be used to check whether the communication interface is open. This is useful if
        opening a COM interface takes a longer time and is non-blocking
        """

    @abstractmethod
    def close(self, args: any = None) -> None:
        """Closes the ComIF and releases any held resources (for example a Communication Port).

        :return:
        """

    @abstractmethod
    def send(self, data: bytes):
        """Send raw data"""

    @abstractmethod
    def receive(self, parameters: any = 0) -> TelemetryListT:
        """Returns a list of received packets. The child class can use a separate thread to poll for
        the packets or use some other mechanism and container like a deque to store packets
        to be returned here.

        :param parameters:
        :return:
        """
        packet_list = []
        return packet_list

    @abstractmethod
    def data_available(self, timeout: float, parameters: any) -> int:
        """Check whether TM data is available.

        :param timeout:
        :param parameters: Can be an arbitrary parameter like a timeout
        :return: 0 if no data is available, number of bytes or anything > 0 otherwise.
        """
