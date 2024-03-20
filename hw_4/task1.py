import threading
import multiprocessing
import time


def fibonacci(n):
    num1 = 0
    num2 = 1
    next_number = num2
    count = 1

    while count <= n:
        count += 1
        num1, num2 = num2, next_number
        next_number = num1 + num2

def sync_run(n, times=10):
    start_time = time.time()
    for _ in range(times):
        fibonacci(n)
    end_time = time.time()
    return end_time - start_time

def threading_run(n, times=10):
    threads = []
    start_time = time.time()
    for _ in range(times):
        thread = threading.Thread(target=fibonacci, args=(n,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    return end_time - start_time

def multiprocessing_run(n, times=10):
    processes = []
    start_time = time.time()
    for _ in range(times):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    return end_time - start_time

n = 100000
results = ""
for _ in range(10):
    sync_time = sync_run(n)
    threading_time = threading_run(n)
    multiprocessing_time = multiprocessing_run(n)

    result = f"sync_time: {sync_time} sec \nthreading_time: {threading_time} sec \nmultiprocessing_time: {multiprocessing_time} sec \n\n"
    results += result


file_path = 'artifacts/task1.txt'


with open(file_path, 'w') as file:
    file.write(results)

file_path