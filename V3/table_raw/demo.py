import pyarrow.parquet as pr
import pandas as pd
import numpy as np
import re
# from demo1 import dim_quality_index_sc_agg_rule, dim_quality_index_windfarm, dim_quality_index_windturbine,
#     fact_quality_index_a5_copq, fact_quality_index_capacity, fact_quality_index_cm_asset, fact_quality_index_cm_detail,
#     fact_quality_index_cm_judgement, fact_quality_index_cm_tbb_cbb, fact_quality_index_contract_quality_targets,
#     fact_quality_index_copq_judgementr, fact_quality_index_copq_workcategory, fact_quality_index_en_plan,
#     fact_quality_index_en_tbb_cbb, fact_quality_index_failure, fact_quality_index_judgement_overdue,
#     fact_quality_index_kpi_quality_targets, fact_quality_index_meantimebetweenfailure,
#     fact_quality_index_tba_detail,fact_quality_index_tba_month

import demo1


def read__csv(csv_file):  # 定义一个函数，传入一个csv文件，返回一个列表，列表里面每个元素都是一个列表，指代一行数据
    df = pd.read_csv(csv_file, encoding='unicode_escape')  # 读取csv文件数据，为DataFrame数据集类型
    df_arr = np.array(df)  # 将数据集类型转化为array类型
    df_list = df_arr.tolist()  # 将array类型转化为列表类型
    return df_list


def read_csv_first_line(file_path):  # 定义一个函数，获取csv表头数据
    csv_data = pd.read_csv(file_path)
    df_list = []
    for i in csv_data:
        df_list.append(i)
    return df_list


if __name__ == '__main__':
    file_plath = r'质量指标表明细.csv'

    lst = read__csv(file_plath)
    # for i in lst:
    #     if type(i[5]) is not str:
    #         print(i)

    type_lst = []
    fact_dict = {}
    for i in lst:
        if type(i[5]) is str:
            if i[5][0:3] in ('dim', 'fac'):
                if i[5] not in type_lst:
                    type_lst.append(i[5])
                    fact_dict[i[5]] = []
                    fact_dict[i[5]].append(i[1])
                else:
                    fact_dict[i[5]].append(i[1])

    for i in fact_dict:
        l1 = []
        l2 = []
        l3 = []
        a = set(fact_dict[i])
        b = eval('demo1.' + i)
        c = set(b['header'][0])

        for g in a:
            if g not in c:
                l1.append(g)
            else:
                l2.append(g)

        for h in c:
            if h not in a:
                l3.append(h)
        if l1 != l3:
            print('表{}在数据库中有而微文档没有的字段为：'.format(i), l3)
            print('表{}在微文档中有而数据库里没有的字段为：'.format(i), l1)
            print('表{}在数据库和微文档中都有的字段为：'.format(i), l2)
            print()
