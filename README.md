# My Internship @ Ordinatrum

Tracking (and saving) my progress throughout my summer internship...

---

- **Case 1**

  - The parse method processes the file content, splitting it into packets and fields using specified delimiters (\n\n\n for packets, | for fields, and : for field values).

- **Case 2**

  - The parse method processes the file content by splitting it into packets and sub-packets, then determining the packet type (either :VTv or :VTu).
  - :VTv packets are parsed using parse_vtv_packet, which maps ventilation modes based on a predefined dictionary.
  - :VTu packets are parsed using parse_vtu_packet, which extracts various fields such as expiratory tidal volume, total expiratory minute volume, and more.

- **Case 3**

  - The parse method processes the file content by splitting it into packets and identifying if they are <profile> or <data> packets.
  - **XML Parsing**
    - Profiles: Parsed using parse_profile, which extracts and stores profile information such as model, units, and enumerations.
    - Data: Parsed using parse_data, which uses the stored profiles to interpret and convert data values based on unit definitions.
  - Data values are interpreted according to their type (WORD, INT, UINT, BOOL, ENUM) and are scaled or converted as necessary.
  - Sure, here is the README entry for case 4 in the same format as your previous cases:

- **Case 4**
  - **Parsing Logic**:
    - The parse method processes the file content based on predefined C data structure (using **cpython** library).
  - **Data Structures**:
    - `BedSideMessageDef` includes fields such as destination and source addresses, function code, sub-code, version, sequence number, and more.
    - `BedSideFloat` includes fields such as alarm state, alarm level, audio alarm level, patient admission, number of parameters, and graph status message.
    - `Parameter` includes nested structures like `ParameterUpdate`, `ExtendedParameterUpdate`, `SetupAndLimits`, `ParameterMessages`, and `MoreSetup`.
  - **Scaling**:
    - If a unit has a “scale” value, the results from the packets will be divided by this value to obtain the final data.
  - **Data Types**:
    - `UTINY` corresponds to unsigned 8-bit bytes.
    - `CHAR` corresponds to signed 8-bit bytes.
    - `COUNT` and `SHORT` correspond to signed 16-bit words.
    - `UCOUNT` corresponds to unsigned 16-bit words.

---
