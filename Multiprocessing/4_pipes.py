from multiprocessing import Process, Pipe

def worker(conn):
    for i in range(5):
        conn.send(i * i)
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()  # use Pipe(duplex=True) for two-way communication
    p = Process(target=worker, args=(child_conn,))
    p.start()

    for _ in range(5):
        print("Received:", parent_conn.recv())

    p.join()

