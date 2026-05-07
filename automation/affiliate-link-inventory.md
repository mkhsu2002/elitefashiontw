# Affiliate Link Inventory

Updated: 2026-05-07

This file tracks live commercial links that require visible disclosure and `rel="sponsored nofollow"` handling.

| Page | Slot | Destination | Status | Notes |
| --- | --- | --- | --- | --- |
| `crossbody-bag-style-guide.html` | Horizon 厚片吐司小包 | `https://www.icareushop.com.tw/SalePage/Index/10671058` | Live link tagged | Three CTAs now include visible disclosure and sponsored/nofollow attributes. |
| `lifestyle-culture/arsenal-mit-japan-stainless-scissors-project.html` | ARSENAL 多功能萬用剪 | `https://www.icareushop.com.tw/SalePage/Index/8922065` | Live link tagged | Generated page and source article now include disclosure. |
| `lifestyle-culture/arsenal-mit-japan-stainless-scissors-project.html` | ARSENAL 長刃家用剪 | `https://www.icareushop.com.tw/SalePage/Index/9669238` | Live link tagged | Generated page and source article now include disclosure. |
| `lifestyle-culture/arsenal-mit-japan-stainless-scissors-project.html` | ARSENAL 不沾事務剪 | `https://www.icareushop.com.tw/SalePage/Index/8944550` | Live link tagged | Generated page and source article now include disclosure. |
| `ai-innovation/petek-smart-pet-care-project.html` | Petek 智能寵物餵食機 S36D | `https://www.icareushop.com.tw/SalePage/Index/9256154` | Live link tagged | Generated page and source article now include disclosure. |
| `ai-innovation/petek-smart-pet-care-project.html` | Petek 13L 自動真空儲糧桶 | `https://www.icareushop.com.tw/SalePage/Index/10397938` | Live link tagged | Generated page and source article now include disclosure. |
| `ai-innovation/petek-smart-pet-care-project.html` | Petek 無線寵物飲水機 W25Pro | `https://www.icareushop.com.tw/SalePage/Index/10403295` | Live link tagged | Generated page and source article now include disclosure. |
| `yoga-complete.html` | 瑜伽墊報告 | `https://www.icareushop.com.tw/page/fsc.yogamat` | Live link tagged | Legacy commercial CTA now has visible disclosure. |
| `outdoor-escapes/backpack-comfort-guide.html` | 登山背包商品 | `https://www.icareushop.com.tw/SalePage/Index/10393954` | Live link tagged | Legacy commercial CTA now has visible disclosure. |
| `outdoor-escapes/taiwan-hiking-routes-and-style.html` | 戶外裝備頁 | `https://www.icareushop.com.tw/page/hiking` | Live link tagged | Legacy commercial CTA now has visible disclosure. |
| `life-proposals/eye-care-presbyopia.html` | 視能商品分類 | `https://www.icareushop.com.tw/categories/eye-care` | Live link tagged | Legacy commercial CTA now has visible disclosure. |

## Generator Guardrail

`scripts/content_pipeline.py` now treats `https://www.icareushop.com.tw/` CTA links as commercial links. Future generated article CTAs for that host are rendered with `target="_blank"` and `rel="sponsored nofollow noopener noreferrer"`, plus a visible disclosure before the first CTA.
