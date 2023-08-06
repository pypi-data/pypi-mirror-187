import azure.functions as func
import datetime
import json
from onedecoding.decode.hexastring import Hexastring
from onedecoding.decode.structs import structs_dict
from onedecoding.decode.auxfuncs import *

SENSOR_STRUCTS = structs_dict["sensor_structs"]
HEADER_STRUCTS = structs_dict["one_main_header_structs"]  # dict with header structs and their variables
DTYPES = structs_dict["data_types"]  # Dict with variables and their data types
BIT_SIZE = structs_dict["bit_size"]  # Dict with data types and their bit length


class Decode:
    def __init__(self, payload, deviceid):
        self.payload = payload
        self.header_dict = self.payload["one_main"]
        self.sensor_list = list(self.payload.items())[2:]
        self.mssg = {
            "deviceid": deviceid,
            "timestamp": self.set_timestamp()
        }
        
    def set_timestamp(self):
        ts = self.payload["ts"]
        return str(datetime.datetime.fromtimestamp(ts))
        
    def process(self):
        """
           Gets the event and decodes header data and sensor data.
        """
        header_data = self.process_header()
        sensor_data = self.process_sensor_list()
        self.mssg = {**self.mssg, **header_data, **sensor_data}
        return self.mssg
    
    def process_header(self):
        head_struct = str(self.header_dict["struct_id"])
        head_data = self.header_dict["data"]
        bm = bitmap(head_struct, HEADER_STRUCTS, DTYPES, BIT_SIZE)
        values = self.decode_string(head_data, bm, 5)
        return create_values_dict(values, bm)
    
    def process_sensor_list(self):
        all_sensors = {}
        for _, sensor in self.sensor_list:
            sensor_dict = self.process_sensor(sensor)
            all_sensors = {**all_sensors, **sensor_dict}
            
        return all_sensors
    
    def process_sensor(self, sensor_dict):
        sensor_id = sensor_dict["struct_id"]
        sensor_data = sensor_dict["data"]
        bm = bitmap(sensor_id, SENSOR_STRUCTS, DTYPES, BIT_SIZE)
        values = self.decode_string(sensor_data, bm, 1)
        return create_values_dict(values, bm)
    
    @staticmethod
    def decode_string(inp: str, bit_map: dict, digits: int) -> list:
        """
        :param inp: string of header data
        :param bit_map: {"loop": (8, "uint32_t"), "battery": (4, "uint16_t"), ...}
        """
        split = [0]+[bit_map[key][1] for key in bit_map]
        slices = Hexastring(inp.strip()).split_by(by=split)
        decimal_values = [slc.to_decimal(dtype=bit_map[key][0], digits=digits) for slc, key in zip(slices, bit_map)]
        return decimal_values
