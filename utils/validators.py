import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from itertools import cycle

def validar_rut(rut):
    """Valida RUT chileno (Módulo 11)."""
    if not rut:
        return
    
    # Limpieza
    rut = rut.upper().replace("-", "").replace(".", "")
    
    # Validar largo mínimo
    if len(rut) < 2:
        raise ValidationError("El RUT es demasiado corto.")

    aux = rut[:-1]
    dv = rut[-1]

    if not aux.isdigit():
        raise ValidationError("El cuerpo del RUT debe ser numérico.")

    # Algoritmo
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == '10':
        dv_calc = 'K'
    else:
        dv_calc = str(res)

    if dv != dv_calc:
        raise ValidationError("RUT inválido (Dígito verificador incorrecto).")

def validar_positivo(value):
    if value < 0:
        raise ValidationError("El valor no puede ser negativo.")

def validar_cantidad_minima(value):
    if value < 1:
        raise ValidationError("La cantidad debe ser al menos 1.")