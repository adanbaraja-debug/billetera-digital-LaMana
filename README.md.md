# Billetera Digital para los Socios - Cooperativa La Maná

**Nombre del proyecto:** Billetera Digital para los Socios de la Cooperativa de Ahorro y Crédito La Maná
**Integrantes:** Adán Vinicio Baraja Vega
**Curso:** Lógica de Programación - 1er Semestre, Paralelo 1B
**Docente:** Ing. Darío Sebastián Cabezas Erazo
**Universidad:** Universidad Internacional del Ecuador (UIDE)
**Fecha:** 30 de junio de 2026

## Objetivo del sistema

Diseñar y programar una billetera digital de consola que permita a un socio de la
cooperativa registrar depósitos y retiros, simular el rendimiento de un depósito a
plazo fijo con tasas de interés referenciales reales del Banco Central del Ecuador
(BCE), y consultar su saldo, resumen e historial de movimientos.

## Caso de estudio

Este proyecto da continuidad a la Cooperativa de Ahorro y Crédito La Maná, desarrollada
por el mismo estudiante en Introducción a las Redes de Datos (Segmento 4 SEPS, oficina
matriz + agencia). Aquí se aborda la misma organización desde Lógica de Programación,
construyendo una herramienta de software para sus socios, siguiendo la orientación del
docente de aplicar el diseño aprendido en los Aprendizajes Autónomos 1 y 2 a un problema
real (similar a un cajero de banco: depositar, retirar, consultar saldo).

## Descripción del problema

Un socio de una cooperativa pequeña (Segmento 4) normalmente solo conoce su saldo
acudiendo a caja o llamando a la cooperativa, y no tiene una forma rápida de comparar
cuánto ganaría dejando su dinero en ahorro a la vista frente a un depósito a plazo fijo.
Esta billetera digital cierra esa brecha.

## Descripción de funcionalidades

1. **Registrar depósito de ahorro**: monto y descripción, con validación de entrada.
2. **Registrar retiro**: valida que no supere el saldo disponible.
3. **Simular depósito a plazo fijo**: pide monto y plazo en días, aplica la tasa pasiva
   referencial del BCE correspondiente (ver documento del proyecto) y calcula el interés
   simple y el monto total estimado; permite registrar la simulación en el historial.
4. **Consultar saldo y resumen por tipo**: depósitos a la vista, retiros, plazo fijo y
   saldo disponible.
5. **Consultar historial de movimientos**: lista todas las operaciones de la sesión.
6. **Salir**.

## Arquitectura

Código organizado en 3 capas (ver `diagramas_lamana/03_diagrama_arquitectura.png`):

- **Capa de Presentación**: menú de consola y funciones de despliegue.
- **Capa de Lógica de Negocio**: validación, cálculos de saldo/resumen y simulación
  de plazo fijo con tasas del BCE.
- **Capa de Datos y Recursos**: estructuras en memoria (set, list de tuplas, dict).

## Contenidos del curso aplicados

- Variables y tipos de datos
- Estructuras de datos: listas, tuplas, diccionarios y conjuntos
- Bucles `while`/`for`
- Funciones y modularización del código
- Estructuras condicionales `if/elif/else`
- Manejo de errores con `try/except`
- Cálculo financiero básico (interés simple) aplicado a datos reales del BCE

## Estructura de archivos

```
├── billetera_socios_lamana.py                       # Código fuente del prototipo
├── README_LaMana.md                                 # Este archivo
├── diagramas_lamana/
│   ├── 01_diagrama_flujo.png
│   ├── 02_diagrama_casos_uso.png
│   └── 03_diagrama_arquitectura.png
└── Proyecto_Integrador_Final_BarajaVega_LaMana.docx  # Documento del proyecto
```

## Cómo ejecutar

```
python3 billetera_socios_lamana.py
```

> Nota: el programa solicita datos por teclado (`input()`), por lo que debe ejecutarse
> en una terminal interactiva (en VS Code: Terminal → New Terminal), no en el panel de
> salida de Code Runner.

## Fuentes de los datos financieros

- Banco Central del Ecuador (BCE) — tasas de interés activas y pasivas referenciales.
- Superintendencia de Economía Popular y Solidaria (SEPS) — segmentación de cooperativas.
- Primicias.ec — análisis del comportamiento de las cooperativas del Segmento 4.

Las referencias completas en formato APA están en el documento Word del proyecto.
