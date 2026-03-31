import sys
import os

# --- CONFIGURACIÓN DE ARQUITECTURA ---
DEPTH = 8192
WIDTH = 18

# --- MAPEO DE INSTRUCCIONES ---
OPCODES_MRI = {
    "ISZ": 0b000, "LAC": 0b001, "AND": 0b010, "TAD": 0b011,
    "JMS": 0b100, "DAC": 0b101, "JMP": 0b110
}

MODES = {"I": 0b01, "IA": 0b10, "IB": 0b11}

OPCODES_IOP = {
    "NOP": 0o700000, "HLT": 0o706000, "CLA": 0o701000, "CMA": 0o701400,
    "STA": 0o700400, "CLL": 0o704000, "STL": 0o702000, "RAL": 0o710000,
    "RAR": 0o730000, "RAL2": 0o710200, "RAR2": 0o730200, "RAL3": 0o710210,
    "RAR3": 0o730210, "SKZ": 0o700004, "SKP": 0o700002, "SKN": 0o700001,
    "SZL": 0o700020, "DTA": 0o700100, "DTB": 0o700140, "DFA": 0o700040,
    "DFB": 0o700060, "INA": 0o700120, "INB": 0o700160,
    "IN":  0o760000, "OUT": 0o740000
}

class AssemblerV2:
    def __init__(self):
        self.symbols = {}
        self.instructions = [0] * DEPTH
        self.listing_data = [] # (pc, word, original_line)
        self.pc = 0
        self.max_addr = 0
        self.first_org = None

    def clean_line(self, line):
        return line.split(';')[0].strip()

    def parse_value(self, val_str):
        """Convierte strings (dec, oct, hex, bin o símbolos) a enteros con prefijos obligatorios/opcionales."""
        if val_str in self.symbols:
            return self.symbols[val_str]
        try:
            val_lower = val_str.lower()
            if val_lower.startswith('0x'): return int(val_lower[2:], 16)
            if val_lower.startswith('0o'): return int(val_lower[2:], 8)
            if val_lower.startswith('0b'): return int(val_lower[2:], 2)
            if val_lower.startswith('0d'): return int(val_lower[2:], 10)
            return int(val_str, 10)
        except (ValueError, TypeError):
            return None

    def first_pass(self, lines):
        """Escanea etiquetas y directivas de control."""
        current_pc = 0
        for raw_line in lines:
            line = self.clean_line(raw_line)
            if not line: continue

            parts = line.split()
            
            if parts[0].endswith(':'):
                label = parts[0][:-1]
                self.symbols[label] = current_pc
                parts = parts[1:]
                if not parts: continue

            mnemonic = parts[0].upper()

            if mnemonic == "ORG":
                current_pc = self.parse_value(parts[1])
                if self.first_org is None:
                    self.first_org = current_pc
            elif mnemonic == "SYM":
                if len(parts) > 2:
                    self.symbols[parts[1]] = self.parse_value(parts[2])
            elif mnemonic == "DATA":
                # DATA puede tener múltiples valores separados por comas
                data_str = "".join(parts[1:])
                values = data_str.split(',')
                current_pc += len(values)
            elif mnemonic in OPCODES_MRI or mnemonic in OPCODES_IOP:
                current_pc += 1
            else:
                # Caso de valor directo o instrucción desconocida
                current_pc += 1

    def second_pass(self, lines):
        """Genera el código binario final y datos para el listing."""
        self.pc = 0
        for line_num, raw_line in enumerate(lines, 1):
            line = self.clean_line(raw_line)
            if not line: 
                continue

            parts = line.split()
            orig_parts = list(parts)
            if parts[0].endswith(':'): parts = parts[1:]
            if not parts: continue

            mnemonic = parts[0].upper()

            if mnemonic == "ORG":
                self.pc = self.parse_value(parts[1])
                continue
            if mnemonic == "SYM":
                continue

            if mnemonic == "DATA":
                data_str = "".join(parts[1:])
                values = data_str.split(',')
                for v in values:
                    val = self.parse_value(v)
                    if val is not None:
                        word = val & 0x3FFFF
                        self.instructions[self.pc] = word
                        self.listing_data.append((self.pc, word, raw_line.strip()))
                    self.pc += 1
                continue

            if mnemonic in OPCODES_MRI:
                opcode = OPCODES_MRI[mnemonic]
                mode = 0
                addr_val = 0
                
                args = parts[1:]
                if args and args[0].upper() in MODES:
                    mode = MODES[args[0].upper()]
                    args = args[1:]
                
                if args:
                    addr_val = self.parse_value(args[0])
                    if addr_val is None:
                        print(f"Error L{line_num}: Símbolo '{args[0]}' no definido.")
                        addr_val = 0
                
                word = (opcode << 15) | (mode << 13) | (addr_val & 0x1FFF)
                self.instructions[self.pc] = word
                self.listing_data.append((self.pc, word, raw_line.strip()))
                self.pc += 1

            else:
                word = 0o700000
                is_valid = False
                for p in parts:
                    p_up = p.upper()
                    if p_up in OPCODES_IOP:
                        word |= OPCODES_IOP[p_up]
                        is_valid = True
                
                if not is_valid:
                    raw_val = self.parse_value(mnemonic)
                    if raw_val is not None:
                        word = raw_val
                        is_valid = True
                    else:
                        print(f"Error L{line_num}: Instrucción desconocida '{mnemonic}'")
                        continue
                
                self.instructions[self.pc] = word & 0x3FFFF
                self.listing_data.append((self.pc, word, raw_line.strip()))
                self.pc += 1
            
            if self.pc > self.max_addr: self.max_addr = self.pc

    def _write_bin(self, f):
        """Escribe el contenido de la memoria en formato Bin de Gowin."""
        f.write(f"#File_format=Bin\n#Address_depth={DEPTH}\n#Data_width={WIDTH}\n")
        for word in self.instructions:
            f.write(f"{format(word, '018b')}\n")

    def save(self, base_path, formats=None):
        """Genera solo los formatos solicitados. Si formats es None, genera todos."""
        if formats is None or 'all' in formats:
            formats = ['mi', 'hex', 'bin', 'lst']

        # .mi (Gowin BRAM)
        if 'mi' in formats:
            with open(base_path + ".mi", 'w') as f:
                self._write_bin(f)
            print(f" -> {base_path}.mi generado")
        
        # .hex (Verilog readmemh)
        if 'hex' in formats:
            with open(base_path + ".hex", 'w') as f:
                for i in range(DEPTH):
                    f.write(f"{format(self.instructions[i], '05x')}\n")
            print(f" -> {base_path}.hex generado")
        
        # .bin (Verilog readmemb)
        if 'bin' in formats:
            with open(base_path + ".bin", 'w') as f:
                for i in range(DEPTH):
                    f.write(f"{format(self.instructions[i], '018b')}\n")
            print(f" -> {base_path}.bin generado")

        # .lst (Listing en Octal para Debugging)
        if 'lst' in formats:
            with open(base_path + ".lst", 'w') as f:
                f.write(f"{'ADDR':<8} {'VALUE':<10} {'SOURCE LINE'}\n")
                f.write("-" * 50 + "\n")
                for addr, word, line in self.listing_data:
                    f.write(f"{format(addr, '05o'):<8} {format(word, '06o'):<10} {line}\n")
            print(f" -> {base_path}.lst generado")
        
        # Actualización automática de init_ram.mi si existe la ruta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        init_ram_path = os.path.join(script_dir, "..", "src", "init_ram.mi")
        try:
            if os.path.exists(os.path.dirname(init_ram_path)):
                with open(init_ram_path, 'w') as f:
                    self._write_bin(f)
                print(f" -> {init_ram_path} (Actualizado para Gowin)")
        except Exception as e:
            print(f" ADVERTENCIA: No se pudo escribir en {init_ram_path}: {e}")

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Ensamblador SIC V2 - Generador de binarios para FPGA y Verilog.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 assembler.py programa.sic --all          # Genera todos los archivos
  python3 assembler.py programa.sic --hex --lst    # Genera solo .hex y .lst
  python3 assembler.py programa.sic                # Por defecto genera todos
        """
    )

    parser.add_argument("input", help="Archivo fuente en ensamblador (.sic)")
    parser.add_argument("-o", "--output", help="Nombre base o ruta de los archivos de salida (opcional)")
    parser.add_argument("--mi", action="store_true", help="Genera archivo .mi para Gowin")
    parser.add_argument("--hex", action="store_true", help="Genera archivo .hex para Verilog (readmemh)")
    parser.add_argument("--bin", action="store_true", help="Genera archivo .bin para Verilog (readmemb)")
    parser.add_argument("--lst", action="store_true", help="Genera listado de ensamblado .lst (Octal)")
    parser.add_argument("--all", action="store_true", help="Genera todos los formatos disponibles")

    args = parser.parse_args()

    input_file = args.input
    base_name = args.output if args.output else os.path.splitext(input_file)[0]
    
    # Determinar formatos a generar
    selected_formats = []
    if args.mi: selected_formats.append('mi')
    if args.hex: selected_formats.append('hex')
    if args.bin: selected_formats.append('bin')
    if args.lst: selected_formats.append('lst')
    if args.all or not selected_formats:
        selected_formats = ['mi', 'hex', 'bin', 'lst']

    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {input_file}")
        return

    print(f"Ensamblando {input_file} -> {base_name}.*")
    asm = AssemblerV2()
    asm.first_pass(lines)
    asm.second_pass(lines)
    asm.save(base_name, selected_formats)
    print("¡Listo!")

if __name__ == "__main__":
    main()
