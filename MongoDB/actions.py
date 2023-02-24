import pymongo
import datetime
from connect import DatabaseTes
from typing import Dict, List, Tuple, Union

class DataActions:

    def __init__(self,db):
        '''
        db: connection to a collection
        '''
        self.db = db
    
    def __check_duplicates_in_the_same_list(self, lista_de_diccionarios: List[Dict])-> Tuple:

        dict_foo = {}
        duplicate_index = []
        list_of_non_duplicates = []
        for n, elemment in enumerate(lista_de_diccionarios):
            if elemment['tesName'] not in dict_foo.keys():
                dict_foo[elemment['tesName']] = 1
                list_of_non_duplicates.append(elemment)
            else:
                dict_foo[elemment['tesName']] += 1
                duplicate_index.append(n)
                print(f'Se ha encontrado un elemento duplicado en {n} con nombre {lista_de_diccionarios[n]["tesName"]}')
        return (list_of_non_duplicates,duplicate_index)

    def __compare_lists(self, list_of_dicts_A: List[Dict] = [], list_of_dicts_B: List[Dict] = []) -> List[Dict]:
        '''
        Busca los diccionarios de B que no están en A
        '''

        # Convertir la lista A en un conjunto de tuplas de los elementos de cada diccionario
        set_a = set((frozenset(d.items()) for d in list_of_dicts_A))

        # Crear una lista de los diccionarios de B que no están en A
        lista_c = [d for d in list_of_dicts_B if frozenset(d.items()) not in set_a]

        # Devolver la lista de diccionarios C
        return lista_c





    def delete_all_and_insert_many(self, New_set_of_documents: List[Dict] = []):
        '''
        Elimina todos los documentos de una colección
        '''
        self.db.delete_many({})
        list_toinsert = self.__check_duplicates_in_the_same_list(New_set_of_documents)[0]
        self.db.insert_many(list_toinsert)
    

    def check_duplicates_and_insert_many(self, list_of_dicts: List[Dict] = []):
        '''
        Chequea que no se intentan insertar elementos existentes en la base de datos
        inserta los documentos que no existen
        '''
        existing_docs = list(dbt.find({}, {"tesName": 1, "_id": 0}))
        list_to_insert = self.__check_duplicates_in_the_same_list(list_of_dicts)[0]
        list_foo = [{'tesName':i['tesName']} for i in list_to_insert]
        list_of_dicts = self.__compare_lists(existing_docs, list_foo)
        self.db.insert_many(list_of_dicts)




if __name__ == '__main__':
    objeto = DatabaseTes(True)
    objeto.connect()
    db = objeto.collection('tes')
    dbt = objeto.collec
    dbt_accion = DataActions(dbt)
    print(dbt.find_one())