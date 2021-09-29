from flask import Flask, request, jsonify
import requests
import os
import tester
from tester import Scraper
from rq import Queue
from rq.job import Job
from red import conn




# Initialize App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
q = Queue(connection=conn)

# Run Downloader
@app.route('/run')
def run():
    job = q.enqueue(tester.run)
    print(job.get_id())
    return 'OK'

@app.route('/copyai/titulos/<keyword>', methods=['GET'])
def run_copyAITitulos(keyword):
    job = q.enqueue(Scraper().getCopyAiTitulos, args=(keyword,))
    return f'OK;{job.get_id()}'

@app.route('/copyai/texto/<keyword>', methods=['GET'])
def run_copyAITexto(keyword):
    job = q.enqueue(Scraper().getCopyAiTexto, args=(keyword,))
    return f'OK;{job.get_id()}'

@app.route('/copyai/completo/<keyword>', methods=['GET'])
def run_copyAICompleto(keyword):
    job = q.enqueue(Scraper().getCopyAiCompleto, args=(keyword,))
    return f'OK;{job.get_id()}'

@app.route('/result/<job_id>', methods=['GET'])
def result(job_id):
    try:
        job = q.fetch_job(job_id)
        if job.get_status() == 'finished':
            return job.result
        else:
            return job.get_status()
    except Exception as e:
        return 'GONE'
    
    

'''
@app.route('/copyai/textos/<keyword>', methods=['GET'])
def run_copyAITextos(keyword):
    print(f"keyword: {keyword}")
    job = q.enqueue(Scraper().getCopyAiTexto(keyword))
    print(job.get_id())
    return f'OK'



@app.route('/run2')
def run_stack():
    job = q.enqueue(Scraper().getStackOverflow)
    print(job.get_id())
    return 'OK'


@app.route('/run3')
def run_TA():
    job = q.enqueue(Scraper().getGithub)
    print(job.get_id())
    return 'OK'
'''

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
