import os
import subprocess
import pandas as pd
import tqdm
from multiprocessing import Pool

def get_bnbcode(address:str):
    # if address.startswith('0x'): 
    #     code_path = '/data/kaixuan/BNB_Scan/' + address[2:] # remove 0x
    # else:
    #     code_path = '/data/kaixuan/BNB_Scan/' + address
    code_path = '/data/kaixuan/BNB_Scan/' + address
    if not os.path.exists(code_path):
        os.makedirs(code_path)
        try:    
            subprocess.run(['getCode', '-n', 'bsc', '-a', address, '-o', code_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell = False)
        except Exception as e:
            print(e, 'for address:', address)
    else:
        print(f'the folder for {address} already exists: {code_path}')

def multi_get_bnbcode(address:list, poolnum:int=10):
    addr_len = len(address)
    with Pool(poolnum) as p:
        ret = list(
            tqdm.tqdm(p.imap(get_bnbcode, address), total=addr_len, desc='down bnbcode'))
        p.close()
        p.join()
    return ret
    


if __name__ == '__main__':

    df = pd.read_csv('/home/kaixuan/SC-SAST/BNB_Scan/BNB-OFFICIAL.csv')
    address = df.address.unique()
    multi_get_bnbcode(address, 10)
    
    
    # print("-"*59)
    # print("test for 0x0012365F0a1E5F30a5046c680DCB21D07b15FcF7:")
    # get_bnbcode('0x0012365F0a1E5F30a5046c680DCB21D07b15FcF7')