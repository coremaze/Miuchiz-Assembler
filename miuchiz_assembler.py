import opcodes
import struct

NEST_DIRECTIVES = ('BBANK', 'PBANK', 'DBANK', 'LOWRAM', 'ORG')
FLASH_SIZE = 0x200000

def LoadText(fileName):
    with open(fileName, 'r') as f:
        return MoveBrackets(f.read())

def UncommentText(text):
    if ';' in text:
        return text[:text.find(';')]
    else:
        return text

def SectionName(text):
    for s in NEST_DIRECTIVES:
        if text.lstrip().startswith('.'+s):
            return s
    return ''

def GetBlock(d, start):
    depth = 0
    sectionLines = []
    started = False
    found_first = False
    for k in d:
        if k == start:
            started = True
        if not started:
            continue
        line = d[k]
        if '{' in line:
            found_first = True
            depth += 1
        if '}' in line:
            depth -= 1
        if found_first:
            if depth == 0:
                end = k
                return (start, end)
    raise Exception(f"Block not closed.")
        
def SubDict(d, start, end):
    new_dict = {}
    started = False
    for k in d:
        if k == start:
            started = True
        if not started:
            continue
        new_dict[k] = d[k]
        if k == end:
            return new_dict

def RemoveDictPart(d, start, end):
    keys = [x for x in d]
    started = False
    excluded_keys = []
    for k in keys:
        if k == start:
            started = True
        if not started:
            continue
        del d[k]
        excluded_keys.append(k)
        if k == end:
            return excluded_keys

def RemoveBrackets(d):
    keys = [x for x in d]
    for k in keys:
        if type(d[k]) != str:
            continue
        d[k] = d[k].strip('}')
        d[k] = d[k].strip('{')
        d[k] = d[k].strip()
        if d[k] == '':
            del d[k]
    keys = [x for x in d]
    for k in keys:
        if type(k) != str:
            continue
        key2 = k.strip('}').strip('{').strip()
        if k != key2:
            d[key2] = d[k]
            del d[k]

def RemoveComments(d):
    keys = [x for x in d]
    for k in keys:
        if type(d[k]) != str:
            continue
        if ';' not in d[k]:
            continue
        d[k] = d[k][:d[k].find(';')]
        d[k] = d[k].strip()
        if d[k] == '':
            del d[k]
    keys = [x for x in d]
    for k in keys:
        if type(k) != str:
            continue
        if ';' not in k:
            continue
        key2 = k[:k.find(';')]
        if k != key2:
            d[key2] = d[k]
            del d[k]

def MoveBrackets(text):
    return text.replace('{', '\n{\n').replace('}', '\n}\n')
            

def ParseIncludes(lines):
    i = 0
    while i < len(lines):
        line = lines[i]
        line = line.strip()
        if line.startswith('.INCLUDE '):
            line = line.lstrip('.INCLUDE ')
            line = line.strip('"')
            included_text = LoadText(line)
            included_lines = included_text.split('\n')
            lines = lines[:i] + included_lines + lines[i+1:]
        i += 1
    return lines
   
def ParseBlocks(d):
    excluded_keys = []
    for k in d:
        d[k] = d[k].strip()
        if d[k] == '':
            excluded_keys.append(k)
            continue
    for key in excluded_keys:
        del d[key]
    keys = [x for x in d]
    
    for k in keys:
        if k in excluded_keys:
            continue
        line = d[k]
        sectionName = SectionName(line)
        if sectionName:
            start, end = GetBlock(d, k)
            section_dict = SubDict(d, start, end)
            full_section_name = section_dict[list(section_dict)[0]]
            del section_dict[list(section_dict)[0]]
            excluded_keys.extend(RemoveDictPart(d, start, end))
            ParseBlocks(section_dict)
            if full_section_name in d:
                d[full_section_name] = {**d[full_section_name], **section_dict}
            else:
                d[full_section_name] = section_dict      
    RemoveComments(d)
    RemoveBrackets(d)
 
def ParseSymbols(d):
    symbols = {}
    keys = list(d)
    for k in keys:
        if type(d[k]) == str:
            line = d[k]
            if line.startswith('.SET '):
                _, symbol, expr = line.split()
                symbols[symbol] = expr
                del d[k]
        elif type(d[k]) == dict:
            sub_symbols = ParseSymbols(d[k])
            symbols = {**symbols, **sub_symbols}
    return symbols

