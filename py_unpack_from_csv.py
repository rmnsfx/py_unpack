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


    with open('9_1.csv', 'r') as f:
        reader = csv.reader(f)

        #for row in reader:
            #print(row)

    data = pd.read_csv("9_1.csv", sep=';')
    data2 = pd.read_csv("9_2.csv", sep=';')

    # Метка времени
    datetime = data.iloc[:,0]
    datetime2 = data2.iloc[:, 0]

    # Ускорение
    A_X_1 = data.iloc[:,1]
    A_X_2 = data.iloc[:,2]

    A_Y_1 = data.iloc[:, 21]
    A_Y_2 = data.iloc[:, 22]

    A_Z_1 = data.iloc[:, 41]
    A_Z_2 = data.iloc[:, 42]

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
    V_X_1 = data.iloc[:, 61]
    V_X_2 = data.iloc[:, 62]

    V_Y_1 = data.iloc[:, 81]
    V_Y_2 = data.iloc[:, 82]

    V_Z_1 = data2.iloc[:, 1]
    V_Z_2 = data2.iloc[:, 2]

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
    X = data2.iloc[:, 21]
    Y = data2.iloc[:, 41]
    Z = data2.iloc[:, 61]

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


    final_out.to_csv('output.csv', index=False, sep=';', decimal=',', header=False)

