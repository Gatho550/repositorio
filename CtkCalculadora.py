import customtkinter as ctk

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
        resultado_label.configure(text=f"La caída de tensión es: {caida_voltaje:.4f} V")
        voltaje_salida_label.configure(text=f"Voltaje de salida: {voltaje_salida:.4f} V")

    except ValueError as e:
        resultado_label.configure(text=str(e))

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
            cobre_recomendacion_label.configure(text=f"Calibre recomendado (Cobre): {recomendaciones['Cobre']} AWG")
        else:
            cobre_recomendacion_label.configure(text="No se encontró calibre adecuado para Cobre.")
        
        if "Aluminio" in recomendaciones:
            aluminio_recomendacion_label.configure(text=f"Calibre recomendado (Aluminio): {recomendaciones['Aluminio']} AWG")
        else:
            aluminio_recomendacion_label.configure(text="No se encontró calibre adecuado para Aluminio.")
    
    except ValueError as e:
        cobre_recomendacion_label.configure(text=str(e))
        aluminio_recomendacion_label.configure(text=str(e))

def mostrar_frame(frame):
    frame_calculadora.pack_forget()
    frame_recomendacion.pack_forget()
    frame_conceptos.pack_forget()
    frame.pack(fill='both', expand=True)

# Crear la ventana principal
root = ctk.CTk()
root.title("Calculadora de Caída de Tensión")
root.geometry("500x600")

# Crear botones de navegación
nav_frame = ctk.CTkFrame(root)
nav_frame.pack(fill='x')

calcular_button = ctk.CTkButton(nav_frame, text="Calculadora", command=lambda: mostrar_frame(frame_calculadora))
calcular_button.pack(side='left', padx=5, pady=5)

recomendar_button = ctk.CTkButton(nav_frame, text="Recomendación", command=lambda: mostrar_frame(frame_recomendacion))
recomendar_button.pack(side='left', padx=5, pady=5)

conceptos_button = ctk.CTkButton(nav_frame, text="Conceptos", command=lambda: mostrar_frame(frame_conceptos))
conceptos_button.pack(side='left', padx=5, pady=5)

# Frame para Calculadora
frame_calculadora = ctk.CTkFrame(root)

# Crear pestañas dentro del frame_calculadora
frame_calculo = ctk.CTkFrame(frame_calculadora)
frame_calculo.pack(fill='both', expand=True)

# Campos para ingresar valores
corriente_label = ctk.CTkLabel(frame_calculo, text="Corriente (Amperios):")
corriente_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

corriente_entry = ctk.CTkEntry(frame_calculo)
corriente_entry.grid(column=1, row=0, padx=10, pady=5)

longitud_label = ctk.CTkLabel(frame_calculo, text="Longitud (Metros):")
longitud_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

longitud_entry = ctk.CTkEntry(frame_calculo)
longitud_entry.grid(column=1, row=1, padx=10, pady=5)

material_label = ctk.CTkLabel(frame_calculo, text="Material:")
material_label.grid(column=0, row=2, padx=10, pady=5, sticky="e")

material_combobox = ctk.CTkComboBox(frame_calculo, values=["Cobre", "Aluminio", "Alucobre"])
material_combobox.grid(column=1, row=2, padx=10, pady=5)
material_combobox.set("Cobre")

calibre_label = ctk.CTkLabel(frame_calculo, text="Calibre (AWG):")
calibre_label.grid(column=0, row=3, padx=10, pady=5, sticky="e")

calibre_entry = ctk.CTkEntry(frame_calculo)
calibre_entry.grid(column=1, row=3, padx=10, pady=5)

voltaje_entrada_label = ctk.CTkLabel(frame_calculo, text="Voltaje de entrada (V):")
voltaje_entrada_label.grid(column=0, row=4, padx=10, pady=5, sticky="e")

