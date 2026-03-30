# Ejercicio 15: Suma de Dos Vectores

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que sume elemento por elemento dos vectores de longitud 10 (octal). Se recomienda el uso del Registro de Índice optimizar el acceso.

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100 - 107` | `VECTOR_1` | Primer conjunto de datos. |
| `120 - 127` | `VECTOR_2` | Segundo conjunto de datos. |
| `140 - 148` | `VECTOR_SUMA` | Resultado de la suma vectorial. |
| `149` | `CTE_1` | Constante 1 para el complemento a 2. |
| `1000` | `INICIO` | Dirección de carga del programa. |
Note que el espacion VECTOR_SUMA tiene un espacio de memoria adicional para posible acarreos
---

## Solución Propuesta (Código Ensamblador)

```sic
; INICIALIZAR REGISTRO INDICE A Y LINK FLAG
    1001    CLA
    1002    DTA
    1003    CLL
; SUMAR DOS TERMINOS Y SUMAR 1 SI LF=1 (ACARREO ANTERIOR)
    1004    LAC IA  100
    1005    SKL
    1006    TAD     149; SUMAR CONSTANTE UNO
    1007    TAD IA  120
    1010    DAC IA  140
    1011    INA
    1012    ISZ     CONTADOR
    1013    JMP     1004; LOOP
; CONSIDERANDO ACARREO FINAL
    1014    CLA
    1015    SKL
    1016    TAD     149; SUMAR CONSTANTE UNO
    1017    DAC IA  140
    1020    HLT
```
