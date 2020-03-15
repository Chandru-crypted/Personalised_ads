import pandas as pd
import numpy as np 
import gen_fake_data as gen
 

# here the inputs are data frame and category 
def df_category(df, category): 
    df = df[df['Category'] == category] 
    print(df)
    return df      
# Now i need to encode and put into a list in a such a way that 
# like [ A, B, C, D, A, dB]
# finding the threshold 
def weighted_avg_thresh(last_10_months): 
    #assume you have the last 10 months data 
    # the data type of the last_10_months is a list
    prev_3_months_avg, prev_7_months_avg = 0, 0
    leng = len(last_10_months)
    for i in range(leng - 1 , leng- 4, -1):
        prev_3_months_avg += last_10_months[i] 
    prev_3_months_avg = prev_3_months_avg/3  # this is the prev_3_month_avg 

    for i in range((leng - 4) ,(leng - 11), -1):
        prev_7_months_avg += last_10_months[i]
    prev_7_months_avg = prev_7_months_avg / 7 
    thresh = (prev_3_months_avg)*(0.6) + (prev_7_months_avg)*(0.4)
    return thresh 

def transition_prob__mat(thresh, df):
    #creating a new column that will have value 1 when the payments is >er than thresh 
    transiton_list = [True if x > thresh else False for x in df['Payments']]
    df['Encode'] = transiton_list
    # creating a transiton table from the trasniton list
    # the number of rows = number of col = unique elements in the transition list 
    nooftrans_T_T,nooftrans_T_F, nooftrans_F_T, nooftrans_F_F = 0.0, 0.0, 0.0, 0.0
    for i in range(len(transiton_list) - 1):
        if transiton_list[i] == True and transiton_list[i + 1] == True :
            nooftrans_T_T += 1
        if transiton_list[i] == True and transiton_list[i + 1] == False :
            nooftrans_T_F += 1
        if transiton_list[i] == False and transiton_list[i + 1] == True :
            nooftrans_F_T += 1
        if transiton_list[i] == False and transiton_list[i + 1] == False :
            nooftrans_F_F += 1  
    #first take the first row as true 
    # take the second row as False
    
    #         True  False 
    # True 
    # False 
    tot_T = nooftrans_T_T + nooftrans_T_F # the sum of the values in the transmat in the first row 
    tot_F = nooftrans_F_T + nooftrans_F_F 
    # creating a new transiton matrix 
    # i will create a numpy array from these values 

    transmat = np.array([(nooftrans_T_T, nooftrans_T_F), (nooftrans_F_T, nooftrans_F_F)])
    print(transmat)
    rows = transmat.shape[0]
    cols = transmat.shape[1]

    for i in range(rows): 
        for j in range(cols):
            if i == 0: 
                transmat[i, j] = transmat[i, j] / tot_T
            if i == 1:
                transmat[i, j] = transmat[i, j] / tot_F
    return transmat
    

def initas(master_df, category): 
    df = df_category(master_df, category)
    threshold = weighted_avg_thresh(list(df['Payments'][:10]))
    transiton_matrix = transition_prob__mat(threshold, df)
    return (transiton_matrix)

def prediction(master_df,category, prev_value):
    transiton_matrix = initas(master_df,category)
    print(transiton_matrix)
    if prev_value == "True":
        current_mat = [1, 0]
        future_mat = np.matmul(transiton_matrix, current_mat)
        future_mat = list(future_mat)
        print(future_mat)
        if future_mat.index(max(future_mat)) == 0 :
            return ("True") 
        if future_mat.index(max(future_mat)) == 1:
            return ("False") 
    if prev_value == "False": 
        current_mat = [0, 1]
        future_mat = np.matmul(transiton_matrix, current_mat)
        future_mat = list(future_mat)
        print(future_mat)
        if future_mat.index(max(future_mat)) == 0:
            return ("True") 
        if future_mat.index(max(future_mat)) == 1:
            return ("False")
