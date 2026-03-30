# Ejercicio 19: Buffer Circular Dinámico

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que gestione un buffer circular de 8 posiciones. El programa debe insertar un dato y actualizar el puntero de escritura de forma cíclica (0-7).

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100 - 107` | `BUFFER` | Espacio circular de datos. |
| `110` | `PUNTERO_ESCR` | Índice de la siguiente posición a escribir. |
| `111` | `DATO_ENTRADA` | Nuevo valor a insertar en el buffer. |
| `112` | `MASCARA_CIRC` | Valor -7 para aritmética modular. |
| `1000` | `INICIO` | Dirección de carga del programa. |

---

## Solución Propuesta (Código Ensamblador)

```sic
    1000    LAC     110; CARGAR PUNTERO EN REGISTRO INDICE A
    1001    DTA
    1002    LAC     111; CARGAR DATO DE ENTRADA
    1003    DAC IA  100; GUARDAR DONDE INDICA EL PUNTERO
    1004    ISZ     110; INCREMENTAR EL PUNTERO
; SI EL PUNTERO ES MAYOR QUE 7 RESETEAR A 0
    1005    LAC     110
    1006    TAD     112; AC <= PUNTERO - 7
    1007    SKP
    1010    JMP     1014
    1012    CLA
    1013    DAC     110
    1014    HLT
```
