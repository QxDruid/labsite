#!/usr/bin/env python3

import numpy as np
import xlwt

# <<<----------------------------------     Класс таблиц испытаний ТССД    ---------------------------------->>>

# объявляем класс таблицы тест обьектов/предметов
class testtable():

    # списки тест обьектов
    objects_BB = ([1]) # Таблица 2 - анализ ВВ
    objects_Metal = ([1]) # Таблица 3 - анализ металлических компонентов
    objects_Introscope = (1,2,3,4) # Таблица 4 - анализ личных вещей (интроскоп)

    subjects_BB = ([1,2,3,4,5],) # Таблица 2 - анализ ВВ2
    subjects_Metal = ([1,2,3,4,5],) # Таблица 3 - анализ металлических компонентов
    subjects_Introscope = ([1],[2],[3],[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]) # Таблица 4 - анализ личных вещей (интроскоп)
    
    def __init__(self, table):
        tables = ((self.objects_BB,self.subjects_BB), (self.objects_Metal,self.subjects_Metal), (self.objects_Introscope,self.subjects_Introscope)) # список всех типов тест обьектов/предметов
        self.data = tables[table] # выбор нужного типа тест обьекта/предмета



# <<<----------------------------------     Функция создания таблицы    ---------------------------------->>>
def create_table(fname, table_type):
# <<<----------------------------------     НАСТРОЙКИ ЛИСТА ЭКСЕЛЬ    ---------------------------------->>>
    # установка шрифта документа
    font_main = xlwt.Font()
    font_main.name = 'Times New Roman'
    font_main.colour_index = 0
    font_main.bold = False

    # установка отсупов и выравнивания
    style_main = xlwt.XFStyle()
    style_main.font = font_main
    style_main.alignment.wrap = 1
    style_main.alignment.horz = style_main.alignment.HORZ_CENTER

    # создаем книгу exel
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test Sheet') # создаем лист Тест

    ws.col(0).width = 2600 # уменьшаем ширину колонки 1
    ws.col(1).width = 2600 # уменьшаем ширину колонки 1
    ws.col(2).width = 2600 # уменьшаем ширину колонки 1
    ws.col(3).width = 2600 # уменьшаем ширину колонки 1
    ws.col(4).width = 1000 # уменьшаем ширину колонки 1
    ws.col(5).width = 2600 # уменьшаем ширину колонки 1
    ws.col(6).width = 2600 # уменьшаем ширину колонки 1
    ws.col(7).width = 2600 # уменьшаем ширину колонки 1
    ws.col(8).width = 2600 # уменьшаем ширину колонки 1

    # В строку 0 пишем названия колонок
    ws.write(0, 0, "Номер",style_main) 
    ws.write(0, 1, "Индекс испытания G",style_main)
    ws.write(0, 2, "Тест объект",style_main)
    ws.write(0, 3, "Тест предмет",style_main)
    ws.write(0, 5, "Номер",style_main) 
    ws.write(0, 6, "Индекс испытания G",style_main)
    ws.write(0, 7, "Тест объект",style_main)
    ws.write(0, 8, "Тест предмет",style_main)

    # <<<----------------------------------     Заполнение таблицы испытаний    ---------------------------------->>>

    array = np.arange(1,101) # массив элементов от 1 до 100 включительно
    with_test_subject = np.random.choice(array, 50, replace = False) # выбираем 50 испытаний в которых будет использован тест предмет
    #print(with_test_subject)
    with_no_test_subject = [item for item in array if item not in with_test_subject] # список оставшихся испытаний без тест предмета
    table = testtable(int(table_type)-1) # выбираем таблицу тест обьектов/предметов для конкретного типа испытаний используя класс testtable

    #print(table.data) # для отладки выводим список тест обьектов/предметов

    counter = 1
    shift_hor = 0
    shift_vert = 0
    # для всех экспериментов заполняем:
    for i in array:
        ws.write(int(i) - shift_vert, 0 + shift_hor, int(i),style_main) # номер эксперимента (колонка 0)
        rand_object = np.random.choice(table.data[0],1,  replace = False)
        ws.write(int(i) - shift_vert, 2 + shift_hor, int(rand_object),style_main) # тест обьект (колонка 1)

        # для всех экспериментво в которых  присутствует тест предмет (колонка 2):
        if i in with_test_subject:
        	ws.write(int(i) - shift_vert,1 + shift_hor,1, style_main)
        	ws.write(int(i) - shift_vert, 3 + shift_hor, int(np.random.choice(table.data[1][int(rand_object)-1],1, replace = False)), style_main)
       

        # для всех экспериментво в которых нет тест предмета:
        if i in with_no_test_subject:
            ws.write(int(i) - shift_vert, 1 + shift_hor, 0, style_main) # Пишем 0 в колонку 'индекс испытания'
            ws.write(int(i) - shift_vert, 3 + shift_hor, 0, style_main) # и 0 в колонку 'Тест предмет'
        

        # переход на новые колонки после 50 элементов (для вмещения таблицы на 1 лист)
        counter += 1
        if counter == 51:
            shift_hor = 5
            shift_vert = 50

    # разделители между двумя рядами 
    for i in range(51):
        ws.write(int(i), 4, '|' ,style_main) # номер эксперимента (колонка 0)
    '''
    # для всех экспериментво в которых  присутствует тест предмет:
    for i in with_test_subject:
        ws.write(int(i),1,1, style_main)
        ws.write(int(i), 3, int(np.random.choice(table.data[1][int(rand_object-1)],1, replace = False)), style_main)
    '''

    # Сохраняем заполненный файл 
    wb.save(fname + '.xls')


# <<<_______________________________________ВЫЗОВ Функции ЕСЛИ ЗАПУСКАЕМ НАПРЯМУЮ _________________________________________>>>
if __name__ == "__main__":
    print("Введите имя файла:") # Вводим имя файла 
    fname = input()
    print("1-BB, 2-Metall, 3-Introscope") # Подсказка
    print("Введите тип исследуемого ТССД:") # вводим тип ТССД
    table_type = input()
    create_table(fname, table_type)
    print('Ok')