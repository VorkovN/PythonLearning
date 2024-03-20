import multiprocessing
import time
from datetime import datetime
from codecs import encode
from threading import Thread

def process_a(input_queue, to_b_end):
    while True:
        if not input_queue.empty():
            msg = input_queue.get()
            print(f"{time.strftime('%H:%M:%S')}; A process; {msg}")
            msg = msg.lower()
            to_b_end.send(msg)
            time.sleep(5)

def process_b(from_a_end, to_main_end):
    while True:
        if from_a_end.poll():
            msg = from_a_end.recv()
            print(f"{time.strftime('%H:%M:%S')}; B process; {msg}")
            msg = encode(msg, 'rot_13')
            to_main_end.send(msg)

def output_thread_func(from_b_end):
    while True:
        if from_b_end.poll():
            print(f"{time.strftime('%H:%M:%S')}; main process; {from_b_end.recv()}")

if __name__ == "__main__":
    input_queue = multiprocessing.Queue()
    ab_push, ab_pull = multiprocessing.Pipe()
    mainb_pull, mainb_push = multiprocessing.Pipe()

    processA = multiprocessing.Process(target=process_a, args=(input_queue, ab_push))
    processB = multiprocessing.Process(target=process_b, args=(ab_pull, mainb_push))
    output_thread = Thread(target=output_thread_func, args=(mainb_pull,))

    processA.start()
    processB.start()
    output_thread.start()

    try:
        while True:
            msg = input()
            print(f"{time.strftime('%H:%M:%S')}; main process; {msg}")

            if msg.lower() == 'exit':
                break
            input_queue.put(msg)
    finally:
        processA.terminate()
        processB.terminate()
        output_thread.join()