# Simulación de Tráfico Vehicular con Procesos Paralelos en Python
## Universidad Politécnica Salesiana
**Proyecto de Computación Paralela**   
Docente: Gabriel León
Estudiantes:  
- Anthony Moya Ochoa
- Daniel Collaguazo Malla
- José Villalta Heredia

---

## Introducción

Este proyecto consiste en el desarrollo de una simulación de **tráfico vehicular en una intersección urbana de Cuenca**, utilizando **paralelismo basado en procesos con Python**. Cada semáforo es un proceso independiente que se comunica con un **controlador central** para sincronizar los estados y evitar colisiones. Además, se visualiza en tiempo real mediante una **interfaz gráfica con Tkinter**, mostrando semáforos y vehículos en movimiento desde una vista superior.

---

## Objetivos

- Simular un entorno realista de tráfico urbano.
- Aplicar principios de **procesamiento paralelo** mediante `multiprocessing`.
- Implementar **sincronización entre procesos** para evitar conflictos de semáforo.
- Representar visualmente los eventos de tráfico con una GUI funcional y clara.

---

## Estructura del Proyecto

### Clases Principales

- `Semaforo`: Controla su propio estado y ejecuta su lógica en un proceso independiente.
- `ControladorTrafico`: Coordina los semáforos, determina el flujo permitido y sincroniza los ciclos.
- `Vehiculo`: Representa un vehículo individual con posición, estado y vía de origen.
- `GUI`: Interfaz gráfica que visualiza el sistema en tiempo real con imágenes para los vehículos.

### Lógica de Control

- Solo una vía o grupo de vías **no conflictivas** puede avanzar en cada ciclo.
- Cada semáforo **solicita permiso** al controlador central antes de cambiar a verde.
- Vehículos **esperan o cruzan** según el estado de su semáforo.
- La simulación se ejecuta en **múltiples ciclos controlados** (mínimo 10 por requerimiento).

---

## Requerimientos Técnicos

- Python 3.8+
- Módulos:
  - `multiprocessing`
  - `tkinter`
  - `PIL` (Pillow)
  - `queue`

```bash
pip install pillow
````

---

## 💻 Ejecución

1. Clona el repositorio:

   ```bash
   git [clone https://github.com/usuario/simulador-trafico.git](https://github.com/DanielCollaguazo2003/Semaforos_Procesos_PY)
   cd semaforos_procesos_py
   ```

2. Ejecuta el archivo principal:

   ```bash
   python main.py
   ```

3. Aparecerá una ventana visual con la **intersección urbana**, semáforos en tiempo real y vehículos que avanzan según las reglas del tráfico.

---

## GUI - Vista Superior

* **Semáforos:** rectángulos negros con luces LED de colores reales (rojo, amarillo, verde).
* **Vehículos:** imágenes PNG con dirección correspondiente.
* **Calles:** representadas como líneas horizontales y verticales con marcas viales.
* **Animación:** vehículos se mueven de acuerdo al estado del semáforo.

---

## Reporte Automático (en consola)

Al finalizar la simulación, se imprime:

* Total de vehículos que cruzaron por cada vía.
* Tiempo promedio de espera por vía.
* Total de ciclos ejecutados correctamente.

---

## Actividades Realizadas

1. ✅ Diseño modular basado en clases (`Semaforo`, `ControladorTrafico`, `Vehiculo`, `GUI`).
2. ✅ Paralelismo implementado con `multiprocessing.Process`.
3. ✅ Sincronización con `Locks`, `Barriers` y colas (`Queue`).
4. ✅ GUI funcional en Tkinter con representación visual clara y realista.
5. ✅ Registro de estadísticas en consola al finalizar.

---

## Capturas de Pantalla

---

## Conclusiones

* El uso de `multiprocessing` permite simular entornos concurrentes de forma realista.
* La sincronización entre procesos es crucial para evitar colisiones y mantener un flujo organizado.
* Tkinter, aunque simple, fue suficiente para representar una GUI efectiva.
* El diseño por clases permite escalar y mantener el sistema fácilmente.

---

## 📁 Estructura del Repositorio

```
simulador-trafico/
│
├── main.py                 # Punto de entrada
├── semaforo.py             # Clase Semáforo
├── controlador.py          # Clase ControladorTrafico
├── vehiculo.py             # Clase Vehiculo
├── gui.py                  # Interfaz gráfica con soporte de imágenes
├── utils.py                # Funciones auxiliares (si existen)
├── img/                    # Imágenes PNG de los vehículos
│   ├── car_north.png
│   ├── car_south.png
│   ├── car_east.png
│   └── car_west.png
└── README.md
```
