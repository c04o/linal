from typing import Any

# Safe inputs
def safe_input(prompt, funcion, mensaje="El input no es válido") -> Any:
  try:
    return funcion(input(prompt)) 
  except:  
    print(mensaje)