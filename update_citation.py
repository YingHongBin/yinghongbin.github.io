from scholarly import scholarly
import subprocess
import re

SCHOLAR_USER = "9560QjYAAAAJ"     # Google Scholar user id
TARGET_FILE_EN = '_i18n/en/pages/about.md'
TARGET_FILE_ZH = '_i18n/zh/pages/about.md'

def get_citation():
    print("Querying Google Scholar...")
    author = scholarly.search_author_id(SCHOLAR_USER)
    author = scholarly.fill(author, sections=['indices'])
    return author['citedby']

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

def git_commit_and_push(citation):
    subprocess.run(["git", "config", "user.email", "bot@example.com"])
    subprocess.run(["git", "config", "user.name", "citation-bot"])
    subprocess.run(["git", "add", TARGET_FILE_EN])
    subprocess.run(["git", "add", TARGET_FILE_ZH])
    subprocess.run(["git", "commit", "-m", f"Update citation: {citation:,}"])
    subprocess.run(["git", "push"])
    print("Pushed changes.")

if __name__ == "__main__":
    citation = get_citation()
    update_file(citation)
    git_commit_and_push(citation)