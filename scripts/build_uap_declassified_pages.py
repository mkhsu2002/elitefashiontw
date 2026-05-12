#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "uap-ufo-declassified"
BASE_URL = "https://tw.elitefasion.com"
CHECK_DATE = "2026 年 5 月 12 日"
PUBLISHED_ISO = "2026-05-12T00:00:00-07:00"
MODIFIED_ISO = "2026-05-12T00:00:00-07:00"


GUIDES = [
    {
        "slug": "pursue-release-01",
        "title": "PURSUE Release 01 解密入口：2026 年第一批美國官方 UAP 檔案怎麼讀",
        "short_title": "PURSUE Release 01 解密入口",
        "description": "繁中深讀 2026 年 5 月 8 日 WAR.GOV/UFO 第一批 PURSUE UAP 解密檔案，說明官方稱為 unresolved cases 的公開背景、素材限制與事件意義。",
        "keywords": ["PURSUE Release 01", "WAR.GOV UFO", "UAP 解密 2026", "美國 UFO 檔案", "UAP unresolved cases"],
        "record_type": "官方入口、新聞稿、解密檔案總覽",
        "official_name": "Presidential Unsealing and Reporting System for UAP Encounters (PURSUE)",
        "agency": "U.S. Department of War、ODNI、AARO、NASA、FBI 等跨機構",
        "record_date": "2026-05-08",
        "status": "公開、滾動新增；官方稱多數材料尚未完成異常解析",
        "summary": "PURSUE Release 01 是目前最有話題性的入口，因為它把新近解密的影片、照片與原始文件放在同一個官方頁面，並宣告後續仍會分批新增。讀者最容易誤讀的地方，是把「已解密」等同於「已證實外星來源」；但官方頁面明確把這批材料定位為 unresolved cases，也就是政府暫時無法做出定論，原因可能只是資料量不足、脈絡不完整或仍待分析。",
        "why": [
            "它是 2026 年 5 月 8 日後的新入口，具備強烈搜尋新鮮度。",
            "關鍵詞可涵蓋 WAR.GOV/UFO、PURSUE、UAP files、declassified UFO files、unresolved UAP records。",
            "適合做為所有新解密資料的總導覽，並把讀者導回 10 篇子頁。"
        ],
        "reading_points": [
            "先看 Release Date 與 Incident Date，避免把公開日期誤認為事件日期。",
            "Type 可能是 PDF、image 或 video，文字頁應優先解析原始說明與 metadata。",
            "unresolved 代表資料不足以歸因，不代表官方支持任何外星結論。",
            "若官方尚未完成解析，文章應使用「目前公開資料顯示」而非「證實」。"
        ],
        "seo_angles": ["2026 UAP 解密", "PURSUE UFO files", "WAR.GOV UFO 中文", "美國 UFO 檔案怎麼看"],
        "sources": [
            ("Department of War release", "https://www.war.gov/News/Releases/Release/Article/4480582/department-of-war-releases-unidentified-anomalous-phenomena-files-in-historic-t/"),
            ("WAR.GOV/UFO PURSUE portal", "https://www.war.gov/UFO/"),
            ("AARO UAP Records", "https://www.aaro.mil/UAP-Records/")
        ],
    },
    {
        "slug": "nasa-astronaut-uap-transcripts",
        "title": "NASA 太空任務對話紀錄導讀：Gemini、Apollo 觀測與 UAP 搜尋熱點",
        "short_title": "NASA 太空任務對話紀錄",
        "description": "整理 NASA 與 PURSUE 釋出的 Gemini、Apollo 任務紀錄，從太空人對話、任務照片與官方科學框架理解太空異常觀測。",
        "keywords": ["NASA UAP", "Gemini 7 UFO", "Apollo UFO", "太空人對話紀錄", "月球異常光點"],
        "record_type": "任務紀錄、對話紀錄、照片與研究報告",
        "official_name": "NASA mission records and UAP Independent Study materials",
        "agency": "NASA、Department of War PURSUE",
        "record_date": "1960s-1970s；2023-2026 公開整理",
        "status": "公開資料；多數需以任務脈絡與影像 metadata 重新判讀",
        "summary": "太空任務紀錄之所以吸引人，是因為它們同時具備人類登月、太空人即時語音與未知物體觀測三種敘事張力。繁中頁面應把焦點放在紀錄本身：誰在什麼任務階段說了什麼、當時是否有推進器、碎片、星體、反光或攝影條件可供排除，而不是直接把模糊光點包裝成結論。",
        "why": [
            "Gemini、Apollo、月球光點等詞本身具有高搜尋量與社群傳播性。",
            "NASA 官方 UAP 報告提供了科學方法框架，可補足歷史紀錄的解讀限制。",
            "適合承接「太空人看到 UFO 嗎」「Apollo 11 UFO」「Gemini 7 bogey」等長尾查詢。"
        ],
        "reading_points": [
            "逐段區分 mission transcript、onboard voice、technical air-to-ground voice transcript。",
            "把可疑物件放回任務時間線，檢查艙段、級間分離、伴飛物與視角。",
            "NASA 2023 報告提醒，沒有校準資料與 metadata 時，目擊紀錄不宜直接下定論。",
            "子頁可用「觀測紀錄」與「官方科學限制」雙欄呈現，降低獵奇感。"
        ],
        "seo_angles": ["NASA UFO 中文", "Apollo UAP 對話", "Gemini 7 UFO 紀錄", "月球 UAP 光點"],
        "sources": [
            ("NASA UAP Independent Study", "https://science.nasa.gov/uap/"),
            ("NASA UAP final report PDF", "https://www.nasa.gov/wp-content/uploads/2023/09/uap-independent-study-team-final-report-0.pdf"),
            ("WAR.GOV/UFO PURSUE portal", "https://www.war.gov/UFO/")
        ],
    },
    {
        "slug": "congress-2023-uap-hearing",
        "title": "2023 美國國會 UAP 聽證逐字稿：Graves、Grusch、Fravor 的證詞怎麼讀",
        "short_title": "2023 美國國會 UAP 聽證逐字稿",
        "description": "繁中導讀 2023 年 7 月 26 日美國眾議院 UAP 聽證逐字稿，整理三位證人的主張、問題焦點與官方查核限制。",
        "keywords": ["UAP hearing transcript", "David Grusch", "Ryan Graves", "David Fravor", "美國國會 UFO 聽證"],
        "record_type": "國會聽證逐字稿與證人書面證詞",
        "official_name": "Unidentified Anomalous Phenomena: Implications on National Security, Public Safety, and Government Transparency",
        "agency": "U.S. House Committee on Oversight and Accountability / Congress.gov",
        "record_date": "2023-07-26",
        "status": "公開國會紀錄；證詞需和 AARO、DoD、NASA 後續報告交叉閱讀",
        "summary": "這場聽證把 UAP 從網路謠言拉回公開問責場景。Ryan Graves 強調飛航安全與通報機制，David Grusch 提出政府隱匿與回收計畫相關主張，David Fravor 則以 2004 年 Tic Tac 經驗作為飛行員證詞。頁面應把三人的角色、證詞屬性與證據層級分開，而不是把所有陳述合併成單一結論。",
        "why": [
            "Grusch、Fravor、Graves 是近年 UAP 搜尋量最高的人名組合之一。",
            "逐字稿可做對話式導讀，讓讀者直接理解問答脈絡。",
            "讀者常從「美國國會 UFO 聽證」「UAP whistleblower」「non-human biologics」等詞進入。"
        ],
        "reading_points": [
            "證詞是國會紀錄，不等於每項主張都已被官方證實。",
            "Grusch 的主張需和 AARO Historical Record Report 的後續查核分開對照。",
            "Graves 的重點偏向飛航安全與通報 stigma，較適合政策角度。",
            "Fravor 的重點是飛行員目視經驗，應與 FLIR 影片、雷達與官方影像分層閱讀。"
        ],
        "seo_angles": ["UAP hearing 中文", "David Grusch 證詞", "Ryan Graves UAP", "Fravor Tic Tac testimony"],
        "sources": [
            ("Congress.gov hearing text", "https://www.congress.gov/event/118th-congress/house-event/116282/text"),
            ("Congress.gov hearing overview", "https://www.congress.gov/event/118th-congress/house-event/116282"),
            ("AARO Historical Record Report", "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf")
        ],
    },
    {
        "slug": "navy-tic-tac-fravor",
        "title": "Tic Tac 事件與 Fravor 證詞：2004 年美國海軍 UAP 案例導讀",
        "short_title": "Tic Tac 事件與 Fravor 證詞",
        "description": "整理 2004 年 Tic Tac / FLIR1 事件、David Fravor 國會證詞與 NAVAIR/DVIDS 影像脈絡，說明影片、目擊與官方結論的差異。",
        "keywords": ["Tic Tac UFO", "FLIR1 UAP", "David Fravor", "Nimitz UAP", "美國海軍 UFO 影片"],
        "record_type": "國會證詞、軍方影像、公開影像資料",
        "official_name": "FLIR / Tic Tac UAP case and 2023 House testimony",
        "agency": "NAVAIR、DVIDS、Congress.gov",
        "record_date": "2004 事件；2020 影像公開；2023 聽證",
        "status": "公開影像與證詞；官方未將其判定為外星技術",
        "summary": "Tic Tac 是近代 UAP 討論中最容易被搜尋到的案例之一，原因在於它同時有飛行員證詞、公開軍方影像與多年媒體討論。適合的導讀方式，是把 Fravor 的目視描述、NAVAIR/DoD 公開影像、後續 AARO 或國會紀錄分開列出，讓讀者知道哪些是親歷敘述、哪些是影片中實際可見的資訊。",
        "why": [
            "Tic Tac、Nimitz、FLIR1 是全球 UAP 搜尋核心詞。",
            "它可連回主頁既有官方影像區，補足文字解說深度。",
            "能教育讀者理解「影片公開」和「官方歸因」不是同一件事。"
        ],
        "reading_points": [
            "不要只看單一影片截圖，需同時看飛行員證詞與官方來源。",
            "目視敘述與感測器畫面各有盲點，兩者互補但不能互相替代。",
            "官方公開影片不代表已公布所有雷達、任務或情報資料。",
            "標題可使用 Tic Tac，但內文須保留 FLIR / NAVAIR / DVIDS 等可查詞。"
        ],
        "seo_angles": ["Tic Tac UFO 中文", "Nimitz UAP 2004", "Fravor 證詞", "FLIR1 影片解讀"],
        "sources": [
            ("Congress.gov hearing text", "https://www.congress.gov/event/118th-congress/house-event/116282/text"),
            ("DVIDS FLIR UAP", "https://www.dvidshub.net/video/955825/flir-uap"),
            ("DVIDS Copyright", "https://www.dvidshub.net/about/copyright")
        ],
    },
    {
        "slug": "fbi-guy-hottel-memo",
        "title": "FBI Guy Hottel 備忘錄：最熱門 UFO 文件為何不是 Roswell 證據",
        "short_title": "FBI Guy Hottel 備忘錄",
        "description": "繁中導讀 FBI Vault 最熱門 UFO 文件 Guy Hottel memo，說明三個飛碟與小型人形遺體說法的來源層級、FBI 未調查狀態與 Roswell 誤讀。",
        "keywords": ["Guy Hottel memo", "FBI Vault UFO", "New Mexico flying saucers", "Roswell FBI", "FBI UFO 文件"],
        "record_type": "FBI 備忘錄與 Vault 文件",
        "official_name": "March 22, 1950 Guy Hottel memo",
        "agency": "Federal Bureau of Investigation",
        "record_date": "1950-03-22；FBI 2013 說明頁",
        "status": "公開；FBI 說明為未查證的二手或三手說法",
        "summary": "Guy Hottel memo 迷人的地方，是它用很短的篇幅聚集了飛碟、New Mexico、雷達干擾與小型人形遺體等爆炸性元素。但 FBI 自己的說明同時指出，這不是 Roswell 證據，也不是 FBI 調查後的結論，而是一則未被追查的轉述。子頁應以「為什麼熱門」和「為什麼不能當證據」雙線處理。",
        "why": [
            "它長期是 FBI Vault 最受注目的 UFO 文件之一。",
            "標題含 FBI、New Mexico、flying saucers、Roswell 等高搜尋詞。",
            "適合做媒體素養型解說，提醒讀者分辨原始文件與證據強度。"
        ],
        "reading_points": [
            "先確認文件日期：1950 年 3 月 22 日，晚於 1947 年 Roswell。",
            "它是轉述資訊，不是 FBI 現場調查報告。",
            "FBI 說明該 memo 不證明 UFO 存在，也沒有後續評估。",
            "可引用文件脈絡，但不要把 memo 標成官方證實。"
        ],
        "seo_angles": ["FBI UFO memo 中文", "Guy Hottel 備忘錄", "Roswell FBI 文件", "New Mexico flying saucers"],
        "sources": [
            ("FBI story: UFOs and the Guy Hottel Memo", "https://www.fbi.gov/news/stories/ufos-and-the-guy-hottel-memo"),
            ("FBI Vault UFO collection", "https://vault.fbi.gov/UFO"),
            ("FBI Vault Guy Hottel file", "https://vault.fbi.gov/hottel_guy/Guy%20Hottel%20Part%2001%20%28Final%29/view")
        ],
    },
    {
        "slug": "cia-robertson-panel-durant-report",
        "title": "CIA Robertson Panel 與 Durant Report：1953 年 UFO 科學顧問會議導讀",
        "short_title": "CIA Robertson Panel 與 Durant Report",
        "description": "深讀 CIA Reading Room 中 Robertson Panel、Durant Report 與 CIA UFO 研究史文件，理解 1953 年科學顧問會議如何影響後續 UFO 檔案公開。",
        "keywords": ["Robertson Panel", "Durant Report", "CIA UFO Special Collection", "CIA Reading Room UFO", "1953 UFO panel"],
        "record_type": "CIA FOIA 文件、會議紀錄、歷史研究",
        "official_name": "Report of Meetings of the Office of Scientific Intelligence Scientific Advisory Panel on UFOs",
        "agency": "Central Intelligence Agency",
        "record_date": "1953-01-14 至 1953-01-18；FOIA release metadata 2011",
        "status": "公開 FOIA 文件；需搭配 CIA 歷史研究閱讀",
        "summary": "Robertson Panel 是理解冷戰早期 UFO 政策的關鍵文字紀錄。它不只是討論『UFO 是什麼』，更反映情報機構如何看待公眾恐慌、空防警報、媒體傳播與科學審查。Durant Report 則提供會議整理，使讀者能看到專家如何把零散目擊轉化為政策建議。",
        "why": [
            "Robertson Panel 與 Durant Report 是 CIA UFO Special Collection 核心搜尋詞。",
            "它能承接「CIA UFO files」「CIA Reading Room UFO」等長尾搜尋。",
            "適合補強主頁的歷史檔案深度，而不與影像案例互搶。"
        ],
        "reading_points": [
            "把 1953 年冷戰空防背景放進解讀，不宜只用現代外星敘事套入。",
            "會議紀錄重點是風險、資料品質與公眾溝通，不是單一事件證明。",
            "CIA 1997/1999 歷史文章可用來理解其後 FOIA 與去機密化脈絡。",
            "頁面應保留 Document Number、Release Decision、Document Page Count 等索引資訊。"
        ],
        "seo_angles": ["CIA UFO 中文", "Robertson Panel 導讀", "Durant Report UFO", "CIA Reading Room UFO 文件"],
        "sources": [
            ("CIA Robertson/Durant report document", "https://www.cia.gov/readingroom/document/0005516128"),
            ("CIA role in UFO study document", "https://www.cia.gov/readingroom/document/0005517742"),
            ("CIA UFO Special Collection", "https://www.cia.gov/readingroom/keyword/ufo-special-collection")
        ],
    },
    {
        "slug": "project-blue-book-fact-sheet",
        "title": "Project Blue Book 官方 Fact Sheet：12618 件報告與 701 件未識別怎麼看",
        "short_title": "Project Blue Book 官方 Fact Sheet",
        "description": "深讀 NARA Project Blue Book 官方頁與美國空軍 Fact Sheet，理解 12,618 件 UFO 報告、701 件未識別與三項官方結論。",
        "keywords": ["Project Blue Book", "藍皮書計畫", "701 unidentified", "12618 sightings", "美國空軍 UFO"],
        "record_type": "NARA 研究指南、空軍 Fact Sheet、微縮膠卷索引",
        "official_name": "Project BLUE BOOK - Unidentified Flying Objects",
        "agency": "U.S. Air Force / National Archives",
        "record_date": "1947-1969；NARA 頁面 2024 reviewed",
        "status": "計畫已結束、檔案去機密化並移交 NARA",
        "summary": "Project Blue Book 是所有 UFO 解密導讀最需要的一塊地基。它提供可被引用的總數、未識別件數與官方結論，也提醒讀者：未識別並不等於外星。讀者若搜尋『藍皮書計畫』『Project Blue Book 中文』『701 件未識別』，這頁能直接給出官方脈絡。",
        "why": [
            "它是歷史 UFO 檔案最常被搜尋的官方計畫。",
            "數字清楚，可做資訊圖表與 FAQ。",
            "NARA 頁面同時提供微縮膠卷、照片、影音與研究指南入口。"
        ],
        "reading_points": [
            "12,618 是報告總數，701 是仍標示未識別的數量。",
            "空軍結論沒有指出國安威脅、超出當時科學技術或外星載具證據。",
            "Project Blue Book 關閉於 1969 年，之後事件不能直接歸入該計畫。",
            "若談具體案例，應再回到日期、地點與原始 case file。"
        ],
        "seo_angles": ["Project Blue Book 中文", "藍皮書計畫 UFO", "701 unidentified UFO", "美國空軍 UFO 檔案"],
        "sources": [
            ("NARA Project BLUE BOOK", "https://www.archives.gov/research/military/air-force/ufos"),
            ("NARA RG 615 UAP collection", "https://www.archives.gov/research/topics/uaps/rg-615"),
            ("AARO Historical Record Report", "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf")
        ],
    },
    {
        "slug": "roswell-report-official-records",
        "title": "Roswell 官方檔案導讀：氣球計畫、GAO 查核與外星材料說法",
        "short_title": "Roswell 官方檔案導讀",
        "description": "整理 NARA Roswell Incident 說明與美國空軍調查脈絡，說明官方如何查核 1947 年 Roswell 事件、氣球計畫材料與外星遺體說法。",
        "keywords": ["Roswell Report", "Roswell Incident", "Project Mogul", "羅斯威爾事件", "UFO 外星材料"],
        "record_type": "NARA 說明、空軍調查、GAO 相關脈絡",
        "official_name": "The Roswell Report: Fact vs. Fiction in the New Mexico Desert",
        "agency": "U.S. Air Force / National Archives / GAO context",
        "record_date": "1947 事件；1994-1995 調查發布",
        "status": "相關文件已解密並屬公開領域；官方未找到外星材料或外星遺體證據",
        "summary": "Roswell 是 UFO 史上最有流量的關鍵詞之一，但官方檔案導讀必須很克制。NARA 說明 Project Blue Book 檔案中找不到討論 1947 Roswell 事件的文件；空軍後續查核則把回收材料指向當時機密氣球計畫相關設備，而不是外星載具。",
        "why": [
            "Roswell、Project Mogul、alien bodies 是長年熱門搜尋詞。",
            "它能把陰謀論流量轉化為官方資料閱讀。",
            "與 FBI Guy Hottel memo 可互相內鏈，澄清 New Mexico 與 Roswell 混淆。"
        ],
        "reading_points": [
            "先區分 1947 事件、1990 年代空軍調查與後來媒體敘事。",
            "不要把 Guy Hottel memo 的 New Mexico 轉述直接接到 Roswell。",
            "NARA 頁面明確說 Project Blue Book records 中未定位到 Roswell 事件討論文件。",
            "官方結論指向氣球計畫材料，且未找到外星材料或遺體紀錄。"
        ],
        "seo_angles": ["Roswell 中文", "羅斯威爾事件官方報告", "Project Mogul UFO", "Roswell alien bodies 查核"],
        "sources": [
            ("NARA Project BLUE BOOK and Roswell Incident", "https://www.archives.gov/research/military/air-force/ufos"),
            ("AARO Historical Record Report", "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"),
            ("FBI Guy Hottel memo explanation", "https://www.fbi.gov/news/stories/ufos-and-the-guy-hottel-memo")
        ],
    },
    {
        "slug": "aaro-historical-record-report",
        "title": "AARO Historical Record Report 導讀：美國政府是否找到外星技術證據",
        "short_title": "AARO Historical Record Report 導讀",
        "description": "繁中整理 AARO 2024 Historical Record Report Volume I，說明美國政府歷來 UAP 調查、逆向工程主張、資料品質限制與主要結論。",
        "keywords": ["AARO Historical Record Report", "off-world technology", "UAP reverse engineering", "AARO 報告 中文", "UAP 歷史報告"],
        "record_type": "AARO 官方歷史報告 PDF",
        "official_name": "Report on the Historical Record of U.S. Government Involvement with UAP, Volume I",
        "agency": "All-domain Anomaly Resolution Office",
        "record_date": "2024-02；公開於 2024-03",
        "status": "公開未機密報告；Volume II 另行處理後續資料",
        "summary": "AARO Historical Record Report 是近年官方回應『美國政府是否藏有外星科技』最重要的長篇文字。它回顧 1945 年以來調查計畫，並對 off-world technology、reverse-engineering、NDA、KONA BLUE、材料樣本等主張逐一做出查核。它的內容不刺激，卻是最能建立可信度的核心頁。",
        "why": [
            "AARO 報告是所有現代 UAP 主張的官方查核基準。",
            "可承接 off-world technology、reverse engineering、UAP report 中文等搜尋。",
            "能把聽證證詞、KONA BLUE、ORNL 材料分析串成完整閱讀路徑。"
        ],
        "reading_points": [
            "AARO 表示未找到任何 UAP 被確認為外星技術的證據。",
            "許多未解案例的共同問題是資料品質不足，而不是必然存在異常技術。",
            "報告將歷史計畫、訪談主張與敏感計畫查核分段處理，閱讀時不可混在一起。",
            "文章可用時間線呈現 Project Sign、Grudge、Blue Book、AAWSAP/AATIP、UAPTF、AARO。"
        ],
        "seo_angles": ["AARO 報告 中文", "UAP 歷史報告", "off-world technology evidence", "美國政府外星科技查核"],
        "sources": [
            ("AARO Historical Record Report PDF", "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"),
            ("AARO UAP Records", "https://www.aaro.mil/UAP-Records/"),
            ("Congress.gov UAP hearing", "https://www.congress.gov/event/118th-congress/house-event/116282/text")
        ],
    },
    {
        "slug": "kona-blue-ornl-materials",
        "title": "KONA BLUE 與 ORNL 材料分析：外星材料與逆向工程主張的官方查核",
        "short_title": "KONA BLUE 與 ORNL 材料分析",
        "description": "深讀 AARO UAP Records 中 KONA BLUE、ORNL 金屬樣本分析與 alleged alien material 主張，理解敏感計畫提案、材料檢測與官方結論。",
        "keywords": ["KONA BLUE", "ORNL UAP specimen", "alien alloy", "UAP material analysis", "外星材料 分析"],
        "record_type": "AARO 資訊文件、ORNL 材料分析摘要、AARO 補充說明",
        "official_name": "DHS KONA BLUE Information Release and ORNL material specimen analyses",
        "agency": "AARO、DHS、Oak Ridge National Laboratory",
        "record_date": "2024-2025 公開資料",
        "status": "公開；KONA BLUE 未獲批准，材料樣本被判定為普通地球合金或一般用途鋁合金",
        "summary": "KONA BLUE 與 ORNL 材料分析很適合作為『最吸引人但最需要冷靜』的子頁。前者牽涉 alleged non-human biologics、回收與逆向工程的 proposed SAP；後者則是把所謂外星材料送進實驗室後，回到成分、結構與製造來源的普通問題。這頁能讓讀者看到官方如何把高概念主張拆成可驗證欄位。",
        "why": [
            "KONA BLUE 是 AARO 報告中最容易引發討論的專有名詞之一。",
            "外星材料、合金、ORNL 分析等詞有強烈搜尋吸引力。",
            "它能把神秘主張導向可驗證科學與文件證據。"
        ],
        "reading_points": [
            "KONA BLUE 被描述為 proposed SAP，AARO 表示未被 DHS 正式批准或建立。",
            "AARO 表示 KONA BLUE 沒有收到材料或資金，公開資料僅限 proposal presentation。",
            "ORNL 針對金屬樣本的分析重點是元素、結構與製造一致性。",
            "若要寫吸睛標題，內文仍須清楚寫出官方查核結論。"
        ],
        "seo_angles": ["KONA BLUE 中文", "ORNL 外星材料", "UAP 金屬樣本", "alien alloy fact check"],
        "sources": [
            ("AARO UAP Records", "https://www.aaro.mil/UAP-Records/"),
            ("AARO Historical Record Report PDF", "https://www.aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf"),
            ("Oak Ridge National Laboratory", "https://www.ornl.gov/")
        ],
    },
]


