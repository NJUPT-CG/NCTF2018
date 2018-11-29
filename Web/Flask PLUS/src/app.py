#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,render_template_string,redirect,request,session,abort,send_from_directory
import os
app = Flask(__name__)
@app.route("/")
def index():
    "主页"
    return render_template("index2.html")
@app.errorhandler(404)
def page_not_found(e):
    def safe_jinja(s):
        blacklist = ['import','getattr','os','class','subclasses','mro','request','args','eval','if','for','subprocess','file','open','popen','builtins','compile','execfile','from_pyfile','config','local','self','item','getitem','getattribute','func_globals','__init__','join','__dict__']
        flag = True
        for no in blacklist:
            if no.lower() in s.lower():
               flag= False
               break
        return flag
    template = '''
{%% block body %%}
    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>%s</h3>
    </div> 
{%% endblock %%}
''' % (request.url)
    if safe_jinja(request.url):
        return render_template_string(template), 404
    else:
        return render_template("404.html"), 404
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

