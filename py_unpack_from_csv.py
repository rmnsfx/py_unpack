import struct
import csv
from tkinter import messagebox

import pandas as pd
from tkinter import *
from tkinter.filedialog import *


A_X = []
A_Y = []
A_Z = []
V_X = []
V_Y = []
V_Z = []
X_sign = []
Y_sign = []
Z_sign = []

fileName_1 = ""
fileName_2 = ""
basedir = "C:/"


def intBitsToFloat(x1, x2):


   b = (x1 << 16) + x2

   s = struct.pack('>I', b)

   return struct.unpack('>f', s)[0]

def intToSign(x):

    if x >> 14 != 0:
        x = x | ~((1 << 15) - 1)
    return x


def convertCsv():

    # file_name_1 = '10_1_2018-05-14 17%3A00.csv'
    # file_name_2 = '10_2_2018-05-14 17%3A00.csv'

    # file_name_1 = '9_1_2018-05-14 16%3A00.csv'
    # file_name_2 = '9_2_2018-05-14 16%3A00.csv'

    # with open(file_name_1 + '.csv', 'r') as f:
    #     reader = csv.reader(f)

    # for row in reader:
    #     print(row)

    global basedir

    f1 = open(fileName_1)
    f2 = open(fileName_2)

    data = pd.read_csv(f1, sep=';', encoding='cp1251')
    data2 = pd.read_csv(f2, sep=';', encoding='cp1251')

    f1.close()
    f2.close()

    # Метка времени
    datetime = data.iloc[:,0].fillna(method='ffill')
    datetime2 = data2.iloc[:, 0].fillna(method='ffill')

    # Ускорение
    A_X_1 = data.iloc[:,1].fillna(0).astype(int)
    A_X_2 = data.iloc[:,2].fillna(0).astype(int)

    A_Y_1 = data.iloc[:, 21].fillna(0).astype(int)
    A_Y_2 = data.iloc[:, 22].fillna(0).astype(int)

    A_Z_1 = data.iloc[:, 41].fillna(0).astype(int)
    A_Z_2 = data.iloc[:, 42].fillna(0).astype(int)

    for A_X_1, A_X_2 in zip(A_X_1, A_X_2):
        A_X.append( intBitsToFloat(A_X_1,A_X_2) )
    for A_Y_1, A_Y_2 in zip(A_Y_1, A_Y_2):
        A_Y.append( intBitsToFloat(A_Y_1,A_Y_2) )
    for A_Z_1, A_Z_2 in zip(A_Z_1, A_Z_2):
        A_Z.append( intBitsToFloat(A_Z_1,A_Z_2) )

    a_x_df = pd.DataFrame(A_X)
    a_y_df = pd.DataFrame(A_Y)
    a_z_df = pd.DataFrame(A_Z)

    # Скорость
    V_X_1 = data.iloc[:, 61].fillna(0).astype(int)
    V_X_2 = data.iloc[:, 62].fillna(0).astype(int)

    V_Y_1 = data.iloc[:, 81].fillna(0).astype(int)
    V_Y_2 = data.iloc[:, 82].fillna(0).astype(int)

    V_Z_1 = data2.iloc[:, 1].fillna(0).astype(int)
    V_Z_2 = data2.iloc[:, 2].fillna(0).astype(int)

    for V_X_1, V_X_2 in zip(V_X_1, V_X_2):
        V_X.append( intBitsToFloat(V_X_1,V_X_2) )
    for V_Y_1, V_Y_2 in zip(V_Y_1, V_Y_2):
        V_Y.append( intBitsToFloat(V_Y_1,V_Y_2) )
    for V_Z_1, V_Z_2 in zip(V_Z_1, V_Z_2):
        V_Z.append( intBitsToFloat(V_Z_1,V_Z_2) )

    v_x_df = pd.DataFrame(V_X)
    v_y_df = pd.DataFrame(V_Y)
    v_z_df = pd.DataFrame(V_Z)

    # Углы
    X = data2.iloc[:, 21].fillna(0).astype(int)
    Y = data2.iloc[:, 41].fillna(0).astype(int)
    Z = data2.iloc[:, 61].fillna(0).astype(int)

    for value1 in X:
        X_sign.append( intToSign(value1) )

    for value2 in Y:
        Y_sign.append( intToSign(value2) )

    for value3 in Z:
        Z_sign.append( intToSign(value3) )

    x_df = pd.DataFrame( X_sign )
    y_df = pd.DataFrame( Y_sign )
    z_df = pd.DataFrame( Z_sign )


    # Сохраняем в CSV

    final_out =  pd.DataFrame()

    final_out['date'] = datetime
    final_out['a_x'] = a_x_df
    final_out['a_y'] = a_y_df
    final_out['a_z'] = a_z_df
    final_out['v_x'] = v_x_df
    final_out['v_y'] = v_y_df
    final_out['v_z'] = v_z_df
    final_out['X'] = x_df
    final_out['Y'] = y_df
    final_out['Z'] = z_df

    name = os.path.split(fileName_1)[1]

    try:
        path = os.makedirs(os.path.dirname(fileName_1) + '_out')

    except Exception:
        path = os.path.split(fileName_1)[0] + '_out'
        print('dir exist' + path)

    finally:
        final_out.to_csv(path +'/'+ name, index=False, sep=';', decimal=',', header=False)

        messagebox.showinfo("","Конвертирование завершено")

    basedir = os.path.dirname(fileName_1)


def _open1(event):

    global fileName_1
    global basedir

    op = askopenfilename(initialdir=basedir,
                         filetypes =(("CSV File", "*.csv"),("All Files","*.*")),
                         title = "Выбор файла")
    ent1.insert(END, op)

    fileName_1 = op
    # print('1')
    # print(os.path.basename(op))

def _open2(event):

    global fileName_2

    op2 = askopenfilename(initialdir=basedir,
                         filetypes =(("CSV File", "*.csv"),("All Files","*.*")),
                         title = "Выбор файла")
    ent2.insert(END, op2)
    # print('2')

    fileName_2 = op2

def _work(event):
    convertCsv()
    # messagebox.showinfo("GUI Python", name_entry.get() + " " + surname_entry.get())


if __name__ == "__main__":

    root = Tk()
    root.geometry('480x150')

    ent1 = Entry(root, width=50, bd=0)
    button1 = Button(root, text='Открыть файл 1')

    ent2 = Entry(root, width=50, bd=0)
    button2 = Button(root, text='Открыть файл 2')

    ent1.grid(row=0, column=0, padx=30)
    button1.grid(row=0, column=1)

    ent2.grid(row=1, column=0, padx=30)
    button2.grid(row=1, column=1)

    button1.bind("<ButtonRelease-1>", _open1)
    button2.bind("<ButtonRelease-1>", _open2)




    button3 = Button(root, text='Запуск', padx="30", pady="10")
    button3.grid(row=2, column=0)
    button3.bind("<ButtonRelease-1>", _work)



    root.mainloop()