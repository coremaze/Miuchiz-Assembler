import opcodes
import random
import struct
import sys

def RemoveComments(lines):
    for i in range(len(lines)):
        if ';' in lines[i]:
            lines[i] = lines[i][:lines[i].find(';')]

def RemoveBlankLines(lines):
    return [x for x in lines if x.strip()]

def StripLines(lines, strip=None):
    for i in range(len(lines)):
        if strip is not None:
            lines[i] = lines[i].strip(strip)
        else:
            lines[i] = lines[i].strip()

def LoadFileLines(fileName):
    with open(fileName, 'r') as f:
        lines = f.read().split('\n')
    return lines

def DoIncludes(lines):
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('.INCLUDE '):
            string = ''
            chars = line[len('.INCLUDE '):]
            chars = [x.strip() for x in chars.split(',')]
            string = ''.join([chr(DecodeNumber(x)) for x in chars])
            includeLines = LoadFileLines(string)
            StripLines(includeLines)
            ReplaceStrings(includeLines)
            RemoveComments(includeLines)
            SplitLabelLines(includeLines)
            StripLines(includeLines)
            includeLines = RemoveBlankLines(includeLines)
            DoIncludes(includeLines)
            lines.pop(i)
            for includeLine in includeLines:
                lines.insert(i, includeLine)
                i += 1
            i -= 1
            
        i += 1

def DecodeNumber(num):
    num = num.strip()
    negative = num.startswith('-')
    if negative:
        num = num[1:]
    if num.startswith('$'):
        num = int(num[1:], base=16)
    elif num.startswith('0b'):
        num = int(num[2:], base=2)
    else:
        num = int(num)
    if negative:
        num = -num
    return num

def ReplaceStrings(lines):
    escaped = False
    inString = False
    for i in range(len(lines)):
        result = ''
        line = lines[i]
        for char in line:
            if not inString and char == '"':
                inString = True
                continue
            if inString:
                if not escaped:
                    if char == '"':
                        result = result[:-1]
                        inString = False
                        continue
                    if char == '\\':
                        escaped = True
                        continue
                else:
                    escaped = False
                    if char == '\\':
                        result += LetterToNum('\\') + ','
                        continue
                    if char == 'n':
                        result += LetterToNum('\n') + ','
                        continue
                result += LetterToNum(char) + ','
                    
            else:
                result += char

        lines[i] = result


def LetterToNum(letter):
    return '$%02X' % ord(letter)

def GetSets(lines, symbols):
    i = 0
    while i < len(lines):
        if lines[i].startswith('.SET '):
            _, symbol, value = lines[i].split(' ')
            if not IsValidLabel(symbol):
                raise Exception(f'Invalid symbol: {symbol}')
            symbols[symbol] = value
            lines.pop(i)
        else:
            i += 1

def IsValidLabel(label):
    if not label:
        return False
    if opcodes.IsOpcode(label.upper()):
        return False
    if ord('0') <= ord(label[0]) <= ord('9'):
        return False
    return label.replace('@','').replace('_', '').isalnum()

def IsValidMacroArgument(arg):
    if len(arg) <= 1: return False
    if not arg.startswith('%'): return False
    arg = arg[1:]
    return IsValidLabel(arg)

def GetMacroInfo(macro, declaration=True):
    if macro.find('(') == -1 or not macro.endswith(')'):
        raise Exception(f"Invalid macro: {macro}")
    macroName = macro[:macro.find('(')]
    if not IsValidLabel(macroName):
        raise Exception(f'Invalid macro name: {macro}')
    argstr = macro[macro.find('(')+1 : -1]
    args = [x.strip() for x in argstr.split(',') if x.strip()]
    if declaration:
        for arg in args:
            if not IsValidMacroArgument(arg):
                raise Exception(f'Invalid macro argument: {arg}')
    return macroName, args
    

    
def GetMacros(lines):
    macros = {}
    i = 0
    current_macro = None
    while i < len(lines):
        if current_macro is not None:
            if lines[i].startswith('.MACRO '):
                raise Exception(f'Embedded macro in {current_macro}')
            if lines[i] == '.ENDMACRO':
                current_macro = None
            else:
                macros[current_macro]['lines'].append(lines[i])
            lines.pop(i)
        elif lines[i].startswith('.MACRO '):
            macro = lines[i][len('.MACRO '):]
            macroName, args = GetMacroInfo(macro)
            macros[macroName] = {'args':args, 'lines':[]}
            current_macro = macroName
            lines.pop(i)
            
        else:
            i += 1
    if current_macro is not None:
        raise Exception(f'Macro not closed: {current_macro}')
    return macros

def IsLabelLine(line):
    return line.endswith(':')
            
