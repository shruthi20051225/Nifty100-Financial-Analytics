import threading
import time
import requests

URL = "http://127.0.0.1:8000/api/v1/screener"

times = []


def worker():

    start = time.time()

    try:
        requests.get(URL)
    except Exception:
        pass

    end = time.time()

    times.append(end - start)


threads = []

overall_start = time.time()

for _ in range(10):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

overall_end = time.time()

print("=" * 50)
print(f"Total Requests : {len(times)}")
print(f"Total Time     : {overall_end-overall_start:.2f} sec")
print(f"Average Time   : {sum(times)/len(times):.3f} sec")
print(f"Fastest        : {min(times):.3f} sec")
print(f"Slowest        : {max(times):.3f} sec")
print("=" * 50)
