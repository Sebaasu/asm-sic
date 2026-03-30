# Manual del Ensamblador SIC (Versión 2.0 - Profesional)

Este documento describe el funcionamiento y la sintaxis del **Ensamblador V2** para el computador SIC. Esta versión profesional introduce soporte para múltiples formatos de salida, control de prefijos numéricos y una interfaz de línea de comandos mejorada.

## 1. Estructura de una Línea de Código
Cada línea en un archivo `.sic` sigue el siguiente formato:
`[ETIQUETA:] MNEMÓNICO [MODO] [ARGUMENTO] [; Comentario]`

- **ETIQUETA:** Opcional. Debe terminar en `:` (ej. `INICIO:`).
- **MNEMÓNICO:** Instrucción MRI (ej. `LAC`), IOP (ej. `CLA`) o Directiva (ej. `DATA`).
- **MODO:** Solo para MRI (`I`, `IA`, `IB`).
- **ARGUMENTO:** Dirección numérica (con prefijo) o nombre de una etiqueta.
- **COMENTARIO:** Todo lo que sigue a un `;` es ignorado.

---

## 2. Directivas y Literales

### `DATA <valor1>, <valor2>, ...`
Inserta datos constantes directamente en la memoria. Soporta múltiples valores separados por comas.
```asm
VALOR: DATA 0d125    ; Guarda 125 en decimal
MASK:  DATA 0o777    ; Guarda 777 en octal
HEXA:  DATA 0x3FF    ; Guarda 1023 en hexadecimal
LISTA: DATA 1, 2, 3   ; Tres palabras consecutivas
```

### Prefijos Numéricos
El ensamblador identifica la base mediante los siguientes prefijos (aplicable en `DATA`, `ORG`, `SYM` y argumentos de instrucciones):
- `0d`: Decimal (ej. `0d10`)
- `0x`: Hexadecimal (ej. `0x1A`)
- `0o`: Octal (ej. `0o77`)
- `0b`: Binario (ej. `0b1010`)
- *(Sin prefijo)*: Se interpreta como decimal por defecto.

### `ORG <dirección>`
Establece la dirección de memoria para las siguientes instrucciones.
```asm
ORG 0x100    ; El código siguiente empezará en la dirección 256
```

### `SYM <nombre> <valor>`
Define una constante global (alias). No ocupa espacio en memoria.
```asm
SYM LIMITE 0d50
LAC LIMITE
```

---

## 3. Modos de Direccionamiento (MRI)

| Sintaxis | Modo | Descripción |
|:---|:---|:---|
| `LAC 0d100` | Directo | Accede a la dirección 100. |
| `LAC I 0o100` | Indirecto | Accede a la dirección apuntada por la dirección 64. |
| `LAC IA 0x10` | Indexado A | Dirección efectiva = 16 + Registro IA. |
| `LAC IB 0b10` | Indexado B | Dirección efectiva = 2 + Registro IB. |

---

## 4. Uso del Ensamblador (CLI)

El script se ejecuta mediante Python y ofrece flexibilidad en la generación de archivos:

```bash
python3 assembler.py <archivo.sic> [opciones]
```

### Opciones Disponibles:
- `-o`, `--output <nombre>`: Especifica el nombre base o ruta de los archivos de salida.
- `--hex`: Genera archivo `.hex` (hexadecimal puro para Verilog `readmemh`).
- `--bin`: Genera archivo `.bin` (binario puro para Verilog `readmemb`).
- `--mi`: Genera archivo `.mi` (formato BRAM para Gowin).
- `--lst`: Genera el listado de ensamblado `.lst` (Octal para depuración).
- `--all`: Genera todos los formatos anteriores.
- `--help`: Muestra la ayuda y ejemplos de uso.

### Ejemplos:
1. **Generación completa (default):**
   `python3 assembler.py programa.sic`
2. **Solo para simulación en Verilog:**
   `python3 assembler.py programa.sic --hex --bin`
3. **Especificando salida y listing:**
   `python3 assembler.py programa.sic -o builds/firmware --lst`

---

## 5. Archivos Generados
1.  **`.mi`**: Archivo binario con cabeceras para el IP Core de Gowin.
2.  **`.hex`**: Valores hexadecimales de 18 bits (5 dígitos hex) por línea.
3.  **`.bin`**: Valores binarios de 18 bits por línea.
4.  **`.lst`**: El **Listing**. Es la herramienta principal de debugging. Muestra:
    *   Dirección de memoria (Octal 5 dígitos).
    *   Contenido de la instrucción (Octal 6 dígitos).
    *   Línea original del código fuente.
