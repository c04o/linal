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