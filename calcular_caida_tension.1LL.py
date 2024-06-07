
def calcular_caida_tension(I, L, material, A):
    # Resistividades en ohmios-metro (Ω·m)
    resistividades = {
        'cobre': 1.68e-8,
        'aluminio': 2.65e-8,
        'alucobre': 3.2e-8
    }
    
    # Obtener la resistividad del material
    rho = resistividades.get(material.lower())
    
    if rho is None:
        raise ValueError(f"Material no reconocido: {material}")
    
    # Calcular la resistencia del cable
    R = rho * (L / A)
    # Calcular la caída de tensión
    delta_V = I * R
    return delta_V

# Ejemplo de uso
corriente = int (input ("Ingrese los amperes: "))  # Amperios
longitud = int (input ("Ingrese la distancia en metros: "))  # Metros
material = 'cobre'  # Material del conductor
area_seccion = 1e-6  # Metros cuadrados

caida_tension = calcular_caida_tension(corriente, longitud, material, area_seccion)
print(f"La caída de tensión es: {caida_tension:.2f} V") # Se modifico el numero .6f para reducir el valor decimal