def EvaluateSymbol(sym, symbols):
    raw_symbol = sym.lstrip('<').lstrip('>').rstrip(',X').rstrip(',Y').lstrip('(').rstrip(')').rstrip(',Y')
    raw_symbol = raw_symbol.split('+')[0]
    raw_symbol = raw_symbol.split('-')[0]
    if raw_symbol not in symbols:
        raise Exception(f"Symbol {sym} does not exist.")
    return EvaluateNumber(sym.replace(sym, symbols[raw_symbol]), symbols)

def EvaluateNumber(sym, symbols):
    sym = sym.replace('-', '+-')
    adds = sym.split('+')
    s = 0
    little = sym.startswith('<')
    big = sym.startswith('>')
    for a in adds:
        a = a.lstrip('<').lstrip('>')
        try:
            if a.startswith('$'):
                a = int(a[1:], base=16)
            else:
                a = int(a)
        except:
            a = EvaluateSymbol(a, symbols)
        s += a
    if little:
        s &= 0xFF
    if big:
        s >>= 8
    return s

def AssembleInstruction(instruction, logical_location, symbols):
    mode = GetInstructionAddressingMode(instruction)
    mnemonic = instruction.split(' ')[0]
    args = [x.strip() for x in instruction.split(' ')[1:] if x.strip()]
    args = ' '.join(args)
    opcode = opcodes.GetOpcode(mnemonic, mode)
    b_instruction = b''
    b_instruction += struct.pack('<B', opcode)
    if mode == 'Relative':
        dest = EvaluateNumber(args, symbols)
        offset = dest - logical_location - 2
        b_instruction += struct.pack('<b', offset)
    elif mode in ('Implied', 'Accumulator'):
        pass
    elif mode == 'Immediate':
        literal = args.lstrip('#')
        literal = EvaluateNumber(literal, symbols)
        b_instruction += struct.pack('<B', literal)
    elif mode in ('Zero Page', 'Zero Page,X', '(Zero Page),Y', '(Zero Page)'):
        zp_ptr = args
        zp_ptr = EvaluateNumber(zp_ptr, symbols)
        b_instruction += struct.pack('<B', zp_ptr)
    elif mode in ('Absolute,X', 'Absolute,Y', 'Absolute'):
        absolute = args
        absolute = EvaluateNumber(absolute, symbols)
        b_instruction += struct.pack('<H', absolute)
    elif mode == 'Bit, Relative':
        args = args.split(',')
        bit = args[0].strip()
        bit = EvaluateNumber(bit, symbols)
        b_instruction += struct.pack('<B', bit)
        dest = args[1].strip()
        dest = EvaluateNumber(dest, symbols)
        offset = dest - logical_location - 3
        b_instruction += struct.pack('<b', offset)
    return b_instruction

def GetInstructionAddressingMode(text):
    mnemonic = text.split(' ')[0]
    args = text.split(' ')[1:]
    args = [x.strip() for x in args if x.strip()]
    RELATIVE = ['BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BRA', 'BVC', 'BVS']
    mode = ''

    if mnemonic in RELATIVE:
        mode = 'Relative'
    elif len(args) == 0:
        mode = 'Implied'
    elif len(args) == 1:
        if args[0].strip() == 'A':
            mode = 'Accumulator'
        elif args[0].startswith('#'):
            mode = 'Immediate'
        elif args[0].startswith('<'):
            mode = 'Zero Page'
        elif args[0].startswith('<') and args[0].endswith(',X'):
            mode = 'Zero Page,X'
        elif args[0].startswith('(') and args[0].endswith(',X)'):
            mode = '(Zero Page,X)'
        elif args[0].startswith('(') and args[0].endswith('),Y'):
            mode = '(Zero Page),Y'
        elif args[0].startswith('(') and args[0].endswith(')'):
            mode = '(Zero Page)'
        elif args[0].endswith(',X'):
            mode = 'Absolute,X'
        elif args[0].endswith(',Y'):
            mode = 'Absolute,Y'
        else:
            mode = 'Absolute'
    elif len(args) == 2:
        if args[1].strip() == 'A':
            mode = 'Accumulator'
        elif args[0].endswith(','):
            mode = 'Bit, Relative'

    
    if mode == '' or mode not in opcodes.GetMnemonicModes(mnemonic):
        raise Exception(f'Cannot Assemble {text}')
    
    return mode

    
    

