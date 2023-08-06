from __future__ import annotations
import os
import struct
from typing import Optional, Any

from spacepackets.ccsds.time import CdsShortTimestamp, CcsdsTimeProvider
from spacepackets.ecss import (
    Ptc,
    PfcUnsigned,
    PfcSigned,
    PfcReal,
    PusTelemetry,
)
from spacepackets.ecss.defs import PusService

from tmtccmd.util.obj_id import ObjectIdU32
from tmtccmd.pus.s20_fsfw_params import (
    CustomSubservice,
)
from tmtccmd.tm.base import PusTmInfoBase, PusTmBase
from tmtccmd.logging import get_console_logger

LOGGER = get_console_logger()


class ParamStruct:
    def __init__(self):
        self.param_id = 0
        self.domain_id = 0
        self.unique_id = 0
        self.linear_index = 0
        self.type_ptc = 0
        self.type_pfc = 0
        self.column = 0
        self.row = 0
        self.param: any = 0


class Service20FsfwTm(PusTmInfoBase, PusTmBase):
    """Custom Parameter Service Telemetry handler tailored towards Flight Software Framework (FSFW)
    TM packets
    """

    def __init__(
        self,
        subservice_id: int,
        object_id: bytearray,
        param_id: bytearray,
        domain_id: int,
        unique_id: int,
        linear_index: int,
        time: CdsShortTimestamp = None,
        ssc: int = 0,
        source_data: bytearray = bytearray([]),
        apid: int = -1,
        packet_version: int = 0b000,
        space_time_ref: int = 0b0000,
        destination_id: int = 0,
    ):
        pus_tm = PusTelemetry(
            service=PusService.S20_PARAMETER,
            subservice=subservice_id,
            time_provider=time,
            seq_count=ssc,
            source_data=source_data,
            apid=apid,
            packet_version=packet_version,
            space_time_ref=space_time_ref,
            destination_id=destination_id,
        )
        self.object_id = ObjectIdU32.from_bytes(obj_id_as_bytes=object_id)
        self.param_struct = ParamStruct()
        self.param_struct.param_id = param_id
        self.param_struct.domain_id = domain_id
        self.param_struct.unique_id = unique_id
        self.param_struct.linear_index = linear_index
        PusTmBase.__init__(self, pus_tm=pus_tm)
        PusTmInfoBase.__init__(self, pus_tm=pus_tm)
        self.__init_without_base(instance=self)
        self.set_packet_info("Parameter Service Reply")

    @staticmethod
    def __init_without_base(instance: Service20FsfwTm):
        tm_data = instance.tm_data
        if len(tm_data) < 8:
            return
        data_size = len(tm_data)
        instance.object_id = ObjectIdU32.from_bytes(obj_id_as_bytes=tm_data[0:4])
        instance.param_struct.param_id = struct.unpack("!I", tm_data[4:8])[0]
        instance.param_struct.domain_id = tm_data[4]
        instance.param_struct.unique_id = tm_data[5]
        instance.param_struct.linear_index = tm_data[6] << 8 | tm_data[7]

        if instance.subservice == CustomSubservice.TC_DUMP:
            # TODO: This needs to be more generic. Furthermore, we need to be able to handle
            #       vector and matrix dumps as well and this is not possible in the current form.
            instance.param_struct.type_ptc = tm_data[8]
            instance.param_struct.type_pfc = tm_data[9]
            instance.param_struct.column = tm_data[10]
            instance.param_struct.row = tm_data[11]
            rows = instance.param_struct.row
            columns = instance.param_struct.column
            ptc = instance.param_struct.type_ptc
            pfc = instance.param_struct.type_pfc
            if data_size > 12:
                if rows == 1 and columns == 1:
                    instance.param_struct.param = deserialize_scalar_entry(
                        ptc=ptc, pfc=pfc, tm_data=tm_data
                    )
                else:
                    LOGGER.warning(
                        "Deserialization of non-scalar parameters not implemented yet"
                    )
            else:
                LOGGER.info(
                    "Error when receiving Pus Service 20 TM: subservice is not 130"
                )

    @classmethod
    def __empty(cls) -> Service20FsfwTm:
        return cls(
            subservice_id=0,
            object_id=bytearray(4),
            param_id=bytearray(),
            domain_id=0,
            unique_id=0,
            linear_index=0,
        )

    @classmethod
    def unpack(
        cls, raw_telemetry: bytes, time_reader: Optional[CcsdsTimeProvider]
    ) -> Service20FsfwTm:
        service_20_tm = cls.__empty()
        service_20_tm.pus_tm = PusTelemetry.unpack(
            raw_telemetry=raw_telemetry, time_reader=time_reader
        )
        if len(service_20_tm.pus_tm.tm_data) < 4:
            LOGGER.warning("Invalid data length, less than 4")
        elif len(service_20_tm.pus_tm.tm_data) < 8:
            LOGGER.warning(
                "Invalid data length, less than 8 (Object ID and Parameter ID)"
            )
        service_20_tm.__init_without_base(instance=service_20_tm)
        return service_20_tm

    def append_telemetry_content(self, content_list: list):
        super().append_telemetry_content(content_list=content_list)
        content_list.append(self.object_id.as_hex_string)

    def append_telemetry_column_headers(self, header_list: list):
        super().append_telemetry_column_headers(header_list=header_list)
        header_list.append("Object ID")

    def get_custom_printout(self) -> str:
        custom_printout = ""
        header_list = []
        content_list = []
        if self.subservice == 130:
            custom_printout = f"Parameter Information:{os.linesep}"
            header_list.append("Domain ID")
            header_list.append("Unique ID")
            header_list.append("Linear Index")
            header_list.append("CCSDS Type")
            header_list.append("Columns")
            header_list.append("Rows")
            # TODO: For more complex parameters like vectors or matrices,
            #       special handling would be nice
            header_list.append("Parameter")

            content_list.append(self.param_struct.domain_id)
            content_list.append(self.param_struct.unique_id)
            content_list.append(self.param_struct.linear_index)
            content_list.append(
                f"PTC: {self.param_struct.type_ptc} | PFC: {self.param_struct.type_pfc}"
            )
            content_list.append(self.param_struct.column)
            content_list.append(self.param_struct.row)
            content_list.append(self.param_struct.param)

            custom_printout += f"{header_list}{os.linesep}"
            custom_printout += f"{content_list}"
        return custom_printout


