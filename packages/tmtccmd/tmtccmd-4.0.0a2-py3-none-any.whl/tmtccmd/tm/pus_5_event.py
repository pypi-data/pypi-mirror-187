# -*- coding: utf-8 -*-
"""Contains classes and functions to deserialize PUS Service 5 Telemetry
"""
from __future__ import annotations
from abc import abstractmethod
import struct
from typing import Optional

from spacepackets.ccsds.time import CcsdsTimeProvider
from spacepackets.ecss.defs import PusService
from spacepackets.ecss.pus_5_event import Subservice
from spacepackets.ecss.tm import CdsShortTimestamp
from tmtccmd.tm.base import PusTmInfoBase, PusTmBase, PusTelemetry
from tmtccmd.util.obj_id import ObjectIdU32
from tmtccmd.logging import get_console_logger


LOGGER = get_console_logger()


class Service5Tm(PusTmBase, PusTmInfoBase):
    def __init__(
        self,
        subservice: Subservice,
        event_id: int,
        object_id: bytearray,
        param_1: int,
        param_2: int,
        time: Optional[CdsShortTimestamp],
        ssc: int = 0,
        apid: int = -1,
        packet_version: int = 0b000,
        space_time_ref: int = 0b0000,
        destination_id: int = 0,
    ):
        """Create a Service 5 telemetry instance.
        Use the unpack function to create an instance from a raw bytestream instead.
        :param subservice: Subservice ID
        :param time: CDS Short Timecode
        :param object_id: 4 byte object ID
        :raises ValueError: Invalid input arguments
        """
        self._object_id = ObjectIdU32.from_bytes(obj_id_as_bytes=object_id)
        self._event_id = event_id
        self._param_1 = param_1
        self._param_2 = param_2
        source_data = bytearray()
        source_data.extend(struct.pack("!H", self._event_id))
        if len(object_id) != 4:
            LOGGER.warning("Object ID must be a bytrarray with length 4")
            raise ValueError
        source_data.extend(object_id)
        source_data.extend(struct.pack("!I", self._param_1))
        source_data.extend(struct.pack("!I", self._param_2))
        pus_tm = PusTelemetry(
            service=PusService.S5_EVENT,
            subservice=subservice,
            time_provider=time,
            seq_count=ssc,
            source_data=source_data,
            apid=apid,
            packet_version=packet_version,
            space_time_ref=space_time_ref,
            destination_id=destination_id,
        )
        PusTmBase.__init__(self, pus_tm=pus_tm)
        PusTmInfoBase.__init__(self, pus_tm=pus_tm)
        self.__init_without_base(instance=self, set_attrs_from_tm_data=False)

    @classmethod
    def __empty(cls) -> Service5Tm:
        return cls(
            subservice=Subservice.TM_INFO_EVENT,
            event_id=0,
            object_id=bytearray(4),
            param_1=0,
            param_2=0,
            time=CdsShortTimestamp.empty(),
        )

    @classmethod
    def unpack(
        cls, raw_telemetry: bytes, time_reader: Optional[CcsdsTimeProvider]
    ) -> Service5Tm:
        service_5_tm = cls.__empty()
        service_5_tm.pus_tm = PusTelemetry.unpack(
            raw_telemetry=raw_telemetry, time_reader=time_reader
        )
        service_5_tm.__init_without_base(
            instance=service_5_tm, set_attrs_from_tm_data=True
        )
        return service_5_tm

    @abstractmethod
    def append_telemetry_content(self, content_list: list):
        super().append_telemetry_content(content_list=content_list)
        content_list.append(str(self._event_id))
        content_list.append(self._object_id.as_hex_string)
        content_list.append(str(hex(self._param_1)) + ", " + str(self._param_1))
        content_list.append(str(hex(self._param_2)) + ", " + str(self._param_2))

    @abstractmethod
    def append_telemetry_column_headers(self, header_list: list):
        super().append_telemetry_column_headers(header_list=header_list)
        header_list.append("Event ID")
        header_list.append("Reporter ID")
        header_list.append("Parameter 1")
        header_list.append("Parameter 2")

    def __str__(self):
        return (
            f"Subservice {self.subservice} | Event ID {self.event_id} | "
            f"Reporter ID 0x{self.reporter_id.as_hex_string} | "
            f"Param 1 {self.param_1} | Param 2 {self.param_2}"
        )

    @property
    def reporter_id(self) -> ObjectIdU32:
        return self._object_id

    @property
    def event_id(self):
        return self._event_id

    @property
    def param_1(self):
        return self._param_1

    @property
    def param_2(self):
        return self._param_2

    @staticmethod
    def __init_without_base(instance: Service5Tm, set_attrs_from_tm_data: bool = False):
        if instance.service != 5:
            LOGGER.warning("This packet is not an event service packet!")
        instance.set_packet_info("Event")
        if instance.subservice == Subservice.TM_INFO_EVENT:
            instance.append_packet_info(" Info")
        elif instance.subservice == Subservice.TM_LOW_SEVERITY_EVENT:
            instance.append_packet_info(" Error Low Severity")
        elif instance.subservice == Subservice.TM_MEDIUM_SEVERITY_EVENT:
            instance.append_packet_info(" Error Med Severity")
        elif instance.subservice == Subservice.TM_HIGH_SEVERITY_EVENT:
            instance.append_packet_info(" Error High Severity")
        tm_data = instance.tm_data
        if len(tm_data) < 14:
            LOGGER.warning(
                f"Length of TM data field {len(tm_data)} shorter than expected 14 bytes"
            )
            raise ValueError
        if set_attrs_from_tm_data:
            instance._event_id = struct.unpack(">H", tm_data[0:2])[0]
            instance._object_id = ObjectIdU32.from_bytes(tm_data[2:6])
            instance._param_1 = struct.unpack(">I", tm_data[6:10])[0]
            instance._param_2 = struct.unpack(">I", tm_data[10:14])[0]
