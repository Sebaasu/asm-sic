# Ejercicio 18: Serie de Fibonacci

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que genere los primeros 14 (octal) términos de la sucesión de Fibonacci y los almacene en un arreglo de memoria.

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100` | `FIB_0` | Primer término (0). |
| `101` | `FIB_1` | Segundo término (1). |
| `102 - 113` | `SUCESION` | Resto de los términos generados. |
| `120` | `CONTADOR` | Tamaño del arreglo (-14 octal). |
| `1000` | `INICIO` | Dirección de carga del programa. |

---

## Solución Propuesta (Código Ensamblador)

```sic
; INICIALIZAR REGISTROS INDICES
    1000    CLA
    1001    DTA
    1002    DTB
    1003    INB
; CALCULO DEL SIGUIENTE TERMINO
    1004    LAC IA  100
    1005    TAD IB  100
    1006    INA
    1007    INB
    1008    DAC IB  100; DEPOSITAR SIGUIENTE TERMINO
    1009    ISZ     120
    1010    JMP     1004; LOOP
    1011    HLT
```
