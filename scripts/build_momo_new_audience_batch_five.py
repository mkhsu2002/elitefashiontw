#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import Any

import build_momo_new_audience_batch_four as base


QUEUE_ID = "Q-0017"
TODAY = base.TODAY


ARTICLES: list[dict[str, Any]] = [
    {
        "slug": "entry-living-bathroom-scent-routine",
        "title": "不靠大量香味堆疊：玄關、客廳、浴室的氣味管理清單",
        "category": "lifestyle-culture",
        "audience": "居家儀式、空間氣味、送禮與清潔除味讀者",
        "items": ["香氛", "香品", "清潔用品", "除味用品"],
        "brands": ["TP0007128", "TP0009664", "TP0002941", "TP0005358", "TP0003706"],
        "cover": "ig_0dafceb8339b7ef4016a18d2e98e1c81939b001ed19e3930ce.png",
        "heroAlt": "玄關邊桌上的擴香、線香、托盤、清潔用品與客廳綠植",
        "excerpt": "氣味管理不是把香味加到最滿，而是先處理玄關、客廳與浴室的來源、通風與收尾。",
        "intro": "家裡的味道常常不是單一問題：玄關有鞋櫃與外出物，客廳有布品與餐後氣味，浴室又有濕氣與清潔用品。若只靠香氛疊加，短時間可能覺得有儀式感，日常卻容易變得混雜。更穩的做法，是先把氣味來源、通風、清潔與香品位置分清楚。",
        "decision": "先處理味道來源，再決定哪個角落需要香氛",
        "sceneLine": "玄關回家、客廳待客、浴室使用後與睡前收拾，是居家氣味最容易被注意到的四個時刻。",
        "priorityLine": "會產生味道的鞋櫃、垃圾桶、濕毛巾和布品要先有清潔與通風位置，香氛與香品才適合作為最後一層氣氛。",
        "mistakeLine": "常見錯誤是把不同氣味產品放在同一個小空間，最後聞到的不是層次，而是不知道從哪裡來的混合味。",
        "taiwanLine": "台灣濕度高，浴室、玄關與窗邊都要考慮通風和保存；香品、擴香與清潔品不適合長期放在濕熱或日照直射的位置。",
        "maintenanceLine": "每週固定清理香氛托盤、替換濕區用品、確認瓶身與香品保存狀態，比一次添購更多味道更能維持乾淨感。",
        "cautionLine": "有兒童、寵物、呼吸道敏感或過敏疑慮的家庭，請先看商品標示、使用方式與空間通風，不把香味當成除菌或健康保證。",
        "disclaimer": "本文為一般居家氣味與清潔用品整理參考，不構成健康、除菌或安全建議；香氛、香品與清潔用品請依商品標示和實際空間使用。",
        "brandReasons": {
            "TP0007128": "可從香氛、居家氣味與日常儀式用品方向查看",
            "TP0009664": "適合補充香氛、擴香與生活香氣參考",
            "TP0002941": "可作為居家香品、香氛與空間氣味比較",
            "TP0005358": "適合查看香品、香舖用品與禮品方向",
            "TP0003706": "可補充居家清潔、收納與日用品",
        },
    },
    {
        "slug": "office-home-snack-cabinet-nuts-tea-dessert",
        "title": "辦公室與家庭都能放的點心櫃：甜點、豆乾、咖啡與茶飲怎麼搭",
        "category": "lifestyle-culture",
        "audience": "辦公室、家庭補貨、下午茶與點心分享讀者",
        "items": ["甜點", "豆乾", "咖啡", "茶飲"],
        "brands": ["TP0004237", "TP0002208", "TP0009178", "TP0000296", "TP0008924", "TP0008451"],
        "cover": "ig_0dafceb8339b7ef4016a18d33209608193b51ca280bf2c3d22.png",
        "heroAlt": "開放層架上的點心罐、豆乾、甜點盒、咖啡器具與茶包收納",
        "excerpt": "點心櫃要好用，關鍵不是囤滿零食，而是把保存、分享、補貨與飲品搭配先分清楚。",
        "intro": "辦公室或家裡有一個點心櫃，看起來是小事，實際上很考驗秩序：甜點怕保存不當，豆乾需要留意開封，咖啡和茶飲也有不同的沖泡習慣。若只照喜好亂買，櫃子很快會變成過期、重複和沒人想吃的集合。",
        "decision": "先用保存條件分層，再用分享頻率決定補貨量",
        "sceneLine": "下午工作空檔、親友來訪、會議分享與週末追劇，是點心櫃最容易被打開的四個時刻。",
        "priorityLine": "常溫甜點、豆乾、沖泡飲與茶包要分層放，已開封品要比未開封備品更靠近手邊，避免一再重複開新的。",
        "mistakeLine": "常見錯誤是只看口味豐富，卻忘了保存期限、開封後吃完速度、是否適合分享，以及飲品是否真的有人會沖。",
        "taiwanLine": "台灣夏季濕熱，點心、茶包與咖啡都要避開悶熱窗邊；公司茶水間若人多，也要把個人補給和共享品分開。",
        "maintenanceLine": "每週看一次開封品、每月整理一次未開封備品，並把快到期品放到最前面，比一次買滿更不容易浪費。",
        "cautionLine": "食品與飲品請依個人飲食需求、過敏原、保存方式和商品標示選擇，本文不宣稱健康、控糖或體態效果。",
        "disclaimer": "本文為一般點心、飲品與辦公室補貨整理參考，不構成營養、健康或個人化飲食建議；食品資訊請以商品頁與包裝標示為準。",
        "brandReasons": {
            "TP0004237": "可從甜品、粉圓與分享型點心方向查看",
            "TP0002208": "適合作為豆乾、鹹點與常溫點心參考",
            "TP0009178": "可補充豆類點心與日常零食選項",
            "TP0000296": "適合查看咖啡杯、杯具與飲品器具",
            "TP0008924": "可作為韓系點心、飲品與生活食品補位",
            "TP0008451": "適合補充無糖茶、茶飲與辦公室飲品",
        },
    },
    {
        "slug": "coffee-cup-desk-afternoon-reset",
        "title": "咖啡杯與下午茶角落：杯具、咖啡豆、濾掛與小點心的補貨順序",
        "category": "lifestyle-culture",
        "audience": "居家辦公、下午茶、咖啡與茶飲補貨讀者",
        "items": ["杯具", "咖啡", "濾掛", "小點心"],
        "brands": ["TP0000296", "TP0002361", "TP0003278", "TP0007409", "TP0002208", "TP0009178"],
        "cover": "ig_0dafceb8339b7ef4016a18d3743c148193a7b0392ddec4ad14.png",
        "heroAlt": "窗邊工作桌上的咖啡濾杯、杯具、蜂蜜、茶飲與抽屜小點心",
        "excerpt": "下午茶角落先從杯具、沖泡動線和小點心保存開始，才不會越買越像臨時堆放。",
        "intro": "一個好用的下午茶角落，不需要像咖啡館，也不需要買滿器具。真正影響日常使用的是：杯子拿得到、沖泡後好清、點心不亂開、飲品補貨有節奏。把這些順序排好，工作日的短暫休息才會真的被使用。",
        "decision": "先決定每天會不會沖，再決定需要多少器具",
        "sceneLine": "上午第二杯、下午三點、臨時來客與晚間收桌，是杯具和小點心最常被使用的四個時刻。",
        "priorityLine": "每天使用的杯具、濾掛、茶包和小點心要放在同一條動線，備品則集中到抽屜或上層，不要擠在桌面。",
        "mistakeLine": "常見錯誤是先買漂亮杯具與濾杯，卻沒有安排濾紙、湯匙、清洗、瀝乾和垃圾處理位置。",
        "taiwanLine": "居家辦公和公司座位都可能空間有限，杯具數量要配合清洗頻率；濕杯、茶包和甜點包裝不要長時間堆在桌邊。",
        "maintenanceLine": "每天下班前清掉濕物和包裝，每週補一次濾掛、茶包或小點心，就能避免工作桌慢慢變成雜物區。",
        "cautionLine": "飲品與食品請依個人體質、咖啡因耐受、過敏原與商品標示選擇，不宣稱提神、健康或代謝效果。",
        "disclaimer": "本文為一般咖啡、茶飲、杯具與點心補貨整理參考，不構成營養或健康建議；食品與飲品資訊請以商品頁與包裝標示為準。",
        "brandReasons": {
            "TP0000296": "可從杯具、咖啡杯與桌面飲品器具查看",
            "TP0002361": "適合補充花草茶、飲品與下午茶風格參考",
            "TP0003278": "可作為異國食材、咖啡與點心補位",
            "TP0007409": "適合查看蜂蜜與日常沖泡搭配",
            "TP0002208": "可補充鹹點、豆乾與常溫點心",
            "TP0009178": "適合作為豆類點心與日常零食參考",
        },
    },
    {
        "slug": "pet-label-cleaning-restock-without-claims",
        "title": "寵物用品補貨先看標示：食品、清潔、玩具與日常記錄怎麼分區",
        "category": "lifestyle-culture",
        "audience": "新手寵物家庭、貓狗用品補貨與清潔整理讀者",
        "items": ["寵物食品", "清潔用品", "玩具", "日常記錄"],
        "brands": ["TP0000199", "TP0001094", "TP0009490", "TP0008082", "TP0000551", "TP0004035"],
        "cover": "ig_0dafceb8339b7ef4016a18d3b0556081938d4c29b7a9bd9e16.png",
        "heroAlt": "寵物用品層架上的食品罐、清潔噴瓶、玩具、牽繩與補貨筆記",
        "excerpt": "寵物用品不要只靠喜好補貨，先把食品、清潔、玩具與開封日期分區，才看得出真正需要什麼。",
        "intro": "寵物用品最容易越買越多：食品、零食、玩具、清潔用品、外出用品都看起來有用，但真的放進家裡後，常常不知道哪個已開封、哪個快用完、哪個其實寵物不習慣。補貨前先看標示與記錄，比追逐新用品更重要。",
        "decision": "先看標示、保存與使用紀錄，再決定補貨",
        "sceneLine": "餵食、外出回家、玩具輪替與清潔收尾，是寵物用品最容易散落或重複購買的四個時刻。",
        "priorityLine": "食品、清潔用品和玩具要分開收，開封日期、適用對象與保存方式要看得到，避免不同用途的用品混在同一盒。",
        "mistakeLine": "常見錯誤是看到可愛或評價高就補，卻沒有確認成分標示、尺寸、材質、寵物習慣與清潔方式。",
        "taiwanLine": "潮濕季節要留意食品保存與玩具乾燥；小宅家庭也要避免把清潔用品和食品放在同一層。",
        "maintenanceLine": "每週把開封食品、玩具狀況和清潔備品看一輪，簡單記下常用與不常用項目，下一次補貨會更準。",
        "cautionLine": "寵物食品、清潔與用品請依商品標示、寵物狀況與獸醫建議判斷，不宣稱健康、營養、行為或照護效果。",
        "disclaimer": "本文為一般寵物用品補貨與收納整理參考，不構成獸醫、營養或行為建議；寵物食品與用品請依商品標示和專業建議選擇。",
        "brandReasons": {
            "TP0000199": "可從寵物食品與日常用品方向查看，並以商品標示為準",
            "TP0001094": "適合補充寵物食品、零食與生活用品參考",
            "TP0009490": "可作為寵物用品、清潔與日常補貨比較",
            "TP0008082": "適合查看寵物食品、用品與日常照顧品項",
            "TP0000551": "可補充寵物食品與日用品補貨選項",
            "TP0004035": "適合查看寵物用品、玩具與外出小物",
        },
    },
    {
        "slug": "family-entry-bathroom-home-supplies",
        "title": "家庭玄關與浴室備品：母嬰用品、牙刷、濕紙巾與居家小物怎麼放",
        "category": "lifestyle-culture",
        "audience": "家庭補貨、親子日用品與小宅收納讀者",
        "items": ["母嬰用品", "牙刷", "濕紙巾", "居家小物"],
        "brands": ["TP0009118", "TP0007362", "TP0000500", "TP0004956", "TP0001633"],
        "cover": "ig_0dafceb8339b7ef4016a18d3f4e28c81938591c9087cf246f4.png",
        "heroAlt": "明亮浴室與玄關層架上的母嬰用品、牙刷、濕紙巾、毛巾與收納盒",
        "excerpt": "家庭備品要先分玄關、浴室與外出包，不要把母嬰用品、牙刷和濕紙巾全部塞在同一格。",
        "intro": "家庭用品最難整理的地方，是每個人都會用，但每個人的使用位置不同。濕紙巾在玄關、浴室、餐桌都可能出現；牙刷和盥洗用品在早晚最忙；母嬰用品又常需要臨時拿取。若沒有分區，補貨再多也只會找不到。",
        "decision": "先按使用位置分區，再按使用者補貨",
        "sceneLine": "出門前、回家後、睡前盥洗與臨時清潔，是家庭備品最常被拿取的四個時刻。",
        "priorityLine": "玄關放外出會用的用品，浴室放盥洗與清潔品，備品集中在一個固定位置，不要讓每個角落都變成小倉庫。",
        "mistakeLine": "常見錯誤是一次買很多家庭用品，卻沒有標示尺寸、適用年齡、開封日期或誰正在使用。",
        "taiwanLine": "小宅或租屋家庭要特別留意浴室濕氣，未開封備品不一定適合全部放浴室；玄關也要保留走道和拿包空間。",
        "maintenanceLine": "每週固定看一次浴室消耗品和外出包，每月整理一次備品箱，補貨會比臨時發現用完更從容。",
        "cautionLine": "母嬰、兒童與盥洗用品請依商品標示、年齡、使用方式與照顧者判斷選擇，不作安全或健康承諾。",
        "disclaimer": "本文為一般家庭備品、母嬰用品與盥洗用品整理參考，不構成醫療、育兒或口腔照護建議；兒童與家庭用品請以商品標示為準。",
        "brandReasons": {
            "TP0009118": "可從母嬰用品、家庭備品與日常補貨方向查看",
            "TP0007362": "適合補充居家小物、母嬰與生活用品",
            "TP0000500": "可作為嬰兒、兒童、寵物與家居百貨參考",
            "TP0004956": "適合查看母嬰用品與生活居家選項",
            "TP0001633": "可補充兒童電動牙刷與盥洗用品",
        },
    },
    {
        "slug": "beauty-scent-gift-shelf-before-buying",
        "title": "保養、香氛與小飾品送禮前先確認：膚況、氣味、保存與退換",
        "category": "lifestyle-culture",
        "audience": "日常保養、香氛送禮、美妝入門與伴手禮讀者",
        "items": ["保養", "香氛", "小飾品", "送禮"],
        "brands": ["TP0001879", "TP0007128", "TP0003071", "TP0004588", "TP0005089", "TP0007447"],
        "cover": "ig_0dafceb8339b7ef4016a18d43e1ef081939be385c9970e3372.png",
        "heroAlt": "窗邊梳妝台上的保養瓶、香氛、銀飾托盤、禮盒與花束",
        "excerpt": "保養、香氛和小飾品很適合送禮，但越貼近身體的物品，越需要先確認膚況、氣味偏好與退換規則。",
        "intro": "保養、香氛和小飾品都很有禮物感，卻也是最容易買錯的品類。氣味太主觀、保養太貼近肌膚、飾品有尺寸和材質差異；若只看包裝漂亮，很可能送出去後對方不敢用、用不上或不好退換。",
        "decision": "先確認對方能不能用，再決定包裝是否好看",
        "sceneLine": "生日、入職、搬家、節日與臨時致意，是保養香氛與小飾品最常出現的送禮時刻。",
        "priorityLine": "越貼近皮膚、嗅覺或尺寸的物品，越需要保留彈性；送禮前先看成分標示、香調描述、材質、尺寸和退換條件。",
        "mistakeLine": "常見錯誤是把自己的喜好當成對方喜好，或把熱門包裝直接等同於適合收禮者。",
        "taiwanLine": "台灣天氣濕熱，保養品與香氛保存要避開高溫日曬；飾品也要考慮收納、防潮與日常配戴習慣。",
        "maintenanceLine": "若是替自己補貨，請記錄開封日期、使用頻率和是否真的會回購；若是送禮，請保留商品資訊和退換方式。",
        "cautionLine": "保養、香氛與貼身用品請依商品標示、個人膚況、過敏史與使用方式選擇，不宣稱保養、抗老或改善效果。",
        "disclaimer": "本文為一般保養、香氛、小飾品與送禮選物參考，不構成醫療、皮膚治療或個人化建議；成分、材質與退換資訊請以商品頁公告為準。",
        "brandReasons": {
            "TP0001879": "可從保養、美妝與日常儀容用品方向查看",
            "TP0007128": "適合補充香氛、禮物與居家氣味用品",
            "TP0003071": "可作為銀飾、項鍊、耳環與送禮小飾品參考",
            "TP0004588": "適合查看極簡保養與日常保養品項",
            "TP0005089": "可補充韓系彩妝保養與送禮小物",
            "TP0007447": "適合作為美妝、保養與日常儀容選項",
        },
    },
]


