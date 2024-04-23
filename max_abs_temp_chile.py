#!/usr/bin/env python
# coding: utf-8

# In[1]:

def main():


    import requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    import undetected_chromedriver as uc
    import time
    import re
    import os



    # In[2]:


    # Funcion para obtener los headers de la tabla, ya que hay diferentes para las tablas en diferentes paginas.
    """
    utilizo undectected_chromedriver para asegurar que el bot podra entrar a la pagina web
    creo el objeto con beautifulsoup
    y luego busco la tabla con div id tablecontainer
    para obtener los nombres de la columna los busco de la misma forma pero con "th" y class = "HDim", el for loop y el if
    son para poder extraer solo los nombres de columna y no el resto de informacion que no me sirve.
    """

    def get_headers():
        html = browser.page_source
        soup = bs(html, 'lxml')
        tabla = soup.find('div', {'id': 'tablecontainer'})

    # th table headers
        headers2 = []
        headers = tabla.find_all("th", class_="HDim")
        for h in headers:
            if len(str(h)) <= 50:
                headers2.extend(h)
            else:
                pass
    
        # elimino duplicados
        headers_without_duplicates = []
        for header in headers2:
            if header not in headers_without_duplicates:
                headers_without_duplicates.append(header)
        return headers_without_duplicates


    # In[3]:


    # FUNCION PARA SACAR LA INFO DE LA TABLA
    """
    Al igual que la funcion anterior, pero ahora obtengo la informacion de la tabla, lo cual cada fila es la informacion de un mes de cierto año
    por lo que mediante "tr" obtengo la informacion como lista y cada item es un mes de un año con su informacion respectiva
    reemplazo los ".." que es informacion que no esta como "00.0" siguiendo el patron de la tabla y luego poder usar regex.
    """
    def get_table(first_row, last_row):
        fix_list = []
        html = browser.page_source
        soup = bs(html,'lxml')
        tabla = soup.find('div',{'id':'tablecontainer'})
        rows = tabla.find_all("tr")
        rowsList = []
        for r in rows:
            row = r.text
            rowsList.append(row)
        
        data = rowsList[first_row:last_row]
        time.sleep(1)
        for i in data:
            rowN = i.replace("..","00.0")
            fix_list.append(rowN)
        print("DONE get_table")
        return fix_list


    # In[4]:


    # Funcion para pasar a dataframe
    """
    Ya tengo la informacion en dos listas diferentes, tanto los nombres de columnas ( que varian pagina a pagina ) y la informaicion respectiva
    utilizo regex para poder separar la info y transformarla en dataframe.
    primero identifico el año y el mes ( 4 digitos, espacio, letras)
    segundo identifico cada valor para separarlo en columna (1 o 2 digitos, punto, un digito (##.#), ademas del signo - que no es obligacion)
    Se pasan a un diccionario dodne la clave es el identificador de año/mes
    Luego se pasa a dataframe para su posterior union.
    """
    def get_dataframe(list_data, header_list):
        dict_data = {}
    
        for cadena in list_data:
            patron_regex_Ym = r'\d{4}\s+[A-Z][a-z]+' #cuatro digitos un espacio o mas, letra mayuscula, letras minusculas.
            patron_regex_num = r'-?\d{1,2}\.\d' #un numero o mas.un numero
            # regex para encontrar lo que busco
            match_Ym = re.findall(patron_regex_Ym, cadena)
            match_num = re.findall(patron_regex_num, cadena)    
            #agrego informacion de clave valor
            dict_data[match_Ym[0]] = match_num
        df_dict = pd.DataFrame.from_dict(dict_data, orient='index', columns=header_list)
        print("DONE get_df")
        return df_dict


    # In[5]:


    url = "https://stat.ine.cl/?lang=es&SubSessionId=9cd00b7a-6e1c-48a0-aa68-667b23a8b203"


    # In[6]:


    """
    aqui comienza el bot a trabajar, utilizo el url de la pagina de estadisticas de chile,
    utilizo Chorme para el bot y luego clickeo en 3 partes diferentes para poder llegar a la tabla que me interesa, "temperaturas maximas absolutas"
    """

    browser = uc.Chrome()
    browser.get(url)
    browser.find_element("xpath", '//*[@id="browsethemes"]/ul/li[2]').click()
    browser.find_element("xpath", '//*[@id="browsethemes"]/ul/li[2]/ul/li[1]/span').click()
    browser.find_element("xpath", '//*[@id="browsethemes"]/ul/li[2]/ul/li[1]/ul/li[1]/a[2]').click()


    # In[7]:


    time.sleep(1)

    html = browser.page_source
    soup = bs(html,'lxml')


    # In[8]:


    # Como son 6 paginas de tablas diferentes, utilizo el rango 1,6 con un loop que que itera y me obtiene cada dataframe mediante las funciones previamente mostradas.

    dataframes = {}

    for n in range(1,6):
        
        headers = []
        if n == 1:
            time.sleep(3)
            headers = get_headers()
            data = get_table(4, 112)
            dataframes[f'data{n}'] = get_dataframe(data,headers)
        else:
            headers = get_headers()
            data = get_table(4, 115)
            dataframes[f'data{n}'] = get_dataframe(data,headers)    
        browser.find_element("xpath", '//*[@id="_ctl0__ctl0_cphCentre_ContentPlaceHolder1__ctl1_OutpoutContainer"]/div[1]/img[3]').click()
        time.sleep(5)


    # In[9]:




    # In[10]:


    # cierro la ventana que he abierto
    browser.close()


    # In[11]:


    # Comprobacion de que todos los dataframes estan ahi.
    for i in dataframes.keys():
        print(i)


    # In[12]:


    dataframes_list = list(dataframes.values())

    # Concatenar todos los dataframes en uno solo
    df_combined = pd.concat(dataframes_list, axis=0)


    # In[17]:


    # utilizo os para poder entrar a la carpeta actual
    directorio_actual = os.getcwd()

    # junto el path con el nombre del archivo
    ruta_csv = os.path.join(directorio_actual, 'max_abs_temp_chile.csv')

    # exporto en el path 
    df_combined.to_csv(ruta_csv, index=True)


    # df_combined.to_csv('max_abs_temp_chile.csv', index=False)
    print("csv done")

if __name__ == "__main__":
    main()