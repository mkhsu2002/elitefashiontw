#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_revenue_growth_batch_two as base


base.TRIGGER_TYPE = "manual-codex-momo-revenue-growth-batch-thirteen-no-newsletter"
base.QUEUE_ID = "MOMO-REV-2026-06-21-W01-B13"

base.COVER_SOURCES = {
    "closet-laundry-hanger-storage-towel-bedding-supplies": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a38279661108198acf1af8bb9123bd3.png",
    "nightstand-bedtime-earplug-reading-light-scent-bedding": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a382692d50c8198ac8c3e88712be41b.png",
    "summer-bedding-tencel-quilt-protector-cool-blanket-order": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a3826bfcafc8198ad94fa6cb34e82e7.png",
    "home-cleaning-tool-wall-mop-broom-sink-trash-bin": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a3826f14fdc8198b3434416457fab86.png",
    "rental-refresh-sticker-light-storage-movable-furniture": "/Users/mkhsu/.codex/generated_images/019ee879-360f-7231-9712-537f4c96f0bb/ig_0de90cb00612aa87016a38272435808198bddf43417a4b2b0f.png",
}

ROW_OVERRIDES = {
    "closet-laundry-hanger-storage-towel-bedding-supplies": {
        "elite_judgment": "衣櫃和洗衣區要先分每天拿、每週洗、換季收三層，衣架、毛巾和床寢才不會互相擠壓。",
        "answer_summary": "衣櫃與洗衣區整理要先看拿取頻率、晾曬動線、毛巾汰換與床寢換季，再比較收納與家用品。",
        "risk_guardrail": "衣架、收納箱、毛巾、床寢與洗衣用品的尺寸、材質、承重、清潔與使用限制請以商品頁及包裝為準。",
    },
    "nightstand-bedtime-earplug-reading-light-scent-bedding": {
        "elite_judgment": "床邊櫃只留下睡前最後十五分鐘會用到的物件，耳塞、閱讀燈、香氛與床寢才有真正位置。",
        "answer_summary": "床邊小物要先分閱讀、安靜、保濕飲水與隔天起身四件事，再比較耳塞、燈具、香氛與床寢。",
        "risk_guardrail": "耳塞、燈具、香氛與床寢不作助眠、療效或健康承諾；材質、香味、亮度、尺寸與使用限制請以商品頁及包裝為準。",
    },
    "summer-bedding-tencel-quilt-protector-cool-blanket-order": {
        "elite_judgment": "夏季床寢先換貼身層，再看保潔墊、薄被與涼被，不要只因為熱就一次買滿所有材質。",
        "answer_summary": "夏季床寢更換要先看貼身觸感、保潔墊清洗頻率、薄被厚度與冷氣房習慣，再比較床寢品牌。",
        "risk_guardrail": "天絲、棉被、保潔墊與涼被不作降溫、抗敏、健康或療效承諾；材質、尺寸、清洗與使用限制請以商品頁及包裝為準。",
    },
    "home-cleaning-tool-wall-mop-broom-sink-trash-bin": {
        "elite_judgment": "清潔工具牆先按髒污來源分區，不是把拖把、掃把、刷具和垃圾桶全掛上牆就算整理。",
        "answer_summary": "居家清潔工具牆要先分地面、水槽、垃圾與擦拭四類，再比較平板拖把、掃把、刷具與垃圾桶。",
        "risk_guardrail": "清潔工具、刷具、垃圾桶與清潔用品的尺寸、材質、清潔限制、適用表面與使用方式請以商品頁及包裝為準。",
    },
    "rental-refresh-sticker-light-storage-movable-furniture": {
        "elite_judgment": "租屋改造先做可復原、可搬走、可減少雜物的項目，貼皮、燈光與家具才不會變成退租壓力。",
        "answer_summary": "租屋改造不動工要先看可復原性、插座位置、收納容量與搬家成本，再比較貼皮、燈具與可移動家具。",
        "risk_guardrail": "貼皮、燈具、收納與家具的尺寸、材質、承重、安裝、退租限制與用電安全請以商品頁、租約與現場條件為準。",
    },
}

