#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Flask
from flask import Flask, render_template, request, json, session, send_file

#Gunicorn.
import multiprocessing
import gunicorn.app.base
from six import iteritems

#Otros
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
import traceback    #Para poder impirmir el error.
from werkzeug.utils import secure_filename  #Para leer nombres de ficheros
import threading
from BrainModel.red_brain import *

store = RedisStore(redis.StrictRedis(host='redis'))
app = Flask(__name__)
KVSessionExtension(store, app)
app.config['SECRET_KEY']='BrainJorge'
lock = threading.Lock() #Creamos el candado
edema = None
retino = None

@app.route("/", methods=['POST','GET'])    #Indicamos el tipo de forma para las peticiones, get o post.
def controlador():
    try:
        print("Peticion recibida")
        if request.method=='POST':
            if 'tipo' in request.form:
                _tipo=request.form['tipo']
            else:
                _tipo=None
        else:
            _tipo=request.args.get('tipo')
        if _tipo=="imagen":
            return procesarImagen(request)
        elif _tipo=="resultado":
            return mostrarResultado()
        else:
            return render_template("principal.html")
    except Exception as e:
        traceback.print_exc(e)
        return e


def procesarImagen(request):
    global brain
    print('Procesando Imagen')
    brain = BrainTumor()

    # Obtenemos el fichero que queremos analizar
    f = request.files['miFichero']
    print('Procesando imagen...')
    # secure_filename te lo guarda con el mismo nombre de fichero.
    f.save('./static/ImagenesBrain/'+secure_filename(f.filename))
    f.close

    print('Clasificando... 2')
    session['nombreImagen']=secure_filename(f.filename)
    lock.acquire()
    session['brain']= brain.classifyTumor("./static/ImagenesBrain/"+secure_filename(f.filename))
    
    print('Ejecutando GradCAM...')
    name_path = ('./static/ImagenesBrain/GradCAM/'+secure_filename(f.filename))
    imGC_plt = brain.img2Cam("./static/ImagenesBrain/"+secure_filename(f.filename), name_path)
    
    session['gradCAM'] = secure_filename(f.filename)
    print('Imagen procesada')
    lock.release()

    return json.dumps({}), 200

def mostrarResultado():
    return render_template("resultado.html", brain=session['brain'], foto = session['gradCAM'])


#####################     Gunicorn      #####################
def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
    
###########################################################

if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '5000'),
        'workers': 1,
        'threads': number_of_workers(),
        'reload': True
    }
    StandaloneApplication(app, options).run()
