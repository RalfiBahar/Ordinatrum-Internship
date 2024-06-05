import ctypes

# Define the C data types in Python
UTINY = ctypes.c_uint8
CHAR = ctypes.c_int8
COUNT = ctypes.c_int16
SHORT = ctypes.c_int16
UCOUNT = ctypes.c_uint16

# Define the structures

class BedSideMessageDef(ctypes.Structure):
    _fields_ = [
        ('dst_addr', UTINY * 6),
        ('src_addr', UTINY * 6),
        ('func_code', COUNT),
        ('sub_code', COUNT),
        ('version', COUNT),
        ('seq_num', COUNT),
        ('req_res', COUNT),
        ('proc_id', COUNT),
        ('oln', UTINY * 32),
        ('return_status', COUNT),
        ('data_count', COUNT)
    ]

class ParameterUpdate(ctypes.Structure):
    _fields_ = [
        ('par_func_code', UTINY),
        ('parcode', UTINY),
        ('par_status', UCOUNT),
        ('par_val', COUNT * 3)
    ]

class ExtendedParameterUpdate(ctypes.Structure):
    _fields_ = [
        ('par_func_code', UTINY),
        ('par_code', UTINY),
        ('par_val', COUNT * 6)
    ]

class LimitValues(ctypes.Structure):
    _fields_ = [
        ('lo_limit', COUNT),
        ('hi_limit', COUNT)
    ]

class SetupAndLimits(ctypes.Structure):
    _fields_ = [
        ('par_func_code', UTINY),
        ('parcode', UTINY),
        ('flag', UCOUNT * 2),
        ('limit_values', LimitValues * 3),
        ('extra_limit', COUNT)
    ]

class ParameterMessage(ctypes.Structure):
    _fields_ = [
        ('attribute', UTINY),
        ('msg_index', UTINY)
    ]

class ParameterMessages(ctypes.Structure):
    _fields_ = [
        ('par_func_code', UTINY),
        ('parcode', UTINY),
        ('messages', ParameterMessage * 3),
        ('value', UCOUNT)
    ]

class MoreSetup(ctypes.Structure):
    _fields_ = [
        ('par_func_code', UTINY),
        ('parcode', UTINY),
        ('val', COUNT * 4)
    ]

class Parameter(ctypes.Structure):
    _fields_ = [
        ('par_udp', ParameterUpdate),
        ('ext_par_udp', ExtendedParameterUpdate),
        ('setup_n_lin', SetupAndLimits),
        ('par_mssg_s', ParameterMessages),
        ('more_setup', MoreSetup),
        ('par_type', UTINY),
        ('parcode', UTINY),
        ('pos', UTINY)
    ]

class RTCCPY(ctypes.Structure):
    _fields_ = [
        ('secpy_rt', UTINY),
        ('micpy_rt', UTINY),
        ('hrcpy_rt', UTINY),
        ('dwcpy_rt', UTINY),
        ('dacpy_rt', UTINY),
        ('mocpy_rt', UTINY),
        ('yrcpy_rt', UCOUNT)
    ]

class BedSideFloat(ctypes.Structure):
    _fields_ = [
        ('alarm_state', UTINY),
        ('alarm_level', UTINY),
        ('audio_alarm_level', UTINY),
        ('patient_admission', UTINY),
        ('number_of_parameters', UTINY),
        ('graph_status_msg', UTINY)
    ]