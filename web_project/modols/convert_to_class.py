from models import Clase
from User import User
from utils.db import  engine

def convert_to_object(dicc):
    lista = []
    for item in dicc:
        listaaux=[]
        clase = Clase(item['_source']['user_id'],item['_source']['name'],item['_source']['description'], item['_source']['duracion'],item['_source']['precio'],item['_source']['modalidad'])
        resp = engine.connect().execute(
            "SELECT * FROM users WHERE id = %s", item['_source']['user_id'])
        resp = resp.fetchone()

        if resp:
            user = User(resp[0], resp[1], resp[2], resp[3],
                        resp[4], resp[5], resp[6], resp[7])
        listaaux.append(clase)
        listaaux.append(user)
        lista.append(listaaux)



    return  lista