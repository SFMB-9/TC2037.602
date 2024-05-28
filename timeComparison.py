import time
import os
from lexer import file_sequencial

def timeComparison(func, arg):
    start = time.time()
    func(arg)
    end= time.time()
    return end - start

def main():
    directory_path = './input_files'
    directory = os.listdir(directory_path)
    for file in directory:
        file_path = os.path.join(directory_path, file)
        sequential_time = timeComparison(file_sequencial, file_path)
        #parallel_time = timeComparison(process_file_parallel, file_path)
        print(f"Sequential time: {sequential_time}")
        #print(f"Parallel time: {parallel_time}")
        #print(f"Speedup: {sequential_time / parallel_time}")

if __name__ == "__main__":
    main()