import os
# As format is XML, I am going to use xml reader library then do customizaton on top of it
import xml.etree.ElementTree as etree
import json

class Parser:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_file = self.input_path_to_file(input_file_path)
        self.packet_split_str = '\n\n\n'
        self.profiles = {}
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
            packet = packet.strip()
            if packet.startswith('<profile'):
                self.parse_profile(packet)
            elif packet.startswith('<data'):
                self.parse_data(packet)
        print(self.result)

    def parse_profile(self, packet):
        xml_tree = etree.fromstring(packet)
        profile_dict = {
            'model': xml_tree.get('model'),
            'units': {}
        }

        xml_units = xml_tree.findall('unit')
        for unit in xml_units:
            #class_type = unit.get('class') maybe not needed
            unit_id = unit.get('ID')
            unit_dict = {
                'type': unit.get('type'),
                'resolution': unit.get('resolution'),
                'range': unit.get('range'),
                'units': unit.get('units'),
                'label': unit.get('label'),
                'scale': unit.get('scale'),
                'enums': {}
            }
            xml_enums = unit.findall('enum')
            for enum in xml_enums:
                enum_value = enum.get('value')
                enum_label = enum.get('label')
                unit_dict['enums'][enum_value] = enum_label

            profile_dict['units'][unit_id] = unit_dict
        
        # Assuming model is like a unique id
        self.profiles[profile_dict['model']] = profile_dict

    def parse_data(self, packet):
        xml_tree = etree.fromstring(packet)
        data_class = xml_tree.get('class')
        data_crc = xml_tree.get('crc')
        data_msgID = xml_tree.get('msgID')
        data_values = xml_tree.text.strip()

        # Only seen type is ORD
        profile = self.profiles.get('ORD') 
        if not profile:
            self.error = 'No profile'
            print(self.error)
            return
        
        parsed_data_dict = {}
        unit_defs = profile['units']

        if data_class in ['alarm', 'monitor', 'setting']:
            for unit_id, unit_dict in unit_defs.items():
                if unit_dict['type'] in ['WORD', 'INT', 'UINT']:
                    scale_value = unit_dict.get('scale', '1')
                    if scale_value is None:
                        scale_value = '1'
                    if scale_value.startswith('E+'):
                        scale = float('1e' + scale_value[2:])
                    elif scale_value.startswith('E-'):
                        scale = float('1e' + scale_value[2:])
                    else:
                        scale = float(scale_value)
                    
                    '''
                    print('s', int(unit_dict.get('range').split(':')[0], 16))
                    print('e', int(unit_dict.get('range').split(':')[1], 16))

                    start = int(unit_dict.get('range').split(':')[0], 16)
                    size = (int(unit_dict.get('range').split(':')[1], 16) - start + 1)
                    end = start + size
                    print(data_values)
                    '''
                    #value = int(data_values[start:end], 16)
                    value = int(data_values, 16)
                    parsed_value = value / scale
                    parsed_data_dict[unit_id] = parsed_value 
                elif unit_dict['type'] == 'BOOL':
                    '''
                    start = int(unit_dict.get('range').split(':')[0], 16)
                    size = (int(unit_dict.get('range').split(':')[1], 16) - start + 1)
                    end = start + size
                    value = int(data_values[start:end], 16)
                    '''
                    value = int(data_values, 16)
                    parsed_data_dict[unit_id] = bool(value)
                elif unit_dict['type'] == 'ENUM':
                    '''
                    start = int(unit_dict.get('range').split(':')[0], 16)
                    size = (int(unit_dict.get('range').split(':')[1], 16) - start + 1)
                    end = start + size
                    value = data_values[start:end]
                    '''
                    value = data_values
                    parsed_data_dict[unit_id] = unit_dict['enums'].get(value, value)

        self.result[len(self.result)] = parsed_data_dict

    def get_result_json(self, output_path='case3/result.json'):
        if self.result is None:
            self.error = 'Result is none'
            print(self.error)
            return
        
        with open(output_path, 'w') as fp:
            json.dump(self.result, fp)


    
parser = Parser('case3/device_3.txt')
parser.parse()
parser.get_result_json()