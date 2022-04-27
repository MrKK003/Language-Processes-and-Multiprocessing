# Kiptyk Kirill SATR-4 2020
import multiprocessing as mp
import time 
import string


def run_provider(lock, buffers, number_of_buffers, file_location):
    file = open(file_location, 'r')
    reading = True
    while reading:
        for i, buffer in enumerate(buffers):
            char = file.read(1)
            if not char:
                reading = False
                break
            lock.acquire()
            buffers[i] += char
            lock.release()

        
def run_manufacturer(lock, buffers, number_of_buffers, consumer_done):
    while not consumer_done.value:
        for i, buffer in enumerate(buffers):
            lock.acquire()
            buffers[i] = buffers[i].lower()
            lock.release()

def run_consumer(lock, buffers, number_of_buffers, output, consumer_done):
    while True:
        all_empty = True
        for i, buffer in enumerate(buffers):
            lock.acquire()
            if buffers[i] is not '':
                all_empty = False
                output.value += buffers[i][0]
                buffers[i] = buffers[i][1:]
            #print(buffers)
            lock.release()
        if all_empty:
            break
    consumer_done.value = True
        
     

def main():

    file_location = str(input('Input location: ')) #/Applications/ТТМП/test.txt
    number_of_buffers=int(input("Введіть число буферів обміну данними: "))
    output_location = "/Applications/ТТМП/output2.txt"

    lock = mp.Lock()
    manager = mp.Manager()
    buffers = manager.list()
    output = manager.Value('s', '')
    consumer_done = manager.Value('b', False)
    processes = []
    for _ in range(number_of_buffers):
        buffers.append("")

    provider = mp.Process(target=run_provider, args = [lock, buffers, number_of_buffers, file_location])
    provider.start()
    processes.append(provider)

    manufacturer = mp.Process(target=run_manufacturer, args = [lock, buffers, number_of_buffers, consumer_done])
    manufacturer.start()
    processes.append(manufacturer)

    consumer = mp.Process(target=run_consumer, args = [lock, buffers, number_of_buffers, output, consumer_done])
    consumer.start()
    processes.append(consumer)

    for process in processes:
        process.join()
    
    out_file = open(output_location, 'w')
    out_file.writelines(output.value.lower())

if __name__ == "__main__": 
    t1=time.perf_counter()
    main()
    t2=time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
