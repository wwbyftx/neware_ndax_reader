import time
import mmap
import logging
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from neware_function import byte_to_list,aux_to_list
import shutil
import os
from xml.dom.minidom import parse # 这个用来解析xml文档
import zipfile
rec_columns = [
    'Index', 'Cycle', ' Step','Status', 'Time', 'Voltage',
    'Current(A)', 'Charge_Capacity(Ah)', 'Discharge_Capacity(Ah)',
    'Charge_Energy(Wh)', 'Discharge_Energy(Wh)', 'Timestamp']

aux_columns = ['Index', 'T']

def read_testinfo(file):

    # from xml.dom.minidom import parseString # 这个用来解析xml字符串
    with open(file, "rb") as g:
        mm = mmap.mmap(g.fileno(), 0, access=mmap.ACCESS_READ)
        mm_size = mm.size()
        head = mm.find(b'SN')
        mm.seek(head+4)
        t = mm.find(b'"')
        value2 = mm.read(t - mm.tell()).decode("gb2312").split("-")[0]
        head = mm.find(b'Barcode')
        mm.seek(head+9)
        t = mm.find(b'"')
        value = mm.read(t - mm.tell()).decode("UTF-8")

    g.close()
    return [value,value2]
    # data = datasource.replace("GB2312","")
    # doc = p(data)
    # value = doc.getElementsByTagName("Barcode")
    # print(value)

def read(file):
    print(file)
    f = zipfile.ZipFile(file, 'r')  # 压缩文件位置
    for x in f.namelist():
        f.extract(x, "./temdata/")  # 解压位置
    f.close()
    files = os.listdir("./temdata/")
    tempfile = ""
    for file in files:
        if len(file.split('_'))>2:
            tempfile = './temdata/'+ file
    data_file = './temdata/data.ndc'
    barcode = read_testinfo("./temdata/TestInfo.xml")
    with open(data_file, "rb") as g:
        mm = mmap.mmap(g.fileno(), 0, access=mmap.ACCESS_READ)
        mm_size = mm.size()

        # Identify the beginning of the data section
        record_len = 94
        header = 517
        mm.seek(header)
        if mm.read(1)!=b'U':
            print(f"File {data_file} does not contain any valid records.")
        mm.seek(header)

        # Read data records
        output = []
        aux = []
        m = 0
        n = 0
        o = 0
        p = 0
        tem = []
        while mm.tell() < mm_size:
            bytes = mm.read(record_len)
            if len(bytes) == record_len:

                # Check for a data record
                if (bytes[0:1] == b'U'):
                    output.append(byte_to_list(bytes))
                    tem.append(bytes)
                    m+=1
                    if len(bytes) !=94:
                        o+=1
                # Check for an auxiliary record
                else:
                    mm.seek(mm.tell()-52)
                    n+=1
        mm.close()
        g.close()
    try:
        with open(tempfile, "rb") as g:
            mm = mmap.mmap(g.fileno(), 0, access=mmap.ACCESS_READ)
            mm_size = mm.size()
            mm.seek(header)
            tem = []

            mm.seek(header)
            i = 0
            while mm.tell() < mm_size:

                i+=1
                bytes = mm.read(record_len)
                if len(bytes) == record_len:

                    # Check for a data record
                    if i%6!=0:
                        aux.append(aux_to_list(bytes))
                        tem.append(bytes)
                        m+=1
                        if len(bytes) !=94:
                            o+=1
                    # Check for an auxiliary record
                    else:
                        mm.seek(mm.tell()-52)
                        n+=1

            mm.close()
            g.close()
    except FileNotFoundError as e:
        pass


    # Create DataFrame and sort by Index
    df = pd.DataFrame(output, columns=rec_columns)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    if not df.Index.is_monotonic_increasing:
        df.sort_values('Index', inplace=True)

    df.reset_index(drop=True, inplace=True)

    #Join temperature data
    aux_df = pd.DataFrame(aux, columns=aux_columns)
    aux_df.drop_duplicates(inplace=True)
    if not aux_df.empty:
        df = df.merge(aux_df, on=['Index'])

    # Postprocessing
    # df.Step = _count_changes(df.Step)
    # df.Cycle = _generate_cycle_number(df)

    # Define precision of fields
    dtype_dict = {
        'Index': 'uint32',
        'Cycle': 'uint16',
        'Step': 'uint32',
        'Status': 'category',
        'Time': 'float32',
        'Voltage': 'float32',
        'Current(mA)': 'float32',
        'Charge_Capacity(mAh)': 'float32',
        'Discharge_Capacity(mAh)': 'float32',
        'Charge_Energy(mWh)': 'float32',
        'Discharge_Energy(mWh)': 'float32'
    }
    try:
        shutil.rmtree(r"./temdata")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


    return df,barcode

if __name__ == "__main__":
    file = r'20230512072749.ndax'
    df,barcode = read(file)
    print(df,barcode)