REPORTS = {
    "pursue-release-01": {
        "lede": "這不是單一 UFO 案件，而是一個新檔案櫃被打開的時刻。2026 年 5 月 8 日，PURSUE 把影片、照片、任務紀錄與歷史文件放到同一個官方入口；最重要的訊號不是「政府證實了什麼」，而是政府承認仍有一批 unresolved UAP records 需要被公開、被讀懂、被外部重新檢視。",
        "timeline": [
            "2026 年 2 月 19 日：川普在公開指令中要求啟動與 UAP、UFO、外星生命相關政府文件的辨識與釋出。",
            "2026 年 5 月 8 日：Department of War 宣布 PURSUE Release 01，表示這是滾動公開的第一批。",
            "Release 01 入口同時列出西部美國紅外線影像、Apollo 任務影像、軍事操作員回報影片、非洲與中東案例等素材。",
            "官方說明強調，頁面收錄的是 unresolved cases；也就是政府尚無法對現象本質做出最終判定。"
        ],
        "sections": [
            {
                "heading": "像一間突然開燈的檔案室",
                "paragraphs": [
                    "PURSUE 的閱讀感不像傳統新聞稿。它更像一間政府檔案室突然打開燈：架上有近年的紅外線截圖，有太空任務影像，有軍事操作員回報，也有歷史文件。它沒有把讀者帶到一個戲劇性結論，而是把不同年代、不同機構、不同品質的材料推到同一張桌上。",
                    "這正是它有趣也危險的地方。對一般讀者來說，『已解密』很容易被聽成『已證實』；但這批資料真正說的是：有些案例已經通過安全審查可以公開，但還沒有被充分分析到足以歸因。換句話說，PURSUE 是透明度工程，不是外星答案發布會。"
                ]
            },
            {
                "heading": "官方真正交代了什麼",
                "paragraphs": [
                    "Department of War 的新聞稿說，這是跨機構工作，牽涉白宮、ODNI、DOE、AARO、NASA、FBI 與情報體系其他單位。官方把重點放在『集中入口』：過去散落於各機構、平台與檔案館的 UAP 材料，現在以一個公開頁面逐批釋出。",
                    "PURSUE 頁面還明確說，這些材料屬於未解案例；未解的原因可能包括資料不足、感測器紀錄不完整、缺乏多角度佐證，或只有單一觀測來源。這句話很關鍵，因為它同時保留神祕性與方法論：讀者可以懷疑、分析、比對，但不能跳過資料品質直接抵達結論。"
                ]
            },
            {
                "heading": "Release 01 裡最吸引人的元素",
                "paragraphs": [
                    "第一批檔案的敘事張力來自素材本身的混合：近年美國西部上空的紅外線不明物體、Apollo 17 月面影像中被框出的亮點、操作員螢幕裡快速掠過的物體、接近阿拉伯聯合大公國的影片、以及非洲空域裡被回報的紅外線目標。每一項都足以成為社群上的單獨話題。",
                    "但如果以雜誌報導角度閱讀，最值得追的不是哪一張圖最像飛碟，而是每份材料缺了什麼。它有沒有時間戳？有沒有平台位置？有沒有距離、速度、方位、感測器型號？有沒有同時被雷達、紅外線與目視捕捉？答案越少，故事越神祕；但證據也越薄。"
                ]
            },
            {
                "heading": "讀者應該帶走的結論",
                "paragraphs": [
                    "PURSUE Release 01 的價值，是讓大眾第一次能用官方入口看到一批新釋出的 unresolved UAP materials。它不要求你相信，也不替你下結論；它把材料擺出來，讓外部研究者、媒體與一般讀者有機會一起檢查。",
                    "所以這篇的核心不是『政府終於承認外星人』，而是『政府承認還有大量材料需要公開與分析』。真正精彩的閱讀方式，是把每一份影像和文字都當成一個待補完的案卷：先看它說了什麼，再看它沒有說什麼。"
                ]
            }
        ],
    },
    "nasa-astronaut-uap-transcripts": {
        "lede": "太空任務裡的不明物體，最迷人的地方不是它們一定來自外星，而是人類在最孤獨的環境裡留下了非常人性的反應：看見、確認、排除、再把疑問交給地面。Gemini 與 Apollo 的紀錄把神祕感放在無線電雜訊、窗外亮點與任務節奏之間。",
        "timeline": [
            "1965 年 12 月：Gemini VII 執行近 14 天長航太任務，期間船員回報看見明亮物體與大量粒子。",
            "1969 年 7 月：Apollo 11 往返月球期間，船員曾討論窗外物體、艙內閃光與不明光源。",
            "1972 年 12 月：Apollo 17 任務影像與對話紀錄後來被納入 UAP 討論，尤其是月面上方亮點與閃光描述。",
            "2023 年：NASA UAP Independent Study 強調，沒有充分校準資料與 metadata 的影像，不應被過度解讀。"
        ],
        "sections": [
            {
                "heading": "太空人看到的是什麼，為什麼大家一直想知道",
                "paragraphs": [
                    "NASA 任務紀錄的魅力，在於它們不是後來加工的傳說，而是任務進行中留下的語音、技術紀錄與照片。當太空人說窗外有一個物體，或描述亮點、閃光、粒子，讀者自然會屏住呼吸：在地球之外，那個被看見的東西究竟是什麼？",
                    "但太空任務不是空白舞台。艙外可能有火箭級、面板、冰晶、碎片、反光、星體、相機雜訊或姿態控制造成的視覺效果。好的報導不能把『不明』寫成『非人類』，而要把任務脈絡補回來：當時飛到哪裡？剛分離了什麼？船員是目視還是從相機看見？"
                ]
            },
            {
                "heading": "Gemini VII：一個明亮物體與大量粒子的瞬間",
                "paragraphs": [
                    "Gemini VII 的故事發生在美國太空計畫快速追趕的年代。Frank Borman 與 Jim Lovell 在狹小座艙裡待了近 14 天，任務重點包括長時間太空飛行與稍後和 Gemini VI-A 的歷史性會合。就在這樣高度緊繃的任務裡，船員回報窗外有明亮物體，並提到周圍似乎有大量粒子。",
                    "這段紀錄之所以被 UAP 社群反覆討論，是因為它既像一次真實目擊，又留下太多未補齊的背景。船員知道自己的 booster 在哪裡，因此『不是 booster』這類判斷會讓故事更有張力；但在軌道環境裡，碎片、反光、分離物與視角錯覺仍然都必須逐一排除。"
                ]
            },
            {
                "heading": "Apollo：月球影像裡的亮點與艙內閃光",
                "paragraphs": [
                    "Apollo 任務的 UAP 閱讀更像考古。Apollo 11 有技術空地通訊、指令艙 onboard voice、任務簡報與事後訪談；Apollo 17 則常被提到月面影像中出現的亮點，以及船員對閃光的描述。這些材料很有畫面感，因為背景是人類最具象徵性的月球旅程。",
                    "然而 NASA 的科學框架提醒我們：單張影像裡的亮點，若缺少相機設定、曝光條件、位置校準、連續影格與物體距離，很難直接變成事件結論。它可以是一個值得追問的異常，也可能只是攝影與任務環境的副產品。"
                ]
            },
            {
                "heading": "這類紀錄的真正價值",
                "paragraphs": [
                    "NASA 相關頁面最值得讀的不是傳奇，而是方法。NASA 2023 年 UAP 研究報告反覆強調高品質資料的重要性：沒有可校準資料，目擊就很難被科學地分析。這讓 Gemini 與 Apollo 的故事反而更迷人，因為它們是資料時代之前的人類觀測筆記。",
                    "把這些內容當作雜誌報導來讀，最好的姿勢不是追求一張決定性照片，而是看見一代太空人如何在未知中工作。他們看見異常、報告異常、繼續任務；而我們今天能做的，是把那一刻放回任務史，而不是急著把它拉進神話。"
                ]
            }
        ],
    },
    "congress-2023-uap-hearing": {
        "lede": "2023 年 7 月 26 日，美國國會的 UAP 聽證像一場被制度化的深夜談話：飛行員、安全倡議者、前情報官員坐在同一排，講述那些過去只在機庫、雷達室與匿名訪談裡流動的故事。",
        "timeline": [
            "2023 年 7 月 26 日：眾議院監督與問責委員會召開 UAP 聽證。",
            "Ryan Graves 以海軍飛行員與 Americans for Safe Aerospace 代表身份，主打飛航安全與通報機制。",
            "David Fravor 以 2004 年 Nimitz / Tic Tac 目擊者身份，描述白色橢圓物體與高速移動。",
            "David Grusch 以曾任 UAP Task Force 相關職務的前情報官員身份，提出回收計畫、逆向工程與非人類生物材料等主張。"
        ],
        "sections": [
            {
                "heading": "這場聽證為什麼像一個轉場",
                "paragraphs": [
                    "過去 UFO 故事常被困在兩個極端：一邊是陰謀論，一邊是嘲笑。但 2023 年國會聽證把問題移到另一個場景：飛行安全、政府透明、軍方通報、情報監督。這讓 UAP 不再只是『你相不相信外星人』，而變成『飛行員遇到無法識別物體時，制度如何接住這件事』。",
                    "三位證人的敘事各自不同。Graves 像是在替飛行員建立安全通道；Fravor 帶來一個具體、鮮明、難忘的目視案例；Grusch 則把問題推向最敏感的政府保密與回收計畫主張。真正要讀懂這場聽證，必須先把三種證詞分開。"
                ]
            },
            {
                "heading": "Graves：最日常也最可怕的飛航風險",
                "paragraphs": [
                    "Ryan Graves 的證詞沒有最戲劇化的外星敘事，卻最接近制度問題。他描述東岸訓練空域裡反覆出現的物體，包含飛行員目視到暗色立方體包在透明球體中的形狀；他還提到有一次近距離接近，讓任務指揮官立即中止飛行。",
                    "這段內容的重點不是『那是什麼』，而是『為什麼這種東西會出現在航線與訓練空域裡，卻沒有順暢通報與分析機制』。如果把 UAP 當成公共安全題，Graves 的證詞就是最穩的入口。"
                ]
            },
            {
                "heading": "Fravor：Tic Tac 事件的現場感",
                "paragraphs": [
                    "David Fravor 的故事具有電影感：2004 年，海軍飛行員在太平洋上空被引導去查看雷達目標；海面下方似乎有白水擾動，空中有一個白色、光滑、沒有明顯翼面或排氣的長橢圓物體。Fravor 形容它像巨大的 Tic Tac 糖。",
                    "他描述自己下降接近時，物體似乎做出反應，接著快速離開；控制員隨後回報該物體出現在約 60 英里外的 CAP point。這段證詞最有力量的地方，是它包含飛行員目視、軍事任務場景與後續影像脈絡，但它仍不是完整技術歸因。"
                ]
            },
            {
                "heading": "Grusch：最爆炸、也最需要查核的主張",
                "paragraphs": [
                    "David Grusch 的證詞把聽證推向另一個層級。他主張自己接觸過多名知情人士，聽聞美國政府或承包體系涉及回收與逆向工程計畫，並在問答中談到所謂 non-human biologics。這些說法在公開場域非常震撼，也因此必須用更高標準閱讀。",
                    "國會紀錄能證明他在公開聽證中作出這些陳述，卻不能自動證明每項陳述的事實性。AARO 後來的歷史報告對許多逆向工程與外星技術主張提出否定結論。讀者要掌握這場事件始末，就必須同時讀聽證與後續官方查核，不能只截取最刺激的一句。"
                ]
            }
        ],
    },
    "navy-tic-tac-fravor": {
        "lede": "如果近代 UAP 有一個最像電影開場的案例，就是 Tic Tac：晴朗海面、航空母艦戰鬥群、飛行員、雷達回報，以及一個看起來沒有機翼、沒有排氣、卻突然消失的白色物體。",
        "timeline": [
            "2004 年 11 月：USS Nimitz 戰鬥群附近出現多日異常雷達目標。",
            "David Fravor 與同僚被引導前往查看，目視白色橢圓物體與海面擾動。",
            "物體在接近過程中快速離開，後續被回報出現在遠處 CAP point。",
            "後來公開的 FLIR 影片成為大眾認識 Tic Tac 案例的核心影像之一。"
        ],
        "sections": [
            {
                "heading": "Tic Tac 為什麼會成為現代 UFO 神話",
                "paragraphs": [
                    "Tic Tac 案例能流行，不只是因為名字好記。它擁有一個好故事所需的全部元素：具名軍方飛行員、航空母艦戰鬥群、雷達脈絡、後來公開的軍方影像，以及無法被簡單一句話收尾的行為描述。",
                    "Fravor 在國會聽證中把現場講得很清楚：物體白色、光滑、外形像一顆巨大的 Tic Tac，沒有可見機翼、窗戶或傳統推進跡象。它不是從遙遠天邊一閃而過，而是在軍事訓練與監控環境中被人員主動接近。"
                ]
            },
            {
                "heading": "現場故事：白水、下降與突然離開",
                "paragraphs": [
                    "Fravor 描述他們被導向一片海域，看到海面有類似白水的擾動，附近有一個白色長橢圓物體在移動。他試圖下降接近，物體似乎調整軸向並與飛機互動，接著在接近到約半英里時快速加速離開。",
                    "最讓人記住的細節，是控制員後來回報物體出現在約 60 英里外的 CAP point。這一段讓故事從單純目視變成『目視經驗加上任務控制脈絡』。但仍要注意，公開可讀資料不等於完整雷達與任務資料全數公開。"
                ]
            },
            {
                "heading": "影片能證明什麼，又不能證明什麼",
                "paragraphs": [
                    "DVIDS 上的 FLIR UAP 影片讓大眾有了一個可反覆觀看的焦點。但影像本身通常只顯示感測器畫面中的目標與追蹤狀態；如果沒有完整距離、速度、平台姿態、鏡頭參數與同步資料，觀眾很容易把畫面中的運動感誤讀成物體本身的極端性能。",
                    "這並不是說影片不重要。它重要，因為它是官方公開的軍方素材；但它不是完整案件。Tic Tac 的真正閱讀方式，是把 Fravor 的目視證詞、其他機組人員說法、DVIDS 影像與後續官方報告分層放在一起，而不是只用一段黑白影像決定結論。"
                ]
            },
            {
                "heading": "一個未完成的案例，為何仍值得讀",
                "paragraphs": [
                    "Tic Tac 的吸引力在於它沒有被輕易消化。它不像氣球案例那樣很快被歸因，也不像純傳聞那樣缺少具名證人。它卡在中間：足夠具體，因此很難忽略；資料又不完整，因此不能被神化成鐵證。",
                    "對讀者而言，這正是成熟閱讀 UAP 的練習。真正有趣的不是立刻選邊站，而是承認一個案子可以同時具備可信目擊、官方影像、資料缺口與未完成結論。Tic Tac 的故事至今仍有力量，正因它停在這個張力裡。"
                ]
            }
        ],
    },
    "fbi-guy-hottel-memo": {
        "lede": "一頁紙，三個飛碟，九具三英尺高的人形遺體。Guy Hottel memo 像是 FBI 檔案室裡最會抓住眼球的短篇小說，但它真正教我們的不是外星人，而是如何辨認一份情報文件的重量。",
        "timeline": [
            "1950 年 3 月 22 日：FBI 華盛頓外勤辦公室主管 Guy Hottel 將一則飛碟回收傳聞寫成 memo 給 J. Edgar Hoover。",
            "1970 年代末：該 memo 已經透過 FOIA 公開。",
            "2011 年：FBI Vault 上線後，這份單頁文件成為最熱門檔案之一。",
            "2013 年：FBI 發文澄清，該 memo 是二手或三手說法，FBI 從未追查。"
        ],
        "sections": [
            {
                "heading": "最像爆料的一頁政府文件",
                "paragraphs": [
                    "Guy Hottel memo 之所以迷人，是因為它幾乎太會說故事。文件轉述一名第三方聲稱，空軍調查員說在新墨西哥回收了三個所謂飛碟；飛碟呈圓形、中央隆起，直徑約 50 英尺，每個裡面都有三具人形但只有三英尺高的身體，穿著細緻金屬布料。",
                    "如果只讀到這裡，它幾乎就是 Roswell 神話的完美燃料。但一份檔案的魅力，不等於一份檔案的證據力。FBI 後來特別提醒：這份 memo 是轉述，不是調查結論；它沒有後續偵辦，也沒有驗證鏈。"
                ]
            },
            {
                "heading": "文件真正說了什麼",
                "paragraphs": [
                    "memo 的故事還包括一個典型冷戰科技細節：所謂飛碟之所以墜落，是因為當地高功率雷達干擾了它們的控制機制。這句話讓故事聽起來更像內線情報，因為它提供了原因，而不是只說『有人看見飛碟』。",
                    "但 FBI 在 2013 年的說明把這份文件拉回現實：它不是新文件，早在 1970 年代末就公開；它日期是 1950 年，晚於 1947 年 Roswell 事件近三年；而且 FBI 檔案沒有資料能證實這則說法是否為當年流傳的惡作劇或傳聞。"
                ]
            },
            {
                "heading": "為什麼它不是 Roswell 證據",
                "paragraphs": [
                    "這份 memo 常被誤當成 FBI 對 Roswell 的承認，原因很簡單：它提到 New Mexico、飛碟、回收與人形遺體。可是官方脈絡完全不同。Roswell 發生在 1947 年 7 月，而 Hottel memo 是 1950 年 3 月的單頁轉述。",
                    "FBI 自己說得很清楚：沒有理由認為兩者相連；而且 FBI 沒有追查這件事。若把它當作 Roswell 證據，就等於把地名、題材與想像力黏在一起，跳過了最基本的時間線與證據鏈。"
                ]
            },
            {
                "heading": "這份文件真正值得讀的原因",
                "paragraphs": [
                    "Guy Hottel memo 的價值，不在於它證明飛碟墜落，而在於它展示了政府檔案中也會保存未驗證傳聞。情報機關收到資訊、轉存資訊、歸檔資訊，並不代表資訊已經被證實。",
                    "這就是它作為雜誌報導題材最精彩的地方：一頁紙如何在數十年後變成網路時代的神話核心？答案不在外星人，而在讀者如何把『官方檔案中出現』誤讀為『官方已證實』。"
                ]
            }
        ],
    },
    "cia-robertson-panel-durant-report": {
        "lede": "1953 年 1 月，一群科學家坐下來研究 UFO。表面上，他們要回答天上那些東西是什麼；更深一層，他們其實在問：當整個國家開始盯著天空，情報機構該如何管理恐慌、媒體與空防壓力？",
        "timeline": [
            "1947-1952 年：UFO 報告量上升，冷戰空防焦慮加劇。",
            "1953 年 1 月 14-17 日：CIA 相關單位召集 Robertson Panel 審查 UFO 資料。",
            "Durant Report 事後整理會議過程與建議。",
            "後續多年，CIA 對其角色與完整報告公開態度保守，反而加深外界對 cover-up 的懷疑。"
        ],
        "sections": [
            {
                "heading": "冷戰天空裡的科學小組",
                "paragraphs": [
                    "Robertson Panel 的背景不是科幻，而是冷戰。1952 年前後，美國出現大量 UFO 報告，包含華府上空雷達與目擊事件。情報機構擔心的未必是外星人，而是空防系統被大量報告淹沒，或敵方利用恐慌干擾美國反應能力。",
                    "CIA 找來以物理學家 H. P. Robertson 為首的非軍方科學家小組，審查空軍資料、影片與案例。Durant Report 則像會議側寫，把專家如何看資料、如何形成建議保存下來。"
                ]
            },
            {
                "heading": "他們看了哪些東西",
                "paragraphs": [
                    "CIA 歷史研究提到，小組檢視了空軍 UFO case histories，也花時間看經典影像案例，例如 Utah Tremonton 影片與 Montana Great Falls 影片。小組對這些影像提出較普通的解釋方向：反光、飛鳥、飛機或其他可被地面框架理解的現象。",
                    "它的結論並不是『每個案例都已完全解開』，而是更政策性的判斷：現有資料沒有顯示 UFO 對國家安全構成直接威脅，也沒有證據支持它們是外星來訪。這個語氣很情報機關：重點不是宇宙真相，而是威脅評估。"
                ]
            },
            {
                "heading": "最具爭議的建議：教育、淡化與監看",
                "paragraphs": [
                    "Robertson Panel 最容易引發後來爭議的部分，是建議政府用公共教育與媒體手段淡化 UFO 報告的神祕感，降低社會恐慌。報告甚至提到可透過媒體、學校、商業團體與大眾文化資源來傳遞訊息。",
                    "此外，小組也建議注意民間 UFO 團體是否可能被顛覆活動利用。從今天看，這些建議很容易被理解為『政府想控制敘事』。但放回 1953 年，它同時反映了麥卡錫時代、冷戰心理戰與空防焦慮。"
                ]
            },
            {
                "heading": "CIA 後來為何更麻煩",
                "paragraphs": [
                    "弔詭的是，CIA 對 Robertson Panel 與 Durant Report 的保密態度，反而讓 cover-up 故事更有燃料。CIA 歷史文章承認，機構曾不希望外界知道 CIA 贊助過小組，也不願完整公開相關材料。",
                    "所以這組文件真正值得讀的，是它揭開一種政府悖論：一方面，官方認為 UFO 沒有足夠證據指向外星威脅；另一方面，官方又用保密與敘事管理方式處理議題。正是這兩件事的交錯，讓 UFO 文化在之後幾十年越燒越旺。"
                ]
            }
        ],
    },
    "project-blue-book-fact-sheet": {
        "lede": "Project Blue Book 是美國 UFO 史的總帳本：12,618 件報告，701 件仍未識別。它像一本巨大的天空日誌，收下了冷戰美國所有仰頭看見異常的人、雷達與軍方表格。",
        "timeline": [
            "1947 年後：美國空軍展開多個 UFO 調查計畫，包含 Sign、Grudge 與後來的 Blue Book。",
            "1952 年：Project Blue Book 正式成為主要調查計畫。",
            "1969 年 12 月 17 日：空軍宣布終止 Project Blue Book。",
            "後續檔案去機密化並移交 National Archives，研究者可透過微縮膠卷與索引查閱。"
        ],
        "sections": [
            {
                "heading": "12,618 件報告背後的美國天空",
                "paragraphs": [
                    "Blue Book 的數字很有力量。從 1947 到 1969 年，空軍接收 12,618 件 UFO sightings，其中 701 件被留下『Unidentified』標籤。這個比例不高，卻足以支撐幾十年的想像：如果多數都能解釋，那剩下的 701 件是什麼？",
                    "作為雜誌報導題材，Blue Book 不該只被寫成『官方否認外星人』。它更像冷戰美國對未知天空的制度化回應：每一份報告都是民眾、飛行員、雷達或地方單位把一個看不懂的瞬間交給國家機器。"
                ]
            },
            {
                "heading": "官方 Fact Sheet 的三個結論",
                "paragraphs": [
                    "NARA 收錄的美國空軍 Fact Sheet 很直接：空軍調查與評估過的 UFO 沒有顯示國家安全威脅；沒有證據指出 unidentified sightings 代表超出當時科學知識的技術；也沒有證據顯示這些未識別目標是外星載具。",
                    "這三點常被懷疑者視為結案陳詞，也常被相信者視為掩飾。但如果細讀，它其實是一份行政結論：以當時調查結果與可用資料，空軍不認為繼續投入官方調查具備必要性。"
                ]
            },
            {
                "heading": "701 件未識別不等於 701 艘外星船",
                "paragraphs": [
                    "『Unidentified』是 Blue Book 最常被誤讀的詞。它表示在可用資料下未能歸因，並不自動表示超自然、外星或高科技。很多案例缺少清晰照片、完整雷達、可靠時間線或可重複檢驗的物理資料。",
                    "但也不能因為官方結論普通，就說 701 件沒有閱讀價值。它們的價值在於顯示未知如何被制度分類：哪些資料足以解釋，哪些資料不足以排除，哪些案例因紀錄品質太差而永遠停在灰色地帶。"
                ]
            },
            {
                "heading": "為什麼 Blue Book 今天仍是入口",
                "paragraphs": [
                    "Blue Book 的檔案已經移交 NARA，包含案卷、行政文件、微縮膠卷、照片與相關影音。這讓它不只是歷史名詞，而是可以被查核的資料庫。想理解現代 UAP 討論，不能跳過 Blue Book，因為許多後來的語言、懷疑與不信任都從這裡開始。",
                    "它留下的最大問題不是『外星人有沒有來』，而是『政府如何處理大量民眾看不懂的天空事件』。這個問題，到 AARO 與 PURSUE 時代仍然沒有消失，只是換了新的資料格式與機構名稱。"
                ]
            }
        ],
    },
    "roswell-report-official-records": {
        "lede": "Roswell 不是單一事件，而是一個不斷被重寫的美國神話：牧場碎片、軍方新聞稿、迅速改口、冷戰氣球計畫、外星遺體傳聞，最後成為全球最有名的 UFO 地名。",
        "timeline": [
            "1947 年 7 月：新墨西哥 Roswell 附近發現不明碎片，軍方初步新聞稿提到 flying disc，隨後改稱氣球。",
            "1994 年：GAO 應國會要求搜尋相關政府紀錄。",
            "1995 年：美國空軍發布 The Roswell Report: Fact vs. Fiction in the New Mexico Desert。",
            "1997 年：空軍發布 Case Closed，處理外星遺體敘事與人體假人記憶混合說法。"
        ],
        "sections": [
            {
                "heading": "一則新聞稿如何成為神話起點",
                "paragraphs": [
                    "Roswell 的起點帶著近乎小說般的節奏：牧場主發現碎片，軍方基地發布回收 flying disc 的消息，隔天又改稱天氣氣球。這種迅速轉向，在任何年代都會引發想像；放在 1947 年，冷戰初期與飛碟熱潮剛起，更是完美的神話土壤。",
                    "後來幾十年，Roswell 逐漸不只是『掉下來什麼』，而是變成『政府是不是從一開始就在隱瞞』。這也是為什麼官方報告必須同時處理材料、紀錄與大眾記憶。"
                ]
            },
            {
                "heading": "官方查到了什麼",
                "paragraphs": [
                    "NARA 的 Roswell 說明指出，在 Project Blue Book records 中找不到討論 1947 Roswell 事件的文件。1994 年 GAO 啟動紀錄搜尋後，空軍也系統性查找現役辦公室、檔案中心與相關紀錄，並訪談可能知情人士。",
                    "空軍 1995 年報告把回收材料指向當時機密的氣球計畫，常被稱為 Project Mogul 相關設備。這類高空氣球用於偵測蘇聯核試，當時屬於敏感計畫；因此『氣球』聽起來普通，但在 1947 年並非單純兒童派對道具，而是冷戰技術的一部分。"
                ]
            },
            {
                "heading": "外星遺體說法如何被處理",
                "paragraphs": [
                    "Roswell 最刺激的部分當然是 alien bodies。NARA 與空軍說明都指出，紀錄沒有顯示回收外星材料或外星遺體。1997 年 Case Closed 則進一步處理所謂遺體記憶，將部分敘事與後來高空測試中的人體假人、事故記憶與年代混淆相連。",
                    "這個官方解釋不一定能說服所有相信者，因為 Roswell 的魅力早已超出單一文件。但如果要建構可信內容，必須先把官方查核說清楚：政府找過哪些紀錄、訪談了哪些類型的人、最後把物證指向什麼。"
                ]
            },
            {
                "heading": "Roswell 今日仍重要的原因",
                "paragraphs": [
                    "Roswell 重要，不是因為官方報告證明了外星飛船；恰恰相反，它重要是因為它展示了機密軍事計畫、模糊新聞發布與大眾想像如何結合，形成一個長壽到幾乎不可摧毀的文化事件。",
                    "讀 Roswell 最好的方式，不是只問『墜毀的是什麼』，還要問『為什麼這件事能活這麼久』。答案可能在冷戰、檔案缺口、政府不信任、媒體敘事與人類對未知的渴望之間。"
                ]
            }
        ],
    },
    "aaro-historical-record-report": {
        "lede": "AARO Historical Record Report 像是一份官方總清算：它回頭翻 1945 年以來的 UAP 調查、祕密計畫傳聞、逆向工程主張與非人類技術說法，試圖回答一句最刺耳的問題：政府到底藏了什麼？",
        "timeline": [
            "1945 年後：美國政府多次以不同名稱調查 UFO/UAP。",
            "2022 年：AARO 成立，接手跨域異常解析與歷史查核任務。",
            "2023 年：國會聽證與吹哨者主張提高政治壓力。",
            "2024 年：AARO 發布 Historical Record Report Volume I，回顧官方調查史並評估外星技術與逆向工程主張。"
        ],
        "sections": [
            {
                "heading": "一份寫給懷疑時代的報告",
                "paragraphs": [
                    "AARO 的歷史報告不是輕鬆讀物。它的語氣冷、結構硬、結論也不浪漫。但正因如此，它是現代 UAP 討論中必讀的一份文本：當國會證詞、媒體爆料與民間研究都指向『政府可能有更深祕密』時，AARO 代表官方體系給出自己的查核版本。",
                    "報告說，AARO 查閱了機密與非機密檔案，訪談約 30 人，並與情報與國防系統中負責 controlled / special access program oversight 的單位合作。它試圖追問的不只是天空異常，而是那些被指稱藏在政府與承包商深處的計畫。"
                ]
            },
            {
                "heading": "最核心的結論：沒有確認外星技術",
                "paragraphs": [
                    "報告的執行摘要很直接：AARO 沒有找到任何美國政府調查、學術研究或官方審查小組曾確認 UAP sighting 代表外星技術的證據。它也表示，多數調查在各種機密層級下都把大部分 sightings 歸因為普通物體、現象或誤認。",
                    "這並不等於每個案例都已解開。AARO 同時承認，許多 UAP reports 仍未解或未識別；但它認為，如果有更多、更高品質資料，多數也可能被歸因為普通物體或現象。這是報告的關鍵張力：承認未知，拒絕把未知直接升級成外星。"
                ]
            },
            {
                "heading": "逆向工程、NDA 與 KONA BLUE",
                "paragraphs": [
                    "報告特別處理所謂 reverse-engineering extraterrestrial technology 的主張。AARO 表示，沒有找到美國政府或私人企業正在逆向工程外星技術的 empirical evidence，並認為許多被點名的人、地點、文件與技術測試不是不存在，就是被錯誤連結到外星敘事。",
                    "其中最值得注意的是 KONA BLUE。AARO 承認它是曾被提出的 prospective special access program，但說它未獲批准、未正式建立，也沒有取得材料或資金。換句話說，這個名字不是憑空捏造，但官方版本裡，它更像一個未成案的 proposal，而不是已運作的外星回收計畫。"
                ]
            },
            {
                "heading": "報告也有它的爭議",
                "paragraphs": [
                    "AARO 報告發布後，並沒有讓爭議停止。支持揭露者質疑 AARO 是否真的取得所有深層 compartmented programs；懷疑者則認為報告終於替長年傳聞劃出證據邊界。這份報告因此不是終點，而是一個官方立場的強力節點。",
                    "讀者要掌握事件始末，應把它和 2023 國會聽證放在一起看：Grusch 的證詞提出最震撼的主張，AARO 的報告則提供官方查核與否定。兩者之間的衝突，正是當代 UAP 討論最核心的戲劇張力。"
                ]
            }
        ],
    },
    "kona-blue-ornl-materials": {
        "lede": "KONA BLUE 與 ORNL 材料分析，是 UAP 世界裡最像科學偵探小說的一章：一邊是『非人類生物材料』與逆向工程計畫的傳聞，一邊是實驗室裡的元素分析、顯微影像與合金結構。",
        "timeline": [
            "AARO 歷史訪談期間：多名受訪者提到 KONA BLUE，稱其與 retrieval、exploitation 或 non-human biologics 保護有關。",
            "AARO 查核後：判定 KONA BLUE 是提出給 DHS 的 prospective special access program，但未獲批准或正式建立。",
            "2022-2024 年：AARO 委託 ORNL 分析一件被稱為 1947 年外星墜毀材料的鎂合金標本。",
            "2024-2026 年：AARO / ORNL 另公布金屬樣本分析，包含鎂合金與鋁矽合金標本，結論均指向地球工業材料。"
        ],
        "sections": [
            {
                "heading": "KONA BLUE：一個名字如何點燃想像",
                "paragraphs": [
                    "KONA BLUE 之所以迷人，是因為它在官方文件裡帶著幾乎完美的神祕感。AARO 說，多名受訪者把它描述成 DHS 轄下用來保護 retrieval 與 exploitation 的敏感 compartment，甚至牽涉 non-human biologics。這些詞一出現，故事就自帶影像感。",
                    "但 AARO 的查核版本把它拉回行政現實：KONA BLUE 是 prospective special access program，也就是被提案過，但沒有被 DHS leadership 批准，沒有正式建立，沒有收到材料，也沒有資金。它的存在感是真的；它的運作狀態，按照官方說法，並不是真的。"
                ]
            },
            {
                "heading": "從祕密計畫到實驗室樣本",
                "paragraphs": [
                    "材料分析是另一條線。AARO 委託 Oak Ridge National Laboratory 分析一件鎂合金標本，該標本被公開聲稱可能來自 1947 年墜毀外星載具，甚至被說成能作為 terahertz waveguide、產生反重力或慣性質量降低效果。",
                    "這類主張聽起來像科幻，但實驗室看的不是故事，而是元素、同位素、晶體結構、層狀組成、熱與機械壓力痕跡。ORNL 的結論是，資料不支持非地球來源，也不支持它曾具備理論上作為 THz waveguide 所需的純單晶鉍層。"
                ]
            },
            {
                "heading": "另一個鋁樣本：普通得很有意義",
                "paragraphs": [
                    "AARO / ORNL 後續也處理一件據稱與 1990 年代 Ohio 中部 UAP 事件相關的鋁樣本。ORNL 分析鑽屑與小塊材料後，認為它是常見的近共晶鋁矽合金，符合 300/400 系列鑄造合金特徵，沒有異常 gamma emission。",
                    "這個結論不刺激，但很重要。它告訴讀者，所謂『外星材料』若要成立，不能只靠來源故事或外觀奇特；它必須在成分、結構、同位素、放射性或功能上跨過地球工業材料的門檻。這兩個 ORNL 案例都沒有跨過。"
                ]
            },
            {
                "heading": "這組文件真正精彩的地方",
                "paragraphs": [
                    "KONA BLUE 與 ORNL 不是在同一層回答問題。KONA BLUE 回答的是『政府內部是否曾有人提案建立與回收／利用相關的敏感計畫』；ORNL 回答的是『被聲稱異常的材料，在實驗室裡是否真的異常』。",
                    "把兩者放在一起讀，會看到 UAP 報導最好的方向：不要只問有沒有陰謀，也不要只嘲笑相信者。真正好的問題是：哪一部分有文件支持？哪一部分只是提案？哪一部分經過實驗？哪一部分在實驗後回到普通地球材料？這樣讀，神祕感沒有消失，反而變得更精準。"
                ]
            }
        ],
    },
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_list(items: list[str]) -> str:
    return "\n".join(f"                    <li>{esc(item)}</li>" for item in items)


def render_timeline(items: list[str]) -> str:
    return "\n".join(f"                        <li>{esc(item)}</li>" for item in items)


def render_report_sections(sections: list[dict[str, object]]) -> str:
    rendered = []
    for section in sections:
        paragraphs = "\n".join(
            f"                    <p>{esc(paragraph)}</p>"
            for paragraph in section["paragraphs"]
        )
        rendered.append(
            f"""                <section class="uap-story-section">
                    <h2>{esc(section["heading"])}</h2>
{paragraphs}
                </section>"""
        )
    return "\n\n".join(rendered)


def render_sources(sources: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'                    <li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a></li>'
        for label, url in sources
    )


def related_links(current_slug: str) -> str:
    items = [guide for guide in GUIDES if guide["slug"] != current_slug][:4]
    return "\n".join(
        f'                    <a href="{esc(item["slug"])}.html">{esc(item["short_title"])}</a>'
        for item in items
    )


def render_page(guide: dict[str, object]) -> str:
    report = REPORTS[guide["slug"]]
    canonical = f"{BASE_URL}/uap-ufo-declassified/{guide['slug']}.html"
    tags = ", ".join(guide["keywords"])
    sources_json = [
        {"@type": "WebPage", "name": label, "url": url}
        for label, url in guide["sources"]
    ]
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guide["title"],
        "description": guide["description"],
        "datePublished": PUBLISHED_ISO,
        "dateModified": MODIFIED_ISO,
        "author": {"@type": "Organization", "name": "Elite Fashion"},
        "publisher": {
            "@type": "Organization",
            "name": "Elite Fashion",
            "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/logo.jpg"},
        },
        "mainEntityOfPage": canonical,
        "citation": sources_json,
    }
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(guide["title"])} | Elite Fashion</title>
    <meta name="description" content="{esc(guide["description"])}">
    <meta name="keywords" content="{esc(tags)}">
    <meta name="author" content="Elite Fashion Team">
    <meta property="article:published_time" content="{PUBLISHED_ISO}">
    <meta property="article:modified_time" content="{MODIFIED_ISO}">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="zh_TW">
    <meta property="og:url" content="{esc(canonical)}">
    <meta property="og:title" content="{esc(guide["title"])}">
    <meta property="og:description" content="{esc(guide["description"])}">
    <meta property="og:image" content="{BASE_URL}/images/logo.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{esc(canonical)}">
    <link rel="stylesheet" href="../css/styles.css?v=1.2">
    <link rel="stylesheet" href="../css/uap-declassified.css?v=1.1">
    <link rel="icon" type="image/svg+xml" href="../images/favicon/favicon.svg">
    <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=6)}
    </script>
