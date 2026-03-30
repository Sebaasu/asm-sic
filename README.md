# SIC Assembler V2.0 (Professional)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A robust, two-pass assembler for the **Simplified Instructional Computer (SIC)**, optimized for FPGA development (Gowin BRAM and Verilog).

---

## Resumen (Español)
Este es un ensamblador profesional para el computador educativo SIC. Traduce archivos de texto `.sic` a lenguaje de máquina en diversos formatos compatibles con FPGAs y simuladores Verilog.

**Características principales:**
- Soporta múltiples bases numéricas con prefijos explícitos (`0x`, `0o`, `0b`, `0d`).
- Genera archivos de listado (`.lst`) en octal para una depuración sencilla.
- Salidas directas para Verilog (`readmemh`/`readmemb`) y Gowin BRAM.
- Directiva `DATA` unificada para manejo de memoria.

---

## Quick Start

### Installation
Ensure you have Python 3.x installed. No external dependencies required.
```bash
git clone https://github.com/youruser/asm-sic.git
cd asm-sic
```

### Basic Usage
Assemble your source code with a single command:
```bash
python3 assembler.py program.sic
```
By default, this generates all supported formats (`.mi`, `.hex`, `.bin`, `.lst`).

### Advanced CLI Options
```bash
python3 assembler.py input.sic -o output_name --hex --lst
```
- `-o`: Custom output filename/path.
- `--hex`: Verilog `readmemh` format.
- `--bin`: Verilog `readmemb` format.
- `--mi`: Gowin BRAM format.
- `--lst`: Debugging listing (Octal).

---

## Syntax Overview
```asm
    ORG 0x0        ; Set start address
START:
    CLA            ; Clear accumulator
    TAD VAL        ; Add VAL to AC
    HLT            ; Halt

VAL: DATA 0d42     ; Define data in decimal
```
For more details, see [assembler.md](assembler.md).

---

## Upgrading from V1.0?
If you have code written for the previous version, please read the [MIGRATION.md](MIGRATION.md) guide to understand how to replace `DEC`, `OCT`, and `HEX` with the new `DATA` directive.

## AI & Integration
If you are using an LLM (like ChatGPT, Claude, or Gemini) to generate code for this assembler, provide it with the [GEMINI.md](GEMINI.md) file as context.

## License
Distributed under the **MIT License**. See `LICENSE` for more information.