def GetInstructionLength(text):
    for string, length in (('.DB ', 1), ('.DW ', 2), ('.DD ', 4), ('.DQ ', 8) ):
        if text.startswith(string):
            args = text.lstrip(string).split(',')
            if not args:
                return 0
            return len(args) * length
    
    mode = GetInstructionAddressingMode(text)
    if mode in ('Implied', 'Accumulator'):
        return 1
    if mode in ('Zero Page', 'Zero Page,X', '(Zero Page,X)', '(Zero Page),Y', '(Zero Page)', 'Relative', 'Immediate'):
        return 2
    if mode in ('Absolute', 'Absolute,X', 'Absolute,Y', 'Bit, Relative'):
        return 3
    else:
        return 0 #raise Exception(f'Cannot identify length for {text}, {mode}')

def GetBankAddress(directive):
    multiplier = GetBankLogicalAddress(directive)
    page = directive.split()[1]
    page = EvaluateNumber(page, symbols={})
    address = page * multiplier
    return address

def GetBankLogicalAddress(directive):
    if directive.startswith('.BBANK '):
        return 0x2000
    elif directive.startswith('.PBANK '):
        return 0x4000
    elif directive.startswith('.DBANK '):
        return 0x8000
    else:
        return 0x0000
    
def FindFileOffsets(d, symbols, base_offset=0, logical_offset=0, directive=''):
    length_dict = {}
    current_offset = base_offset
    for k in d:
        element = d[k]
        if type(element) == str:
            if len(element.split(':')) > 1:
                label, element = element.split(':')[0].strip(), ''.join(element.split(':')[1:]).strip()
                symbols[label] = str(logical_offset)
            length_dict[current_offset, logical_offset] = element
            if not element.strip():
                continue
            current_offset += GetInstructionLength(element)
            logical_offset += GetInstructionLength(element)
        else:
            if k.split()[0] in ('.BBANK', '.PBANK', '.DBANK'):
                new_dict, _ = FindFileOffsets(element, symbols, GetBankAddress(k), GetBankLogicalAddress(k), k.split()[0])
            elif k == '.LOWRAM':
                new_dict, _ = FindFileOffsets(element, symbols, -0x10000, 0x80, k)
            elif k.split()[0] == '.ORG':
                new_logical_offset = EvaluateNumber(k.split()[1], symbols)
                new_dict, current_offset = FindFileOffsets(element, symbols, current_offset, new_logical_offset, '')
            else:
                new_dict, current_offset = FindFileOffsets(element, symbols, current_offset, logical_offset, '')
            length_dict = {**length_dict, **new_dict}
    return length_dict, current_offset
    
def ReplaceSymbols(d, symbols):
    for k in d:
        for symbol in symbols:
            if symbol in d[k].replace('<', '').replace('>', '').replace('#', '').replace('$', '').split():
                d[k] = d[k].replace(symbol, symbols[symbol])

def Assemble(d, symbols):
    output = bytearray(0x200000)
    for k in d:
        physical_address, logical_address = k
        if physical_address < 0:
            continue
        if d[k].startswith('.'):
            for string, length, fmt in (('.DB ', 1, '<B'), ('.DW ', 2, '<H'), ('.DD ', 4, '<I'), ('.DQ ', 8, '<Q') ):
                if d[k].startswith(string):
                    args = d[k].lstrip(string).split(',')
                    opcodes = b''
                    for arg in args:
                        arg = arg.strip()
                        num = EvaluateNumber(arg, symbols)
                        opcodes += struct.pack(fmt, num)
        else:         
            opcodes = AssembleInstruction(d[k],logical_address, symbols)
                
        l = len(opcodes)
        output[physical_address : physical_address + l] = opcodes
            
    return output

text = LoadText('test.asm')
lines = text.split('\n')
lines = ParseIncludes(lines)
sections = dict([(str(i), line) for i, line in enumerate(lines)])
ParseBlocks(sections)
symbols = ParseSymbols(sections)
fileOffsets, _ = FindFileOffsets(sections, symbols)
ReplaceSymbols(fileOffsets, symbols)

output = Assemble(fileOffsets, symbols)
#print(fileOffsets)

with open('output.dat', 'wb') as f:
    f.write(output)
