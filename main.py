from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import openpyxl
import sqlite3 as db

def age_group(edad):
    if edad <= 20:
        return 1
    if edad >20 and edad <=30:
        return 2
    elif edad >30 and edad <=40:
        return 3
    elif edad > 40 and edad <=50:
        return 4
    elif edad > 50 and edad <= 60:
        return 5
    else: 6

if __name__ == '__main__':

    df = pd.read_csv('clientes.csv', delimiter=';')

    df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'])
    df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'])

    df['age'] = (datetime.now() - df['fecha_nacimiento']) // timedelta(days=365)
    df['age_group'] = df['age'].apply(lambda x: age_group(x))

    # delinquency =  {current-date} days -{due_date} days
    df['delinquency'] = datetime.now().day - df['fecha_vencimiento'].dt.day

    df = df.rename({'fecha_nacimiento': 'birth_date',
                    'fecha_vencimiento': 'due_date',
                    'deuda': 'due_balance',
                    'direccion': 'address',
                    'telefono': 'phone',
                    'correo': 'email',
                    'estatus_contacto': 'status',
                    'prioridad': 'priority'}, axis=1)

    df['phone'] = df['phone'].apply(lambda x: str(x))

    df['last_name'] = df['last_name'].apply(lambda x: x.upper() if x is not np.nan else x)
    df['first_name'] = df['first_name'].apply(lambda x: x.upper() if x is not np.nan else x)

    df['address'] = df['address'].apply(lambda x: x.upper() if x is not np.nan else x)
    df['gender'] = df['gender'].apply(lambda x: x.upper() if x is not np.nan else x)
    df['status'] = df['status'].apply(lambda x: x.upper() if x is not np.nan else x)

    df2 = df[[
        'fiscal_id', 'first_name', 'last_name',
        'gender', 'birth_date', 'age', 'age_group',
        'due_date', 'due_balance', 'address'
    ]]

    df3 =df[[
        'fiscal_id','email',
        'status','priority'
    ]]

    df4 =df[[
        'fiscal_id','phone',
        'status','priority'
    ]]

    df2.to_excel('clientes.xlsx', index=False)
    df3.to_excel('emails.xlsx', index=False)
    df4.to_excel('phones.xlsx', index=False)

    #conexion si no existe la crea
    engine = db.connect('database')
    engine.commit()

    #Extraer exceles y convertirlo en dataFrame
    excelClientes = pd.read_excel('clientes.xlsx', sheet_name='Sheet1')
    excelEmails = pd.read_excel('emails.xlsx', sheet_name='Sheet1')
    excelPhones = pd.read_excel('phones.xlsx', sheet_name='Sheet1')

    # df2.to_sql(...) = excelClientes.to_sql(...)
    try:
        excelClientes.to_sql(name='clientes', con=engine, index=False)
        excelEmails.to_sql(name='emails', con=engine, index=False)
        excelPhones.to_sql(name='phones', con=engine, index=False)
    except ValueError:
        print("Tables already exists")