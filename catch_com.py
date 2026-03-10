import bibtexparser
import requests
import os
import time
import re

# ================= 設定區 =================
# 您的 bib 檔案名稱 (請確認檔案名稱是否正確)
bib_filename = 'ConnectedPapers-for-TradingAgent.bib'

# 下載存放的資料夾名稱
output_folder = 'TradingAgents_Papers'
# =========================================

def sanitize_filename(filename):
    """移除檔案名稱中的非法字元，避免存檔失敗"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_pdf(url, save_path):
    """下載 PDF 的核心函式"""
    try:
        # 偽裝成瀏覽器，避免被擋
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            print(f"   [!] 下載失敗 (Status code: {response.status_code})")
            return False
    except Exception as e:
        print(f"   [!] 發生錯誤: {e}")
        return False

def main():
    # 1. 檢查並建立資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"[*] 已建立資料夾: {output_folder}")

    # 2. 讀取 BibTeX 檔案
    if not os.path.exists(bib_filename):
        print(f"[Error] 找不到檔案: {bib_filename}，請確認路徑。")
        return

    with open(bib_filename, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    entries = bib_database.entries
    total = len(entries)
    print(f"[*] 成功讀取 {total} 篇文獻資料，開始下載...\n")

    success_count = 0
    fail_list = []

    # 3. 逐一下載
    for index, entry in enumerate(entries):
        title = entry.get('title', 'Untitled').replace('\n', ' ')
        year = entry.get('year', 'Unknown')
        
        # 嘗試取得 arXiv ID
        arxiv_id = entry.get('arxivid')
        
        # 如果 arxivid 欄位是空的，嘗試從 url 或 doi 判斷 (有些 BibTeX 格式不同)
        if not arxiv_id:
            if 'arxiv.org' in entry.get('url', ''):
                # 簡單從 URL 提取 ID (例如 https://arxiv.org/abs/2412.20138)
                match = re.search(r'arxiv\.org/(?:abs|pdf)/([\d\.]+)', entry.get('url', ''))
                if match:
                    arxiv_id = match.group(1)

        # 準備檔案名稱: "2024 - 論文標題.pdf"
        safe_title = sanitize_filename(title)
        # 限制檔名長度避免過長報錯
        if len(safe_title) > 150:
            safe_title = safe_title[:150] + "..."
            
        filename = f"{year} - {safe_title}.pdf"
        save_path = os.path.join(output_folder, filename)

        print(f"[{index+1}/{total}] 正在處理: {title[:50]}...")

        # 判斷是否可以下載
        if os.path.exists(save_path):
            print("   [O] 檔案已存在，跳過。")
            success_count += 1
            continue

        if arxiv_id:
            # 建構 arXiv PDF 連結
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            print(f"   -> 發現 arXiv ID: {arxiv_id}，開始下載...")
            
            if download_pdf(pdf_url, save_path):
                print("   [V] 下載成功！")
                success_count += 1
                # 禮貌性延遲，避免對 arXiv 伺服器造成過大壓力
                time.sleep(1) 
            else:
                fail_list.append(title)
        else:
            print("   [X] 非 arXiv 論文或找不到 ID，跳過。")
            fail_list.append(title)

    # 4. 總結
    print("\n" + "="*30)
    print(f"任務完成！")
    print(f"成功下載: {success_count} 篇")
    print(f"未下載: {len(fail_list)} 篇")
    
    if fail_list:
        print("\n以下論文需手動檢查 (可能為 IEEE/ACM 付費論文或非公開資源):")
        for t in fail_list:
            print(f"- {t}")

if __name__ == "__main__":
    main()
