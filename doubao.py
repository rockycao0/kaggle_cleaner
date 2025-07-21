# encoding: utf-8
import pandas as pd

print('hello world')

import os
from openai import OpenAI

role = '你是一名专业的数据搜索与分析工程师'
url = 'https://www.kaggle.com/datasets/shubhammeshram579/bank-customer-churn-prediction'
prompt = f"### 你将根据用户需求，搜索以下网页{url}并提取相关信息。根据以下规则一步步执行： 1. 是否为表格分类或表格回归任务（该任务的数据类型只包含表格数据，同时有明确的预测目标） 2. 该任务使用的数据文件路径（在任何情况下输出一个列表，并假设该任务的Data Explorer作为根目录，如果该数据集使用固定的训练集和测试集，此项置空） 3. 该数据集使用的训练集路径（假设该任务的Data Explorer作为根目录，必须训练集和测试集同时存在，否则置空） 4. 该数据集使用的测试集路径（假设该任务的Data Explorer作为根目录，必须训练集和测试集同时存在，否则置空） 5. 该数据集的文件是否需要进一步处理（比如需要合并多个表，如果需要请给出合并的方法，否则置空） 6. 任务类型（从多分类，二分类，回归，时间序列四类中选择一个，当冲突时按顺序优先） 7. 该任务是否有多个预测目标（是或否） 8. 任务目标在文件中的列名（输出一个列表） 9. 可用的特征，输出一个列表 10. 是否同时在openml上存在 11. 是否在UCI上存在 12. 是否由其他kaggle数据集处理得到 13. 是否在其他数据网站中出现，如果有，请用列表输出所在的网站 参考输出： 是，application_record.csv,credit_record.csv,,,, 通过 ID 列合并 application_record.csv 和 credit_record.csv,, 二分类，否，['ID', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_PHONE', 'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'MONTHS_BALANCE', 'STATUS'], 否，否，否， 要求： 1 以csv的格式给出输出 2 输出内容不包含表头，不包含其他额外内容 ###"
# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key
    api_key='76107d8c-0565-4d93-b090-022be0e42c0a',
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-pro-32k-character-250715",
    # model="deepseek-r1-250528",
    messages=[
        {"role": "system", "content": role},
        {"role": "user", "content": prompt},
    ],
)
print(completion.choices[0].message.content)
