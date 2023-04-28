from flask import Flask
import json
from flask import request
import requests
import pandas
from database import *
import os
import urllib.request
import pandas
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/download/<book_id>")
def DownloadExcel(book_id):
    book = Book(title="title", author="author", published="published", date_added=datetime.datetime.now(),
                    date_deleted=datetime.datetime.max)
    try:
        int(book_id)
    except:
        pass
    else:
        DatabaseConnector.get_borrowsExcel(book_id)
    return f'<a href=\"statisticsBook{book_id}.xlsx\" download>Скачать статистику по книге</a>'

app.run("127.0.0.1", port=8081)
