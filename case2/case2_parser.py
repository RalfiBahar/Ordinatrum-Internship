import os

class Parser:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_file = self.input_path_to_file(input_file_path)
        self.packet_split_str = '\n\n\n'
        self.subpacket_split_char = '\n'
        self.field_split_char = '|'
        self.field_value_split_char = ':'
        self.result = {}
        self.error = ''

    def input_path_to_file(self, input_file_path):
        with open(input_file_path, 'r') as file:
            return file.read()

    def parse(self):
        if os.stat(self.input_file_path).st_size == 0:
            self.error = 'File not found'
            print(self.error)
            return
        
        packets = self.input_file.split(self.packet_split_str)

        for packet in packets:
            sub_packets = packet.strip().split(self.subpacket_split_char)
            packet_type = sub_packets[0].strip()
            packet_data = {}
            if packet_type.startswith(':VTv'):
                packet_data = self.parse_vtv_packet(sub_packets[:1])
            elif packet_type.startswith(':VTu'):
                packet_data = self.parse_vtu_packet(sub_packets[:1])

            if packet_data:
                self.result[len(self.result)] = packet_data

        print(self.result)

    def field_extraction(self, sub_packets, field_definitions):
        curr_packet_data = {}
        for sub_packet in sub_packets:
            for field_name, (start, size, multiplier) in field_definitions.items():
                end = start + size
                field_value = sub_packet[start:end].strip()
                try:
                    field_value = float(field_value) * multiplier
                except:
                    # Keep field value in string format withot multiplier
                    self.error = 'Field value float conversion error'
                    continue
                curr_packet_data[field_name] = field_value
        return curr_packet_data

    def parse_vtv_packet(self, sub_packets):
        field_defs = {'VentilationMode': (48, 1, 0)}
        vent_modes = {
            "v": "VCV", 
            "p": "PCV", 
            "g": "PCV-VG", 
            "G": "BiLevel-VG",
            "s": "SIMV-VC", 
            "i": "SIMV-PC", 
            "S": "SIMV-PCVG", 
            "B": "BiLevel",
            "c": "CPAP/PSV", 
            "n": "NIV", 
            "N": "nCPAP", 
            "V": "VG-PS"
        }

        vtv_packet_data = self.field_extraction(sub_packets, field_defs)
        if 'VentilationMode' in vtv_packet_data:
            vent_mode_val = vtv_packet_data['VentilationMode']
            vtv_packet_data['VentilationMode'] = vent_modes.get(vent_mode_val) #No deafult rn?

        return vtv_packet_data
    
    def parse_vtu_packet(self, sub_packets):
        field_defs = {
            'ExpiratoryTidalVolTVexp': (4, 4, 1),
            'TotalExpMinuteVolMVexp': (8, 4, 0.01),
            'RespiratoryRateTotal': (12, 3, 1),
            'FiO2': (15, 3, 1),
            'InspiratoryTime': (199, 3, 0.1),
            'ExpiratoryTime': (202, 3, 0.1)
        }
        return self.field_extraction(sub_packets, field_defs)
    
parser = Parser('case2/device_2.txt')
parser.parse()
