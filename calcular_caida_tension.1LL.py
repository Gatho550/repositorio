import tkinter as tk
from tkinter import ttk

def calcular_caida_tension():
    try:
        # Recoger datos de las entradas del usuario
        corriente = float(corriente_entry.get())
        longitud = float(longitud_entry.get())
        material = material_combobox.get()
        calibre = int(calibre_entry.get())
        voltaje_entrada = float(voltaje_entrada_entry.get())
        sistema_fase = sistema_fase_combobox.get()

        # Resistividades de los materiales en ohmios por metro
        resistividades = {
            'Cobre': 1.68e-8,
            'Aluminio': 2.65e-8,
            'Alucobre': 3.2e-8
        }
        
        # Áreas de sección en mm^2 para diferentes calibres AWG
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

        # Obtener resistividad del material seleccionado y convertirla a ohmios por mm^2 por metro
        rho = resistividades.get(material)
        if rho is None:
            raise ValueError(f"Material no reconocido: {material}")
        rho = rho * 1000000  # Convertir a ohmios por mm^2 por metro

        # Obtener área de sección del calibre seleccionado
        area_seccion = areas_seccion.get(calibre)
        if area_seccion is None:
            raise ValueError(f"Calibre no reconocido: {calibre}")

        # Calcular la resistencia del conductor
        R = rho * (longitud / area_seccion)

        # Ajustar resistencia para sistemas bifásicos y trifásicos
        if sistema_fase == "Bifásico":
            R *= 2
        elif sistema_fase == "Trifásico":
            R *= 3

        # Calcular la caída de tensión
        caida_voltaje = corriente * R
        voltaje_salida = voltaje_entrada - caida_voltaje
        
        # Mostrar resultados
        resultado_label.config(text=f"La caída de tensión es: {caida_voltaje:.10f} V")
        voltaje_salida_label.config(text=f"Voltaje de salida: {voltaje_salida:.10f} V")

    except ValueError as e:
        resultado_label.config(text=str(e))