def __deserialize_unsigned_scalar_entry(
    pfc: int, ptc: int, tm_data: bytes, param_len: int, len_error_str: str
) -> Optional[Any]:
    if pfc == PfcUnsigned.ONE_BYTE:
        if param_len < 1:
            LOGGER.warning(f"{len_error_str} 1")
            raise None
        return tm_data[12]
    elif pfc == PfcUnsigned.TWO_BYTES:
        if param_len < 2:
            LOGGER.warning(f"{len_error_str} 2")
            return None
        return struct.unpack("!H", tm_data[12:14])[0]
    if pfc == PfcUnsigned.FOUR_BYTES:
        if param_len < 4:
            LOGGER.warning(f"{len_error_str} 4")
            return None
        return struct.unpack("!I", tm_data[12:16])[0]
    elif pfc == PfcUnsigned.EIGHT_BYTES:
        if param_len < 8:
            LOGGER.warning(f"{len_error_str} 8")
            return None
        return struct.unpack("!Q", tm_data[12:20])[0]
    else:
        LOGGER.warning(f"Parsing of unsigned PTC {ptc} not implemented for PFC {pfc}")
        return None


def __deserialize_signed_scalar_entry(
    pfc: int, ptc: int, tm_data: bytes, param_len: int, len_error_str: str
) -> Optional[Any]:
    if pfc == PfcSigned.ONE_BYTE:
        if param_len < 1:
            LOGGER.warning(f"{len_error_str} 1")
            return None
        return struct.unpack("!b", tm_data[12:13])[0]
    elif pfc == PfcSigned.TWO_BYTES:
        if param_len < 2:
            LOGGER.warning(f"{len_error_str} 2")
            return None
        return struct.unpack("!h", tm_data[12:14])[0]
    elif pfc == PfcSigned.FOUR_BYTES:
        if param_len < 4:
            LOGGER.warning(f"{len_error_str} 4")
            return None
        return struct.unpack("!i", tm_data[12:16])[0]
    elif pfc == PfcSigned.EIGHT_BYTES:
        if param_len < 8:
            LOGGER.warning(f"{len_error_str} 8")
            return None
        return struct.unpack("!q", tm_data[12:20])[0]
    else:
        LOGGER.warning(f"Parsing of signed PTC {ptc} not implemented for PFC {pfc}")
        return None


def deserialize_scalar_entry(ptc: int, pfc: int, tm_data: bytes) -> Optional[Any]:
    param_data = tm_data[12:]
    param_len = len(param_data)
    len_error_str = "Invalid parameter data size, smaller than "
    if param_len == 0:
        return None
    if ptc == Ptc.UNSIGNED:
        return __deserialize_unsigned_scalar_entry(
            pfc, ptc, tm_data, param_len, len_error_str
        )
    elif ptc == Ptc.SIGNED:
        return __deserialize_signed_scalar_entry(
            pfc, ptc, tm_data, param_len, len_error_str
        )
    if ptc == Ptc.REAL:
        if pfc == PfcReal.FLOAT_SIMPLE_PRECISION_IEEE:
            if param_len < 4:
                LOGGER.warning(f"{len_error_str} 4")
                return None
            return struct.unpack("!f", tm_data[12:16])[0]
        elif pfc == PfcReal.DOUBLE_PRECISION_IEEE:
            if param_len < 8:
                LOGGER.warning(f"{len_error_str} 8")
                return None
            return struct.unpack("!d", tm_data[12:20])[0]
        else:
            LOGGER.warning(
                f"Parsing of real (floating point) PTC {ptc} not implemented "
                f"for PFC {pfc}"
            )
            return None
