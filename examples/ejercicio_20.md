# Ejercicio 20: Código Automodificable

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que altere su propia lógica en tiempo de ejecución. El objetivo es modificar la dirección de operando de una instrucción `DAC` dentro de un bucle para rellenar un bloque de memoria sin usar registros de índice.

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100` | `RELLENO` | Dato con el que se rellenará |
| `101` | `CONTADOR` | Numero de datos para rellenar en negativo (-7 oct). |
| `150 - 157` | `ZONA_RELLENO` | Destino de los datos generados. |
| `1000` | `INICIO` | Dirección de carga del programa. |

---

## Solución Propuesta (Código Ensamblador)

```sic
    1000    LAC     100; CARGAR RELLENO
    1001    DAC     150; DEPOSITAR RELLENO
    1002    ISZ     1001; YA QUE EL ARGUMENTO (DIRECCIÓN) DE UNA INSTRUCCION SE ENCUENTRA EN SU PARTE LSB INCREMENTAR LA INSTRUCCIÓN RESULTARÁ EN EL INCREMENTO DEL ARGUMENTO.
    1003    ISZ     CONTADOR
    1004    JMP     1000
    1005    HLT
```