base.TOPIC_HUBS = {
    "closet-laundry-hanger-storage-towel-bedding-supplies": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "commute-style-reset", "title": "通勤衣櫥與鞋包選物指南", "file": "commute-style-reset.html", "url": "/commute-style-reset", "category": "casual-chic"}]},
    "nightstand-bedtime-earplug-reading-light-scent-bedding": {"topicCategory": "recovery-sleep", "topicCategoryLabel": "睡眠與恢復", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "summer-bedding-tencel-quilt-protector-cool-blanket-order": {"topicCategory": "recovery-sleep", "topicCategoryLabel": "睡眠與恢復", "primaryHub": {"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}, "secondaryHubs": [{"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}]},
    "home-cleaning-tool-wall-mop-broom-sink-trash-bin": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "body-rhythm-reset", "title": "身體節奏與恢復生活指南", "file": "body-rhythm-reset.html", "url": "/body-rhythm-reset", "category": "wellness-movement"}]},
    "rental-refresh-sticker-light-storage-movable-furniture": {"topicCategory": "home-rituals", "topicCategoryLabel": "居家儀式", "primaryHub": {"key": "mature-life-reset", "title": "人生重整與一人生活秩序", "file": "mature-life-reset.html", "url": "/mature-life-reset", "category": "lifestyle-culture"}, "secondaryHubs": [{"key": "ai-work-reset-45", "title": "AI 工作重整與第二曲線", "file": "ai-work-reset-45.html", "url": "/ai-work-reset-45", "category": "ai-innovation"}]},
}

