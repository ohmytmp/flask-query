import json
import flask
import hashlib

from ohmytmp import Ohmytmp
from ohmytmp_plugins.taggy import TagInterpreter
from ohmytmp_plugins.simimg import SimImg


app = flask.Flask("qwq")

sha_p = dict()
p_sha = dict()

ai = Ohmytmp()
si = SimImg()
ti = TagInterpreter()

ai.register(si)
ai.register(ti)
ai.walk('../example')
ai.walk('./')
print(si.data)
print(ti.data)

def showimgs(files: list) -> str:
    print(files)
    jsrc = list()
    for p in files:
        if p not in p_sha:
            psha = hashlib.new('sha256', p.encode('utf8')).hexdigest()
            p_sha[p] = psha
            sha_p[psha] = p
        jsrc.append('/file/%s' % p_sha[p])
    return open('img.html', 'r').read().replace(
        '["Untitled.png"]',
        json.dumps(jsrc)
    )


@app.route('/')
def root():
    return 'Hello world!'


@app.route('/file/<fsha256>')
def file(fsha256: str) -> flask.Response:
    return flask.send_file(sha_p[fsha256])


@app.route('/sim/<phash>')
def sim(phash: int) -> str:
    return showimgs(si.findsim(int(phash), 4))

@app.route('/tag/<tags>')
def tag(tags: str) -> str:
    return showimgs(ti.getsrcs(tags))
