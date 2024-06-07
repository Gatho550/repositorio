import tkinter as tk
from tkinter import ttk

def calcular_caida_tension():
    try:
        corriente = float(corriente_entry.get())
        longitud = float(longitud_entry.get())
        material = material_combobox.get()
        calibre = int(calibre_entry.get())
        voltaje_entrada = float(voltaje_entrada_entry.get())
        sistema_fase = sistema_fase_combobox.get()

        resistividades = {
            'cobre': 1.68e-8,
            'aluminio': 2.65e-8,
            'alucobre': 3.2e-8
        }
        
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

        rho = resistividades.get(material.lower())

        if rho is None:
            raise ValueError(f"Material no reconocido: {material}")

        area_seccion = areas_seccion.get(calibre)

        if area_seccion is None:
            raise ValueError(f"Calibre no reconocido: {calibre}")

        R = rho * (longitud / area_seccion)

        # Factor de corrección para sistemas bifásicos y trifásicos
        if sistema_fase == "Bifásico":
            R *= 2
        elif sistema_fase == "Trifásico":
            R *= 3

        caida_voltaje = corriente * R
        voltaje_salida = voltaje_entrada - caida_voltaje
        
        resultado_label.config(text=f"La caída de tensión es: {caida_voltaje:.10f} V")
        voltaje_salida_label.config(text=f"Voltaje de salida: {voltaje_salida:.10f} V")

    except ValueError as e:
        resultado_label.config(text=str(e))

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de Caída de Tensión")
root.geometry("400x400")

# Crear Notebook para pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Pestaña de Calculadora
frame_calculadora = ttk.Frame(notebook)
notebook.add(frame_calculadora, text='Calculadora')

# Campos para ingresar valores
corriente_label = ttk.Label(frame_calculadora, text="Corriente (Amperios):")
corriente_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

corriente_entry = ttk.Entry(frame_calculadora)
corriente_entry.grid(column=1, row=0, padx=10, pady=5)

longitud_label = ttk.Label(frame_calculadora, text="Longitud (Metros):")
longitud_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

longitud_entry = ttk.Entry(frame_calculadora)
longitud_entry.grid(column=1, row=1, padx=10, pady=5)

material_label = ttk.Label(frame_calculadora, text="Material:")
material_label.grid(column=0, row=2, padx=10, pady=5, sticky="e")

material_combobox = ttk.Combobox(frame_calculadora, values=["Cobre", "Aluminio", "Alucobre"])
material_combobox.grid(column=1, row=2, padx=10, pady=5)
material_combobox.current(0)

calibre_label = ttk.Label(frame_calculadora, text="Calibre (AWG):")
calibre_label.grid(column=0, row=3, padx=10, pady=5, sticky="e")

calibre_entry = ttk.Entry(frame_calculadora)
calibre_entry.grid(column=1, row=3, padx=10, pady=5)

voltaje_entrada_label = ttk.Label(frame_calculadora, text="Voltaje de entrada (V):")
voltaje_entrada_label.grid(column=0, row=4, padx=10, pady=5, sticky="e")

voltaje_entrada_entry = ttk.Entry(frame_calculadora)
voltaje_entrada_entry.grid(column=1, row=4, padx=10, pady=5)

sistema_fase_label = ttk.Label(frame_calculadora, text="Sistema de Fase:")
sistema_fase_label.grid(column=0, row=5, padx=10, pady=5, sticky="e")

sistema_fase_combobox = ttk.Combobox(frame_calculadora, values=["Monofásico", "Bifásico", "Trifásico"])
sistema_fase_combobox.grid(column=1, row=5, padx=10, pady=5)
sistema_fase_combobox.current(0)

calcular_button = ttk.Button(frame_calculadora, text="Calcular", command=calcular_caida_tension)
calcular_button.grid(column=0, row=6, columnspan=2, pady=10)

resultado_label = ttk.Label(frame_calculadora, text="")
resultado_label.grid(column=0, row=7, columnspan=2)

voltaje_salida_label = ttk.Label(frame_calculadora, text="")
voltaje_salida_label.grid(column=0, row=8, columnspan=2)

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