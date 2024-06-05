import os

class Parser:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_file = self.input_path_to_file(input_file_path)
        self.packet_split_str = '\n\n\n'
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
            fields = packet.strip().split(self.field_split_char)
            packet_data = {}
            for field in fields:
                if self.field_value_split_char in field:
                    field_name = field.split(self.field_value_split_char, 1)[0].strip()
                    field_value = field.split(self.field_value_split_char, 1)[1].strip()
                    packet_data[field_name] = field_value
            if packet_data: 
                self.result[len(self.result)] = packet_data

        print(self.result)

parser = Parser('case1/device_1.txt')
parser.parse()
