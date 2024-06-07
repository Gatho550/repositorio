def calcular_caida_tension(I, L, material, calibre):
    # Resistividades en ohmios-metro (Ω·m)
    resistividades = {
        'cobre': 1.68e-8,
        'aluminio': 2.65e-8,
        'alucobre': 3.2e-8
    }
    
    # Áreas de sección transversal en mm² para diferentes calibres de AWG
    areas_seccion = {
        20: 0.518,
        18: 0.823,
        16: 1.31,
        14: 2.08,
        12: 3.31,
        10: 5.26,
        8: 8.37,
        6: 13.3,
        4: 21.2,
        2: 33.6,
        1: 42.4,
        0: 53.5,
        00: 67.4,
        000: 85.0,
        0000: 107,
    }

    # Obtener la resistividad del material
    rho = resistividades.get(material.lower())
    
    if rho is None:
        raise ValueError(f"Material no reconocido: {material}")
    
    # Obtener el área de la sección transversal basada en el calibre seleccionado
    area_seccion = areas_seccion.get(calibre)

    if area_seccion is None:
        raise ValueError(f"Calibre no reconocido: {calibre}")
    
    # Calcular la resistencia del cable
    R = rho * (L / area_seccion)

    # Calcular la caída de tensión
    delta_V = I * R
    return delta_V

# Ejemplo de uso
corriente = int(input("Ingrese los amperes: "))  # Amperios
longitud = int(input("Ingrese la distancia en metros: "))  # Metros
material = input("Material a usar: ")  # Material del conductor
calibre = int(input("Calibre del cable (AWG): "))  # Calibre del cable según AWG

caida_tension = calcular_caida_tension(corriente, longitud, material, calibre)
print(f"La caída de tensión es: {caida_tension:.2f} V")  # Se modificó el número .6f para reducir el valor decimal
