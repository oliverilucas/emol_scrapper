import csv
import pandas as pd
from os.path import exists

def make_csv(title,summary,body,today,link):
    csv_columns = ['titulo','resumen','cuerpo','fecha','link']
    dict_data = [{'titulo': title, 'resumen': summary, 'cuerpo': body, 'fecha': today, 'link': link}]
    csv_file = "news/emol_news.csv"

    if exists("news/emol_news.csv") == True:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter="|")
            for data in dict_data:
                writer.writerow(data)
    else:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter="|")
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
