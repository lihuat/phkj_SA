import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime

print("开始计算")
starttime = datetime.datetime.now()

#导入数据
three_month_back_data = pd.read_excel("SA退还数据/三个月还款数据源.xlsx",dtype={'贷款编号':'O','SA工号':'O'})
three_month_back_data = three_month_back_data.drop_duplicates("贷款编号") #按照贷款编号去重
three_month_back_data=three_month_back_data.reset_index(drop=True) #重置索引


M2_plus_penalty_all = pd.read_excel("扣罚汇总/M2+扣罚汇总.xlsx",dtype={'贷款编号':'O','SA工号':'O'})
M2_penalty_all = pd.read_excel("扣罚汇总/首次M2扣罚汇总.xlsx",dtype={'贷款编号':'O','SA工号':'O'})

M2_plus_penalty_all_1 = M2_plus_penalty_all[["贷款编号","暂押金额","扣押月份","退还月份","逾期等级"]]
M2_penalty_all_1 = M2_penalty_all[["贷款编号","暂押金额","扣押月份","退还月份","逾期等级"]]

three_month_back_data_1 = pd.merge(three_month_back_data, M2_penalty_all_1,
                                   on="贷款编号", how="left")
three_month_back_data_2 = pd.merge(three_month_back_data, M2_plus_penalty_all_1,
                                   on="贷款编号", how="left")
for i in tqdm(range(len(three_month_back_data_1))):
    if np.isnan(three_month_back_data_1.loc[i, "扣押月份"]) == True:
        three_month_back_data_1.drop([i], inplace=True)

three_month_back_data_1 = three_month_back_data_1.reset_index(drop=True)

for i in tqdm(range(len(three_month_back_data_1))):
    if np.isnan(three_month_back_data_1.loc[i,"退还月份"]) == False:
        three_month_back_data_1.drop([i],inplace=True)
    else:
        pass

three_month_back_data_1=three_month_back_data_1.reset_index(drop=True)

for i in tqdm(range(len(three_month_back_data_2))):
    if np.isnan(three_month_back_data_2.loc[i, "扣押月份"]) == True:
        three_month_back_data_2.drop([i], inplace=True)

three_month_back_data_2 = three_month_back_data_2.reset_index(drop=True)

for i in tqdm(range(len(three_month_back_data_2))):
    if np.isnan(three_month_back_data_2.loc[i,"退还月份"]) == False:
        three_month_back_data_2.drop([i],inplace=True)
    else:
        pass

three_month_back_data_2=three_month_back_data_2.reset_index(drop=True)

#结清数据匹配
settle_data = pd.read_excel("SA退还数据/结清数据源.xlsx",dtype={'贷款编号':'O','SA工号':'O'})
#settle_data['贷款编号'] = settle_data['贷款编号'].astype('O')
settle_data_1 = pd.merge(settle_data,M2_penalty_all_1,on="贷款编号",how="left")
settle_data_2 = pd.merge(settle_data,M2_plus_penalty_all_1,on="贷款编号",how="left")

for i in tqdm(range(len(settle_data_1))):
    if np.isnan(settle_data_1.loc[i, "扣押月份"]) == True:
        settle_data_1.drop([i], inplace=True)

settle_data_1 = settle_data_1.reset_index(drop=True)


for i in tqdm(range(len(settle_data_1))):
    if np.isnan(settle_data_1.loc[i,"退还月份"]) == False:
        settle_data_1.drop([i],inplace=True)
    else:
        pass

settle_data_1=settle_data_1.reset_index(drop=True)

#匹配M2+
for i in tqdm(range(len(settle_data_2))):
    if np.isnan(settle_data_2.loc[i, "扣押月份"]) == True:
        settle_data_2.drop([i], inplace=True)

settle_data_2 = settle_data_2.reset_index(drop=True)

for i in tqdm(range(len(settle_data_2))):
    if np.isnan(settle_data_2.loc[i,"退还月份"]) == False:
        settle_data_2.drop([i],inplace=True)
    else:
        pass

settle_data_2=settle_data_2.reset_index(drop=True)

all_1 = pd.concat([settle_data_1,settle_data_2,three_month_back_data_1,
                   three_month_back_data_2],ignore_index=True,sort=False)
print("计算完成，正在保存数据...")
all_1.to_excel("数据输出/SA单笔退还明细.xlsx")
endtime = datetime.datetime.now()
print("用时：%d秒"%(endtime-starttime).seconds)
