import random as random
import pandas as pd


def payment_list():
    pay = []
    for pay_tr in range(0, 6):
        pay.append(random.randrange(1,10000))
    return (pay)

def categories():
    items = ['Food', 'Phone Bill', 'Clothing', 'Entertaintment', 'Fuel', 'Health']
    random.shuffle(items)
    return(items)

def onemonth(month_name):
    pay = payment_list()
    category = categories()
    month = []
    for month_name_itr in range(len(category)):
        month.append(str(month_name))
    return (pay, category, month)

def oneperson(uniq_no):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    bigpay, bigcategory, bigmonth, bigunique_no  = [], [], [], []
    for monthname in months:
        pay, category, month = onemonth(monthname)
        bigpay.extend(pay)
        bigcategory.extend(category)
        bigmonth.extend(month)
        bigunique_no.extend([uniq_no]*len(category))
    data = {'Unique_no':bigunique_no, 'Month':bigmonth, 'Category':bigcategory, 'Payments':bigpay}
    df = pd.DataFrame(data)
    return df
