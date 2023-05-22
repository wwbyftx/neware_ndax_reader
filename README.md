# neware_ndax_reader
neware  ndax格式文件的读取，包含温度、备注等
你可以用一下方式读取ndax文件为dataframe

file = r'20221216230450.ndax'
df,barcodes = neware_ndax_reader.read(file)
