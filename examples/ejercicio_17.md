# Ejercicio 17: Encontrar el Máximo de un Arreglo

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que recorra un arreglo de números positivos y determine cuál es el valor más grande.

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100 - 117` | `ARREGLO` | Datos numéricos (20 octal elementos). |
| `120` | `LONGITUD` | Tamaño del arreglo (-20 octal). |
| `150` | `VALOR_MAXIMO` | El mayor valor encontrado tras el recorrido. |
| `151` | `CTE_1` | Constante 1 para el complemento a 2. |
| `1000` | `INICIO` | Dirección de carga del programa. |

---

## Solución Propuesta (Código Ensamblador)

```sic
; ASUMIENDO IA Y VALOR_MAXIMO INICIALIZADOS EN CERO
; ETAPA 1: CARGAR VALOR Y OBTENER COMPLEMENTO A DOS
    1000    LAC     150
    1001    CMA
    1002    TAD     151
    1003    TAD IA  100; ETAPA 2: COMPARAR
    1004    SKP
    1005    JMP     1010
; ACTUALIZAR DATO
    1006    LAC IA  100
    1007    DAC     150
    ; PREPARAR EL SIGUIENTE BUCLE
    1010    INA
    1011    ISZ     120
    1012    JMP     1000
    1013    HLT
```
