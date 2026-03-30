# GEMINI.md: LLM Technical Guide for SIC Assembler V2.0

This file provides the technical context for Large Language Models (LLMs) to understand, generate, or troubleshoot code for the SIC V2.0 Assembler.

## Architecture Context
- **Word Width:** 18 bits.
- **Memory Depth:** 8192 words (13-bit addressing).
- **Primary Base:** Octal (historical and debugging preference).
- **Target Platform:** FPGA (Gowin, Verilog).

## Instruction Format
### 1. Memory Reference Instructions (MRI)
**Format:** `[Opcode (3 bits)] [Mode (2 bits)] [Address (13 bits)]`
- **Opcodes:**
  - `ISZ`: 000 | `LAC`: 001 | `AND`: 010 | `TAD`: 011
  - `JMS`: 100 | `DAC`: 101 | `JMP`: 110
- **Addressing Modes:**
  - `Direct`: 00 (No prefix)
  - `Indirect (I)`: 01
  - `Indexed A (IA)`: 10
  - `Indexed B (IB)`: 11

### 2. Input/Output & Processor Instructions (IOP)
**Format:** `[Opcode 111 (3 bits)] [Micro-operations (15 bits)]`
- Standard Base: `0o700000` (Octal).
- **Common Micro-ops:**
  - `NOP`: 700000 | `HLT`: 706000 | `CLA`: 701000 | `CMA`: 701400
  - `STA`: 700400 | `CLL`: 704000 | `RAL`: 710000 | `RAR`: 730000
  - `SKZ`: 700004 | `SKP`: 700002 | `SKN`: 700001 | `INA`: 700120
- **Note:** IOP instructions can be combined in a single line (e.g., `CLA CMA`).

## Syntax Rules
- **Line Structure:** `[LABEL:] MNEMONIC [MODE] [ARGUMENT] [; COMMENT]`
- **Labels:** Must end with a colon (e.g., `START:`).
- **Directives:**
  - `ORG <addr>`: Set Program Counter.
  - `DATA <v1>, <v2>...`: Allocate memory and insert data (supports comma-separated values).
  - `SYM <name> <val>`: Define global constant (alias).
- **Numeric Literals:**
  - `0x`: Hex | `0o`: Octal | `0b`: Binary | `0d`: Decimal.
  - **Precedence:** Labels > Literals.

## Implementation Specs (Python)
- **Class:** `AssemblerV2`
- **Parsing:** Two-pass (1. Symbol table, 2. Machine code generation).
- **Output:** Supports `.mi` (Gowin), `.hex` (Verilog), `.bin` (Verilog), `.lst` (Octal Listing).

---
**Guidelines for IA:**
1. When generating code, prefer using `0x` for addresses and `0d` for constant data to avoid confusion.
2. Always use `ORG` to explicitly set memory locations.
3. Combine IOP instructions only when semantically compatible.
