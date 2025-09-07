from typing import Any

# Safe inputs


def safe_input(prompt, funcion, mensaje="El input no es válido") -> Any:
    while True:
        try:
            return funcion(input(prompt))
        except:
            print(mensaje)


def pretty_number(num, decimals=4):
    # Devuelve un número formateado de manera legible:
    # - Enteros con separador de miles.
    # - Flotantes con separador de miles y decimales limitados.
    # - Notación científica para números muy grandes o muy pequeños.
    # Si es int, usa separadores de miles
    if isinstance(num, int):
        return f"{num:,}"

    # Si es float, decidir si usar notación científica
    if isinstance(num, float):
        if abs(num) != 0 and (abs(num) < 1e-4 or abs(num) >= 1e6):
            return f"{num:.{decimals}e}"
        else:
            return f"{num:,.{decimals}f}".rstrip("0").rstrip(".")

    # Por si acaso le pasan algo raro
    return str(num)


# Añadir tolerancia para comparaciones de punto flotante
TOLERANCIA = 1e-10


def es_cero(valor: float) -> bool:
    return abs(valor) < TOLERANCIA


def es_uno(valor: float) -> bool:
    return abs(valor - 1) < TOLERANCIA


# Matrices de cambio, de numeros a numeros en potencia (supercript) y numeros de subscript (Para en lugar de imprimir X2, poder imprimir X₂)
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# Esta funcion convierte todos los numeros del string a subscript


def to_subscript(string: str):
    return string.translate(SUB)

# Esta funcion convierte todos los numeros del string a superscript


def to_superscript(string: str):
    return string.translate(SUP)

# Mejorar la función de impresión de términos
# Para escribir un termino sin variable el argumento variable debe ser 0


def termino_a_string(coeficiente: float, variable: int | None, es_primer_termino: bool = False):
    nombre_variable = ""
    if variable != None:
        if variable <= 0:
            raise Exception(
                "No se puede imprimir un termio con un numero de variable negativa")
        nombre_variable = to_subscript(f"X{variable}")

    if es_cero(coeficiente):
        return ""

    signo = "" if es_primer_termino else " "
    if not es_primer_termino:
        signo = "+ " if coeficiente > 0 else "- "

    coeficiente_abs = abs(coeficiente)
    if es_uno(coeficiente_abs):
        return f"{signo}{nombre_variable}"
    else:
        return f"{signo}{pretty_number(coeficiente_abs)}{nombre_variable}"
