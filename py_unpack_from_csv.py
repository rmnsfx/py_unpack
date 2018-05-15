import struct
import csv
import pandas as pd

def intBitsToFloat(x1, x2):


   b = (x1 << 16) + x2

   s = struct.pack('>I', b)

   return struct.unpack('>f', s)[0]

def intToSign(x):

    if x >> 14 != 0:
        x = x | ~((1 << 15) - 1)
    return x


A_X = []
A_Y = []
A_Z = []
V_X = []
V_Y = []
V_Z = []
X_sign = []
Y_sign = []
Z_sign = []

if __name__ == "__main__":

    file_name_1 = '10_1_2018-05-14 17%3A00.csv'
    file_name_2 = '10_2_2018-05-14 17%3A00.csv'

    # file_name_1 = '9_1_2018-05-14 16%3A00.csv'
    # file_name_2 = '9_2_2018-05-14 16%3A00.csv'

    # with open(file_name_1 + '.csv', 'r') as f:
    #     reader = csv.reader(f)

    # for row in reader:
    #     print(row)

    data = pd.read_csv(file_name_1, sep=';')
    data2 = pd.read_csv(file_name_2, sep=';')

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


    final_out.to_csv('out_' + file_name_1, index=False, sep=';', decimal=',', header=False)