</head>
<body>
    <nav class="navbar" role="navigation" aria-label="主導覽列">
        <div class="container">
            <div class="nav-brand">
                <a href="../index.html" class="logo"><img src="../images/logo.jpg" alt="Elite Fashion Logo"></a>
            </div>
            <button class="mobile-menu-toggle" aria-label="開啟選單" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="../index.html">首頁</a></li>
                <li><a href="../ai-innovation.html">人工智能</a></li>
                <li><a href="../lifestyle-culture.html">生活品味</a></li>
                <li><a href="../all-articles.html">文章列表</a></li>
                <li><a href="../uap-ufo-declassified-database.html">UAP 總覽</a></li>
            </ul>
        </div>
    </nav>

    <header class="uap-detail-hero">
        <div class="container">
            <a class="uap-back-link" href="../uap-ufo-declassified-database.html">回到 UAP/UFO 解密資料庫</a>
            <p class="uap-detail-kicker">官方檔案深讀</p>
            <h1>{esc(guide["title"])}</h1>
            <p>{esc(guide["description"])}</p>
        </div>
    </header>

    <main class="uap-detail-main">
        <article class="container uap-detail-layout">
            <aside class="uap-record-card" aria-label="檔案摘要">
                <h2>檔案摘要</h2>
                <dl>
                    <dt>官方原名</dt>
                    <dd>{esc(guide["official_name"])}</dd>
                    <dt>來源機構</dt>
                    <dd>{esc(guide["agency"])}</dd>
                    <dt>資料型態</dt>
                    <dd>{esc(guide["record_type"])}</dd>
                    <dt>日期</dt>
                    <dd>{esc(guide["record_date"])}</dd>
                    <dt>目前狀態</dt>
                    <dd>{esc(guide["status"])}</dd>
                    <dt>查核日期</dt>
                    <dd>{CHECK_DATE}</dd>
                </dl>
            </aside>

            <div class="uap-detail-content">
                <section class="uap-story-lede">
                    <p>{esc(report["lede"])}</p>
                </section>

                <section class="uap-timeline-section">
                    <h2>事件時間線</h2>
                    <ol class="uap-timeline">
{render_timeline(report["timeline"])}
                    </ol>
                </section>

{render_report_sections(report["sections"])}

                <section class="uap-source-box">
                    <h2>官方來源與延伸查核</h2>
                    <ul>
{render_sources(guide["sources"])}
                    </ul>
                    <p>本頁為繁體中文導讀，不代表任何美國政府機構立場；官方結論、檔案狀態與素材權利仍以原始頁面為準。</p>
                </section>

                <section>
                    <h2>下一步閱讀</h2>
                    <div class="uap-related-links">
{related_links(guide["slug"])}
                    </div>
                </section>
            </div>
        </article>
    </main>

    <script src="../js/main.js"></script>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for guide in GUIDES:
        (OUT_DIR / f"{guide['slug']}.html").write_text(render_page(guide), encoding="utf-8")
    print(f"Generated {len(GUIDES)} UAP guide pages in {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
