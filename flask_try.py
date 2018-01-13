from flask import Flask, request, jsonify, abort, make_response, render_template
from pycirculate.anova import AnovaController
from threading import Timer
import datetime
import logging
import json
import os
import sys
import warnings
import multiprocessing
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    return 'You entered: {}'.format(request.form)

@app.route('/control', methods=['POST'])
def control():
    print "Cooking Temperature: "+ request.form['target_temp']
    print "Cooking Time: "+ request.form['set_time']
    for message in app.messages:
        print app.messages.pop()
    # print "temp: "+ str(app.anova.read_temp())
    return render_template('form.html')

def app_task(messages):
    app.messages = messages
    app.run(host='0.0.0.0', port=5000, use_reloader=False)


def anova_task(messages):
    print "Start anova"
    anova = AnovaController("88:4A:EA:15:5A:AB")
    while True:
        print "in anova task"
        messages.append ("temp: "+ str(anova.read_temp()))
        time.sleep(3)

def main():
    # print "temp: " + str(app.anova.read_temp())
    # app.run(host='0.0.0.0', port=5000, use_reloader=False)
    print "in main"
    manager = multiprocessing.Manager()
    messages = manager.list()
    p_app = multiprocessing.Process(
        target = app_task,
        args = (messages,))
    p_anova = multiprocessing.Process(
        target = anova_task,
        args = (messages,))

    p_app.start()
    p_anova.start()
    p_app.join()
    p_anova.join()

if __name__== '__main__':
        # anova = AnovaController("88:4A:EA:15:5A:AB")
    main()







