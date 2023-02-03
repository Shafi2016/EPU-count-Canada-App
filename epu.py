import streamlit as st
import numpy as np
import pandas as pd
import os
import base64

def main():
    st.title("Total and EPU  boolean newspapers articles for Canada")
    uploaded_file = st.file_uploader("Upload a csv file with date,title,body_text", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, error_bad_lines=False)
        data = data[['date','title','body_text']]
        df = data[['date', 'title', 'body_text']]

        def wordestimaor(X):
            X['count'] = (X.body_text.str.contains(" uncertainty|uncertain|uncertainties,",case = False,regex=True)) & (X.body_text.str.contains(" economic|economy ",case = False,regex=True))& (X.body_text.str.contains(" policy|policies,|tax|taxes,|spending|regulation|regulations, budget|deficit|central bank ",case = False,regex=True))
            return X

        df = wordestimaor(df)    
        df1 = df[['date', 'count','body_text']]

        #Making new column for count numerical
        def numCount(asd):
            if asd['count'] == True:
                return int(1)
            else:
                return int(0)
        
        #Applying function of the dataframe   
        df1['countNew'] = df1.apply(lambda asd: numCount(asd), axis = 1)                                                    
        df2 = df1[['date', 'countNew','body_text']]                                                                                             

        # Get total article count
        df2['date'] = pd.to_datetime(df2['date'], dayfirst=True)
        df5 = df2['date'].dt.date.value_counts().sort_index().reset_index()
        df5.columns = ['date','countNew'] 
        df5.rename(columns={'countNew': 'total_articles'}, inplace=True)                                                       
        df3 = df2[df2['countNew'] != 0]
        # Convert 'date' column to datetime format
        df3['date'] = pd.to_datetime(df3['date'], dayfirst=True)

        # Check if the conversion was successful
        if not df3['date'].dt.date.isna().any():
            df6 = df3['date'].dt.date.value_counts().sort_index().reset_index()
            df6.columns = ['date','countNew']
            df6.rename(columns={'countNew': 'boolean_articles'}, inplace=True)                                      
            merged_df = df5.merge(df6, on='date', how='inner')
            merged_df['date'] = pd.to_datetime(merged_df['date'])
            merged_df.set_index('date', inplace=True)
            monthly_total = merged_df.resample('MS').sum()
            st.write(monthly_total)
            st.markdown("### Save output to csv")
            
    if st.button("Download as csv"):
            csv = monthly_total.to_csv(index= True)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="merged_df.csv">Download csv file</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



