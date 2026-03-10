# BibTeX to arXiv PDF Auto-Fetcher 🤖📚

這是一個輕量、穩健且高度自動化的 Python 爬蟲腳本，專為學術研究與文獻整理設計。只要提供一份標準的 `.bib` (BibTeX) 檔案，本程式就能自動解析文獻資料，精準鎖定 arXiv 論文，並將 PDF 檔案自動下載、重新命名與歸檔。

## ✨ 核心特色 (Features)

* **🧠 智慧解析與特徵回退 (Smart Extraction & Fallback)**
    使用 `bibtexparser` 精準讀取 BibTeX 結構。當文獻缺少明確的 `arxivid` 欄位時，程式會自動啟動 Regex 正規表達式，從 URL 或備用欄位中反向萃取 ID，大幅提升下載命中率。
* **🛡️ 檔案系統防護 (Robust File I/O)**
    內建 `sanitize_filename` 機制，自動過濾作業系統不允許的非法字元（如 `\/*?:"<>|`），並動態限制檔名長度（最大 150 個字元），完美避免因論文標題過長或含特殊符號而導致的存檔崩潰。
* **🚦 斷點續傳與冪等性 (Idempotent Execution)**
    每次下載前會自動檢查硬碟中是否已存在該檔案。若檔案已存在則無縫跳過，支援隨時中斷與重新執行，不浪費任何網路頻寬。
* **🕵️‍♂️ 網路禮儀與防阻擋 (Anti-Scraping & Politeness)**
    內建 User-Agent 偽裝機制，並採用串流寫入 (Streaming) 大幅降低記憶體佔用。同時實作了禮貌性延遲 (`time.sleep`)，避免對 arXiv 伺服器造成過大壓力而遭封鎖 IP。

## 🛠️ 事前準備 (Prerequisites)

請確保你的開發環境已安裝 Python 3.7+。
請使用專案內附的 `requirements.txt` 安裝必要的外部依賴套件：

```pip install -r requirements.txt```

Note: requirements.txt 內容僅包含 bibtexparser 與 requests。

🚀 使用方法 (Usage)
準備文獻庫： 將你的 BibTeX 檔案（例如 ConnectedPapers-for-TradingAgent.bib）放入與腳本相同的目錄下。

設定參數 (可選)： 打開 catch_com.py，你可以在腳本開頭的設定區修改輸入的檔名與輸出的資料夾名稱：
```
Python
# ================= 設定區 =================
bib_filename = 'ConnectedPapers-for-TradingAgent.bib' # 你的 bib 檔案名稱
output_folder = 'TradingAgents_Papers'              # 下載存放的資料夾名稱
# =========================================
```
執行腳本：

```python catch_com.py```
驗收成果： 程式執行完畢後，所有成功下載的論文將會以 YYYY - 論文標題.pdf 的格式，整齊地存放在你指定的資料夾中。

📊 執行報告與注意事項
程式執行結束後，會在終端機印出詳細的成功/失敗統計報告。

未下載清單 (Fail List)： 若遇到非開源的付費論文（如 IEEE / ACM 數位圖書館的專屬文獻），或者非 arXiv 來源的項目，程式會自動將其記錄在失敗清單中，方便使用者後續進行手動查閱與下載。
