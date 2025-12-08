import re
import os
import requests 

api_key = os.getenv('SERPAPI_KEY')
SCHOLAR_USER = "9560QjYAAAAJ"     # Google Scholar user id
TARGET_FILE_EN = '_i18n/en/pages/about.md'
TARGET_FILE_ZH = '_i18n/zh/pages/about.md'

def get_citation():
    print("Querying Google Scholar...")
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_USER,
        "api_key": api_key
    }

    res = requests.get("https://serpapi.com/search", params=params)
    return res.json()['cited_by']['table'][0]['citations']['all']

def update_file(citation):
    
    # 格式化引用数为千分位逗号格式
    citation_str = f"{citation:,}"
    
    # 正则表达式匹配 "citations of xxxx" 格式,其中 xxxx 是带千分位逗号的数字
    pattern = r'citations of ([\d,]+)'
    replacement = f'citations of {citation_str}'
    
    # 更新英文文件
    with open(TARGET_FILE_EN, 'r', encoding='utf-8') as f:
        content_en = f.read()
    
    content_en = re.sub(pattern, replacement, content_en)
    
    with open(TARGET_FILE_EN, 'w', encoding='utf-8') as f:
        f.write(content_en)
    
    # 更新中文文件
    with open(TARGET_FILE_ZH, 'r', encoding='utf-8') as f:
        content_zh = f.read()
    
    # 中文文件中匹配 "被引用 xxxxx 次" 格式
    pattern_zh = r'被引用 ([\d,]+) 次'
    replacement_zh = f'被引用 {citation_str} 次'
    
    content_zh = re.sub(pattern_zh, replacement_zh, content_zh)
    
    with open(TARGET_FILE_ZH, 'w', encoding='utf-8') as f:
        f.write(content_zh)
    
    print(f"Updated citation to {citation_str}")

if __name__ == "__main__":
    citation = get_citation()
    update_file(citation)