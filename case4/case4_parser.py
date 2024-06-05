import os
import ctypes
import json
from case4_types import (
    BedSideMessageDef, 
    BedSideFloat, 
    Parameter
)

class Parser:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_file = self.input_path_to_file(input_file_path)
        self.result = {}
        self.error = ''

    def input_path_to_file(self, input_file_path):
        with open(input_file_path, 'rb') as file:
            return file.read()

    def parse(self):
        if os.stat(self.input_file_path).st_size == 0:
            self.error = 'File not found'
            print(self.error)
            return
        
        self.result = self.parse_data(self.input_file)
        print(self.result)

    def parse_data(self, data):
        initial_pointer_for_bytes = 60
        pointer_for_bytes = initial_pointer_for_bytes
        bedside_message = BedSideMessageDef.from_buffer_copy(data[:pointer_for_bytes])
        pointer_for_bytes += 6
        bedside_float = BedSideFloat.from_buffer_copy(data[initial_pointer_for_bytes:pointer_for_bytes])

        parameters = []
        #print(bedside_float.number_of_parameters) int conversion not needed range method includes
        for _ in range(bedside_float.number_of_parameters):
            parameter = Parameter.from_buffer_copy(data[pointer_for_bytes:(pointer_for_bytes + ctypes.sizeof(Parameter))])
            parameters.append(parameter)
            pointer_for_bytes += ctypes.sizeof(Parameter)
        
        extracted_values = self.extract_values_of_parameters(parameters)
        
        return {'bedside_message': bedside_message, 'bedside_float': bedside_float, 'extracted_values': extracted_values}
    
    def extract_values_of_parameters(self, parameters):
        extracted_values = []
        for parameter in parameters:
            if parameter.par_udp.parcode == 58:
                extracted_values.append(('HR', parameter.par_udp.par_val[0]))
            elif parameter.par_udp.parcode == 34:
                extracted_values.append(('RR', parameter.par_udp.par_val[0]))
            elif parameter.par_udp.parcode in {77, 78, 79, 80, 177, 178, 179, 180}:
                if parameter.par_type in {2, 3, 18}:
                    extracted_values.append(('MBP', parameter.par_udp.par_val[0]))
                    extracted_values.append(('SYSBP', parameter.par_udp.par_val[1]))
                    extracted_values.append(('DIABP', parameter.par_udp.par_val[2]))
                elif parameter.par_type == 6:
                    extracted_values.append(('MBP', parameter.par_udp.par_val[0]))
                    extracted_values.append(('CPP', parameter.par_udp.par_val[1]))
                else:
                    extracted_values.append(('MBP', parameter.par_udp.par_val[0]))
            elif parameter.par_udp.parcode in {45, 208}:
                extracted_values.append(('SPO2', parameter.par_udp.par_val[0]))
                extracted_values.append(('PPR', parameter.par_udp.par_val[1]))
            elif parameter.par_udp.parcode in {35, 184, 185, 186, 187}:
                extracted_values.append(('T1', parameter.par_udp.par_val[0]))
                extracted_values.append(('T2', parameter.par_udp.par_val[1]))
            elif parameter.par_udp.parcode in {24, 124}:
                extracted_values.append(('MNIBP', parameter.par_udp.par_val[0]))
                extracted_values.append(('SYSIBP', parameter.par_udp.par_val[1]))
                extracted_values.append(('DIAIBP', parameter.par_udp.par_val[2]))
        return extracted_values
    
    def get_result_json(self, output_path='case4/result.json'):
        if self.result is None:
            self.error = 'Result is none'
            print(self.error)
            return
        
        # Currently just converting object to string maybe later convert a way it can be accesed again by json
        # maybe stringfy bytes??? 
        self.result['bedside_message'] = self.result['bedside_message'].__repr__()
        self.result['bedside_float'] = self.result['bedside_float'].__repr__()

        with open(output_path, 'w') as fp:
            json.dump(self.result, fp)

parser = Parser('case4/device_4.txt')
parser.parse()
parser.get_result_json()