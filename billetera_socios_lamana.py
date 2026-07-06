"""
Billetera Digital para los Socios - Cooperativa de Ahorro y Credito La Mana
Proyecto Integrador (Avance 1) - Logica de Programacion
Autor: Adan Vinicio Baraja Vega
UIDE - Ingenieria en Software - Primer Semestre, Paralelo 1B

Continuidad del caso "Cooperativa de Ahorro y Credito La Mana" desarrollado en
Introduccion a las Redes de Datos (Trabajos Autonomos 1 y 2, Proyecto Integrador
Avance 1): cooperativa del Segmento 4 del sector financiero popular y solidario,
regulada por la SEPS, con oficina matriz en La Mana y una nueva agencia.

Este prototipo representa la billetera digital que un SOCIO usaria para dar
seguimiento a sus propios movimientos en la cooperativa (no reemplaza al Core
Financiero institucional, que es de uso interno del personal).

El programa esta organizado en 3 capas (ver Figura 3 del documento de Avance 1):
 - Capa de Datos y Recursos
 - Capa de Logica de Negocio
 - Capa de Presentacion
"""

from datetime import datetime

# =========================================================
# CAPA DE DATOS Y RECURSOS
# =========================================================

# Conjunto (set) de tipos de movimiento validos en la billetera del socio.
TIPOS_MOVIMIENTO = {"deposito_ahorro", "deposito_plazo_fijo", "retiro", "otros"}

# Lista que funciona como historial de movimientos. Cada movimiento se guarda
# como una tupla inmutable: (fecha, tipo, monto, descripcion)
historial = []

# Diccionario de totales acumulados por tipo de movimiento
totales_tipo = {}

# Tasas de interes pasivas referenciales por plazo, segun el Banco Central del
# Ecuador (BCE), tasas vigentes citadas en el documento de Avance 1. Se usan
# para simular el rendimiento de un deposito a plazo fijo. Clave: plazo
# maximo en dias; valor: tasa efectiva anual (%).
TASAS_PLAZO_FIJO = {
    60: 4.62,    # 30 a 60 dias
    90: 4.94,    # 61 a 90 dias
    120: 5.14,   # 91 a 120 dias
    180: 5.20,   # 121 a 180 dias
    360: 5.67,   # 181 a 360 dias
    36500: 6.93,  # 361 dias y mas
}

SALDO_MINIMO_ALERTA = 0  # si el saldo de ahorro a la vista baja de aqui, se alerta


# =========================================================
# CAPA DE LOGICA DE NEGOCIO
# =========================================================

def validar_monto(texto):
    """Convierte el texto a numero y valida que sea positivo.
    Lanza ValueError si el texto no es numerico o si el monto es <= 0."""
    monto = float(texto)
    if monto <= 0:
        raise ValueError("el monto debe ser mayor a 0")
    return monto


def validar_dias(texto):
    """Convierte el texto a entero y valida que el plazo sea positivo."""
    dias = int(texto)
    if dias <= 0:
        raise ValueError("el plazo en dias debe ser mayor a 0")
    return dias


def tasa_por_plazo(dias):
    """Devuelve la tasa de interes referencial del BCE que corresponde al
    plazo solicitado, recorriendo el diccionario TASAS_PLAZO_FIJO ordenado."""
    for limite in sorted(TASAS_PLAZO_FIJO):
        if dias <= limite:
            return TASAS_PLAZO_FIJO[limite]
    return TASAS_PLAZO_FIJO[max(TASAS_PLAZO_FIJO)]


def registrar_movimiento(tipo, monto, descripcion):
    """Registra un movimiento en el historial y actualiza el acumulado del
    tipo correspondiente."""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    movimiento = (fecha, tipo, monto, descripcion)
    historial.append(movimiento)
    totales_tipo[tipo] = totales_tipo.get(tipo, 0) + monto


def calcular_saldo():
    """Calcula el saldo disponible en ahorro a la vista: depositos de ahorro
    menos retiros. Los depositos a plazo fijo se muestran aparte porque no
    son de disponibilidad inmediata."""
    depositos_vista = sum(m[2] for m in historial if m[1] == "deposito_ahorro")
    retiros = sum(m[2] for m in historial if m[1] == "retiro")
    plazo_fijo = sum(m[2] for m in historial if m[1] == "deposito_plazo_fijo")
    saldo_disponible = depositos_vista - retiros
    return depositos_vista, retiros, plazo_fijo, saldo_disponible


def calcular_resumen_tipos():
    """Devuelve los totales por tipo de movimiento ordenados de mayor a menor."""
    return dict(sorted(totales_tipo.items(), key=lambda item: item[1], reverse=True))


def simular_plazo_fijo(monto, dias):
    """Simula el interes que generaria un deposito a plazo fijo, aplicando la
    tasa referencial del BCE que corresponde al plazo (interes simple,
    practica habitual en depositos a plazo fijo de cooperativas)."""
    tasa = tasa_por_plazo(dias)
    interes = monto * (tasa / 100) * (dias / 360)
    total = monto + interes
    return tasa, interes, total


