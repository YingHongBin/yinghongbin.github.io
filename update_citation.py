import re
import requests 

SCHOLAR_USER = "9560QjYAAAAJ"     # Google Scholar user id
TARGET_FILE_EN = '_i18n/en/pages/about.md'
TARGET_FILE_ZH = '_i18n/zh/pages/about.md'

def get_citation():
    print("Querying Google Scholar...")
    url = f"https://scholar.google.com/citations?user={SCHOLAR_USER}&hl=en"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # 使用正则表达式提取引用数
    # Google Scholar页面中引用数通常在 "Cited by" 后面
    pattern = r'<td class="gsc_rsb_std">(\d+)</td>'
    match = re.search(pattern, response.text)
    
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Could not find citation count in Google Scholar page")

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