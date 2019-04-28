# Top Level for personal Financial Data downloaded from Nationwide in the Data folder

import pandas as pd
import FinancialAnalysis as FA
import pandas as pd
from difflib import SequenceMatcher
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import AffinityPropagation
import dash
import dash_core_components as dcc
import dash_html_components as html


def readHeader(fname):
    header = {}
    with open(fname, 'r', encoding = 'latin1') as f:
        for row in f:
            
            if not row.strip():
                return header
            key = row.split(',')[0]
            value = row.split(',')[1]
            header[key] = value
    
    return header        
    

def readCSV(fname):
    """ readCSV """

    header = readHeader(fname)
    if 'Credit' in header['"Account Name:"']:
        return readCSVCredit(fname)
    else:
        return readCSVAccount(fname)

def readCSVAccount(fname):
    """ Reads a single file from Nationwide Account Statements """
    df = pd.read_csv(fname,skiprows=4, encoding='latin_1')
    # We dont need the balance just the in and out
    df = df.drop(columns = "Balance")

    # Move Columns so that they can be consistent with the credit card
    df["Transactions"]= df["Transaction type"]
    df["Transactions"] += df["Description"]
    df = df.drop(columns = "Transaction type")
    df = df.drop(columns = "Description")

    return df

def readCSVCredit(fname):
    """" Reads a single """
    df = pd.read_csv(fname,skiprows=4, encoding='latin_1')
    df["Transactions"] += df["Location"]
    df = df.drop(columns = "Location")
    return df   

def readCSV_multple(filenames):
    """ Reads multple files in """

    li = []
    for fname in filenames:
        li.append(readCSV(fname))
    
    df =  pd.concat(li,ignore_index = True, sort=False)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Paid out'] = df['Paid out'].str.strip('£').astype(float)
    df['Paid in'] = df['Paid in'].str.strip('£').astype(float)
    return df

def getLabels():
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

    return labels
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



def categorize(df,labels):
    df['Tags']=''
    for key in labels.keys():
        ind = 0
        for label in labels[key]:
            ind = ind | df['Transactions'].str.contains(label)
        
        df.loc[ind,'Tags'] = key
    return df


#read data
path = './Data'
filenames = [os.path.join(path,name) for name in os.listdir(path)]

df = readCSV_multple(filenames)


#df = df.loc[(df['Date'] > "2019-02-06") & (df['Date'] < "2019-03-05")]

labels = getLabels()

df = categorize(df,labels)

print(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
html.H4(children='Transactions'),
generate_table(df)
])


if __name__ == "__main__":



    app.run_server(debug=True)
    

