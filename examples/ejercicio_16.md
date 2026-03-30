# Ejercicio 16: Conteo de Bits Encendidos (Hamming Weight)

## Enunciado
Diseñar un programa en ensamblador para el procesador **SIC de 18 bits** que cuente cuántos bits están en "1" dentro de una palabra de 18 bits. Se debe rotar el acumulador bit a bit y evaluar el bit de enlace (Link).

## Mapa de Memoria
| Dirección (Octal) | Contenido / Etiqueta | Descripción |
| :--- | :--- | :--- |
| `100` | `DATO` | Palabra a evaluar. |
| `101` | `CUENTA_BITS` | Cantidad de bits en alto encontrados. |
| `102` | `ITERACIONES` | Constante -22 (octal) para los 18 bits. |
| `1000` | `INICIO` | Dirección de carga del programa. |

---

## Solución Propuesta (Código Ensamblador)

```sic
    1000    LAC     100; CARGAR DATO
    1001    RAL; ROTAR IZQUIERDA, DERECHA TAMBIEN SIRVE
    1002    SZL; EVALUAR LINK FLAG
    1003    ISZ     101
    1004    ISZ     102; INCREMENTAR ITERACIONES
    1005    JMP     1001, LOOP
    1006    HLT
```
