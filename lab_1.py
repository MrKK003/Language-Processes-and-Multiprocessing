#Виконав студент групи САТР-4 Кіптик Кірілл Вікторович
#Варіант 6
import numpy as np
import re

consonаnt_letters = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z','B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Z']
answer_counter = 0
answer_array=[]

#Відкрваємо та читаємо файл
file_location = str(input('Input location: ')) #/Applications/ТПМП/test.txt
file1 = open(file_location, "r+")
text = file1.read()

#Введення роздільників
text_array = re.split(',|\.|:|\n|;|\*|\+|\-|\?|\!|\(|\)|\=|\s+',text)

#Убираємо усі пусті слоова
for x in text_array:
    if x=='':
       text_array.remove('') 

#Головний цикл, проходимо по кожному слову в масиві
for x in text_array:
    counter_1=0
    counter_2=0
    letter_counter=0

    #Зменшення слова до 30 літерр 
    x = x[:30] + (x[30:] and '')
    
    #Проходимо по всім буквам слова
    for letter in x:

        if letter in consonаnt_letters:
            counter_1=counter_1+1
            if counter_1>counter_2:
                counter_2=counter_1
        else: 
            counter_1=0  

        letter_counter=letter_counter+1 

        if letter_counter>29:
            break  

    if counter_2>answer_counter:
        answer_counter=counter_2
        answer_array.clear()
        answer_array.append(x)
    elif counter_2==answer_counter:
        if x not in answer_array:
            answer_array.append(x)



#print(text_array)
print("The biggest cluster(s) of consonant letters is(are) located in:",answer_array)
print("The cluster contains",answer_counter,"letters")


file1.close