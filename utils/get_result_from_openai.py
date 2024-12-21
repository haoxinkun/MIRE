#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :get_result_from_openai.py
@说明        :代用openai获取测试结果
@时间        :2024/12/13 11:04:04
@作者        :xinkun hao
@版本        :1.0
'''

import os
import json
import requests
import base64

import pandas as pd



LLM_MODEL_NAME = 'minicpm-2.6'
LLM_ENDPOIN_URL= 'http://192.168.141.233:8034/v1/chat/completions'
api_key= 'token-abc123'


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_gpt_result(messages):
    """_summary_

    Arguments:
        messages {dict list} --   "messages":[{"role":"user","content":query}]

    Returns:
        str -- 回答文本
    """
    
    api_url= LLM_ENDPOIN_URL

    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data={
        "model": LLM_MODEL_NAME,
        "messages": messages, 
        "temperature": 0.1,
        "max_tokens": 64
    }
    
    # response = requests.post(api_url, data=json.dumps(data), headers=headers,  proxies=proxies)
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        result = response.json()
    else:
       raise Exception(f"The LLM service is unavailable {LLM_ENDPOIN_URL} \n info: {response.text}")
        
    return result['choices'][0]['message']['content']


import ast

# 加载test数据
test_data = "/Work/haoxinkun7091/MIRE/data/test1/test1.json"
image_dir = "/Work/haoxinkun7091/MIRE/data/test1/images"
save_data = "/Work/haoxinkun7091/MIRE/data/test1/test1.csv"
test_df = pd.read_csv(save_data)
# 将指定列转换为列表类型
test_df['image'] = test_df['image'].apply(ast.literal_eval)
# test_df["predict"] = ""


for idx, sample in test_df.iterrows():
    if not pd.isna(sample["predict"]):
        continue
    images = sample["image"]
    instruction = sample["instruction"].replace("<image>", "图片已经在开头给出")
    image_paths = [os.path.join(image_dir, image) for image in images]
    print(image_paths)
    base64_images = [encode_image(image_path) for image_path in image_paths]
    messages=[
    {"role": "system", "content": "You are a helpful assistant."}, # 很重要！！！
        {
        "role": "user", 
            "content": [
            {
                "type":"text", 
                "text": instruction
            },
            {
                "type":"image_url",
                "image_url":
                {
                    "url":f"data:image/png;base64,{base64_images}"
                }
            }
        ]
            # "content": f"<img>{image_path}</img>" + "识别图片中菜名返回中文名,返回```json\n{\n  \"name\": \"XXX\"\n}\n``` "
        }]
    answer = get_gpt_result(messages)
    test_df.iloc[idx, -1] = answer
    test_df.to_csv(test_data.replace("json", "csv"))
    # line = [filename.replace(".jpg", ""), answer]
    print(answer)
    # break