def InjectMacros(lines, macros):
    i = 0
    macro_identifier = 0
    while i < len(lines):
        if '(' not in lines[i]:
            pass
        elif not lines[i].endswith(')'):
            pass
        elif opcodes.IsOpcode(lines[i].split(' ')[0]):
            pass
        else:
            name, args = GetMacroInfo(lines[i], declaration=False)
            if name not in macros:
                raise Exception(f'Macro does not exist: {name}')
            macro = macros[name]
            if len(args) != len(macro['args']):
                raise Exception(f'Wrong args for macro: {lines[i]}')
            lines_to_inject = macro['lines'][:]
            for mArg, lArg in sorted(zip(macro['args'], args), key=lambda x: len(x[0]), reverse=True):
                for j in range(len(lines_to_inject)):
                    #replace arguments
                    lines_to_inject[j] = lines_to_inject[j].replace(mArg, lArg)
                    #handle labels
                    if IsLabelLine(lines_to_inject[j]):
                        label = lines_to_inject[j][:-1]
                        if not IsValidLabel(label):
                            raise Exception(f'Invalid label {label}')
                        new_label = f'@@@@@@@@@{random.randint(100000,9999999999999999999999999999)}_@_{macro_identifier}'
                        macro_identifier += 1
                        for x in range(len(lines_to_inject)):
                            lines_to_inject[x] = lines_to_inject[x].replace(label, new_label)
                        
            #Replace macro line with the macro's contents
            lines.pop(i)
            for iLine in lines_to_inject:
                lines.insert(i, iLine)
                i += 1
            i -= 1
                    
        i += 1
        

def GetBankLogicalAddress(bank):
    bank = bank.lstrip('.')
    if bank == 'BBANK': return 0x2000
    if bank == 'PBANK': return 0x4000
    if bank == 'DBANK': return 0x8000
    raise Exception(f'Not a bank: {bank}')

def MakeDefaultPCs(lines):
    i = 0
    while i < len(lines):
        first_word = lines[i].split(' ')[0]
        if first_word in ('.DBANK', '.PBANK', '.DBANK'):
            i += 1
            lines.insert(i, f'.AT {GetBankLogicalAddress(first_word)}')
            i += 1
            lines.insert(i, f'.PC {GetBankLogicalAddress(first_word)}')
        elif first_word == '.LOWRAM':
            i += 1
            lines.insert(i, f'.AT -$1000000')
            i += 1
            lines.insert(i, f'.PC $80')
        elif first_word == '.AT':
            arg = lines[i].split(" ")[1]
            i += 1
            lines.insert(i, f'.PC {arg}')
        i += 1

def MultiSplit(text, splits, keep_separator=False):
    l = [text]
    for split in splits:
        for i in range(len(l)):
            t = l.pop(i)
            j = 0
            t_split = t.split(split)
            if keep_separator:
                for x in range(1, 2*(len(t_split)-1), 2):
                    t_split.insert(x, split)
            for s in t_split:
                l.insert(i + j, s)
                j += 1
    return [x for x in l if x]

def SubstituteSymbols(lines, symbols):
    for i in range(len(lines)):
        split_line = MultiSplit(lines[i], [' ', '\t', '+', '-', '<', '>', '(', ')', '#', ','], keep_separator=True)
        for symbol in symbols:
            split_line = [(x if x != symbol else symbols[symbol]) for x in split_line]
        lines[i] = ''.join(split_line)

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

def GetBankAddress(directive, symbols={}):
    multiplier = GetBankLogicalAddress(directive.split(' ')[0])
    page = directive.split()[1]
    page = DecodeNumber(page)
    address = page * multiplier
    return address

def MakeSegments(lines):
    segments = {}
    seg_addr = None
    bank_type = None
    for line in lines:
        if line.split()[0] in ('.BBANK', '.PBANK', '.DBANK'):
            seg_addr = GetBankAddress(line)
            bank_type = line.split()[0][1:]
            if seg_addr not in segments:
                segments[seg_addr] = []
        elif line.split()[0] == '.LOWRAM':
            seg_addr = -0x1000000
            bank_type = 'LOWRAM'
            if seg_addr not in segments:
                segments[seg_addr] = []
        else:
            if seg_addr is None:
                raise Exception(f'Line is not in any bank: {line}')
            segments[seg_addr].append( (bank_type, line))
    return segments

def MakeSegmentOffsets(segments, symbols):
    offset_segments = {}
    for segment in segments:
        offset_segments[segment] = []
        PC = None
        addr = None
        for entry in segments[segment]:
            bank_type, line = entry
            if line.split(' ')[0] == '.AT':
                addr = DecodeNumber(line.split(' ')[1])
            elif line.split(' ')[0] == '.PC':
                PC = DecodeNumber(line.split(' ')[1])
            elif IsLabelLine(line):
                label = line[:-1]
                if not IsValidLabel(label):
                    raise Exception(f'Invalid label: {label}')
                symbols[label] = str(PC)
            else:
                length = GetInstructionLength(line)
                offset_segments[segment].append( [bank_type, addr, PC, line] )
                addr += length
                PC += length
    return offset_segments

