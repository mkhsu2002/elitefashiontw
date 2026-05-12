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
        "description": "繁中導讀 2026 年 5 月 8 日 WAR.GOV/UFO 第一批 PURSUE UAP 解密檔案，說明官方稱為 unresolved cases 的閱讀重點、限制與常見查詢詞。",
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
        "description": "整理 NASA 與 PURSUE 釋出的 Gemini、Apollo 任務紀錄閱讀方式，說明太空人對話、任務照片與 UAP 搜尋詞如何避免被過度解讀。",
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
        "description": "整理 CIA Reading Room 中 Robertson Panel、Durant Report 與 CIA UFO 研究史文件，說明 1953 年科學顧問會議如何影響後續 UFO 檔案公開。",
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
        "description": "繁中導讀 NARA Project Blue Book 官方頁與美國空軍 Fact Sheet，整理 12,618 件 UFO 報告、701 件未識別與三項官方結論。",
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
        "description": "導讀 AARO UAP Records 中 KONA BLUE、ORNL 金屬樣本分析與 alleged alien material 主張，說明 proposed SAP、材料檢測與官方結論。",
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


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_list(items: list[str]) -> str:
    return "\n".join(f"                    <li>{esc(item)}</li>" for item in items)


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
    <link rel="stylesheet" href="../css/uap-declassified.css?v=1.0">
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
                <section>
                    <h2>這份內容為什麼值得讀</h2>
                    <p>{esc(guide["summary"])}</p>
                </section>

                <section>
                    <h2>讀者最常搜尋的切入點</h2>
                    <ul>
{render_list(guide["why"])}
                    </ul>
                </section>

                <section>
                    <h2>繁中導讀時要抓的重點</h2>
                    <ul>
{render_list(guide["reading_points"])}
                    </ul>
                </section>

                <section>
                    <h2>延伸查詢詞</h2>
                    <div class="uap-keyword-cloud">
{''.join(f'                        <span>{esc(item)}</span>\\n' for item in guide["seo_angles"])}
                    </div>
                </section>

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
