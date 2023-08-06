structs_dict = {
    "one_main_header_structs":
    {
        "10000": ["loop", "battery", "charge_status"],
        "10001": ["loop", "battery", "charge_status", "lte_rssi"],
        "10002": [
            "loop", "battery", "charge_status", "lte_rssi",
            "latitude","longitude", "gps_hdop", "gps_speed", 
            "gps_course", "gps_num_satelliter"
        ]
    },
    "sensor_structs":
    {
        "30": [
            "LAS", "LASmin", "LASmax", "LAF", "LAFmin", 
            "LAFmax", "LAeq", "LA10", "LA20", "LA30", "LA40", 
            "LA50", "LA60", "LA70", "LA80", "LA90", "LA99"
        ],
        "23": [
            "pm_1", "pm_2_5", "pm_10"
        ]
    },
    "data_types":
    {
        "loop": "uint32_t",
        "battery": "uint16_t",
        "charge_status": "uint8_t",
        "lte_rssi": "uint16_t",
        "latitude": "float",
        "longitude": "float",
        "gps_hdop": "float",
        "gps_speed": "float",
        "gps_course": "float",
        "gps_num_satelliter": "uint8_t",
        "LAS": "float", "LASmin": "float", "LASmax": "float",
        "LAF": "float", "LAFmin": "float", "LAFmax": "float",
        "LAeq": "float", "LA10": "float", "LA20": "float",
        "LA30": "float", "LA40": "float", "LA50": "float",
        "LA60": "float", "LA70": "float", "LA80": "float",
        "LA90": "float", "LA99": "float",
        "pm_1": "float", "pm_2_5": "float", "pm_10": "float"
    },
    "bit_size":
    {
        "uint8_t": 2,
        "uint16_t": 4,
        "uint32_t": 8,
        "float": 8
    }
}