def SubstituteSymbols2(offset_segments, symbols):
    for segment in offset_segments:
        for inst in offset_segments[segment]:
            bank_type, addr, PC, line = inst
            lines = [line]
            SubstituteSymbols(lines, symbols)
            line = lines[0]
            inst[3] = line

def EvaluateNumber(sym):
    sym = sym.replace('-', '+-')
    adds = sym.split('+')
    s = 0
    little = sym.startswith('<')
    big = sym.startswith('>')
    for a in adds:
        a = a.lstrip('<').lstrip('>')
        if a.startswith('$'):
            a = int(a[1:], base=16)
        else:
            a = int(a)

        s += a
    if little:
        s &= 0xFF
    if big:
        s >>= 8
    return s

def AssembleInstruction(instruction, logical_location):
    b_instruction = b''
    if instruction.split(' ')[0] in ('.DB', '.DW', '.DD', '.DQ'):
        for string, length, fmt in (('.DB ', 1, '<B'), ('.DW ', 2, '<H'), ('.DD ', 4, '<I'), ('.DQ ', 8, '<Q') ):
            if instruction.startswith(string):
                args = instruction.lstrip(string).split(',')
                for arg in args:
                    arg = arg.strip()
                    num = EvaluateNumber(arg)
                    b_instruction += struct.pack(fmt, num)
        return b_instruction
    
    mode = GetInstructionAddressingMode(instruction)
    mnemonic = instruction.split(' ')[0]
    args = [x.strip() for x in instruction.split(' ')[1:] if x.strip()]
    args = ' '.join(args)
    opcode = opcodes.GetOpcode(mnemonic, mode)
    b_instruction += struct.pack('<B', opcode)
    if mode == 'Relative':
        dest = EvaluateNumber(args)
        offset = dest - logical_location - 2
        b_instruction += struct.pack('<b', offset)
    elif mode in ('Implied', 'Accumulator'):
        pass
    elif mode == 'Immediate':
        literal = args.lstrip('#')
        literal = EvaluateNumber(literal)
        b_instruction += struct.pack('<B', literal)
    elif mode in ('Zero Page', 'Zero Page,X', '(Zero Page),Y', '(Zero Page)'):
        zp_ptr = args
        zp_ptr = MultiSplit(zp_ptr, ['(', ')', ','])[0]
        zp_ptr = EvaluateNumber(zp_ptr)
        b_instruction += struct.pack('<B', zp_ptr)
    elif mode in ('Absolute,X', 'Absolute,Y', 'Absolute'):
        absolute = args
        absolute = MultiSplit(absolute, [','])[0]
        absolute = EvaluateNumber(absolute)
        b_instruction += struct.pack('<H', absolute)
    elif mode == 'Bit, Relative':
        args = MultiSplit(args, [',', ' '])[0]
        bit = args[0].strip()
        bit = EvaluateNumber(bit)
        b_instruction += struct.pack('<B', bit)
        dest = args[1].strip()
        dest = EvaluateNumber(dest)
        offset = dest - logical_location - 3
        b_instruction += struct.pack('<b', offset)
        
    return b_instruction

def Assemble(offset_segments):
    output = bytearray(0x200000)
    for segment in offset_segments:
        file_location = segment
        for inst in offset_segments[segment]:
            bank_type, addr, PC, text = inst
            if bank_type == 'LOWRAM':
                continue
            offset_from_file_location = addr - GetBankLogicalAddress(bank_type)
            opcodes = AssembleInstruction(text, PC)
            output[file_location+offset_from_file_location : file_location+offset_from_file_location + len(opcodes)] = opcodes
    return output


def SplitLabelLines(lines):
    i = 0
    while i < len(lines):
        if ':' in lines[i]:
            line = lines[i]
            loc = line.find(':')
            lines[i] = line[:loc+1].strip()
            i += 1
            lines.insert(i, line[loc+1:].strip())
        i += 1

def main():
    if len(sys.argv) == 3:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    elif len(sys.argv) == 2:
        inputFile = sys.argv[1]
        outputFile = 'Flash.dat'
    else:
        print('Usage: miuchiz_assembler.py <input file> <output file>')
        return
    
    #Load file, its includes, and clean up the lines
    lines = LoadFileLines(inputFile)
    StripLines(lines)
    ReplaceStrings(lines)
    RemoveComments(lines)
    SplitLabelLines(lines)
    StripLines(lines)
    lines = RemoveBlankLines(lines)
    DoIncludes(lines)

    #Get .SETs
    symbols = {}
    GetSets(lines, symbols)

    #Inject macros
    macros = GetMacros(lines)
    InjectMacros(lines, macros)

    #Give each bank and .AT a default program counter
    MakeDefaultPCs(lines)

    SubstituteSymbols(lines, symbols)
    segments = MakeSegments(lines)
    offset_segments = MakeSegmentOffsets(segments, symbols)

    #Substitute symbols again now that we know label positions
    SubstituteSymbols2(offset_segments, symbols)

    output = Assemble(offset_segments)
    with open(outputFile, 'wb') as f:
        f.write(output)

if __name__ == '__main__':
    main()
