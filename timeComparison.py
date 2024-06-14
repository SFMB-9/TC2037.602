# Salvador Federico Milanés Braniff | A01029956
# Eduardo Porto Morales | A01027893
# Valeria Tapia | A01028038

import multiprocessing
import time
import os
from lexer import process_file, load_transition_table

def sequential_tasks(directory, directory_path, transition_table):
    #print("Beginnig sequential tasks")
    for file in directory:
        file_path = os.path.join(directory_path, file)
        process_file(file_path, transition_table)
    #print("Sequential tasks finished")

def parallel_tasks(directory, directory_path, transition_table):
    #print("Beginnig parallel tasks")
    processes = []
    for file in directory:
        file_path = os.path.join(directory_path, file)
        p = multiprocessing.Process(target = process_file, args=(file_path, transition_table))
        processes.append(p)
        p.start()
    
    for process in processes:
        process.join()
    #print("Parallel tasks finished")

def main():
    directory_path = './input_files'
    directory = os.listdir(directory_path)
    transition_table = load_transition_table("transition_tables/python_lexer.tbl")

    # Sequential execution time
    ti = time.perf_counter()
    sequential_tasks(directory, directory_path, transition_table)
    tf = time.perf_counter()
    #sequential_time = tf - ti
    #print(f"Sequential time: {sequential_time:0.4f} seconds")
    parallel_time = tf - ti
    print(f"Parallel time: {parallel_time:0.4f} seconds")

    # Parallel execution time
    ti = time.perf_counter()
    parallel_tasks(directory, directory_path, transition_table)
    tf = time.perf_counter()
    sequential_time = tf - ti
    print(f"Sequential time: {sequential_time:0.4f} seconds")
    #parallel_time = tf - ti
    #print(f"Parallel time: {parallel_time:0.4f} seconds")

    # Calculate speedup, efficiency and number of cores
    num_cores = multiprocessing.cpu_count()
    speedup = sequential_time / parallel_time
    efficiency = speedup / num_cores

    print(f"Number of CPU cores available: {num_cores}")
    print(f"Speedup: {speedup:0.4f}")
    print(f"Efficiency: {efficiency:0.4f}")


if __name__ == "__main__":
    main()