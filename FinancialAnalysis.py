# Top Level for personal Financial Data downloaded from Nationwide in the Data folder

import pandas as pd
import FinancialAnalysis as FA
import pandas as pd
from difflib import SequenceMatcher
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AffinityPropagation

def readCSV(fname):
    
    df = pd.read_csv(fname,skiprows=4, encoding='latin_1')
    
    return df

if __name__ == "__main__":


    #read header

    #read data
    df = pd.read_csv('./Data/Statement Download 2019-Mar-10 11-36-30.csv',skiprows=4, encoding='latin_1')
    print(df.keys())

    #Add all files to ledger (one massive dataframe) with consistent date range (do one month) and tag for account
    mine = './Data/Statement Download 2019-Mar-10 11-35-36.csv'
    df = pd.read_csv(mine,skiprows=4, encoding='latin_1')
    df = df.drop(columns = "Balance")
    df["Transactions"]= df["Transaction type"]
    df["Transactions"] += df["Description"]
    df = df.drop(columns = "Transaction type")
    df = df.drop(columns = "Description")
    df['Date'] = pd.to_datetime(df['Date'])

    df_mine = df.loc[(df['Date'] > "2019-02-06") & (df['Date'] < "2019-03-05")]

    print(df_mine.keys())

    joint = './Data/Statement Download 2019-Mar-10 11-35-53.csv'
    df = pd.read_csv(joint,skiprows=4, encoding='latin_1')
    df = df.drop(columns = "Balance")
    df["Transactions"]= df["Transaction type"]
    df["Transactions"] += df["Description"]
    df = df.drop(columns = "Transaction type")
    df = df.drop(columns = "Description")
    df['Date'] = pd.to_datetime(df['Date'])
    df_joint = df.loc[(df['Date'] > "2019-02-06") & (df['Date'] < "2019-03-05")]
    print(df_joint.keys())

    creditCard = './Data/Statement Download 2019-Mar-10 11-36-30.csv'
    df = pd.read_csv(creditCard,skiprows=4, encoding='latin_1')
    print(df.keys())

    df = pd.concat([df,df_joint,df_mine],ignore_index = True)

    df['Paid out'] = df['Paid out'].str.strip('£').astype(float)
    df['Paid in'] = df['Paid in'].str.strip('£').astype(float)
    
    labels = {'Supermarkets':['TESCO','CO-OP','MORRISONS','SAINSBURYS',"SAINSBURY'S","ALDI",'MORRISON'],
         'Eating Out':["CHATWINS","COSTA",'ARCHITECT','PIPER','BROOKLYN CRAFT','MCDONALDS','HARVESTER','SARNIES OF SHREWSBURY'],
         'Funsies':['CHESTER ZOO','BILLINGTON-DYKES'],
         'Hospital':['COUNTESS'],
         'Car and Trains':['LITTLE ROO','TRANSPORT FOR WALES'],
         'Amazon':['AMAZON','Amazon','AMZN'],
         'EAGE':['EAGE'],
         'Retail':['B&M','CARD FACTORY','MOTHERCARE','THE WORKS','SPORTSDIRECT','WILKO','HOLLAND & BARRETT '],
         'Bills':['NOWTV','PLUSNET',"OVO ENERGY","mortgage","PNET","NETFLIX","Spotify"],
         'Car Loan': ["RCIFINSERV-OMEGA"],
         'Cash':["ATM Withdrawal"],
         'Salary':["ITASCA"],
         'Transfers':["Transfer","NATIONWIDE C/CARD","DIRECT DEBIT PAYMENT"],
         'Childcare':['CHB','CHILDCARE'],
         'Mums Payements':['MRS L USHER'],
         'Interest':['Interest'],
         'Cheque Deposit':['Cheque deposit']
         }

    df['Tags']=''
    exc_total = 0
    exc_totals = []
    pie_labels = []
    for key in labels.keys():
        ind = 0
        for label in labels[key]:

            ind = ind | df['Transactions'].str.contains(label)
        
        df.loc[ind,'Tags'] = key
        print(str(key) + ' = ' + str(df['Paid out'][ind].sum()))    
        if key != "Transfers":
            exc_total += df['Paid out'][ind].sum()
            exc_totals.append(df['Paid out'][ind].sum())
            pie_labels.append(key)
    print('Total (exc. Transfers) = ' + str(exc_total))
    
    #Test for totals
    assert exc_total == df.loc[df["Tags"] != "Transfers","Paid out"].sum()
    plt.pie(exc_totals,labels = pie_labels)
    plt.show()