base.BLUEPRINTS = {
    "closet-laundry-hanger-storage-towel-bedding-supplies": {
        "heroAlt": "晨光中的衣櫃與洗衣收納區，有木質衣架、藤編籃、摺疊毛巾、淺色床寢與綠植",
        "audience": "想把衣櫃、洗衣籃、毛巾與床寢備品整理成清楚動線的人",
        "excerpt": "衣櫃與洗衣區不是收越多越好，先分每天拿、每週洗、換季收，才知道衣架、收納箱、毛巾與床寢要買到哪裡。",
        "tags": ["衣櫃收納", "洗衣區整理", "毛巾床寢", "居家備品"],
        "intro": "衣櫃和洗衣區最容易被誤會成兩個地方：一邊收衣服，一邊處理髒衣。實際生活裡，它們每天都在互相影響：衣架不夠會讓晾衣卡住，毛巾沒有汰換位置會佔滿層板，床寢備品若和當季衣物混放，換床單時就會變成翻箱倒櫃。好的整理不是把收納盒買滿，而是讓乾淨、待洗、待換季與備品各自有路可走。",
        "editorialAngle": "先分每天拿、每週洗、換季收三層。",
        "sections": [
            ("第一層：每天會拿的衣物不要被備品擋住", "每天穿的襯衫、外套、通勤衣物應該在視線最順的位置。床寢和毛巾備品若放在同一層，會讓每天拿衣服都像在搬家。", "衣架、收納籃與層架要先服務拿取頻率，再服務照片裡的整齊。"),
            ("第二層：每週會洗的毛巾與家居布品要有回收路線", "毛巾、浴巾、擦拭布和床單都會從乾淨變待洗，再回到乾淨層。若沒有固定籃位，很容易堆在椅背或洗衣機旁。", "先看家中洗衣頻率，再決定毛巾和床寢備品數量。"),
            ("第三層：換季物要退到不干擾的位置", "厚被、涼被、冬季毯與少用枕套可以放高處或深層，但要保留清楚標記與拿取路徑。", "台灣濕度高，收納前的乾燥、清潔與包材透氣性都要保守看待。"),
            ("常見錯誤：買太多同尺寸收納盒", "同尺寸盒子看起來整齊，卻不一定適合毛巾、床包、衣架和小物。分類應由物品尺寸與使用頻率決定，不是由盒子決定。", "如果一個盒子需要被搬開兩次才拿得到，代表它不該放高頻用品。"),
            ("下單前的衣櫃盤點", "先數目前衣架缺口、毛巾輪替數、床寢套數與換季被品位置。盤點完再買，會比一次買齊更少浪費。", "Elite Fashion 編輯團隊的判斷是：衣櫃洗衣區真正有轉換價值的商品，是能讓下一次洗完、晾完、收回去都少一步。"),
        ],
        "faq": [("衣櫃和洗衣區要一起整理嗎？", "建議一起看，因為衣架、待洗籃、毛巾和床寢都會在兩個區域之間流動。"), ("毛巾備品要準備多少？", "先看家庭人數和洗衣頻率，不要只因為櫃子有空間就補滿。"), ("收納箱越多越好嗎？", "不一定。高頻物品若被收進太深的箱子，反而會降低使用效率。")],
    },
    "nightstand-bedtime-earplug-reading-light-scent-bedding": {
        "heroAlt": "夜晚床邊櫃有暖色閱讀燈、無字耳塞盒、陶瓷香氛瓶、水杯、托盤、亞麻床寢與打開的書",
        "audience": "想讓床邊櫃維持安靜、好拿、不堆雜物的人",
        "excerpt": "床邊櫃只放睡前最後十五分鐘會用到的物件，耳塞、閱讀燈、香氛與床寢才不會變成雜物展示。",
        "tags": ["床邊櫃", "睡前小物", "閱讀燈", "香氛床寢"],
        "intro": "床邊櫃是一天最後一個工作台，也最容易堆滿沒有結束的事情。充電線、書、香氛、耳塞、護手霜、水杯與隔天要帶的東西全部放上去，看似方便，實際上會讓睡前視線變吵。更好的方式，是只留下最後十五分鐘真正會碰到的物件：看、放、關、起身。其餘都應該回到抽屜、書桌或玄關。",
        "editorialAngle": "用最後十五分鐘決定床邊物件。",
        "sections": [
            ("先分閱讀、安靜、飲水與起身", "閱讀燈和書屬於看，耳塞屬於安靜，水杯屬於睡前補充，隔天眼鏡或髮圈屬於起身。四類混在一起，就會越放越滿。", "每一類只留一到兩件高頻用品，床邊櫃才會真正安靜。"),
            ("燈光要照到書，不要照亮整個房間", "閱讀燈的位置比造型更重要。光線應落在書頁或床側，不需要讓整個臥室重新變亮。", "亮度、色溫、燈具尺寸與用電條件請回商品頁確認。"),
            ("香氛是最後一層，不是睡眠保證", "香氛可以讓床邊更有儀式感，但不應被寫成助眠或療效。若床邊已經堆滿紙張和衣物，先整理比新增香味更重要。", "香味、材質、使用方式與過敏疑慮都應以商品頁及包裝為準。"),
            ("常見錯誤：把床邊櫃當小倉庫", "床邊櫃越大，越容易放進不該在睡前出現的東西。真正成熟的床邊配置，是讓拿取變少，而不是讓收納變多。", "若一件物品連續一週都沒有在睡前使用，就移出床邊。"),
            ("下單前的床邊測試", "關掉主燈，躺到平常的位置，伸手測試燈、書、水杯、耳塞和眼鏡是否都能安全拿到。這比看商品照更接近真實。", "Elite Fashion 編輯團隊的判斷是：床邊櫃的質感不是擺得滿，而是每一次關燈前都不用再整理一次。"),
        ],
        "faq": [("床邊櫃應該放香氛嗎？", "可以，但香氛應放在整理與通風之後，且不應期待療效或助眠保證。"), ("耳塞需要固定放床邊嗎？", "如果經常因環境聲音受干擾，可以放在固定小盒中；材質與配戴感仍要自行確認。"), ("閱讀燈怎麼選？", "先看照射範圍、床邊高度、插座位置與是否容易關閉。")],
    },
    "summer-bedding-tencel-quilt-protector-cool-blanket-order": {
        "heroAlt": "陽光通透的夏季臥室，白色床鋪上有淺藍床單、薄被、保潔墊層次與薄荷色涼被",
        "audience": "想在夏天前更換床包、保潔墊、薄被與涼被的人",
        "excerpt": "夏季床寢更換要從貼身層開始，再看保潔墊、薄被與冷氣房習慣，不要只因為熱就一次買滿。",
        "tags": ["夏季床寢", "天絲床包", "保潔墊", "涼被"],
        "intro": "夏天換床寢最容易只用一個字決定：涼。但真正睡起來舒服的床，不只看單一材質，而是貼身層、保潔層、覆蓋層和清洗頻率一起成立。台灣夏季有濕氣、冷氣房、午後悶熱和頻繁流汗等情境；若只買一條涼被，卻忽略保潔墊是否悶、床包是否好洗，床仍然不會變得好維持。",
        "editorialAngle": "先換貼身層，再決定覆蓋層。",
        "sections": [
            ("第一步先看貼身層", "床包、枕套和被套是最常接觸皮膚的層次。材質、清洗方式和更換頻率，比單看觸感形容更重要。", "天絲、棉或混紡名稱都要回到商品頁標示，不自行延伸效果。"),
            ("保潔墊不是越厚越安心", "保潔墊要看床墊尺寸、透氣感、清洗頻率與是否容易移位。若這一層太悶，後面再換涼被也難以補救。", "防水、抗菌、涼感等描述請以商品頁與標示為準。"),
            ("薄被與涼被要看冷氣習慣", "有些人夏天仍需要薄被，有些人只需要涼被或毯。選擇前先看冷氣溫度、是否共睡與半夜是否容易踢被。", "不要把材質想像成保證舒適，使用情境才是關鍵。"),
            ("常見錯誤：一次換整床但沒有備用組", "床寢換新後如果沒有換洗組，清洗週期會變得緊張。與其把預算全放在單一高價品，不如先建立可輪替的兩組邏輯。", "尤其潮濕季節，晾乾時間要納入購買數量。"),
            ("下單前的四層順序", "貼身層、保潔層、覆蓋層、備用層。四層都想清楚，再比較尺寸和材質。", "Elite Fashion 編輯團隊的判斷是：夏季床寢的好買點不是追求最涼，而是讓清洗、替換與冷氣房使用都順。"),
        ],
        "faq": [("夏季床寢先買涼被嗎？", "不一定。建議先看床包和保潔墊，因為它們更貼近身體且影響清洗頻率。"), ("保潔墊會不會太悶？", "需看材質、厚度與商品標示，不能只看名稱判斷。"), ("床寢需要準備幾組？", "通常至少要考慮換洗輪替，但實際數量要看洗衣頻率和晾乾條件。")],
    },
    "home-cleaning-tool-wall-mop-broom-sink-trash-bin": {
        "heroAlt": "明亮廚房旁的清潔工具牆，有平板拖把、掃把、水槽刷、抹布籃、簡約垃圾桶與植栽",
        "audience": "想把清潔工具從角落雜物整理成可維持系統的人",
        "excerpt": "清潔工具牆要先分地面、水槽、垃圾與擦拭四類，再決定平板拖把、掃把、刷具與垃圾桶放哪裡。",
        "tags": ["清潔工具", "平板拖把", "水槽清潔", "垃圾桶收納"],
        "intro": "居家清潔工具最常見的問題不是不夠，而是每一樣都沒有明確位置。平板拖把、掃把、水槽刷、抹布、垃圾袋和小垃圾桶如果全擠在角落，清潔會變成每次都要先搬東西。清潔工具牆的價值，是把地面、水槽、垃圾與擦拭拆開，讓你在髒污剛出現時就能伸手處理，而不是等到週末才一次崩潰整理。",
        "editorialAngle": "把髒污來源分開，清潔才不會拖延。",
        "sections": [
            ("地面工具要看走道與晾乾", "拖把、掃把和除塵工具要有可晾乾、不卡門、不碰到乾淨用品的位置。只掛得漂亮但拿取不順，很快會回到地上。", "先量工具長度、牆面高度和門片開合。"),
            ("水槽刷具要和餐具分開", "水槽刷、刮刀或清潔布不應和杯盤工具混在一起。濕物要能瀝乾，也要避免滴到收納層板。", "材質、適用表面與清潔限制請看商品標示。"),
            ("垃圾桶位置決定日常維持", "垃圾桶不是越大越好。廚房、玄關或浴室需要的是剛好順手、容易倒、容易清潔的容量。", "若垃圾桶太遠，小垃圾會先出現在桌面。"),
            ("常見錯誤：清潔用品和工具互相遮擋", "噴瓶、補充包、刷具與抹布如果都放同一格，真正要用時會先找不到。工具牆應保留分類，而不是追求滿版。", "涉及清潔劑時，請依照商品標示保存與使用。"),
            ("下單前的四區配置", "地面、水槽、垃圾、擦拭。每一區只放最常用的兩到三件工具，其餘補充品退到櫃內。", "Elite Fashion 編輯團隊的判斷是：好清潔工具牆會讓小髒污更快被處理，而不是讓牆面看起來像工具展示。"),
        ],
        "faq": [("清潔工具牆適合小宅嗎？", "適合，但更需要控制數量，只保留最常用的工具。"), ("拖把和掃把要掛起來嗎？", "若牆面和晾乾條件允許，掛起來通常更好拿也更不佔地。"), ("垃圾桶要買大一點嗎？", "看空間和倒垃圾頻率。太大可能累積氣味，太小則會溢出。")],
    },
    "rental-refresh-sticker-light-storage-movable-furniture": {
        "heroAlt": "色彩豐富的租屋客廳，有可移動推車、立燈、收納格、貼皮板材樣片、單椅、窗簾與綠植",
        "audience": "想改善租屋空間但不想動工、鑽牆或造成退租麻煩的人",
        "excerpt": "租屋改造不動工要先看可復原性、插座位置、收納容量與搬家成本，再比較貼皮、燈具與可移動家具。",
        "tags": ["租屋改造", "不動工佈置", "可移動家具", "居家收納"],
        "intro": "租屋改造最迷人的地方，是用小物件讓空間立刻有變化；最危險的地方，也是太快被變化感帶走。貼皮、立燈、收納櫃、推車和可移動家具看起來都不需要動工，但它們仍然會佔空間、需要清潔、影響退租，甚至增加搬家成本。真正成熟的租屋升級，應該先問三件事：能不能復原、能不能搬走、能不能減少日常雜物。",
        "editorialAngle": "先看可復原、可搬走、可減少雜物。",
        "sections": [
            ("可復原性先於風格", "貼皮、掛鉤、燈具和收納若會留下痕跡，就要先看租約與屋況。漂亮不是第一條件，退租時能否恢復才是。", "任何安裝、黏貼或承重都應回商品頁與租約確認。"),
            ("燈光要看插座，不要只看角落氛圍", "租屋常見問題是插座少、牆面不能動、動線窄。立燈、桌燈或延長線都要先畫出線路，避免變成絆腳與視覺混亂。", "用電安全與線材規格不可只靠照片判斷。"),
            ("可移動家具要真的能移動", "推車、小邊桌、收納櫃若太重或輪子不好用，就只是另一件大型家具。購買前要看尺寸、重量、輪子、門寬與搬家條件。", "可移動的價值在於日常能調整，不是名稱裡有輪子。"),
            ("常見錯誤：用收納掩蓋過量物品", "收納格和箱子會讓空間暫時整齊，但如果物品量沒有下降，只是把雜物換一個形狀。", "先減少低頻物件，再決定收納尺寸。"),
            ("下單前的租屋四問", "會不會留痕、搬家能不能帶走、日常會不會更好清、是否真的增加可用空間。四題都通過，再買。", "Elite Fashion 編輯團隊的判斷是：租屋升級的價值不是讓房間像樣品屋，而是讓每天回家少一點將就。"),
        ],
        "faq": [("租屋可以用貼皮改造嗎？", "要先看租約、牆面或家具材質，以及商品移除後是否可能留痕。"), ("租屋最先買燈還是收納？", "先看插座、動線和雜物來源。若桌面混亂，收納可能比燈更優先。"), ("可移動家具怎麼選？", "看尺寸、重量、輪子、門寬和未來搬家成本，不只看外型。")],
    },
}


