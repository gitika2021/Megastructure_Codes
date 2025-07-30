import os
import psutil
from multiprocessing import Process

def write_hello(core_id):
    # Set affinity to the specified CPU core
    p = psutil.Process(os.getpid())
    p.cpu_affinity([core_id])  # set process to use only core_id

    # File path based on core ID
    file_name = f"hello_core_{core_id}.txt"

    # Write to the file
    with open(file_name, "w") as f:
        f.write(f"Hello from core {core_id}, PID {os.getpid()}\n")

    print(f"Wrote file {file_name} on CPU core {core_id}")

if __name__ == "__main__":
    num_cores = os.cpu_count() or 1  # fallback to 1 if can't detect

    processes = []
    for core in range(min(4, num_cores)):  # limit to 4 processes for example
        p = Process(target=write_hello, args=(core,))
        p.start()
        processes.append(p)

    # Wait for all to complete
    for p in processes:
        p.join()

    print("All files written.")
