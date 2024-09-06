# Простой поисковик по документам

Этот проект реализует простой поисковик по текстам документов, используя Elasticsearch для индексации и поиска, а SQLite для хранения данных.

## Требования

Python 3.6+
Elasticsearch 7.x+
SQLite

## Установка

1. Создайте виртуальное окружение:

bash
   python3 -m venv env
   source env/bin/activate
   
2. Установите зависимости:
   
bash
   pip install -r requirements.txt
   
## Настройка

1. Создайте файл конфигурации config.json:

json
   {
     "elasticsearch_host": "http://localhost:9200", 
     "database_path": "mydatabase.db",
     "csv_url": "https://yadi.sk/d/UYooXd9q2yqTMQ?dl=1" 
   }
   
   * ⒷⓃelasticsearch_hostⓃ:Ⓑ  Адрес вашего сервера Elasticsearch (по умолчанию localhost:9200).
   * ⒷⓃdatabase_pathⓃ:Ⓑ  Путь к файлу базы данных SQLite (по умолчанию  Ⓝmydatabase.dbⓃ).
   * ⒷⓃcsv_urlⓃ:Ⓑ URL вашего CSV-файла с данными о документах.

2. Создайте таблицу в базе данных:

sql
   CREATE TABLE documents (
     id INTEGER PRIMARY KEY,
     text TEXT,
     created_date DATETIME,
     rubrics TEXT
   );
   
## Запуск

1. Запустите сервер Elasticsearch:

    Зависит от вашей установки Elasticsearch
    Обычно запускается с помощью команды service elasticsearch start
   
2. Запустите скрипт:

    bash
        
    python app.py   
## Использование

1. ⒷЗагрузите CSV-файл с данными о документах:Ⓑ  
    *  Используйте API-запрос  ⓃPOST /documentsⓃ  с  Ⓝmultipart/form-dataⓃ  и  CSV-файлом.  
    *  Сервис проиндексирует данные в Elasticsearch и сохранит информацию в SQLite.

2. ⒷПоиск по текстам:Ⓑ
    *  Используйте API-запрос  ⓃGET /documentsⓃ  с параметром  ⓃqueryⓃ  (строка для поиска). 
    *  Сервис вернет список документов, соответствующих запросу.

3. ⒷПолучение документа по ID:Ⓑ
    *  Используйте API-запрос  ⓃGET /documents/{id}Ⓝ  с  ⓃidⓃ  документа.

4. ⒷУдаление документа по ID:Ⓑ
    *  Используйте API-запрос  ⓃDELETE /documents/{id}Ⓝ  с  ⓃidⓃ  документа.
