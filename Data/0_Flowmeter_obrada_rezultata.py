import pandas as pd
import re
import numpy as np

ime_datoteke_bez_ext = 'asinc mode'
ime_datoteke = ime_datoteke_bez_ext + '.txt'
#Broj sekunda između izlaznih rezultata (male poteškoće kod puno krivih rezultata 
#(čije je trajanje bilo veće od sekunde))
interval_u_sekundama = 480  
data = []
errors =[]

with open(ime_datoteke) as f:
    read_data = f.read()
    data = read_data.split('\n')
    clean_data = []
    for line in data:
        m_data = re.findall(r".\d\d\d\.\d\d", line, flags=0)
        timestamp = re.findall(r"\d\d\:\d\d\:\d\d", line, flags=0)
        if len(m_data) ==6 and len(timestamp) == 1:
            flux = m_data[2]
            temp = m_data[1]
            press = m_data[0]
            time = timestamp[0]
            try:
                clean_data.append([pd.Timestamp(time), float(flux), float(press)*0.0689475729, float(temp)])
            except:
                pass


df = pd.DataFrame(clean_data, columns=['Time, min','Flow, mL/min','Pressure, bar', 'Temp., °C'])
df['Time, min'] = df['Time, min'] - df['Time, min'][0]
df['Time, min'] = df['Time, min'].dt.total_seconds()/60
#df = df.set_index('Time, s').groupby(['Time, s']).mean().dropna(how='all')
df = df.groupby(['Time, min'],as_index=False).mean().dropna(how='all')
#
df = df.groupby(np.arange(len(df))//interval_u_sekundama).mean()
print(df)
 
writer = pd.ExcelWriter(ime_datoteke_bez_ext + '.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()