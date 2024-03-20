import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import matplotlib.pyplot as plt

def integrate_part(f, a, b, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def parallel_integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type='thread'):
    parts = [((a + i * (b - a) / n_jobs), (a + (i + 1) * (b - a) / n_jobs), n_iter // n_jobs) for i in range(n_jobs)]
    total = 0

    if executor_type == 'thread':
        executor_class = ThreadPoolExecutor
    else:
        executor_class = ProcessPoolExecutor

    with executor_class(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_part, f, part[0], part[1], part[2]) for part in parts]
        for future in futures:
            total += future.result()

    return total

def measure_time(f, a, b, n_jobs, executor_type):
    start_time = time.time()
    result = parallel_integrate(f, a, b, n_jobs=n_jobs, executor_type=executor_type)
    end_time = time.time()
    return end_time - start_time

cpu_num = 16
times_thread = []
times_process = []
for n_jobs in range(1, cpu_num * 2 + 1):
    times_thread.append(measure_time(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_type='thread'))
    times_process.append(measure_time(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_type='process'))

print(times_thread)
print(times_process)
plt.figure(figsize=(32, 10))
plt.plot(range(1, cpu_num*2 + 1), times_thread, label='ThreadPoolExecutor')
plt.plot(range(1, cpu_num*2 + 1), times_process, label='ProcessPoolExecutor')
plt.xlabel('Number of Jobs')
plt.ylabel('Time (s)')
plt.title('Performance Comparison')
plt.legend()
plt.grid(True)


plt.savefig('artifacts/task2_min_proc_freq.png')
plt.close()