def update_queue(articles: list[dict[str, Any]], config: dict[str, Any]) -> None:
    path = base.ROOT / config["paths"]["queueJson"]
    queue = base.pipeline.load_json(path)
    by_slug = {article["slug"]: article for article in articles}
    series = next((item for item in queue["series"] if item.get("queueId") == QUEUE_ID), None)
    if series is None:
        series = {
            "queueId": QUEUE_ID,
            "topic": "氣味管理、點心飲品、寵物補貨、家庭備品與送禮選物延伸",
            "direction": "延伸剩餘可用 momo A/B 品牌到日常補貨與送禮情境；公開文章聚焦讀者採買順序、保存限制與可查證商品頁資訊。",
            "plannedCount": len(ARTICLES),
            "status": "planned",
            "source": "momo-ab-new-audience-roadmap",
            "createdAt": base.pipeline.now_iso(),
            "seriesName": "momo 新受眾第五批",
            "items": [
                {
                    "order": index,
                    "slug": spec["slug"],
                    "title": spec["title"],
                    "targetReader": spec["audience"],
                    "category": spec["category"],
                    "status": "planned",
                }
                for index, spec in enumerate(ARTICLES, start=1)
            ],
        }
        queue["series"].append(series)
        queue["nextQueueSequence"] = max(int(queue.get("nextQueueSequence", 1)), 18)
    spec_by_slug = {spec["slug"]: spec for spec in ARTICLES}
    for index, item in enumerate(series["items"], start=1):
        spec = spec_by_slug.get(item.get("slug"), {})
        item.setdefault("order", index)
        if spec:
            item.setdefault("targetReader", spec["audience"])
            item.setdefault("category", spec["category"])
            item.setdefault("title", spec["title"])
        article = by_slug.get(item.get("slug"))
        if article:
            item["status"] = "published"
            item["articleId"] = article["id"]
            item["file"] = article["file"]
            item["publishedAt"] = article["publishedAt"]
    series["status"] = "completed" if all(item.get("status") == "published" for item in series["items"]) else "in_progress"
    queue["updatedAt"] = base.pipeline.now_iso()
    base.pipeline.write_json(path, queue)