def load_matrix_rows() -> list[dict[str, str]]:
    with base.MATRIX_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    for row in rows[60:65]:
        copied = dict(row)
        copied.update(ROW_OVERRIDES[copied["slug"]])
        selected.append(copied)
    return selected


def update_tracker(articles: list[dict[str, Any]], tracker_rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    by_merchant = {row["merchant_id"]: row for row in tracker_rows}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]:
            mentions[product["merchantId"]].append(article)
    for merchant_id, hits in mentions.items():
        row = by_merchant[merchant_id]
        row["coverage_status"] = "live"
        row["article_created"] = "true"
        row["link_status"] = "usable"
        row["risk_notes"] = row.get("risk_notes") or "不使用誇大推薦語氣，商品規格以 momo 商品頁為準"
        slugs = [item for item in row.get("article_slug", "").split(";") if item]
        urls = [item for item in row.get("live_url", "").split(";") if item]
        increment = 0
        for article in hits:
            if article["slug"] not in slugs:
                slugs.append(article["slug"])
                increment += 1
            if article["url"] not in urls:
                urls.append(article["url"])
        row["article_slug"] = ";".join(slugs)
        row["live_url"] = ";".join(urls)
        try:
            existing_mentions = int(row.get("mention_count") or 0)
        except ValueError:
            existing_mentions = 0
        row["mention_count"] = str(existing_mentions + increment)
        row["last_mentioned_at"] = base.TODAY
        note = "2026-06-21 momo 收益型內容第十三組 5 篇已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with base.TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tracker_rows)


def update_latest_run(config: dict[str, Any], articles: list[dict[str, Any]]) -> None:
    base.pipeline.write_json(
        base.ROOT / config["paths"]["latestRunJson"],
        {
            "version": 1,
            "updatedAt": base.pipeline.now_iso(),
            "status": "generated",
            "triggerType": base.TRIGGER_TYPE,
            "queueId": base.QUEUE_ID,
            "newsletter": "not_sent_manual_codex_publish",
            "articleIds": [article["id"] for article in articles],
            "articleSlugs": [article["slug"] for article in articles],
            "notes": "Codex 手動生成 momo 收益型內容第十三組；直接推上 main 不會自動寄送電子報。",
        },
    )


base.load_matrix_rows = load_matrix_rows
base.update_tracker = update_tracker
base.update_latest_run = update_latest_run


if __name__ == "__main__":
    sys.exit(base.main())