# =========================================================
# CAPA DE PRESENTACION
# =========================================================

def mostrar_menu():
    print("\n===== BILLETERA DIGITAL - SOCIO COAC LA MANA =====")
    print("1. Registrar deposito (ahorro a la vista)")
    print("2. Registrar retiro")
    print("3. Simular deposito a plazo fijo (tasa BCE)")
    print("4. Consultar saldo y resumen por tipo")
    print("5. Consultar historial de movimientos")
    print("6. Salir")


def pedir_movimiento(tipo, etiqueta):
    """Solicita los datos de un movimiento, validando el monto con un bucle
    while + try/except hasta recibir un valor correcto."""
    while True:
        texto_monto = input(f"Ingrese el monto del {etiqueta}: $")
        try:
            monto = validar_monto(texto_monto)
            break
        except ValueError as error:
            print(f"Entrada invalida ({error}). Intente nuevamente.")
            continue

    if tipo == "retiro":
        _, _, _, saldo_disponible = calcular_saldo()
        if monto > saldo_disponible:
            print(f"Retiro rechazado: el saldo disponible es de ${saldo_disponible:.2f}.")
            return

    descripcion = input("Descripcion (opcional): ").strip() or "Sin descripcion"
    registrar_movimiento(tipo, monto, descripcion)
    print(f"{etiqueta.capitalize()} de ${monto:.2f} registrado correctamente.")


def pedir_simulacion_plazo_fijo():
    """Solicita monto y plazo, valida ambos, y muestra el resultado de la
    simulacion. Permite registrar el deposito simulado como movimiento real."""
    while True:
        texto_monto = input("Monto a depositar a plazo fijo: $")
        try:
            monto = validar_monto(texto_monto)
            break
        except ValueError as error:
            print(f"Entrada invalida ({error}). Intente nuevamente.")

    while True:
        texto_dias = input("Plazo en dias (ej. 90, 180, 360): ")
        try:
            dias = validar_dias(texto_dias)
            break
        except ValueError as error:
            print(f"Entrada invalida ({error}). Intente nuevamente.")

    tasa, interes, total = simular_plazo_fijo(monto, dias)
    print(f"\nTasa referencial aplicada (BCE): {tasa:.2f}% anual")
    print(f"Interes estimado en {dias} dias: ${interes:.2f}")
    print(f"Monto total estimado al vencimiento: ${total:.2f}")

    confirmar = input("¿Desea registrar este deposito a plazo fijo? (s/n): ").strip().lower()
    if confirmar == "s":
        registrar_movimiento("deposito_plazo_fijo", monto,
                              f"Plazo fijo a {dias} dias, tasa {tasa:.2f}%")
        print("Deposito a plazo fijo registrado en el historial.")


def mostrar_saldo():
    depositos_vista, retiros, plazo_fijo, saldo_disponible = calcular_saldo()
    print(f"\nDepositos en ahorro a la vista: ${depositos_vista:.2f}")
    print(f"Retiros totales:                ${retiros:.2f}")
    print(f"Saldo disponible (a la vista):  ${saldo_disponible:.2f}")
    print(f"Depositos a plazo fijo:         ${plazo_fijo:.2f}")
    if saldo_disponible < SALDO_MINIMO_ALERTA:
        print("Alerta: el saldo disponible es negativo, revise sus retiros.")


def mostrar_resumen():
    resumen = calcular_resumen_tipos()
    if not resumen:
        print("\nAun no hay movimientos registrados.")
        return
    print("\n--- Resumen por tipo de movimiento ---")
    for tipo, total in resumen.items():
        print(f"{tipo:20s}: ${total:.2f}")


def mostrar_historial():
    if not historial:
        print("\nNo hay movimientos registrados todavia.")
        return
    print("\n--- Historial de movimientos ---")
    for fecha, tipo, monto, descripcion in historial:
        signo = "-" if tipo == "retiro" else "+"
        print(f"[{fecha}] {tipo:20s} {signo}${monto:.2f}  - {descripcion}")


def ejecutar_billetera():
    """Funcion principal: ejecuta el bucle del menu hasta que el socio
    elija la opcion de salir."""
    print("Bienvenido a la Billetera Digital de los socios de la")
    print("Cooperativa de Ahorro y Credito La Mana.")
    while True:
        mostrar_menu()
        opcion = input("Elija una opcion (1-6): ").strip()

        if opcion == "1":
            pedir_movimiento("deposito_ahorro", "deposito de ahorro")
        elif opcion == "2":
            pedir_movimiento("retiro", "retiro")
        elif opcion == "3":
            pedir_simulacion_plazo_fijo()
        elif opcion == "4":
            mostrar_saldo()
            mostrar_resumen()
        elif opcion == "5":
            mostrar_historial()
        elif opcion == "6":
            print("Gracias por usar su Billetera Digital. Hasta luego.")
            break
        else:
            print("Opcion invalida. Por favor elija un numero del 1 al 6.")
            continue


if __name__ == "__main__":
    ejecutar_billetera()