def update_tracker(articles: list[dict[str, Any]], tracker_rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    by_merchant = {row["merchant_id"]: row for row in tracker_rows}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for article in articles:
        merchant_ids = {product["merchantId"] for product in [*article.get("mainProducts", []), *article.get("sidebarProducts", [])]}
        merchant_ids.update(brand["merchantId"] for brand in article.get("featuredBrands", []))
        for merchant_id in merchant_ids:
            mentions[merchant_id].append(article)
    for merchant_id, hits in mentions.items():
        row = by_merchant[merchant_id]
        row["coverage_status"] = "live"
        row["article_created"] = "true"
        row["link_status"] = "usable"
        row["risk_notes"] = row.get("risk_notes") or "不使用誇大推薦語氣，商品規格以 momo 商品頁為準"
        existing_slugs = [part for part in row.get("article_slug", "").split(";") if part]
        existing_urls = [part for part in row.get("live_url", "").split(";") if part]
        increment = 0
        for article in hits:
            if article["slug"] not in existing_slugs:
                existing_slugs.append(article["slug"])
                increment += 1
            if article["url"] not in existing_urls:
                existing_urls.append(article["url"])
        row["article_slug"] = ";".join(existing_slugs)
        row["live_url"] = ";".join(existing_urls)
        if increment:
            row["mention_count"] = str(int(row.get("mention_count") or 0) + increment)
        row["last_mentioned_at"] = TODAY
        note = "2026-05-28 momo 新受眾第五批氣味點心寵物家庭與送禮文章已置入。"
        if note not in row.get("notes", ""):
            row["notes"] = (row.get("notes", "").rstrip() + (" " if row.get("notes", "").strip() else "") + note).strip()
    with base.TRACKER_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(tracker_rows)


def main() -> int:
    base.QUEUE_ID = QUEUE_ID
    base.ARTICLES = ARTICLES
    base.update_queue = update_queue
    base.update_tracker = update_tracker
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
