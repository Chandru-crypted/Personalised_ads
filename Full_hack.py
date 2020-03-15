import pandas as pd
import numpy as np 
import gen_fake_data as gen
import Financial_data as fn
 
def category(master_df, num, year):
    #it will take the inputs data frame, the category , the year 
    #print(m_df)
    master_df['Month_year'] = master_df['Month'].map(str)+ "/" + master_df["Year"].map(str)
    master_df['timestamp'] = pd.to_datetime(master_df['Month_year'],format='%m/%Y')
    df1 = master_df.drop(['Unique_no','Year','Month','Month_year'],axis = 'columns')
    df2 = df1[df1['Category']== num]
    df3= df2.drop(['Category'],axis='columns')
    df4 = df3.rename(columns={'timestamp':'ds','Payments':'y'})
    return df4

def fb_model(dataframe, periods):
    # periods the number of days the model has to run 
    from fbprophet import Prophet
    model=Prophet()
    model.fit(dataframe)
    future=model.make_future_dataframe(periods=62)
    forecast=model.predict(future)
    forecast["yhat"] = np.where(forecast["yhat"]<0,0,forecast["yhat"])
    
    forecast['Year'] = forecast['ds'].apply(lambda time: time.year)
    forecast['Month'] = forecast['ds'].apply(lambda time: time.month)
    forecast[(forecast['Year'] == 2016) & (forecast['Month']==3)].sum()['yhat'] / 31


def inputs_to_mark_and_model(dataframe, category, year):
    # generated the fake data 
    # we will have a master data frame
    m_df = dataframe
    print(m_df.head())      # take this off     
    transiton_list = [True if x > thresh else False for x in df['Payments']]
    df['Encode'] = transiton_list
    pres_state = m_df['Encode'][-1]
    cat = category
    # here we have assumed to that we will be predciting the next month 
    # value from the prev 12 months data 
    which_month_to_predict = 62 
    the_predecited = fn.prediction(m_df, cat, pres_state)
    if the_predecited == "True":
        df_ip =category(m_df, category, year)
        fb_model(df_ip, which_month_to_predict)
    else:
        return False 

def reading_the_excel_file(): 
    M-dataframe = pd.read_excel(r"C:\Users\chand\Downloads\user1.xlsx")
    print(M-dataframe.head())
    uniquecategory = M-dataframe['Category'].unique()
    for category in uniquecategory:
        dataframe = M-dataframe[M-dataframe['Category'] == category] 
        v = inputs_to_mark_and_model(dataframe, category)
        if (v):
            print("The high low funcitons") 
        if v == False: 
            continue
            
    # i will be trying to predict the future data w.r.t to the present data 
    
