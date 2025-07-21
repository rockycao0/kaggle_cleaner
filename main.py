# encoding: utf-8
import pandas as pd
import os
import csv
from gemini import agent
from tqdm import tqdm
from utils import logger
data = pd.read_excel('kaggle筛选是否可用2.xlsx')
csv_file_name = 'kaggle_gemini.csv'
history_file = pd.read_csv(csv_file_name, encoding='utf-8-sig')
history = history_file['dataset_url'].tolist()
fieldnames = [
    'idx',
    'name',
    'dataset_url',
    'is_tabular_task',
    'data_file_paths',
    'training_set_path',
    'test_set_path',
    'requires_further_processing',
    'task_type',
    'has_multiple_prediction_targets',
    'target_column_names',
    'available_features',
    'exists_on_openml',
    'exists_on_uci',
    'derived_from_other_kaggle_dataset',
    'appears_on_other_data_websites',
    'domain'
]
if os.path.exists(csv_file_name):
    file_mode = 'a'
else:
    file_mode = 'w'
with open(csv_file_name, file_mode, newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if file_mode == 'w':
        writer.writeheader()    
    for _, sample in tqdm(data.head(100).iterrows()):
        if sample['dataset_Url'] in history:
            logger.info(f"Skipping {sample['dataset_Url']} as it already exists in history.")
            continue
        else:
            logger.info(f"Processing {sample['dataset_Url']}...")
            info = agent(sample['dataset_Url'])
            info['dataset_url'] = sample['dataset_Url']
            info['idx'] = sample['idx']
            info['name'] = sample['name']
            try:
                writer.writerow(info)
            except Exception as e:
                logger.error(f"When writing to CSV for {sample['dataset_Url']}: {e}")
                raise e
