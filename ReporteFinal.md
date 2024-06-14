# Reporte Final

#### Salvador Federico Milanés Braniff | A01029956
#### Eduardo Porto Morales | A01027893
#### Valeria Tapia | A01028038

### 1. Medición de Tiempos de Ejecución

Para evaluar el rendimiento de las versiones secuencial y paralela del programa, se realizaron múltiples ejecuciones y se midieron los tiempos de cada una. Los resultados se muestran a continuación:

#### Ejecución Secuencial:
```python
# Sequential execution time
ti = time.perf_counter()
sequential_tasks(directory, directory_path, transition_table)
tf = time.perf_counter()
sequential_time = tf - ti
print(f"Sequential time: {sequential_time:0.4f} seconds")
```

#### Ejecución Paralela:
```python
# Parallel execution time
ti = time.perf_counter()
parallel_tasks(directory, directory_path, transition_table)
tf = time.perf_counter()
parallel_time = tf - ti
print(f"Parallel time: {parallel_time:0.4f} seconds")
```

### 2. Speedup y Eficiencia

El speedup se calcula como el cociente entre el tiempo de ejecución secuencial y el tiempo de ejecución paralelo. La eficiencia se calcula dividiendo el speedup por el número de núcleos de CPU disponibles.
    
```python
num_cores = multiprocessing.cpu_count()
speedup = sequential_time / parallel_time
efficiency = speedup / num_cores

print(f"Number of CPU cores available: {num_cores}")
print(f"Speedup: {speedup:0.4f}")
print(f"Efficiency: {efficiency:0.4f}")
```

### 3. Complejidad Computacional

La complejidad computacional de la versión secuencial del programa es de O(n), donde n es el número de archivos de entrada a procesar, cada archivo se procesa de manera independiente y el tiempo de procesamiento depende del tamaño del archivo y de la complejidad de la tabla de transición.
La versión paralela reduce la complejidad a O(n/p), donde p es el número de núcleos de CPU disponibles.

### 4. Contraste con los Tiempos Obtenidos
La versión paralela del programa mostró una mejora significativa en el tiempo de ejecución en comparación con la versión secuencial. Esto es esperado ya que la paralelización permite utilizar múltiples núcleos de CPU simultáneamente, reduciendo el tiempo total de procesamiento.

### 5. Conclusiones
- La paralelización puede mejorar significativamente el tiempo de ejecución de programas que pueden dividir su carga de trabajo en tareas independientes.
- La eficiencia de la paralelización depende del número de núcleos de CPU disponibles y de la capacidad del programa para dividir su carga de manera equilibrada.
- En nuestro caso, la versión paralela demostró un speedup considerable, lo que indica que el programa está bien adaptado para ejecución en múltiples núcleos.

### 6. Implicaciones Éticas
El desarrollo de tecnología que utiliza procesamiento paralelo tiene implicaciones éticas importantes:

- Eficiencia Energética: La paralelización puede llevar a un uso más eficiente de los recursos computacionales, reduciendo el consumo de energía y la huella de carbono.
- Privacidad y Seguridad: Al procesar datos de manera más rápida y eficiente, es crucial garantizar que se mantengan prácticas de privacidad y seguridad robustas para proteger la información sensible.
- Desigualdad Tecnológica: El acceso a tecnología avanzada de procesamiento paralelo puede estar limitado a organizaciones con recursos significativos, lo que podría aumentar la brecha tecnológica entre diferentes sectores de la sociedad.
