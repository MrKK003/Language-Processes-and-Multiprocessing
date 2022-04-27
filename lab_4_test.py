import time
import multiprocessing as mp



def file_len(fname):
    with open(fname) as f:
        for i,l in enumerate(f):
            pass
    return i+1


def provider(lock, number_of_clipboards, all_clipboards,file,file_location):

    file_length=file_len(file_location)
    v=int(number_of_clipboards)
    lines_in_clipboard = file_length // v
    last_clipboard_start = lines_in_clipboard * (v-1)+1

    for x in range(v-1):
        for i in range(lines_in_clipboard):
            ch_counter=0
            while True:
                char = file.read(1)   
     
                all_clipboards[x].insert(ch_counter,char)

                ch_counter+1
                if char=='\n':  
                    break
       
        all_clipboards[x].reverse()

    
    for i in range(last_clipboard_start,file_length+1):
        ch_counter=0
        while True:
            char = file.read(1)


            all_clipboards[v-1].insert(ch_counter,char)


            ch_counter+1
            if char=='\n':  
                break
            if not char: 
                break

    all_clipboards[v-1].reverse()

    file.close() 


def manufacturer(lock, all_clipboards,new_text):

    counter=0

    for x in all_clipboards:
        for previous_ch in x:
            new_ch=previous_ch.lower()


            new_text.insert(counter,new_ch)


            counter+1

      
    new_text.reverse()




def consumer(lock, new_text):

    output=open("/Applications/ТТМП/output.txt","w")


    output.writelines(new_text)




def main():

    lock = mp.Lock()
    new_text=[]

    number_of_clipboards=int(input("Input number of clipboards: "))
    file_location = str(input('Input location: ')) #/Applications/ТТМП/test.txt
    file = open(file_location, "r+")

    all_clipboards=[[] for i in range(number_of_clipboards)]
    
    
    provider(lock,number_of_clipboards, all_clipboards, file, file_location)

    manufacturer(lock,all_clipboards,new_text)

    consumer(lock,new_text)

    #print(new_text)

if __name__ == "__main__": 
    t1=time.perf_counter()
    main()
    t2=time.perf_counter()
    print(f'Finished in {t2-t1} seconds')