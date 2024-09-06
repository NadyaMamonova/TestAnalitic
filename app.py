# основная логика приложения:
from elasticsearch import Elasticsearch
import sqlite3
import csv
import requests
import json
import os

# Конфигурационный файл
CONFIG_FILE = "config.json"

# Загружаем конфигурацию
try:
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print("Файл конфигурации не найден!")
    exit()

# Подключение к Elasticsearch
es = Elasticsearch(hosts=[config['elasticsearch_host']])

# Проверка подключения к Elasticsearch
if not es.ping():
    print("Ошибка подключения к Elasticsearch!")
    exit()

# Подключение к БД
db_path = config['database_path']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание индекса (если не существует)
es.indices.create(index="documents", ignore=400)

# Загрузка CSV-файла
csv_url = config['csv_url']
try:
    response = requests.get(csv_url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Ошибка загрузки CSV: {e}")
    exit()

# Проверка существования CSV-файла
csv_file_path = "posts.csv"
if os.path.exists(csv_file_path):
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                doc_id = int(row['id'])
            except ValueError:
                print(f"Ошибка преобразования id: {row['id']}")
                continue

            text = row['text']
            created_date = row['created_date']
            rubrics = json.loads(row['rubrics'])

            # Индексация документа в Elasticsearch
            es_response = es.index(index="documents", body={"text": text})
            doc_id = es_response['_id']

            # Загрузка CSV-файла
            csv_url = config['csv_url']
            try:
                response = requests.get(csv_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Ошибка загрузки CSV: {e}")
                exit()

            # Проверка существования CSV-файла
            csv_file_path = "posts.csv"
            if os.path.exists(csv_file_path):
                with open(csv_file_path, "r", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            doc_id = int(row['id'])
                        except ValueError:
                            print(f"Ошибка преобразования id: {row['id']}")
                            continue

                        text = row['text']
                        created_date = row['created_date']
                        rubrics = json.loads(row['rubrics'])

                        # Индексация документа в Elasticsearch
                        es_response = es.index(index="documents", body={"text": text})
                        doc_id = es_response['_id']

                        # Сохранение в БД
                        try:
                            cursor.execute(
                                "INSERT INTO documents (id, text, created_date, rubrics) VALUES (?, ?, ?, ?)",
                                (doc_id, text, created_date, json.dumps(rubrics)),
                            )
                            conn.commit()
                        except sqlite3.IntegrityError:
                            print(f"Документ с ID {doc_id} уже существует!")
                            continue


        # Индексация документа
        def index_document(doc_id, text):
            body = {"text": text}
            es.index(index="documents", id=doc_id, body=body)


        # Поиск по тексту
        def search_documents(query):
            response = es.search(
                index="documents",
                body={
                    "query": {"match": {"text": query}},
                    "sort": {"created_date": {"order": "desc"}},
                    "size": 20,
                },
            )

            results = []
            for hit in response["hits"]["hits"]:
                doc_id = hit["_id"]
                with conn:
                    cursor.execute("SELECT id, rubrics, text, created_date FROM documents WHERE id = ?", (doc_id,))
                    document = cursor.fetchone()
                    if document:
                        results.append(document)

            return results


        # Удаление документа
        def delete_document(doc_id):
            try:
                es.delete(index="documents", id=doc_id)
                with conn:
                    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
                    conn.commit()
                print(f"Документ с ID {doc_id} удален.")
            except Exception as e:
                print(f"Ошибка удаления документа: {e}")


        # Удаление документа
        doc_id = 1
        delete_document(doc_id)

        # Закрытие соединения с БД
        conn.close()