import pandas as pd
import numpy as np
import math
import operator


def read_dataframe(path = "biz_data.csv"):
    df = pd.read_csv(path, low_memory= False)
    df = df.drop(["vertical_ids","founded_year"],axis = 1)
    df['revenue'][np.isnan(df['revenue'])] = -1
    df['city_id'][np.isnan(df['city_id'])] = -1
    return df


df = read_dataframe()    
company_list = list(df["company_id"])
country_list = list(df["country_id"])
city_list = list(df["city_id"])
staff_list = list(df["staff_qty"])
revenue_list = list(df["revenue"])


def check_id(real_id):
    for i in range(0, len(company_list)):
        if company_list[i] == real_id:
            return i
    print("id does not exist")
    quit()


def company_competitors(index_id):
    n_company = {}
    for i in range(0, len(company_list)):
        if i != index_id and country_list[i] == country_list[index_id] and city_list[i] == city_list[index_id]:
            if revenue_list[index_id] == -1 and revenue_list[i] == -1:
                n_company[i] = abs(staff_list[i] - staff_list[index_id])
            if revenue_list[index_id] != -1 and revenue_list[i] != -1:
                n_company[i] = (abs(revenue_list[i] - revenue_list[index_id]))    
    return n_company


def sort_print_ten_company(n_company):
    n_company_sort = sorted(n_company.items(),key = operator.itemgetter(1),reverse = False)
    for i in range(0, 10):
        print(company_list[n_company_sort[i][0]])



import time

def main():
    real_id = int(input("Input id company: "))
    start = time.time()
    index_id = check_id(real_id)
    n_company = company_competitors(index_id)
    sort_print_ten_company(n_company)
    print("Thời gian chạy chương trình: ", time.time() - start)
if __name__ == '__main__':
    main()