import time
from multiprocessing import Process, Queue

def producer(q):
    for i in range(10):
        q.put(i)
        print(f'Produced {i}')
        time.sleep(0.2)
    q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumed {item}")
        time.sleep(1)

if __name__ == "__main__":
    q = Queue()
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))

    p.start()
    c.start()
    p.join()
    c.join()