voltaje_entrada_entry = ctk.CTkEntry(frame_calculo)
voltaje_entrada_entry.grid(column=1, row=4, padx=10, pady=5)

sistema_fase_label = ctk.CTkLabel(frame_calculo, text="Sistema de Fase:")
sistema_fase_label.grid(column=0, row=5, padx=10, pady=5, sticky="e")

sistema_fase_combobox = ctk.CTkComboBox(frame_calculo, values=["Monofásico", "Bifásico", "Trifásico"])
sistema_fase_combobox.grid(column=1, row=5, padx=10, pady=5)
sistema_fase_combobox.set("Monofásico")

# Botón para calcular
calcular_button = ctk.CTkButton(frame_calculo, text="Calcular", command=calcular_caida_tension)
calcular_button.grid(column=0, row=6, columnspan=2, pady=10)

# Etiquetas para mostrar resultados
resultado_label = ctk.CTkLabel(frame_calculo, text="")
resultado_label.grid(column=0, row=7, columnspan=2)

voltaje_salida_label = ctk.CTkLabel(frame_calculo, text="")
voltaje_salida_label.grid(column=0, row=8, columnspan=2)

# Frame para Recomendación
frame_recomendacion = ctk.CTkFrame(root)

# Campos para ingresar valores de la recomendación
carga_label = ctk.CTkLabel(frame_recomendacion, text="Carga (Amperios):")
carga_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

carga_entry = ctk.CTkEntry(frame_recomendacion)
carga_entry.grid(column=1, row=0, padx=10, pady=5)

voltaje_label = ctk.CTkLabel(frame_recomendacion, text="Voltaje (V):")
voltaje_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

voltaje_entry = ctk.CTkEntry(frame_recomendacion)
voltaje_entry.grid(column=1, row=1, padx=10, pady=5)

distancia_label = ctk.CTkLabel(frame_recomendacion, text="Distancia (Metros):")
distancia_label.grid(column=0, row=2, padx=10, pady=5, sticky="e")

distancia_entry = ctk.CTkEntry(frame_recomendacion)
distancia_entry.grid(column=1, row=2, padx=10, pady=5)

recomendar_button = ctk.CTkButton(frame_recomendacion, text="Recomendar Calibre", command=recomendar_calibre)
recomendar_button.grid(column=0, row=3, columnspan=2, pady=10)

cobre_recomendacion_label = ctk.CTkLabel(frame_recomendacion, text="")
cobre_recomendacion_label.grid(column=0, row=4, columnspan=2)

aluminio_recomendacion_label = ctk.CTkLabel(frame_recomendacion, text="")
aluminio_recomendacion_label.grid(column=0, row=5, columnspan=2)

# Frame para Conceptos
frame_conceptos = ctk.CTkFrame(root)

# Crear botones para conceptos
concepto1_button = ctk.CTkButton(frame_conceptos, text="Código de colores", command=lambda: mostrar_concepto('codigo_colores.txt'))
concepto1_button.pack(fill='x', padx=10, pady=5)

concepto2_button = ctk.CTkButton(frame_conceptos, text="Calibres", command=lambda: mostrar_concepto('calibres.txt'))
concepto2_button.pack(fill='x', padx=10, pady=5)

concepto3_button = ctk.CTkButton(frame_conceptos, text="Material del cable", command=lambda: mostrar_concepto('material.txt'))
concepto3_button.pack(fill='x', padx=10, pady=5)

# Textbox para mostrar los conceptos
concepto_text = ctk.CTkTextbox(frame_conceptos, wrap='word')
concepto_text.pack(fill='both', expand=True)

def mostrar_concepto(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        content = file.read()
    concepto_text.configure(state='normal')
    concepto_text.delete("1.0", 'end')
    concepto_text.insert("1.0", content)
    concepto_text.configure(state='disabled')

# Mostrar el frame de calculadora por defecto
mostrar_frame(frame_calculadora)

# Ejecutar el bucle de eventos
root.mainloop()
