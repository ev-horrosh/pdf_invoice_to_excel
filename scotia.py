import os
import pandas as pd
import camelot

from tkinter import Tk
from tkinter import filedialog
from glob import glob


root = Tk().withdraw()

def select_file():
    folder = filedialog.askdirectory(title="Select Folder with pdf Files")
    files=sorted([f for f in glob(f'{folder}/*.pdf')]) #<-----pdf folder path
    return folder, files


def data(dfs):
  dfs_list=[]
  for i in dfs:
    tables = camelot.read_pdf(i, flavor='stream', row_tol=8, table_areas=['12,563,577,115'], split_text=True)
    data=tables[0].df
    df=pd.DataFrame(data)
    df.columns=df.loc[0]
    df.columns=[' '.join(x.split('\n')) for x in df.columns]
    df=df.drop([0])
    df=df.drop(columns=['FECHA VALOR','ORIG','REFERENCIA'])
    last_saldo=(df.loc[df['CONCEPTO'].str.contains('Saldo'),'CONCEPTO']==True).index[-1]
    df=df.drop(df.index[last_saldo:],axis=0)
    df.columns=['FECHA OPER', 'CONCEPTO', 'DESCRIPCION', 'CARGO', 'ABONO', 'SALDO']
    df=df.append(pd.Series(dtype='object').astype('category'), ignore_index=True)
    dfs_list.append(df)
  return pd.concat(dfs_list)


# df=df.reset_index(drop=True)

# df.info()

# from numpy.core.numeric import NaN
# # df['SALDO']=df['SALDO'].str.replace(',','').astype('float')
# # df[['CARGO','ABONO']].str.replace(',','').replace('',NaN).astype('float')

if __name__=='__main__':
    FOLDER,FILES=select_file()
    df=data(FILES)
    df.to_csv(f'{FOLDER}/AFP ORIENTE.csv', index=False)