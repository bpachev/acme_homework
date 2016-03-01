import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def init_store(csv_path='P00000001-ALL.csv'):
# csv_path = 'test1.csv'
 i = 0
 n_chunk = 50000
 col_types = {"cmte_id":object,"cand_id":object,"cand_nm":object,"contbr_nm":object,"contbr_city":object,"contbr_st":object,"contbr_zip":object,"contbr_employer":object,"contbr_occupation":object,"contb_receipt_amt":np.float,"receipt_desc":object,"memo_cd":object,"memo_text":object,"form_tp":object,"file_num":object,"tran_id":object,"election_tp":object}
# data_cols = ["cmte_id","cand_id","cand_nm","contbr_nm","contbr_city","contbr_st","contbr_zip","contbr_employer","contbr_occupation","contb_receipt_amt","contb_receipt_dt","receipt_desc","memo_cd","memo_text","form_tp","file_num","tran_id","election_tp"]
 data_cols = ['cand_nm','contb_receipt_amt','contb_receipt_dt','contbr_st','contbr_occupation']
 first = True
 reader = pd.read_csv(csv_path,sep=',',dtype=col_types, index_col=False,parse_dates='contb_receipt_dt',skipinitialspace=True,chunksize=n_chunk)
 my_store = pd.HDFStore('campaignData.h5')
 for chunk in reader:
  if first:
   first = False
   my_store.append('campaign', chunk, data_columns=data_cols,index=False,min_itemsize=50)
  else:
   my_store.append('campaign', chunk, index=False)
  print "On chunk %d"%i
  i += 1

def prob2():
 store= pd.HDFStore('campaignData.h5')
 N_rom_IO = len(store.select('campaign',where=["'contbr_st' == 'IA'","'cand_nm'=='Romney, Mitt'"],columns=['contbr_st']))
 N_obam_IO = len(store.select('campaign',where=["'contbr_st' == 'IA'","'cand_nm'=='Obama, Barack'"],columns=['contbr_st']))
 print "Number of contributions for Romney in Iowa %d" % N_rom_IO
 print "Number of contributions for Obama in Iowa %d" % N_obam_IO

def prob3():
 
 store= pd.HDFStore('campaignData.h5')
 cands = ['Romney, Mitt','Obama, Barack']
 conts = {cand:0 for cand in cands}
 amount = {cand:0 for cand in cands}
 for cand in cands:
  for df in store.select('campaign',where=["'cand_nm'='{}'".format(cand)],columns=["contb_receipt_amt"],chunksize=10000):
   conts[cand] += df.shape[0]
   amount[cand] += df.contb_receipt_amt.sum()
 cand_info=pd.DataFrame({'Count': conts,'Net Contb':amount},index=cands)
 plt.subplot(211)
 cand_info["Count"].plot(kind='bar')
 plt.suptitle("Number of contributions")
 plt.subplot(212)
 plt.suptitle("Net donations")
 cand_info["Net Contb"].plot(kind='bar')
 plt.show()

def prob4():
 store=pd.HDFStore('campaignData.h5')
 groups = store.select_column('campaign','contbr_occupation').unique()
 avmount = []
 counts = []
 for group in groups:
  tamt,tcont=0,0
  for df in store.select('campaign',where=["'contr_occupation'='%s'"%group],columns=['conntb_receipt_amount'],chunk_size=10000):
   tamt += df.conbt_receipt_amount.sum()
   tcont += df.shape[0]
  avamount.append(tamt/float(tcont))
  counts.append(tcont)
 occ_info = pd.DataFrame({'Count':tcont,'Avg Contb':amount},index=groups)
 occ_info.sort(columns='Count',ascending=False,inplace=True)
 plt.subplot(211)
 occ_info['Count'][:20].plot(kind='bar')
 plt.subplot(212)
 occ_info['Avg Contb'][:20].plot(kind='bar')
 plt.show()

 
