# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for


app = Flask(__name__)
        
@app.route("/", methods=['GET', 'POST'])
def hello():
    return "765765!"

if __name__ == "__main__":
    app.run()