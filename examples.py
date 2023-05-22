import neware_ndax_reader


file = r'20221216230450.ndax'
df,barcodes = neware_ndax_reader.read(file)
print(df)
