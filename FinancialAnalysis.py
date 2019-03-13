# Top Level for personal Financial Data downloaded from Nationwide in the Data folder

import pandas as pd

if __name__ == "__main__":


    #read header

    #read data
    df = pd.read_csv('./Data/Statement Download 2019-Mar-10 11-36-30.csv',skiprows=4, encoding='latin_1')
    print(df.keys())

    #Add all files to ledger (one massive dataframe) with consistent date range (do one month) and tag for account
