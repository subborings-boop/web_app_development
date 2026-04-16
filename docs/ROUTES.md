# 路由設計文件 (ROUTES) - 食譜收藏夾系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `templates/index.html` | 顯示首頁（包含搜尋框與推薦食譜） |
| 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 註冊處理 | POST | `/auth/register` | — | 接收註冊表單，存入 DB，重導向至登入頁 |
| 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 登入處理 | POST | `/auth/login` | — | 驗證帳密，設定 session，重導向至首頁 |
| 登出處理 | GET | `/auth/logout` | — | 清除 session，重導向 |
| 食譜列表與搜尋 | GET | `/recipes` | `templates/recipe/list.html` | 列出所有公開食譜，支援 `?q=` 參數作基礎搜尋 |
| 食材過濾搜尋 | GET | `/recipes/search_by_ingredients` | `templates/recipe/search_result.html` | 依據選擇的多樣食材進行過濾 |
| 檢視食譜詳情 | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示單筆食譜詳情 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipe/form.html` | 顯示新增食譜表單（需登入） |
| 建立食譜 | POST | `/recipes` | — | 儲存表單資料，重導向至詳情頁 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/recipe/form.html` | 顯示編輯表單（需為擁有者） |
| 更新食譜 | POST | `/recipes/<id>/update` | — | 更新 DB，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除 DB 資料，重導向至首頁（需權限） |

## 2. 每個路由的詳細說明

### 2.1 頁面呈現模組 (Main)
- **`/` (GET)**
  - 處理邏輯：取得最新數筆公開食譜 `Recipe.get_all(public_only=True)` 與所有可用食材 `Ingredient.get_all()`。
  - 輸出：渲染 `index.html`。

### 2.2 認證模組 (Auth Blueprint - `/auth`)
- **`/register` (GET/POST)**
  - 邏輯：驗證欄位、密碼一致性等。呼叫 `User.create()`，密碼做雜湊處理後儲存。
  - 輸出：GET 渲染 `auth/register.html`，POST 後重導向至 `/auth/login`。
  
- **`/login` (GET/POST)**
  - 邏輯：呼叫 `User.get_by_email()`。若存在且密碼比對正確，寫入 session。
  - 輸出：GET 渲染 `auth/login.html`，POST 登入成功後重導向至首頁。

- **`/logout` (GET)**
  - 邏輯：執行 `session.clear()` 清除登入狀態，重導向首頁。

### 2.3 食譜模組 (Recipe Blueprint - `/recipes`)
- **`/recipes` (GET)**
  - 處理邏輯：若有 `?q=` 參數，依標題進行模糊搜尋；否則呼叫 `Recipe.get_all()` 列出全部公開食譜。
  - 輸出：渲染 `recipe/list.html`。

- **`/recipes/search_by_ingredients` (GET)**
  - 處理邏輯：接收多個食材 ID（例 `?ing=1&ing=3`），呼叫 `Recipe.search_by_ingredients([1, 3])` 進行條件查詢。
  - 輸出：渲染 `recipe/search_result.html`。

- **`/recipes/<recipe_id>` (GET)**
  - 處理邏輯：根據 id 查詢該食譜，判斷使用者是否有權限檢視（公開，或為建立者）。
  - 輸出：渲染 `recipe/detail.html`。錯誤回傳 404/403。

- **`/recipes/new` (GET) & `/recipes` (POST)**
  - 處理邏輯：需登入（自定義 login_required 裝飾器）。POST 接收建立標題、圖片、步驟等與「食材陣列」。
  - 輸出：GET 渲染 `recipe/form.html`，POST 建檔成功後跳轉至 `/recipes/<id>`。

- **`/<recipe_id>/edit` (GET) & `/<recipe_id>/update` (POST)**
  - 處理邏輯：需登入且為該食譜擁有者。POST 處理欄位與多對多關聯的更動。

- **`/<recipe_id>/delete` (POST)**
  - 處理邏輯：擁有者或管理員身分。刪除該筆資料後重導向到首頁。

## 3. Jinja2 模板清單

- `templates/base.html`：基底共用模板（含 nav、footer 等區塊宣告）
- `templates/index.html`：首頁（繼承 base）
- `templates/auth/login.html`：登入頁（繼承 base）
- `templates/auth/register.html`：註冊頁（繼承 base）
- `templates/recipe/list.html`：一般食譜列表（繼承 base）
- `templates/recipe/search_result.html`：使用食材組合篩選的結果頁（繼承 base）
- `templates/recipe/detail.html`：食譜詳情頁（繼承 base）
- `templates/recipe/form.html`：新增/編輯共用表單（繼承 base）
