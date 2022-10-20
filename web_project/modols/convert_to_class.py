from Models.clase import Clase

def convert_to_object(dicc):
    lista = []
    for item in dicc:
        print(dicc)
        print(item['_source']['name'])
        print(item['_source']['user_id'])
        clase = Clase(item['_source']['user_id'],item['_source']['name'],item['_source']['description'])
        lista.append(clase)

    return  lista