def recomendar_calibre():
    try:
        # Recoger datos de las entradas del usuario
        carga = float(carga_entry.get())
        voltaje = float(voltaje_entry.get())
        distancia = float(distancia_entry.get())
        
        # Resistividades de los materiales en ohmios por metro
        resistividades = {
            'Cobre': 1.68e-8,
            'Aluminio': 2.65e-8
        }
        
        # Áreas de sección en mm^2 para diferentes calibres AWG
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
        
        # Norma: caída de tensión máxima permitida (por ejemplo, 3% del voltaje nominal)
        caida_tension_max = 0.03 * voltaje

        recomendaciones = {}
        
        for material, rho in resistividades.items():
            rho = rho * 1000000  # Convertir a ohmios por mm^2 por metro
            
            for calibre, area_seccion in areas_seccion.items():
                # Calcular resistencia del conductor
                R = rho * (distancia / area_seccion)
                
                # Calcular la caída de tensión
                caida_voltaje = carga * R
                
                # Verificar si la caída de tensión está dentro del límite permitido
                if caida_voltaje <= caida_tension_max:
                    recomendaciones[material] = calibre
                    break
        
        # Mostrar recomendaciones
        if "Cobre" in recomendaciones:
            cobre_recomendacion_label.config(text=f"Calibre recomendado (Cobre): {recomendaciones['Cobre']} AWG")
        else:
            cobre_recomendacion_label.config(text="No se encontró calibre adecuado para Cobre.")
        
        if "Aluminio" in recomendaciones:
            aluminio_recomendacion_label.config(text=f"Calibre recomendado (Aluminio): {recomendaciones['Aluminio']} AWG")
        else:
            aluminio_recomendacion_label.config(text="No se encontró calibre adecuado para Aluminio.")
    
    except ValueError as e:
        cobre_recomendacion_label.config(text=str(e))
        aluminio_recomendacion_label.config(text=str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de Caída de Tensión")
root.geometry("400x500")

# Crear Notebook para pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Pestaña de Calculadora
frame_calculadora = ttk.Frame(notebook)
notebook.add(frame_calculadora, text='Calculadora')

# Crear Notebook dentro de la pestaña Calculadora
notebook_calculadora = ttk.Notebook(frame_calculadora)
notebook_calculadora.pack(fill='both', expand=True)

# Pestaña de Cálculo
frame_calculo = ttk.Frame(notebook_calculadora)
notebook_calculadora.add(frame_calculo, text='Cálculo')

# Campos para ingresar valores
corriente_label = ttk.Label(frame_calculo, text="Corriente (Amperios):")
corriente_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

corriente_entry = ttk.Entry(frame_calculo)
corriente_entry.grid(column=1, row=0, padx=10, pady=5)

longitud_label = ttk.Label(frame_calculo, text="Longitud (Metros):")
longitud_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

longitud_entry = ttk.Entry(frame_calculo)
longitud_entry.grid(column=1, row=1, padx=10, pady=5)

material_label = ttk.Label(frame_calculo, text="Material:")
material_label.grid(column=0, row=2, padx=10, pady=5, sticky="e")

material_combobox = ttk.Combobox(frame_calculo, values=["Cobre", "Aluminio", "Alucobre"])
material_combobox.grid(column=1, row=2, padx=10, pady=5)
material_combobox.current(0)

calibre_label = ttk.Label(frame_calculo, text="Calibre (AWG):")
calibre_label.grid(column=0, row=3, padx=10, pady=5, sticky="e")

calibre_entry = ttk.Entry(frame_calculo)
calibre_entry.grid(column=1, row=3, padx=10, pady=5)

voltaje_entrada_label = ttk.Label(frame_calculo, text="Voltaje de entrada (V):")
voltaje_entrada_label.grid(column=0, row=4, padx=10, pady=5, sticky="e")

voltaje_entrada_entry = ttk.Entry(frame_calculo)
voltaje_entrada_entry.grid(column=1, row=4, padx=10, pady=5)

sistema_fase_label = ttk.Label(frame_calculo, text="Sistema de Fase:")
sistema_fase_label.grid(column=0, row=5, padx=10, pady=5, sticky="e")

sistema_fase_combobox = ttk.Combobox(frame_calculo, values=["Monofásico", "Bifásico", "Trifásico"])
sistema_fase_combobox.grid(column=1, row=5, padx=10, pady=5)
sistema_fase_combobox.current(0)

calcular_button = ttk.Button(frame_calculo, text="Calcular", command=calcular_caida_tension)
calcular_button.grid(column=0, row=6, columnspan=2, pady=10)

resultado_label = ttk.Label(frame_calculo, text="")
resultado_label.grid(column=0, row=7, columnspan=2)

voltaje_salida_label = ttk.Label(frame_calculo, text="")
voltaje_salida_label.grid(column=0, row=8, columnspan=2)

# Nueva pestaña dentro de Calculadora
frame_recomendacion = ttk.Frame(notebook_calculadora)
notebook_calculadora.add(frame_recomendacion, text='Recomendación de Calibre')

# Campos para ingresar valores de la nueva pestaña
carga_label = ttk.Label(frame_recomendacion, text="Carga (Amperios):")
carga_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

carga_entry = ttk.Entry(frame_recomendacion)
carga_entry.grid(column=1, row=0, padx=10, pady=5)

voltaje_label = ttk.Label(frame_recomendacion, text="Voltaje (V):")
voltaje_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

voltaje_entry = ttk.Entry(frame_recomendacion)
voltaje_entry.grid(column=1, row=1, padx=10, pady=5)

distancia_label = ttk.Label(frame_recomendacion, text="Distancia (Metros):")
distancia_label.grid(column=0, row=2, padx=10, pady=5, sticky="e")

distancia_entry = ttk.Entry(frame_recomendacion)
distancia_entry.grid(column=1, row=2, padx=10, pady=5)

recomendar_button = ttk.Button(frame_recomendacion, text="Recomendar Calibre", command=recomendar_calibre)
recomendar_button.grid(column=0, row=3, columnspan=2, pady=10)

cobre_recomendacion_label = ttk.Label(frame_recomendacion, text="")
cobre_recomendacion_label.grid(column=0, row=4, columnspan=2)

aluminio_recomendacion_label = ttk.Label(frame_recomendacion, text="")
aluminio_recomendacion_label.grid(column=0, row=5, columnspan=2)

# Pestaña de Conceptos
frame_conceptos = ttk.Frame(notebook)
notebook.add(frame_conceptos, text='Conceptos')

# Crear Notebook para pestañas de conceptos
notebook_conceptos = ttk.Notebook(frame_conceptos)
notebook_conceptos.pack(fill='both', expand=True)

# Pestaña de Concepto 1
frame_concepto1 = ttk.Frame(notebook_conceptos)
notebook_conceptos.add(frame_concepto1, text='Concepto 1')

concepto1_label = ttk.Label(frame_concepto1, text="Aquí se muestra el concepto 1.")
concepto1_label.pack()

# Pestaña de Concepto 2
frame_concepto2 = ttk.Frame(notebook_conceptos)
notebook_conceptos.add(frame_concepto2, text='Concepto 2')

concepto2_label = ttk.Label(frame_concepto2, text="Aquí se muestra el concepto 2.")
concepto2_label.pack()

# Pestaña de Concepto 3
frame_concepto3 = ttk.Frame(notebook_conceptos)
notebook_conceptos.add(frame_concepto3, text='Concepto 3')

concepto3_label = ttk.Label(frame_concepto3, text="Aquí se muestra el concepto 3.")
concepto3_label.pack()

# Ejecutar el bucle de eventos
root.mainloop()