import multiprocessing as mp
import time 
import string

def file_len(fname):
    with open(fname) as f:
        for i,l in enumerate(f):
            pass
    return i+1

def provider(lock, number_of_clipboards, all_clipboards, file, file_length, q):

    lines_in_clipboard = file_length // number_of_clipboards
    last_clipboard_start = lines_in_clipboard * (number_of_clipboards-1)+1
    time.sleep(10)
    if number_of_clipboards==1:
        for k in range(file_length+1):
            while True:
                char=file.read(1)

                lock.acquire()    
                all_clipboards[0]+=char
                lock.release()

                if char=='\n':  
                    break
                if not char: 
                    break
    
    else:
        for x in range(number_of_clipboards-1):
            for i in range(lines_in_clipboard):
                while True:
                    char=file.read(1)
                    lock.acquire()
                    all_clipboards[x]+=char
                    lock.release()

                    if char=='\n':  
                        break

        for k in range(last_clipboard_start,file_length+1):
            while True:
                char=file.read(1)
                
                lock.acquire()    
                all_clipboards[number_of_clipboards-1]+=char
                lock.release()

                if char=='\n':  
                    break
                if not char: 
                    break


def manufacturer(lock, all_clipboards, new_text, q):
    #time.sleep(10)
    for x in all_clipboards:
        lock.acquire()
        new_text.append(x)
        lock.release()

    for k in range(0,len(new_text)):
        lock.acquire()
        new_text[k]=new_text[k].lower()
        lock.release()

def consumer(lock, new_text):

    output=open("/Applications/ТТМП/output1.txt","w")
    for x in new_text:
        output.writelines(x)


def main():
    
    lock = mp.Lock()
    manager = mp.Manager()
    processes = []
    file_location = str(input('Input location: ')) #/Applications/ТТМП/test.txt
    number_of_clipboards=int(input("Enter number of clipboards: "))
    file = open(file_location, "r+")

    file_length=file_len(file_location)

    all_clipboards=manager.list()
    new_text=manager.list()

    for i in range(number_of_clipboards): 
        all_clipboards.append("")

    q = mp.Queue()
    p1 = mp.Process(target=provider, args = [lock, number_of_clipboards, all_clipboards, file, file_length, q])
    p1.start()
    processes.append(p1)

    while True:
        if p1.is_alive():
            time.sleep(0.1)
        else:
            p2 = mp.Process(target=manufacturer, args = [lock, all_clipboards, new_text, q])
            p2.start()
            processes.append(p2)
            break

    while True:
        if p2.is_alive():
            time.sleep(0.1)
        else:
            p3 = mp.Process(target=consumer, args = [lock, new_text])
            p3.start()
            processes.append(p3)
            break

    for process in processes:
        process.join()
    
    #print(new_text)

if __name__ == "__main__": 
    t1=time.perf_counter()
    main()
    t2=time.perf_counter()
    print(f'Finished in {t2-t1} seconds')