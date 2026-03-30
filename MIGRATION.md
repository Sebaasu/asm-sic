# Migration Guide: Assembler V2.0 (Professional)

This guide provides a roadmap for users of the previous SIC Assembler version to update their source code and workflows to the new **Version 2.0**.

## Breaking Changes

### 1. Data Directives Removed
The `DEC`, `OCT`, and `HEX` directives have been removed to eliminate redundancy and ambiguity.
- **Old Syntax:** `VAL: DEC 10` / `VAL: OCT 12` / `VAL: HEX 0A`
- **New Syntax:** `VAL: DATA 0d10` / `VAL: DATA 0o12` / `VAL: DATA 0x0A`

### 2. Mandatory/Recommended Prefixes
The new parser relies on explicit prefixes for clarity. While plain integers still default to decimal, using prefixes is the new standard:
- `0d`: Decimal (e.g., `0d100`)
- `0x`: Hexadecimal (e.g., `0x64`)
- `0o`: Octal (e.g., `0o144`)
- `0b`: Binary (e.g., `0b1100100`)

## How to Update Your Source Code

### Step-by-Step Conversion
1.  **Search and Replace:** Use a text editor to replace all occurrences of `DEC`, `OCT`, and `HEX` with `DATA`.
2.  **Add Prefixes:** For each value after a `DATA` directive, ensure the base is clear.
    - If you used `OCT 777`, it must become `DATA 0o777`.
    - If you used `HEX 1FFF`, it must become `DATA 0x1FFF`.
3.  **Check Labels:** If your labels were named `DATA`, `DEC`, `OCT`, or `HEX`, you must rename them as they may now conflict with the new directive or be confusing.

## New Features

### Multi-Value DATA
You can now define multiple constants in a single line:
`TABLE: DATA 0d1, 0x02, 0o03, 0b100`

### Listing File (`.lst`)
A new debugging tool is generated. Use the `.lst` file instead of the old `.oct` for debugging. It provides a side-by-side view of your source code and the generated octal machine code.

### Flexible CLI
The command-line interface has changed.
- **Old:** `python ensambladorV2.py prog.sic`
- **New:** `python assembler.py prog.sic --all` (or use flags like `--hex --lst` to save time).

---
**Version 2.0** is designed for high-performance FPGA workflows. If you encounter issues during migration, please consult the `assembler.md` manual.
