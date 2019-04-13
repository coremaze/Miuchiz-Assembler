opcodes = {
  0x69: {
    "name": "ADC",
    "mode": "Immediate"
  },
  0x65: {
    "name": "ADC",
    "mode": "Zero Page"
  },
  0x75: {
    "name": "ADC",
    "mode": "Zero Page,X"
  },
  0x6D: {
    "name": "ADC",
    "mode": "Absolute"
  },
  0x7D: {
    "name": "ADC",
    "mode": "Absolute,X"
  },
  0x79: {
    "name": "ADC",
    "mode": "Absolute,Y"
  },
  0x61: {
    "name": "ADC",
    "mode": "(Zero Page,X)"
  },
  0x71: {
    "name": "ADC",
    "mode": "(Zero Page),Y"
  },
  0x72: {
    "name": "ADC",
    "mode": "(Zero Page)"
  },
  0x29: {
    "name": "AND",
    "mode": "Immediate"
  },
  0x25: {
    "name": "AND",
    "mode": "Zero Page"
  },
  0x35: {
    "name": "AND",
    "mode": "Zero Page,X"
  },
  0x2D: {
    "name": "AND",
    "mode": "Absolute"
  },
  0x3D: {
    "name": "AND",
    "mode": "Absolute,X"
  },
  0x39: {
    "name": "AND",
    "mode": "Absolute,Y"
  },
  0x21: {
    "name": "AND",
    "mode": "(Zero Page,X)"
  },
  0x31: {
    "name": "AND",
    "mode": "(Zero Page),Y"
  },
  0x32: {
    "name": "AND",
    "mode": "(Zero Page)"
  },
  0x0A: {
    "name": "ASL",
    "mode": "Accumulator"
  },
  0x06: {
    "name": "ASL",
    "mode": "Zero Page"
  },
  0x16: {
    "name": "ASL",
    "mode": "Zero Page,X"
  },
  0x0E: {
    "name": "ASL",
    "mode": "Absolute"
  },
  0x1E: {
    "name": "ASL",
    "mode": "Absolute,X"
  },
  0x0F: {
    "name": "BBR0",
    "mode": "Bit, Relative"
  },
  0x1F: {
    "name": "BBR1",
    "mode": "Bit, Relative"
  },
  0x2F: {
    "name": "BBR2",
    "mode": "Bit, Relative"
  },
  0x3F: {
    "name": "BBR3",
    "mode": "Bit, Relative"
  },
  0x4F: {
    "name": "BBR4",
    "mode": "Bit, Relative"
  },
  0x5F: {
    "name": "BBR5",
    "mode": "Bit, Relative"
  },
  0x6F: {
    "name": "BBR6",
    "mode": "Bit, Relative"
  },
  0x7F: {
    "name": "BBR7",
    "mode": "Bit, Relative"
  },
  0x8F: {
    "name": "BBS0",
    "mode": "Bit, Relative"
  },
  0x9F: {
    "name": "BBS1",
    "mode": "Bit, Relative"
  },
  0xAF: {
    "name": "BBS2",
    "mode": "Bit, Relative"
  },
  0xBF: {
    "name": "BBS3",
    "mode": "Bit, Relative"
  },
  0xCF: {
    "name": "BBS4",
    "mode": "Bit, Relative"
  },
  0xDF: {
    "name": "BBS5",
    "mode": "Bit, Relative"
  },
  0xEF: {
    "name": "BBS6",
    "mode": "Bit, Relative"
  },
  0xFF: {
    "name": "BBS7",
    "mode": "Bit, Relative"
  },
  0x90: {
    "name": "BCC",
    "mode": "Relative"
  },
  0xB0: {
    "name": "BCS",
    "mode": "Relative"
  },
  0xF0: {
    "name": "BEQ",
    "mode": "Relative"
  },
  0x89: {
    "name": "BIT",
    "mode": "Immediate"
  },
  0x24: {
    "name": "BIT",
    "mode": "Zero Page"
  },
  0x34: {
    "name": "BIT",
    "mode": "Zero Page,X"
  },
  0x2C: {
    "name": "BIT",
    "mode": "Absolute"
  },
  0x3C: {
    "name": "BIT",
    "mode": "Absolute,X"
  },
  0x30: {
    "name": "BMI",
    "mode": "Relative"
  },
  0xD0: {
    "name": "BNE",
    "mode": "Relative"
  },
  0x10: {
    "name": "BPL",
    "mode": "Relative"
  },
  0x80: {
    "name": "BRA",
    "mode": "Relative"
  },
  0x00: {
    "name": "BRK",
    "mode": "Implied"
  },
  0x50: {
    "name": "BVC",
    "mode": "Relative"
  },
  0x70: {
    "name": "BVS",
    "mode": "Relative"
  },
  0x18: {
    "name": "CLC",
    "mode": "Implied"
  },
  0xD8: {
    "name": "CLD",
    "mode": "Implied"
  },
  0x58: {
    "name": "CLI",
    "mode": "Implied"
  },
  0xB8: {
    "name": "CLV",
    "mode": "Implied"
  },
  0xC9: {
    "name": "CMP",
    "mode": "Immediate"
  },
  0xC5: {
    "name": "CMP",
    "mode": "Zero Page"
  },
  0xD5: {
    "name": "CMP",
    "mode": "Zero Page,X"
  },
  0xCD: {
    "name": "CMP",
    "mode": "Absolute"
  },
  0xDD: {
    "name": "CMP",
    "mode": "Absolute,X"
  },
  0xD9: {
    "name": "CMP",
    "mode": "Absolute,Y"
  },
  0xC1: {
    "name": "CMP",
    "mode": "(Zero Page,X)"
  },
  0xD1: {
    "name": "CMP",
    "mode": "(Zero Page),Y"
  },
  0xD2: {
    "name": "CMP",
    "mode": "(Zero Page)"
  },
  0xE0: {
    "name": "CPX",
    "mode": "Immediate"
  },
  0xE4: {
    "name": "CPX",
    "mode": "Zero Page"
  },
  0xEC: {
    "name": "CPX",
    "mode": "Absolute"
  },
  0xC0: {
    "name": "CPY",
    "mode": "Immediate"
  },
  0xC4: {
    "name": "CPY",
    "mode": "Zero Page"
  },
  0xCC: {
    "name": "CPY",
    "mode": "Absolute"
  },
  0x3A: {
    "name": "DEC",
    "mode": "Accumulator"
  },
  0xC6: {
    "name": "DEC",
    "mode": "Zero Page"
  },
  0xD6: {
    "name": "DEC",
    "mode": "Zero Page,X"
  },
  0xCE: {
    "name": "DEC",
    "mode": "Absolute"
  },
  0xDE: {
    "name": "DEC",
    "mode": "Absolute,X"
  },
  0xCA: {
    "name": "DEX",
    "mode": "Implied"
  },
  0x88: {
    "name": "DEY",
    "mode": "Implied"
  },
  0x49: {
    "name": "EOR",
    "mode": "Immediate"
  },
  0x45: {
    "name": "EOR",
    "mode": "Zero Page"
  },
  0x55: {
    "name": "EOR",
    "mode": "Zero Page,X"
  },
  0x4D: {
    "name": "EOR",
    "mode": "Absolute"
  },
  0x5D: {
    "name": "EOR",
    "mode": "Absolute,X"
  },
  0x59: {
    "name": "EOR",
    "mode": "Absolute,Y"
  },
  0x41: {
    "name": "EOR",
    "mode": "(Zero Page,X)"
  },
  0x51: {
    "name": "EOR",
    "mode": "(Zero Page),Y"
  },
  0x52: {
    "name": "EOR",
    "mode": "(Zero Page)"
  },
  0x1A: {
    "name": "INC",
    "mode": "Accumulator"
  },
  0xE6: {
    "name": "INC",
    "mode": "Zero Page"
  },
  0xF6: {
    "name": "INC",
    "mode": "Zero Page,X"
  },
  0xEE: {
    "name": "INC",
    "mode": "Absolute"
  },
  0xFE: {
    "name": "INC",
    "mode": "Absolute,X"
  },
  0xE8: {
    "name": "INX",
    "mode": "Implied"
  },
  0xC8: {
    "name": "INY",
    "mode": "Implied"
  },
  0x4C: {
    "name": "JMP",
    "mode": "Absolute"
  },
  0x6C: {
    "name": "JMP",
    "mode": "(Absolute)"
  },
  0x7C: {
    "name": "JMP",
    "mode": "(Absolute,X)"
  },
  0x20: {
    "name": "JSR",
    "mode": "Absolute"
  },
  0xA9: {
    "name": "LDA",
    "mode": "Immediate"
  },
  0xA5: {
    "name": "LDA",
    "mode": "Zero Page"
  },
  0xB5: {
    "name": "LDA",
    "mode": "Zero Page,X"
  },
  0xAD: {
    "name": "LDA",
    "mode": "Absolute"
  },
  0xBD: {
    "name": "LDA",
    "mode": "Absolute,X"
  },
  0xB9: {
    "name": "LDA",
    "mode": "Absolute,Y"
  },
  0xA1: {
    "name": "LDA",
    "mode": "(Zero Page,X)"
  },
  0xB1: {
    "name": "LDA",
    "mode": "(Zero Page),Y"
  },
  0xB2: {
    "name": "LDA",
    "mode": "(Zero Page)"
  },
  0xA2: {
    "name": "LDX",
    "mode": "Immediate"
  },
  0xA6: {
    "name": "LDX",
    "mode": "Zero Page"
  },
  0xB6: {
    "name": "LDX",
    "mode": "Zero Page,Y"
  },
  0xAE: {
    "name": "LDX",
    "mode": "Absolute"
  },
  0xBE: {
    "name": "LDX",
    "mode": "Absolute,Y"
  },
  0xA0: {
    "name": "LDY",
    "mode": "Immediate"
  },
  0xA4: {
    "name": "LDY",
    "mode": "Zero Page"
  },
  0xB4: {
    "name": "LDY",
    "mode": "Zero Page,Y"
  },
  0xAC: {
    "name": "LDY",
    "mode": "Absolute"
  },
  0xBC: {
    "name": "LDY",
    "mode": "Absolute,Y"
  },
  0x4A: {
    "name": "LSR",
    "mode": "Accumulator"
  },
  0x46: {
    "name": "LSR",
    "mode": "Zero Page"
  },
  0x56: {
    "name": "LSR",
    "mode": "Zero Page,X"
  },
  0x4E: {
    "name": "LSR",
    "mode": "Absolute"
  },
  0x5E: {
    "name": "LSR",
    "mode": "Absolute,X"
  },
  0xEA: {
    "name": "NOP",
    "mode": "Implied"
  },
  0x09: {
    "name": "ORA",
    "mode": "Immediate"
  },
  0x05: {
    "name": "ORA",
    "mode": "Zero Page"
  },
  0x15: {
    "name": "ORA",
    "mode": "Zero Page,X"
  },
  0x0D: {
    "name": "ORA",
    "mode": "Absolute"
  },
  0x1D: {
    "name": "ORA",
    "mode": "Absolute,X"
  },
  0x19: {
    "name": "ORA",
    "mode": "Absolute,Y"
  },
  0x01: {
    "name": "ORA",
    "mode": "(Zero Page,X)"
  },
  0x11: {
    "name": "ORA",
    "mode": "(Zero Page),Y"
  },
  0x12: {
    "name": "ORA",
    "mode": "(Zero Page)"
  },
  0x48: {
    "name": "PHA",
    "mode": "Implied"
  },
  0xDA: {
    "name": "PHX",
    "mode": "Implied"
  },
  0x5A: {
    "name": "PHY",
    "mode": "Implied"
  },
  0x68: {
    "name": "PLA",
    "mode": "Implied"
  },
  0xFA: {
    "name": "PLX",
    "mode": "Implied"
  },
  0x7A: {
    "name": "PLY",
    "mode": "Implied"
  },
  0x2A: {
    "name": "ROL",
    "mode": "Accumulator"
  },
  0x26: {
    "name": "ROL",
    "mode": "Zero Page"
  },
  0x36: {
    "name": "ROL",
    "mode": "Zero Page,X"
  },
  0x2E: {
    "name": "ROL",
    "mode": "Absolute"
  },
  0x3E: {
    "name": "ROL",
    "mode": "Absolute,X"
  },
  0x6A: {
    "name": "ROR",
    "mode": "Accumulator"
  },
  0x66: {
    "name": "ROR",
    "mode": "Zero Page"
  },
  0x76: {
    "name": "ROR",
    "mode": "Zero Page,X"
  },
  0x6E: {
    "name": "ROR",
    "mode": "Absolute"
  },
  0x7E: {
    "name": "ROR",
    "mode": "Absolute,X"
  },
  0x40: {
    "name": "RTI",
    "mode": "Implied"
  },
  0x60: {
    "name": "RTS",
    "mode": "Implied"
  },
  0xE9: {
    "name": "SBC",
    "mode": "Immediate"
  },
  0xE5: {
    "name": "SBC",
    "mode": "Zero Page"
  },
  0xF5: {
    "name": "SBC",
    "mode": "Zero Page,X"
  },
  0xED: {
    "name": "SBC",
    "mode": "Absolute"
  },
  0xFD: {
    "name": "SBC",
    "mode": "Absolute,X"
  },
  0xF9: {
    "name": "SBC",
    "mode": "Absolute,Y"
  },
  0xE1: {
    "name": "SBC",
    "mode": "(Zero Page,X)"
  },
  0xF1: {
    "name": "SBC",
    "mode": "(Zero Page),Y"
  },
  0xF2: {
    "name": "SBC",
    "mode": "(Zero Page)"
  },
  0x38: {
    "name": "SEC",
    "mode": "Implied"
  },
  0xF8: {
    "name": "SED",
    "mode": "Implied"
  },
  0x78: {
    "name": "SEI",
    "mode": "Implied"
  },
  0x85: {
    "name": "STA",
    "mode": "Zero Page"
  },
  0x95: {
    "name": "STA",
    "mode": "Zero Page,X"
  },
  0x8D: {
    "name": "STA",
    "mode": "Absolute"
  },
  0x9D: {
    "name": "STA",
    "mode": "Absolute,X"
  },
  0x99: {
    "name": "STA",
    "mode": "Absolute,Y"
  },
  0x81: {
    "name": "STA",
    "mode": "(Zero Page,X)"
  },
  0x91: {
    "name": "STA",
    "mode": "(Zero Page),Y"
  },
  0x92: {
    "name": "STA",
    "mode": "(Zero Page)"
  },
  0x86: {
    "name": "STX",
    "mode": "Zero Page"
  },
  0x96: {
    "name": "STX",
    "mode": "Zero Page,Y"
  },
  0x8E: {
    "name": "STX",
    "mode": "Absolute"
  },
  0x84: {
    "name": "STY",
    "mode": "Zero Page"
  },
  0x94: {
    "name": "STY",
    "mode": "Zero Page,X"
  },
  0x8C: {
    "name": "STY",
    "mode": "Absolute"
  },
  0x64: {
    "name": "STZ",
    "mode": "Zero Page"
  },
  0x74: {
    "name": "STZ",
    "mode": "Zero Page,X"
  },
  0x9C: {
    "name": "STZ",
    "mode": "Absolute"
  },
  0x9E: {
    "name": "STZ",
    "mode": "Absolute,X"
  },
  0xAA: {
    "name": "TAX",
    "mode": "Implied"
  },
  0xA8: {
    "name": "TAY",
    "mode": "Implied"
  },
  0x14: {
    "name": "TRB",
    "mode": "Zero Page"
  },
  0x1C: {
    "name": "TRB",
    "mode": "Absolute"
  },
  0x04: {
    "name": "TSB",
    "mode": "Zero Page"
  },
  0x0C: {
    "name": "TSB",
    "mode": "Absolute"
  },
  0xBA: {
    "name": "TSX",
    "mode": "Implied"
  },
  0x8A: {
    "name": "TXA",
    "mode": "Implied"
  },
  0x9A: {
    "name": "TXS",
    "mode": "Implied"
  },
  0x98: {
    "name": "TYA",
    "mode": "Implied"
  },
  0x87: {
    "name": "SMB0",
    "mode": "Zero Page"
  },
  0x97: {
    "name": "SMB1",
    "mode": "Zero Page"
  },
  0xA7: {
    "name": "SMB2",
    "mode": "Zero Page"
  },
  0xB7: {
    "name": "SMB3",
    "mode": "Zero Page"
  },
  0xC7: {
    "name": "SMB4",
    "mode": "Zero Page"
  },
  0xD7: {
    "name": "SMB5",
    "mode": "Zero Page"
  },
  0xE7: {
    "name": "SMB6",
    "mode": "Zero Page"
  },
  0xF7: {
    "name": "SMB7",
    "mode": "Zero Page"
  },
  0x07: {
    "name": "RMB0",
    "mode": "Zero Page"
  },
  0x17: {
    "name": "RMB1",
    "mode": "Zero Page"
  },
  0x27: {
    "name": "RMB2",
    "mode": "Zero Page"
  },
  0x37: {
    "name": "RMB3",
    "mode": "Zero Page"
  },
  0x47: {
    "name": "RMB4",
    "mode": "Zero Page"
  },
  0x57: {
    "name": "RMB5",
    "mode": "Zero Page"
  },
  0x67: {
    "name": "RMB6",
    "mode": "Zero Page"
  },
  0x77: {
    "name": "RMB7",
    "mode": "Zero Page"
  },
  0x08: {
    "name": "PHP",
    "mode": "Implied"
  },
  0x28: {
    "name": "PLP",
    "mode": "Implied"
  }
  
}

def GetMnemonicModes(name):
    modes = []
    for k in opcodes:
        if opcodes[k]['name'].upper() == name.upper():
            modes.append(opcodes[k]['mode'])
    return modes

def GetOpcode(name, mode):
    for k in opcodes:
        if opcodes[k]['name'] == name and opcodes[k]['mode'] == mode:
            return k

def IsOpcode(name):
    for k in opcodes:
        if opcodes[k]['name'] == name:
            return True
    return False
