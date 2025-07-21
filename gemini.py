# encoding: utf-8
from google import genai
import re
import json
import requests
import os
from utils import logger
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

config = json.load(open('config.json', 'r', encoding='utf-8-sig'))
api_key = config.get('api')
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10), # 指数退避，每次等待 1s, 2s, 4s, 8s, 10s (max_delay=10)
    stop=stop_after_attempt(5),                           # 最多重试 5 次
    retry=retry_if_exception_type((  
        requests.exceptions.ConnectionError
    )),
    reraise=True # 如果所有重试都失败，重新抛出最后一次捕获的异常
)
def agent(url):
    client = genai.Client(api_key=api_key)
    prompt = f"""
As a professional data engineer, you'll analyze user requirements, search the specified webpage ({url}), and extract relevant information based on the following rules:
"""
    rules = """
Is it a tabular classification or tabular regression task? (The task's data type only includes tabular data, with a clear prediction target.)
Data file paths used in this task (Refer to content under class=sc-lixPIL sc-hESRMw cjszVW bDmlrl. The file name must be an accessible CSV file and must appear on the webpage. Assume the task's Data Explorer as the root directory. If the dataset uses fixed training and testing sets, leave this empty.)
Training set path used in this dataset (Assume the task's Data Explorer as the root directory. Both training and testing sets must exist; otherwise, leave this empty.)
Test set path used in this dataset (Assume the task's Data Explorer as the root directory. Both training and testing sets must exist; otherwise, leave this empty.)
Does this dataset require further processing? (e.g., merging multiple tables. If so, provide the merging method in this answer; otherwise, leave empty.)
Task type (Choose one from [multi_classification, binary_classification, regression, time_series]. Do not use quotes. Prioritize in this order if there are conflicts.)
Does this task have multiple prediction targets? (Yes or No)
Column names of the task's targets in the file (Output as a list.)
Available features (Output as a list.)
Does it also exist on OpenML?
Does it exist on UCI?
Is it derived from other Kaggle datasets?
Does it appear on other data websites? (If yes, output the website(s) as a list; otherwise, output "No".)
which domains it most matches? (select one form [
    "Financial Services",
    "Retail & E-commerce",
    "Healthcare & Biotech",
    "Manufacturing & Industrial IoT",
    "Telecommunications",
    "Energy & Utilities",
    "Transportation & Logistics",
    "Agriculture & Food",
    "Real Estate & Urban Planning",
    "Human Resources"
])
Reference Output:
{
  "is_tabular_task": "Yes",
  "data_file_paths": [
    "Churn_Modelling.csv"
  ],
  "training_set_path": null,
  "test_set_path": null,
  "requires_further_processing": "No",
  "task_type": "binary_classification",
  "has_multiple_prediction_targets": "No",
  "target_column_names": [
    "Exited"
  ],
  "available_features": [
    "RowNumber",
    "CustomerId",
    "Surname",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary"
  ],
  "exists_on_openml": "No",
  "exists_on_uci": "No",
  "derived_from_other_kaggle_dataset": "No",
  "appears_on_other_data_websites": [],
  "domain": "Financial Services"
}
Requirements:
Output the result in dictionary format with excatly same key.
The output content must not contain any extra information (e.g., headers or conversational text).
Please check the output format carefully to ensure it meets the requirements.
"""
    # 调用 Gemini API 生成内容
    logger.info(f"Processing {url}...")
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt + rules
    )
    text = response.text.strip()
    logger.info(f"Response for {url}: {text}")
    # 使用正则表达式提取 JSON 字符串

    match = re.search(r'{.*}', text, re.DOTALL)
    if match:
    # 提取匹配到的字符串
      json_string = match.group(0)
      try:
          # 尝试将提取的字符串解析为字典
          data_dict = json.loads(json_string)
      except json.JSONDecodeError as e:
          logger.error(f"解析JSON失败: {e}")
          raise ValueError("无法解析JSON字符串,请检查输出格式是否正确.")
    else:
        logger.error("未找到任何 {} 结构。")
        raise ValueError("输出中未找到JSON格式]]结构,请检查输出内容.")
    return data_dict