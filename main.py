from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import datetime
from datetime import timedelta
import time
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from pandas import Series
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
import selenium.webdriver.support.ui as ui
from pprint import pprint
from airtable import Airtable


app = Flask(__name__)
app.secret_key = 'clave_secreta'
#app.permanent_session_lifetime = timedelta(hours=24)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('logged_in', None) == True:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    return render_template('index.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
   error = None
   if request.method == 'POST':
      if request.form['password'] != 'credility' or request.form['mail'] != 'mati@credility.com':
         error = 'usuario y/o contraseña incorrecta.'
         return render_template('login.html', error=error)
      else:
         session['logged_in'] = True
         return redirect(url_for('index'))
   return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
   session['logged_in'] = False
   return redirect(url_for('login'))

@app.route('/clientes/')
@login_required
def clientes():
    return render_template('clientes.html')

@app.route('/nosis/')
@login_required
def nosis():
    return render_template('nosis.html')

@app.route('/nosisresult/', methods=["GET", "POST"])
@login_required
def nosisresult():
   cuit = request.form['cuit_nosis']
   nosis_sociedad = request.form['nosis_soc']
   id_airtable = request.form['id_air']
   if nosis_sociedad == 'personal':
      options = Options()
      options.headless = False
      #driver = webdriver.Chrome('./Chrome/chromedriver', chrome_options=options)
      driver = webdriver.Chrome(executable_path='./Chrome/chromedriver', chrome_options=options)
      # keys
      usuario = '457993'
      contra = '079778'
      #cliente:
      cuit_long = str(cuit)[0:2]+'-'+str(cuit)[2:10]+'-'+str(cuit)[10:11]
      start_time = time.time()
      # registro en NOSIS
      driver.get('http://sac31.nosis.com/net/manager')
      driver.find_element_by_id('Email').send_keys(usuario)
      driver.find_element_by_id('Clave').send_keys(contra)
      try:
         driver.find_element_by_xpath('//*[@id="frmInicioSesion"]/div/div/div[2]/div[2]/button').click()
      except NoSuchElementException:
         driver.find_element_by_id('iniciarSesion').click()
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(cuit)
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(Keys.ENTER)
      time.sleep(15)
      driver.find_element_by_id('btnConsultar').click()
      try:
         time.sleep(15)
      except NoSuchElementException:
         time.sleep(120)
      try:
         driver.find_element_by_id('link-continuar').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[2]').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').click()
      except NoSuchElementException:
         pass
      nacimiento = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[2]/div[3]/div[1]/span/b').text
      score_nosis = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]').text
      codigo_afip = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[14]/ul[2]/li[3]/span/b').text
      nosis_name = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/b').text
      domicilio = (str(driver.find_element_by_xpath("//*[contains(text(), 'Domicilio fiscal')]/following-sibling::ul").text).split("\n")[0])
      inscripcion_afip = str(driver.find_element_by_xpath("//*[contains(text(), 'Inscripción AFIP')]/following-sibling::div").text)
      #inscripcion_afip = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[16]/div[1]/div/div[3]/div[2]').text
      try:
         ganancias = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[16]/div[1]/div/div[2]/div[2]').text
      except NoSuchElementException:
         ganancias = ''
      try:
         iva = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[16]/div[1]/div/div[2]/div[3]/span').text
      except NoSuchElementException:
         iva = ''
      tabla_cda = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[4]/div/div/table[2]/tbody').text
      concurso = str(tabla_cda.partition('Concurso o Quiebra: ')[2][0:6])
      antecedentes_fiscales = str(tabla_cda.partition('Antecedentes Fiscales: ')[2][0:6])
      juicios = str(tabla_cda.partition('Juicios - Demandado: ')[2][0:6])
      oficios = str(tabla_cda.partition('Oficios Judiciales: ')[2][0:6])
      referencias = str(tabla_cda.partition('Referencias Comerciales: ')[2][0:6])
      cheques = str(tabla_cda.partition('Cheques Rechazados del BCRA: ')[2][0:6])
      tabla_AFIP = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[16]/table/tbody').text
      NSE = (str(driver.find_element_by_xpath("//*[contains(text(), 'Nivel Socioeconómico (NSE):')]").text).split('Nivel Socioeconómico (NSE): ')[1].split(' (')[0])
      try:
         compromisos = (str(driver.find_element_by_xpath("//*[contains(text(), 'Total de compromisos mensuales sistema financiero: ')]").text).split('Total de compromisos mensuales sistema financiero: ')[1])
      except NoSuchElementException:
         compromisos ='-'
      try:
         empleador_dir = str(driver.find_element_by_xpath("//*[contains(text(), 'Empleador: ')]").text).split(' ')[1]
      except NoSuchElementException:
         empleador_dir ='-'

      def Seg_Social(tabla):
         if 'Reg Seg Social Empleador' in tabla:
            return ('Cumple')
         else:
            return ('Rechaz')
      
      head_deuda_01 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[1]/thead'):
            ths = tr.find_elements_by_tag_name('th')
            if ths:
               head_deuda_01.append([th.text for th in ths])
      except IndexError:
         pass

      tabla_deuda_01 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[1]/tbody'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
               tabla_deuda_01.append([td.text for td in tds])
      except IndexError:
         pass

      head_deuda_02 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/thead'):
            ths = tr.find_elements_by_tag_name('th')
            if ths:
               head_deuda_02.append([th.text for th in ths])
      except IndexError:
         pass

      tabla_deuda_02 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/tbody'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
               tabla_deuda_02.append([td.text for td in tds])
      except IndexError:
         pass               
            
      tabla_deuda_sit01 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[1]/tbody'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
               tabla_deuda_sit01.append([td.get_attribute("class") for td in tds])
      except IndexError:
         pass  

      tabla_deuda_sit02 = []
      try:
         for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/tbody'):
            tds = tr.find_elements_by_tag_name('td')
            if tds:
               tabla_deuda_sit02.append([td.get_attribute("class") for td in tds])
      except IndexError:
         pass

      head_deuda_01_01 = []
      head_deuda_01_02 = []
      head_deuda_01_03 = []
      try:
         for cell in (head_deuda_01)[0][1:]:
            head_deuda_01_01.append(int(cell))
         year01 = head_deuda_01_01[0]
         year02 = head_deuda_01_01[1]
         head_deuda_01_02 = (head_deuda_01_01)[1:]
         head_deuda_01_03 = []
         for cell in head_deuda_01_02:
               if cell < 10:
                     if cell == 1:
                        year01 = year02
                     head_deuda_01_03.append(str(year01)+'-0'+str(cell))
               else:
                     head_deuda_01_03.append(str(year01)+'-'+str(cell))
      except IndexError:
         pass

      try:
         num_deuda_head01 = np.array(head_deuda_01_03)[-12:]
         deuda_reshaped_head01 = num_deuda_head01.reshape(1,12)

         num_deuda_01 = np.array(tabla_deuda_01)
         deuda_reshaped_01 = num_deuda_01.reshape(int(num_deuda_01.size/13),13)
      except ValueError:
         pass

      head_deuda_02_01 = []
      head_deuda_02_02 = []
      head_deuda_02_03 = []
      try:
         for cell in (head_deuda_02)[0][1:]:
            head_deuda_02_01.append(int(cell))
         year01 = head_deuda_02_01[0]
         year02 = head_deuda_02_01[1]
         head_deuda_02_02 = (head_deuda_02_01)[1:]
         head_deuda_02_03 = []
         for cell in head_deuda_02_02:
               if cell < 10:
                     if cell == 1:
                        year01 = year02
                     head_deuda_02_03.append(str(year01)+'-0'+str(cell))
               else:
                     head_deuda_02_03.append(str(year01)+'-'+str(cell))
      except IndexError:
         pass

      tabla_deuda_final = []
      try:
         num_deuda_head02 = np.array(head_deuda_02_03)[-12:]
         deuda_reshaped_head02 = num_deuda_head02.reshape(1,12)

         num_deuda_02 = np.array(tabla_deuda_02)
         deuda_reshaped_02 = num_deuda_02.reshape(int(num_deuda_02.size/13),13)

         tabla_deuda_final = np.concatenate((deuda_reshaped_01,deuda_reshaped_02[:,1:]),axis=1)
         tabla_final = pd.DataFrame(tabla_deuda_final, columns = ['Banco'] + head_deuda_01_03[-12:]+head_deuda_02_03[-12:])

      except ValueError:
         pass
      
      tabla_file = str(cuit)+'_nosis_deuda.csv'        

      deuda_nosis_ult = 0
      deuda_nosis_ult_tabla = []

      try:
         deuda_nosis_ult_tabla = list(tabla_deuda_final[2:3,1:])[0]
      except TypeError:
         pass
      
      if  deuda_nosis_ult_tabla == []:
         pass
      else:
         for n in deuda_nosis_ult_tabla:
            if n!='':
               deuda_nosis_ult = n
         deuda_nosis_ult = deuda_nosis_ult.replace(",", "")
            
      tabla_head_nosis = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[3]/div[1]/table/thead'):
         ths = tr.find_elements_by_tag_name('th')
         if ths:
            tabla_head_nosis.append([th.text for th in ths])
      tabla_head = tabla_head_nosis[0]

      tabla_resumen_nosis = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[3]/div[1]/table/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_resumen_nosis.append([td.text for td in tds])
      tabla_resumen = tabla_resumen_nosis[0]

      aportes = 0
      try:
         AP = str(tabla_resumen).split("'Empleador',")[1].split("'', '', 'Consultas recibidas'")[0]
         count_p = (AP.count('P'))
         count_i = (AP.count('I'))
         count_pp = (AP.count('PP'))
         count_n = (AP.count("''"))
         count_p + count_i + count_pp + count_n
         aportes = 0
         if count_i+count_pp > 6:
            aportes = 3
         if count_i+count_pp <= 6:
            aportes = 2
            if int(count_i+count_pp) <= 3:
                  aportes = 1
                  if count_i+count_pp == 0:
                     aportes = 0    
         else:
            aportes = 4
      except IndexError:
         aportes = 0   

      year_resumen_01 = tabla_head[1]
      year_resumen_02 = tabla_head[2]
      if int(tabla_head[3])>12:
         year_resumen_03 = tabla_head[3]

      tabla_head_final = []
      for mes in tabla_head[1:]:
         if int(mes) <= 12 and int(mes) >= 10:
            tabla_head_final.append(str(year_resumen_01)+'-'+str(mes))
         if int(mes) == 1:
            year_resumen_01 = year_resumen_02
            year_resumen_02 = year_resumen_03
            tabla_head_final.append(str(year_resumen_01)+'-0'+str(mes))
         if int(mes) < 10 and int(mes) > 1:
            tabla_head_final.append(str(year_resumen_01)+'-0'+str(mes))

      BCRA_list = []      
      try:
         BCRA = str(tabla_resumen).split("'Situación',")[1].split("'Cantidad de tarjetas'")[0]
         BCRA_rep = BCRA.replace("''", "'0'")
         BCRA_rep_final = BCRA_rep.replace("'", "")
         BCRA_list = []
         for n in BCRA_rep_final:
            if n ==str(''):
               BCRA_list.append(0)
            if n == '0' or n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6':
               BCRA_list.append(int(n))
         dict_BCRA = dict(zip(tabla_head_final, BCRA_list))
      except (IndexError, ValueError):
          dict_BCRA ={}

      rechazados_list = []
      try:
         cheques_rechazados = str(tabla_resumen).split("'Rechazados',")[1].split(", 'Recuperados'")[0]
         rechazados_rep = cheques_rechazados.replace("'-'", "'0'")
         rechazados_rep_02 = rechazados_rep.replace(" ", "")
         rechazados_rep_final = rechazados_rep_02.replace("'", "")
         rechazados_replace_list = rechazados_rep_final.split(",")
         for n in rechazados_replace_list:
            rechazados_list.append(int(n))
         dict_rechazados = dict(zip(tabla_head_final, rechazados_list))
      except (IndexError, ValueError):
         pass
      try:
         cheques_rechazados = str(tabla_resumen).split("'Rechazados',")[1].split(", 'No Recuperados'")[0]
         rechazados_rep = cheques_rechazados.replace("'-'", "'0'")
         rechazados_rep_02 = rechazados_rep.replace(" ", "")
         rechazados_rep_final = rechazados_rep_02.replace("'", "")
         rechazados_replace_list = rechazados_rep_final.split(",")
         for n in rechazados_replace_list:
            rechazados_list.append(int(n))
         dict_rechazados = dict(zip(tabla_head_final, rechazados_list))
      except (IndexError, ValueError):
         pass

      recuperados_list = []
      try:
         cheques_recuperados = str(tabla_resumen).split("'Recuperados',")[1].split(", 'No recuperados'")[0]
         recuperados_rep = cheques_recuperados.replace("'-'", "'0'")
         recuperados_rep_02 = recuperados_rep.replace(" ", "")
         recuperados_rep_final = recuperados_rep_02.replace("'", "")
         recuperados_replace_list = recuperados_rep_final.split(",")
         for n in recuperados_replace_list:
            recuperados_list.append(int(n))
         dict_recuperados = dict(zip(tabla_head_final, recuperados_list))
      except IndexError:
         pass

      no_recuperados_list = []
      try:
         cheques_no_recuperados = str(tabla_resumen).split("'No recuperados',")[1].split(", '', '', ")[0]
         no_recuperados_rep = cheques_no_recuperados.replace("'-'", "'0'")
         no_recuperados_rep_02 = no_recuperados_rep.replace(" ", "")
         no_recuperados_rep_final = no_recuperados_rep_02.replace("'", "")
         no_recuperados_replace_list = no_recuperados_rep_final.split(",")
         for n in no_recuperados_replace_list:
            no_recuperados_list.append(int(n))
         dict_no_recuperados = dict(zip(tabla_head_final, no_recuperados_list))
      except (IndexError, ValueError):
         pass
      try:
         cheques_no_recuperados = str(tabla_resumen).split("'No recuperados',")[1].split(", 'No pago multa'")[0]
         no_recuperados_rep = cheques_no_recuperados.replace("'-'", "'0'")
         no_recuperados_rep_02 = no_recuperados_rep.replace(" ", "")
         no_recuperados_rep_final = no_recuperados_rep_02.replace("'", "")
         no_recuperados_replace_list = no_recuperados_rep_final.split(",")
         no_recuperados_list = []
         for n in no_recuperados_replace_list:
            no_recuperados_list.append(int(n))
         dict_no_recuperados = dict(zip(tabla_head_final, no_recuperados_list))
      except (IndexError, ValueError):
         pass

      driver.close()

      BCRA_sit = 0
      check_sit2 = 0
      for n in BCRA_list:
         if n == 2:
            BCRA_sit = 1
            check_sit2 +=1
            if n == 1:
                  BCRA_sit = 1 
                  check_sit2 = 0
                  
      if check_sit2 > 2 and BCRA_sit == 1:
         BCRA_sit = 2

      BCRA_list_12 = BCRA_list[12:]
      for n in BCRA_list_12:
         if n > 2:
            BCRA_sit = 3

      BCRA_ult = 0
      for n in BCRA_list:
         if n!=0:
            BCRA_ult = n
            
      cheques_cant = 0
      if sum (no_recuperados_list) >= 5:
         cheques_cant = 3 
      if sum (no_recuperados_list) <= 2 and sum(rechazados_list) > 1:
         cheques_cant = 2 
      if sum (rechazados_list) == 1:
         cheques_cant = 1

      if juicios == 'Cumple' or oficios == 'Cumple':
         legal_output = 0
      else:
         legal_output = 1
         
      if antecedentes_fiscales == 'Cumple':
         antecedentes_fiscales_output = 0
      else:
         antecedentes_fiscales_output = 1

      if concurso == 'Cumple':
         concurso_output = 0
      else:
         concurso_output = 1

      if Seg_Social(tabla_AFIP) == 'Cumple':
         empleador_output = 1
      else:
         empleador_output = 0

      if ganancias == 'Activo':
         ganancias_output = 1
      else:
         ganancias_output = 0

      if iva == 'Activo':
         iva_output = 1
      else:
         iva_output = 0

      if cheques == 'Cumple':
         cheques_output = 0
      else:
         cheques_output = 1
         
      if referencias == 'Cumple':
         referencias_output = 0
      else:
         referencias_output = 1
         
      nacimiento_output =  str(nacimiento.partition(' ')[0])
      codigo_output =  str(codigo_afip.partition(' - ')[0])
      actividad_output = str(codigo_afip.partition(' - ')[2])
      domicilio_output = str(domicilio.split("\n")[0])
      AFIP_output = str(inscripcion_afip.partition(' [')[0])

      elapsed_time = time.time() - start_time
      print ('OK. Tiempo:', str(datetime.timedelta(seconds = elapsed_time)).partition('.')[0])

      head_deuda_01_01 = []
      head_deuda_01_02 = []
      head_deuda_01_03 = []
      try:
         for cell in (head_deuda_01)[0][1:]:
            head_deuda_01_01.append(int(cell))
         year01 = head_deuda_01_01[0]
         if head_deuda_01_01[1]>12:
            year02 = head_deuda_01_01[1]
         else:
            year02 = year01
         head_deuda_01_02 = (head_deuda_01_01)[1:]
         head_deuda_01_03 = []
         for cell in head_deuda_01_02:
               if cell < 10:
                     if cell == 1:
                        year01 = year02
                     head_deuda_01_03.append(str(year01)+'-0'+str(cell))
               else:
                     head_deuda_01_03.append(str(year01)+'-'+str(cell))
      except IndexError:
         pass

      try:
         num_deuda_head01 = np.array(head_deuda_01_03)[-12:]
         deuda_reshaped_head01 = num_deuda_head01.reshape(1,12)

         num_deuda_01 = np.array(tabla_deuda_01)
         deuda_reshaped_01 = num_deuda_01.reshape(int(num_deuda_01.size/13),13)

         num_deuda_sit01 = np.array(tabla_deuda_sit01)
         deuda_reshaped_sit01 = num_deuda_sit01.reshape(int(num_deuda_sit01.size/13),13)
      except ValueError:
         pass

      head_deuda_02_01 = []
      head_deuda_02_02 = []
      head_deuda_02_03 = []
      try:
         for cell in (head_deuda_02)[0][1:]:
            head_deuda_02_01.append(int(cell))
         year01 = head_deuda_02_01[0]
         if head_deuda_02_01[1]>12:
            year02 = head_deuda_02_01[1]
         else:
            year02 = year01
         head_deuda_02_02 = (head_deuda_02_01)[1:]
         head_deuda_02_03 = []
         for cell in head_deuda_02_02:
               if cell < 10:
                     if cell == 1:
                        year01 = year02
                     head_deuda_02_03.append(str(year01)+'-0'+str(cell))
               else:
                     head_deuda_02_03.append(str(year01)+'-'+str(cell))
      except IndexError:
         pass

      tabla_deuda_final = []
      tabla_deuda_sit_final = []
      try:
         num_deuda_head02 = np.array(head_deuda_02_03)[-12:]
         deuda_reshaped_head02 = num_deuda_head02.reshape(1,12)

         num_deuda_02 = np.array(tabla_deuda_02)
         deuda_reshaped_02 = num_deuda_02.reshape(int(num_deuda_02.size/13),13)

         num_deuda_sit02 = np.array(tabla_deuda_sit02)
         deuda_reshaped_sit02 = num_deuda_sit02.reshape(int(num_deuda_sit02.size/13),13)

         tabla_deuda_final = np.concatenate((deuda_reshaped_01,deuda_reshaped_02[:,1:]),axis=1)
         tabla_final = pd.DataFrame(tabla_deuda_final, columns = ['Banco'] + head_deuda_01_03[-12:]+head_deuda_02_03[-12:])
  
         tabla_deuda_sit_final = np.concatenate((deuda_reshaped_sit01,deuda_reshaped_sit02[:,1:]),axis=1)
      except ValueError:
         pass

      tabla_file = str(cuit)+'_nosis_deuda.csv'
      
      nosis_personales = []
      try:
         nosis_personales = np.concatenate((head_deuda_01_03[-12:],head_deuda_02_03[-12:], tabla_deuda_final[2][1:]))
      except IndexError:
         pass

      for n in range (1,25):
         try:
            globals()['nosisper%s' % n] = nosis_personales[n+23].replace(",", "")
         except IndexError:
            pass
         
      for n in range(1,10):
         try:
            globals()['banco%s' % n] = tabla_deuda_final[n+2][0]
         except IndexError:
            globals()['banco%s' % n] = ''

      for n in range(1,10):
         globals()['deudabanco%s' % n ]=[]
         try:
            globals()['deudabanco%s' % n ].append(tabla_deuda_final[n+2][19:])
         except IndexError:
            globals()['deudabanco%s' % n ].append('')

      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco1_%s' % n ] = deudabanco1[0][n]
            except IndexError:
                  globals()['deudabanco1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco2_%s' % n ] = deudabanco2[0][n]
            except IndexError:
                  globals()['deudabanco2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco3_%s' % n ] = deudabanco3[0][n]
            except IndexError:
                  globals()['deudabanco3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco4_%s' % n ] = deudabanco4[0][n]
            except IndexError:
                  globals()['deudabanco4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco5_%s' % n ] = deudabanco5[0][n]
            except IndexError:
                  globals()['deudabanco5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco6_%s' % n ] = deudabanco6[0][n]
            except IndexError:
                  globals()['deudabanco6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco7_%s' % n ] = deudabanco7[0][n]
            except IndexError:
                  globals()['deudabanco7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco8_%s' % n ] = deudabanco8[0][n]
            except IndexError:
                  globals()['deudabanco8_%s' % n ] = ''
      except IndexError:
         pass
      
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco9_%s' % n ] = deudabanco9[0][n]
            except IndexError:
                  globals()['deudabanco9_%s' % n ] = ''
      except IndexError:
         pass
         
      for n in range(1,10):
         globals()['deudabancosit%s' % n ]=[]
         try:
            globals()['deudabancosit%s' % n ].append(tabla_deuda_sit_final[n+2][19:])
         except IndexError:
            globals()['deudabancosit%s' % n ].append('')

      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit1_%s' % n ] = deudabancosit1[0][n]
            except IndexError:
                  globals()['deudabancosit1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit2_%s' % n ] = deudabancosit2[0][n]
            except IndexError:
                  globals()['deudabancosit2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit3_%s' % n ] = deudabancosit3[0][n]
            except IndexError:
                  globals()['deudabancosit3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit4_%s' % n ] = deudabancosit4[0][n]
            except IndexError:
                  globals()['deudabancosit4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit5_%s' % n ] = deudabancosit5[0][n]
            except IndexError:
                  globals()['deudabancosit5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit6_%s' % n ] = deudabancosit6[0][n]
            except IndexError:
                  globals()['deudabancosit6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit7_%s' % n ] = deudabancosit7[0][n]
            except IndexError:
                  globals()['deudabancosit7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit8_%s' % n ] = deudabancosit8[0][n]
            except IndexError:
                  globals()['deudabancosit8_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit9_%s' % n ] = deudabancosit9[0][n]
            except IndexError:
                  globals()['deudabancosit9_%s' % n ] = ''
      except IndexError:
         pass

      nosis_output = [ nacimiento_output, codigo_output, score_nosis, deuda_nosis_ult, nosis_name, actividad_output,
                     domicilio_output, antecedentes_fiscales_output, concurso_output, aportes, BCRA_sit,
                     cheques_cant, BCRA_ult, AFIP_output, empleador_output, ganancias_output, iva_output,
                     cheques_output, legal_output, referencias_output, empleador_dir, compromisos, NSE ]
      
      nosis_per = [ nosisper1, nosisper2, nosisper3, nosisper4, nosisper5, nosisper6, nosisper7, nosisper8, nosisper9, nosisper10, nosisper11, nosisper12,
                  nosisper13, nosisper14, nosisper15, nosisper16, nosisper17, nosisper18, nosisper19, nosisper20, nosisper21, nosisper22, nosisper23, nosisper24 ]
      
      deuda_bancos = [ banco1, banco2, banco3, banco4, banco5, banco6, banco7, banco8, banco9,
                     deudabanco1_0, deudabanco1_1, deudabanco1_2, deudabanco1_3, deudabanco1_4, deudabanco1_5, deudabanco2_0, deudabanco2_1, deudabanco2_2, deudabanco2_3, 
                     deudabanco2_4, deudabanco2_5, deudabanco3_0, deudabanco3_1, deudabanco3_2, deudabanco3_3, deudabanco3_4, deudabanco3_5, deudabanco4_0, deudabanco4_1, 
                     deudabanco4_2, deudabanco4_3, deudabanco4_4, deudabanco4_5, deudabanco5_0, deudabanco5_1, deudabanco5_2, deudabanco5_3, deudabanco5_4, deudabanco5_5,
                     deudabanco6_0, deudabanco6_1, deudabanco6_2, deudabanco6_3, deudabanco6_4, deudabanco6_5, deudabanco7_0, deudabanco7_1, deudabanco7_2, deudabanco7_3,
                     deudabanco7_4, deudabanco7_5, deudabanco8_0, deudabanco8_1, deudabanco8_2, deudabanco8_3, deudabanco8_4, deudabanco8_5, deudabanco9_0, deudabanco9_1,
                     deudabanco9_2, deudabanco9_3, deudabanco9_4, deudabanco9_5, deudabancosit1_0, deudabancosit1_1, deudabancosit1_2, deudabancosit1_3, deudabancosit1_4, 
                     deudabancosit1_5, deudabancosit2_0, deudabancosit2_1, deudabancosit2_2, deudabancosit2_3, deudabancosit2_4, deudabancosit2_5, deudabancosit3_0, deudabancosit3_1, 
                     deudabancosit3_2, deudabancosit3_3, deudabancosit3_4, deudabancosit3_5, deudabancosit4_0, deudabancosit4_1, deudabancosit4_2, deudabancosit4_3, deudabancosit4_4, 
                     deudabancosit4_5, deudabancosit5_0, deudabancosit5_1, deudabancosit5_2, deudabancosit5_3, deudabancosit5_4, deudabancosit5_5, deudabancosit6_0, deudabancosit6_1, 
                     deudabancosit6_2, deudabancosit6_3, deudabancosit6_4, deudabancosit6_5, deudabancosit7_0, deudabancosit7_1, deudabancosit7_2, deudabancosit7_3, deudabancosit7_4,
                     deudabancosit7_5, deudabancosit8_0, deudabancosit8_1, deudabancosit8_2, deudabancosit8_3, deudabancosit8_4, deudabancosit8_5, deudabancosit9_0, deudabancosit9_1,
                     deudabancosit9_2, deudabancosit9_3, deudabancosit9_4, deudabancosit9_5 ]

      dict_nosis =  {'Nombre:': nosis_name, 'CUIT:': cuit_long, 'Score Nosis:': score_nosis, 'Nacimiento:': nacimiento_output, 'Registro AFIP:': AFIP_output,
                     'Código AFIP:': codigo_output, 'Actividad:': actividad_output, 'Domicilio:': domicilio_output, 'Compromisos Mensuales:': compromisos, 'NSE:': NSE,
                     'Empleador:': empleador_dir, 'Deuda (miles):': deuda_nosis_ult, 'Ganancias?:': ganancias_output, 'IVA?:': iva_output, 'Es empleador?:': empleador_output, 
                     'Ultima Situación BCRA:': BCRA_ult, 'Situación BCRA:': BCRA_sit, 'Antecedentes Fiscales:': antecedentes_fiscales_output, 'Concursos:': concurso_output, 
                     'Aportes:': aportes, 'Cheques cantidad:': cheques_cant, 'Cheques situación:': cheques_output, 'Legales:': legal_output, 'Referencias:': referencias_output}
      
      session['nosis_soc'] = nosis_sociedad
      session['nosistabla'] = nosis_output
      session['deuda_bancos'] = deuda_bancos
      session['deuda_nosis'] = nosis_per
      try:
         nosis_personales_lista = nosis_personales.tolist()
      except AttributeError:
         nosis_personales_lista = nosis_personales
      session['nosis_personales'] = nosis_personales_lista
      return render_template("nosisresult.html", nosisresult = dict_nosis)

   else:
      options = Options()
      options.headless = True
      #driver = webdriver.Chrome('./Chrome/chromedriver', chrome_options=options)
      driver = webdriver.Chrome(executable_path='./Chrome/chromedriver', chrome_options=options)
      # keys
      usuario = '457993'
      contra = '079778'
      # cliente:
      cuit_long = str(cuit)[0:2]+'-'+str(cuit)[2:10]+'-'+str(cuit)[10:11]
      start_time = time.time()
      # registro en Nosis
      driver.get('http://sac31.nosis.com/net/manager')
      driver.find_element_by_id('Email').send_keys(usuario)
      driver.find_element_by_id('Clave').send_keys(contra)
      try:
         driver.find_element_by_xpath('//*[@id="frmInicioSesion"]/div/div/div[2]/div[2]/button').click()
      except NoSuchElementException:
         driver.find_element_by_id('iniciarSesion').click()
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(cuit)
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(Keys.ENTER)
      time.sleep(15)
      driver.find_element_by_id('btnConsultar').click()
      try:
         time.sleep(15)
      except NoSuchElementException:
         time.sleep(120)
      try:
         driver.find_element_by_id('link-continuar').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[2]').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').click()
      except NoSuchElementException:
         pass
      score_nosis = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]').text
      codigo_afip = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[2]/ul[2]/li[3]/span/b').text
      contrato_social = driver.find_element_by_xpath("//*[contains(text(), 'Contrato social:')]").text
      nosis_name = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[2]/div[2]/div').text
      domicilio = driver.find_element_by_xpath("//*[contains(text(), 'Domicilio fiscal')]/following-sibling::ul").text
      inscripcion_afip = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[4]/div[1]/div/div[1]/div[4]').text
      ganancias = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[4]/div[1]/div/div[2]/div[2]').text
      iva = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[4]/div[1]/div/div[2]/div[3]/span').text
      facturacion = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[2]/ul[1]/li[1]/span/b').text
      empleados = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[2]/ul[1]/li[2]/span/b').text
      tabla_cda = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div/div/table[2]/tbody').text
      concurso = str(tabla_cda.partition('Concurso o Quiebra: ')[2][0:6])
      antecedentes_fiscales = str(tabla_cda.partition('Antecedentes Fiscales: ')[2][0:6])
      juicios = str(tabla_cda.partition('Juicios - Demandado: ')[2][0:6])
      oficios = str(tabla_cda.partition('Oficios Judiciales: ')[2][0:6])
      referencias = str(tabla_cda.partition('Referencias Comerciales: ')[2][0:6])
      cheques = str(tabla_cda.partition('Cheques Rechazados del BCRA: ')[2][0:6])
      tabla_AFIP = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[4]/table/tbody').text
      def Seg_Social(tabla):
         if 'Reg Seg Social Empleador' in tabla:
            return ('Cumple')
         else:
            return ('Rechaz')

      head_deuda_01 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[1]/thead'):
         ths = tr.find_elements_by_tag_name('th')
         if ths:
            head_deuda_01.append([th.text for th in ths])

      tabla_deuda_01 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[1]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_deuda_01.append([td.text for td in tds])

      head_deuda_02 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[2]/thead'):
         ths = tr.find_elements_by_tag_name('th')
         if ths:
            head_deuda_02.append([th.text for th in ths])

      tabla_deuda_02 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[2]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_deuda_02.append([td.text for td in tds])
            
      tabla_deuda_sit01 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[1]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_deuda_sit01.append([td.get_attribute("class") for td in tds])

      tabla_deuda_sit02 = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[6]/div[2]/table[2]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_deuda_sit02.append([td.get_attribute("class") for td in tds])

      head_deuda_01_01 = []
      for cell in (head_deuda_01)[0][1:]:
         head_deuda_01_01.append(int(cell))
      year01 = head_deuda_01_01[0]
      year02 = head_deuda_01_01[1]
      head_deuda_01_02 = (head_deuda_01_01)[1:]
      head_deuda_01_03 = []
      for cell in head_deuda_01_02:
            if cell < 10:
                  if cell == 1:
                     year01 = year02
                  head_deuda_01_03.append(str(year01)+'-0'+str(cell))
            else:
                  head_deuda_01_03.append(str(year01)+'-'+str(cell))

      num_deuda_head01 = np.array(head_deuda_01_03)[-12:]
      deuda_reshaped_head01 = num_deuda_head01.reshape(1,12)

      num_deuda_01 = np.array(tabla_deuda_01)
      deuda_reshaped_01 = num_deuda_01.reshape(int(num_deuda_01.size/13),13)

      head_deuda_02_01 = []
      for cell in (head_deuda_02)[0][1:]:
         head_deuda_02_01.append(int(cell))
      year01 = head_deuda_02_01[0]
      year02 = head_deuda_02_01[1]
      head_deuda_02_02 = (head_deuda_02_01)[1:]
      head_deuda_02_03 = []
      for cell in head_deuda_02_02:
            if cell < 10:
                  if cell == 1:
                     year01 = year02
                  head_deuda_02_03.append(str(year01)+'-0'+str(cell))
            else:
                  head_deuda_02_03.append(str(year01)+'-'+str(cell))

      num_deuda_head02 = np.array(head_deuda_02_03)[-12:]
      deuda_reshaped_head02 = num_deuda_head02.reshape(1,12)

      num_deuda_02 = np.array(tabla_deuda_02)
      deuda_reshaped_02 = num_deuda_02.reshape(int(num_deuda_02.size/13),13)

      tabla_deuda_final = np.concatenate((deuda_reshaped_01,deuda_reshaped_02[:,1:]),axis=1)
      tabla_final = pd.DataFrame(tabla_deuda_final, columns = ['Banco'] + head_deuda_01_03[-12:]+head_deuda_02_03[-12:])

      tabla_file = str(cuit)+'_nosis_deuda.csv'        

      deuda_nosis_ult = 0
      deuda_nosis_ult_tabla = list(tabla_deuda_final[2:3,1:])[0]
      for n in deuda_nosis_ult_tabla:
         if n!='':
            deuda_nosis_ult = n
            
      tabla_head_nosis = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[4]/div[1]/table/thead'):
         ths = tr.find_elements_by_tag_name('th')
         if ths:
            tabla_head_nosis.append([th.text for th in ths])
      tabla_head = tabla_head_nosis[0]

      tabla_resumen_nosis = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[4]/div[1]/table/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
            tabla_resumen_nosis.append([td.text for td in tds])
      tabla_resumen = tabla_resumen_nosis[0]

      aportes = 0
      try:
         AP = str(tabla_resumen).split("'Empleador',")[1].split("'', '', 'Consultas recibidas'")[0]
         count_p = (AP.count('P'))
         count_i = (AP.count('I'))
         count_pp = (AP.count('PP'))
         count_n = (AP.count("''"))
         count_p + count_i + count_pp + count_n
         aportes = 0
         if count_i+count_pp > 6:
            aportes = 3
         if count_i+count_pp <= 6:
            aportes = 2
            if int(count_i+count_pp) <= 3:
                  aportes = 1
                  if count_i+count_pp == 0:
                     aportes = 0    
         else:
            aportes = 4
      except IndexError:
         aportes = 0   

      year_resumen_01 = tabla_head[1]
      year_resumen_02 = tabla_head[2]
      if int(tabla_head[3])>12:
         year_resumen_03 = tabla_head[3]

      tabla_head_final = []
      for mes in tabla_head[1:]:
         if int(mes) <= 12 and int(mes) >= 10:
            tabla_head_final.append(str(year_resumen_01)+'-'+str(mes))
         if int(mes) == 1:
            year_resumen_01 = year_resumen_02
            year_resumen_02 = year_resumen_03
            tabla_head_final.append(str(year_resumen_01)+'-0'+str(mes))
         if int(mes) < 10 and int(mes) > 1:
            tabla_head_final.append(str(year_resumen_01)+'-0'+str(mes))
            
      BCRA_list = []
      try:
         BCRA = str(tabla_resumen).split("'Situación',")[1].split("'Cantidad de tarjetas'")[0]
         BCRA_rep = BCRA.replace("''", "'0'")
         BCRA_rep_final = BCRA_rep.replace("'", "")
         BCRA_list = []
         for n in BCRA_rep_final:
            if n ==str(''):
               BCRA_list.append(0)
            if n == '0' or n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6':
               BCRA_list.append(int(n))
         dict_BCRA = dict(zip(tabla_head_final, BCRA_list))
      except (IndexError, ValueError):
          dict_BCRA ={}

      rechazados_list = []
      try:
         cheques_rechazados = str(tabla_resumen).split("'Rechazados',")[1].split(", 'Recuperados'")[0]
         rechazados_rep = cheques_rechazados.replace("'-'", "'0'")
         rechazados_rep_02 = rechazados_rep.replace(" ", "")
         rechazados_rep_final = rechazados_rep_02.replace("'", "")
         rechazados_replace_list = rechazados_rep_final.split(",")
         for n in rechazados_replace_list:
            rechazados_list.append(int(n))
         dict_rechazados = dict(zip(tabla_head_final, rechazados_list))
      except (IndexError, ValueError):
         pass
      try:
         cheques_rechazados = str(tabla_resumen).split("'Rechazados',")[1].split(", 'No Recuperados'")[0]
         rechazados_rep = cheques_rechazados.replace("'-'", "'0'")
         rechazados_rep_02 = rechazados_rep.replace(" ", "")
         rechazados_rep_final = rechazados_rep_02.replace("'", "")
         rechazados_replace_list = rechazados_rep_final.split(",")
         for n in rechazados_replace_list:
            rechazados_list.append(int(n))
         dict_rechazados = dict(zip(tabla_head_final, rechazados_list))
      except (IndexError, ValueError):
         pass

      recuperados_list = []
      try:
         cheques_recuperados = str(tabla_resumen).split("'Recuperados',")[1].split(", 'No recuperados'")[0]
         recuperados_rep = cheques_recuperados.replace("'-'", "'0'")
         recuperados_rep_02 = recuperados_rep.replace(" ", "")
         recuperados_rep_final = recuperados_rep_02.replace("'", "")
         recuperados_replace_list = recuperados_rep_final.split(",")
         for n in recuperados_replace_list:
            recuperados_list.append(int(n))
         dict_recuperados = dict(zip(tabla_head_final, recuperados_list))
      except IndexError:
         pass

      no_recuperados_list = []
      try:
         cheques_no_recuperados = str(tabla_resumen).split("'No recuperados',")[1].split(", '', '', ")[0]
         no_recuperados_rep = cheques_no_recuperados.replace("'-'", "'0'")
         no_recuperados_rep_02 = no_recuperados_rep.replace(" ", "")
         no_recuperados_rep_final = no_recuperados_rep_02.replace("'", "")
         no_recuperados_replace_list = no_recuperados_rep_final.split(",")
         for n in no_recuperados_replace_list:
            no_recuperados_list.append(int(n))
         dict_no_recuperados = dict(zip(tabla_head_final, no_recuperados_list))
      except (IndexError, ValueError):
         pass
      try:
         cheques_no_recuperados = str(tabla_resumen).split("'No recuperados',")[1].split(", 'No pago multa'")[0]
         no_recuperados_rep = cheques_no_recuperados.replace("'-'", "'0'")
         no_recuperados_rep_02 = no_recuperados_rep.replace(" ", "")
         no_recuperados_rep_final = no_recuperados_rep_02.replace("'", "")
         no_recuperados_replace_list = no_recuperados_rep_final.split(",")
         no_recuperados_list = []
         for n in no_recuperados_replace_list:
            no_recuperados_list.append(int(n))
         dict_no_recuperados = dict(zip(tabla_head_final, no_recuperados_list))
      except (IndexError, ValueError):
         pass

      tabla_aportes = []
      aportes_path = ['8','9','10']
      try:
         for n in aportes_path:
            for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div['+ n +']/div[1]/div[1]/table/tbody'):
               tds = tr.find_elements_by_tag_name('td')
               if tds:
                     tabla_aportes.append([td.text for td in tds])
               try:
                  fecha_aportes_01 = tabla_aportes[0][0]
                  seguridad_aportes_01 = tabla_aportes[0][1]
                  obra_aportes_01 = tabla_aportes[0][2]
                  patronal_aportes_01 = tabla_aportes[0][3]
                  fecha_aportes_02 = tabla_aportes[0][4]
                  seguridad_aportes_02 = tabla_aportes[0][5]
                  obra_aportes_02 = tabla_aportes[0][6]
                  patronal_aportes_02 = tabla_aportes[0][7]
                  fecha_aportes_03 = tabla_aportes[0][8]
                  seguridad_aportes_03 = tabla_aportes[0][9]
                  obra_aportes_03 = tabla_aportes[0][10]
                  patronal_aportes_03 = tabla_aportes[0][11]
                  fecha_aportes_04 = tabla_aportes[0][12]
                  seguridad_aportes_04 = tabla_aportes[0][13]
                  obra_aportes_04 = tabla_aportes[0][14]
                  patronal_aportes_04 = tabla_aportes[0][15]
                  fecha_aportes_05 = tabla_aportes[0][16]
                  seguridad_aportes_05 = tabla_aportes[0][17]
                  obra_aportes_05 = tabla_aportes[0][18]
                  patronal_aportes_05 = tabla_aportes[0][19]
                  fecha_aportes_06 = tabla_aportes[0][20]
                  seguridad_aportes_06 = tabla_aportes[0][21]
                  obra_aportes_06 = tabla_aportes[0][22]
                  patronal_aportes_06 = tabla_aportes[0][23]
                  fecha_aportes_07 = tabla_aportes[0][24]
                  seguridad_aportes_07 = tabla_aportes[0][25]
                  obra_aportes_07 = tabla_aportes[0][26]
                  patronal_aportes_07 = tabla_aportes[0][27]
                  fecha_aportes_08 = tabla_aportes[0][28]
                  seguridad_aportes_08 = tabla_aportes[0][29]
                  obra_aportes_08 = tabla_aportes[0][30]
                  patronal_aportes_08 = tabla_aportes[0][31]
                  fecha_aportes_09 = tabla_aportes[0][32]
                  seguridad_aportes_09 = tabla_aportes[0][33]
                  obra_aportes_09 = tabla_aportes[0][34]
                  patronal_aportes_09 = tabla_aportes[0][35]
                  fecha_aportes_10 = tabla_aportes[0][36]
                  seguridad_aportes_10 = tabla_aportes[0][37]
                  obra_aportes_10 = tabla_aportes[0][38]
                  patronal_aportes_10 = tabla_aportes[0][39]
                  fecha_aportes_11 = tabla_aportes[0][40]
                  seguridad_aportes_11 = tabla_aportes[0][41]
                  obra_aportes_11 = tabla_aportes[0][42]
                  patronal_aportes_11 = tabla_aportes[0][43]
                  fecha_aportes_12 = tabla_aportes[0][44]
                  seguridad_aportes_12 = tabla_aportes[0][45]
                  obra_aportes_12 = tabla_aportes[0][46]
                  patronal_aportes_12 = tabla_aportes[0][47]
               except NoSuchElementException:
                  pass         
      except IndexError:
         pass


      #puede ser div[10] también
      tabla_semestres = []
      semestres_path = ['10','11','12']
      try:
         for n in semestres_path:
            for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div['+ n +']/div/div[1]/table/thead'):
               ths = tr.find_elements_by_tag_name('th')
               if ths:
                     tabla_semestres.append([th.text for th in ths])
               try:
                  semestre_01 = tabla_semestres[0][10]
                  semestre_02 = tabla_semestres[0][11]
                  semestre_03 = tabla_semestres[0][12]
                  semestre_04 = tabla_semestres[0][13]
                  semestre_05 = tabla_semestres[0][14]
                  semestre_06 = tabla_semestres[0][15]
               except NoSuchElementException:
                  pass
      except IndexError:
         pass

      tabla_consultas = []
      try:
         for n in semestres_path:
            for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div['+ n +']/div/div[1]/table/tfoot'):
               ths = tr.find_elements_by_tag_name('th')
               if ths:
                     tabla_consultas.append([th.text for th in ths])
               try:  
                  consulta_01 = tabla_consultas[0][7]
                  consulta_02 = tabla_consultas[0][8]
                  consulta_03 = tabla_consultas[0][9]
                  consulta_04 = tabla_consultas[0][10]
                  consulta_05 = tabla_consultas[0][11]
                  consulta_06 = tabla_consultas[0][12]
               except NoSuchElementException:
                  pass
      except IndexError:
         pass

      driver.close()

      BCRA_sit = 0
      check_sit2 = 0
      for n in BCRA_list:
         if n == 2:
            BCRA_sit = 1
            check_sit2 +=1
            if n == 1:
                  BCRA_sit = 1 
                  check_sit2 = 0
                  
      if check_sit2 > 2 and BCRA_sit == 1:
         BCRA_sit = 2

      BCRA_list_12 = BCRA_list[12:]
      for n in BCRA_list_12:
         if n > 2:
            BCRA_sit = 3

      BCRA_ult = 0
      for n in BCRA_list:
         if n!=0:
            BCRA_ult = n
            
      cheques_cant = 0
      if sum (no_recuperados_list) >= 5:
         cheques_cant = 3 
      if sum (no_recuperados_list) <= 2 and sum(rechazados_list) > 1:
         cheques_cant = 2 
      if sum (rechazados_list) == 1:
         cheques_cant = 1

      if juicios == 'Cumple' or oficios == 'Cumple':
         legal_output = 0
      else:
         legal_output = 1
         
      if antecedentes_fiscales == 'Cumple':
         antecedentes_fiscales_output = 0
      else:
         antecedentes_fiscales_output = 1

      if concurso == 'Cumple':
         concurso_output = 0
      else:
         concurso_output = 1

      if Seg_Social(tabla_AFIP) == 'Cumple':
         empleador_output = 1
      else:
         empleador_output = 0

      if ganancias == 'Activo':
         ganancias_output = 1
      else:
         ganancias_output = 0

      if iva == 'Activo':
         iva_output = 1
      else:
         iva_output = 0

      if cheques == 'Cumple':
         cheques_output = 0
      else:
         cheques_output = 1
         
      if referencias == 'Cumple':
         referencias_output = 0
      else:
         referencias_output = 1
         
      contrato_output =  str(contrato_social.partition(': ')[2])
      codigo_output =  str(codigo_afip.partition(' - ')[0])
      actividad_output = str(codigo_afip.partition(' - ')[2])
      domicilio_output = str(domicilio.split("\n")[0])
      AFIP_output = str(inscripcion_afip.partition(' [')[0])

      head_deuda_02_01 = []

      head_deuda_01_01 = []
      for cell in (head_deuda_01)[0][1:]:
         head_deuda_01_01.append(int(cell))
      year01 = head_deuda_01_01[0]
      if head_deuda_01_01[1]>12:
         year02 = head_deuda_01_01[1]
      else:
         year02 = year01
      head_deuda_01_02 = (head_deuda_01_01)[1:]
      head_deuda_01_03 = []
      for cell in head_deuda_01_02:
            if cell < 10:
                  if cell == 1:
                     year01 = year02
                  head_deuda_01_03.append(str(year01)+'-0'+str(cell))
            else:
                  head_deuda_01_03.append(str(year01)+'-'+str(cell))

      num_deuda_head01 = np.array(head_deuda_01_03)[-12:]
      deuda_reshaped_head01 = num_deuda_head01.reshape(1,12)

      num_deuda_01 = np.array(tabla_deuda_01)
      deuda_reshaped_01 = num_deuda_01.reshape(int(num_deuda_01.size/13),13)

      num_deuda_sit01 = np.array(tabla_deuda_sit01)
      deuda_reshaped_sit01 = num_deuda_sit01.reshape(int(num_deuda_sit01.size/13),13)


      head_deuda_02_01 = []
      for cell in (head_deuda_02)[0][1:]:
         head_deuda_02_01.append(int(cell))
      year01 = head_deuda_02_01[0]
      if head_deuda_02_01[1]>12:
         year02 = head_deuda_02_01[1]
      else:
         year02 = year01
      head_deuda_02_02 = (head_deuda_02_01)[1:]
      head_deuda_02_03 = []
      for cell in head_deuda_02_02:
            if cell < 10:
                  if cell == 1:
                     year01 = year02
                  head_deuda_02_03.append(str(year01)+'-0'+str(cell))
            else:
                  head_deuda_02_03.append(str(year01)+'-'+str(cell))

      num_deuda_head02 = np.array(head_deuda_02_03)[-12:]
      deuda_reshaped_head02 = num_deuda_head02.reshape(1,12)

      num_deuda_02 = np.array(tabla_deuda_02)
      deuda_reshaped_02 = num_deuda_02.reshape(int(num_deuda_02.size/13),13)

      num_deuda_sit02 = np.array(tabla_deuda_sit02)
      deuda_reshaped_sit02 = num_deuda_sit02.reshape(int(num_deuda_sit02.size/13),13)

      tabla_deuda_final = np.concatenate((deuda_reshaped_01,deuda_reshaped_02[:,1:]),axis=1)
      tabla_final = pd.DataFrame(tabla_deuda_final, columns = ['Banco'] + head_deuda_01_03[-12:]+head_deuda_02_03[-12:])

      tabla_deuda_sit_final = np.concatenate((deuda_reshaped_sit01,deuda_reshaped_sit02[:,1:]),axis=1)

      tabla_file = str(cuit)+'_nosis_deuda.csv'

      nosis_tabla = np.concatenate((head_deuda_01_03[-12:],head_deuda_02_03[-12:], tabla_deuda_final[2][1:]))

      for n in range (1,25):
         globals()['nosisdeuda%s' % n] = nosis_tabla[n+23].replace(",", "")
         
      for n in range(1,10):
         try:
            globals()['banco%s' % n] = tabla_deuda_final[n+2][0]
         except IndexError:
            globals()['banco%s' % n] = ''

      for n in range(1,10):
         globals()['deudabanco%s' % n ]=[]
         try:
            globals()['deudabanco%s' % n ].append(tabla_deuda_final[n+2][19:])
         except IndexError:
            globals()['deudabanco%s' % n ].append('')

      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco1_%s' % n ] = deudabanco1[0][n]
            except IndexError:
                  globals()['deudabanco1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco2_%s' % n ] = deudabanco2[0][n]
            except IndexError:
                  globals()['deudabanco2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco3_%s' % n ] = deudabanco3[0][n]
            except IndexError:
                  globals()['deudabanco3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco4_%s' % n ] = deudabanco4[0][n]
            except IndexError:
                  globals()['deudabanco4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco5_%s' % n ] = deudabanco5[0][n]
            except IndexError:
                  globals()['deudabanco5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco6_%s' % n ] = deudabanco6[0][n]
            except IndexError:
                  globals()['deudabanco6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco7_%s' % n ] = deudabanco7[0][n]
            except IndexError:
                  globals()['deudabanco7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco8_%s' % n ] = deudabanco8[0][n]
            except IndexError:
                  globals()['deudabanco8_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabanco9_%s' % n ] = deudabanco9[0][n]
            except IndexError:
                  globals()['deudabanco9_%s' % n ] = ''
      except IndexError:
         pass
         
      for n in range(1,10):
         globals()['deudabancosit%s' % n ]=[]
         try:
            globals()['deudabancosit%s' % n ].append(tabla_deuda_sit_final[n+2][19:])
         except IndexError:
            globals()['deudabancosit%s' % n ].append('')

      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit1_%s' % n ] = deudabancosit1[0][n]
            except IndexError:
                  globals()['deudabancosit1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit2_%s' % n ] = deudabancosit2[0][n]
            except IndexError:
                  globals()['deudabancosit2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit3_%s' % n ] = deudabancosit3[0][n]
            except IndexError:
                  globals()['deudabancosit3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit4_%s' % n ] = deudabancosit4[0][n]
            except IndexError:
                  globals()['deudabancosit4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit5_%s' % n ] = deudabancosit5[0][n]
            except IndexError:
                  globals()['deudabancosit5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit6_%s' % n ] = deudabancosit6[0][n]
            except IndexError:
                  globals()['deudabancosit6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit7_%s' % n ] = deudabancosit7[0][n]
            except IndexError:
                  globals()['deudabancosit7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit8_%s' % n ] = deudabancosit8[0][n]
            except IndexError:
                  globals()['deudabancosit8_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
            try:
                  globals()['deudabancosit9_%s' % n ] = deudabancosit9[0][n]
            except IndexError:
                  globals()['deudabancosit9_%s' % n ] = ''
      except IndexError:
         pass


      #elapsed_time = time.time() - start_time
      #print ('OK. Tiempo:', str(datetime.timedelta(seconds = elapsed_time)).partition('.')[0])

      nosis_output = [contrato_output, codigo_output, score_nosis, deuda_nosis_ult, nosis_name, actividad_output,
                     domicilio_output, antecedentes_fiscales_output, concurso_output, aportes, BCRA_sit,
                     cheques_cant, BCRA_ult, AFIP_output, empleador_output, ganancias_output, iva_output, empleados,
                     facturacion, cheques_output, legal_output, referencias_output]

      nosis_deuda = [ nosisdeuda1, nosisdeuda2, nosisdeuda3, nosisdeuda4, nosisdeuda5, nosisdeuda6, nosisdeuda7, nosisdeuda8, nosisdeuda9, nosisdeuda10, nosisdeuda11, nosisdeuda12,
                     nosisdeuda13, nosisdeuda14, nosisdeuda15, nosisdeuda16, nosisdeuda17, nosisdeuda18, nosisdeuda19, nosisdeuda20, nosisdeuda21, nosisdeuda22, nosisdeuda23, nosisdeuda24 ]
      
      deuda_bancos = [ banco1, banco2, banco3, banco4, banco5, banco6, banco7, banco8, banco9,
                     deudabanco1_0, deudabanco1_1, deudabanco1_2, deudabanco1_3, deudabanco1_4, deudabanco1_5, deudabanco2_0, deudabanco2_1, deudabanco2_2, deudabanco2_3, 
                     deudabanco2_4, deudabanco2_5, deudabanco3_0, deudabanco3_1, deudabanco3_2, deudabanco3_3, deudabanco3_4, deudabanco3_5, deudabanco4_0, deudabanco4_1, 
                     deudabanco4_2, deudabanco4_3, deudabanco4_4, deudabanco4_5, deudabanco5_0, deudabanco5_1, deudabanco5_2, deudabanco5_3, deudabanco5_4, deudabanco5_5,
                     deudabanco6_0, deudabanco6_1, deudabanco6_2, deudabanco6_3, deudabanco6_4, deudabanco6_5, deudabanco7_0, deudabanco7_1, deudabanco7_2, deudabanco7_3,
                     deudabanco7_4, deudabanco7_5, deudabanco8_0, deudabanco8_1, deudabanco8_2, deudabanco8_3, deudabanco8_4, deudabanco8_5, deudabanco9_0, deudabanco9_1,
                     deudabanco9_2, deudabanco9_3, deudabanco9_4, deudabanco9_5, deudabancosit1_0, deudabancosit1_1, deudabancosit1_2, deudabancosit1_3, deudabancosit1_4, 
                     deudabancosit1_5, deudabancosit2_0, deudabancosit2_1, deudabancosit2_2, deudabancosit2_3, deudabancosit2_4, deudabancosit2_5, deudabancosit3_0, deudabancosit3_1, 
                     deudabancosit3_2, deudabancosit3_3, deudabancosit3_4, deudabancosit3_5, deudabancosit4_0, deudabancosit4_1, deudabancosit4_2, deudabancosit4_3, deudabancosit4_4, 
                     deudabancosit4_5, deudabancosit5_0, deudabancosit5_1, deudabancosit5_2, deudabancosit5_3, deudabancosit5_4, deudabancosit5_5, deudabancosit6_0, deudabancosit6_1, 
                     deudabancosit6_2, deudabancosit6_3, deudabancosit6_4, deudabancosit6_5, deudabancosit7_0, deudabancosit7_1, deudabancosit7_2, deudabancosit7_3, deudabancosit7_4,
                     deudabancosit7_5, deudabancosit8_0, deudabancosit8_1, deudabancosit8_2, deudabancosit8_3, deudabancosit8_4, deudabancosit8_5, deudabancosit9_0, deudabancosit9_1,
                     deudabancosit9_2, deudabancosit9_3, deudabancosit9_4, deudabancosit9_5 ]

      final_aportes = [ fecha_aportes_01, fecha_aportes_02, fecha_aportes_03, fecha_aportes_04, fecha_aportes_05, fecha_aportes_06, fecha_aportes_07, fecha_aportes_08,
                        fecha_aportes_09, fecha_aportes_10, fecha_aportes_11, fecha_aportes_12, seguridad_aportes_01, seguridad_aportes_02, seguridad_aportes_03, seguridad_aportes_04,
                        seguridad_aportes_05, seguridad_aportes_06, seguridad_aportes_07, seguridad_aportes_08, seguridad_aportes_09, seguridad_aportes_10, seguridad_aportes_11,
                        seguridad_aportes_12, obra_aportes_01, obra_aportes_02, obra_aportes_03, obra_aportes_04, obra_aportes_05, obra_aportes_06, obra_aportes_07, obra_aportes_08,
                        obra_aportes_09, obra_aportes_10, obra_aportes_11, obra_aportes_12, patronal_aportes_01, patronal_aportes_02, patronal_aportes_03, patronal_aportes_04, 
                        patronal_aportes_05, patronal_aportes_06, patronal_aportes_07, patronal_aportes_08, patronal_aportes_09, patronal_aportes_10, patronal_aportes_11, 
                        patronal_aportes_12, consulta_01, consulta_02,consulta_03, consulta_04,consulta_05, consulta_06,semestre_01, semestre_02,semestre_03, semestre_04,semestre_05,
                        semestre_06 ]
      
      dict_nosis =  {'Razón Social:': nosis_name, 'CUIT:': cuit_long, 'Score Nosis:': score_nosis, 'Contrato Social:': contrato_output, 'Registro AFIP:': AFIP_output, 
                     'Código AFIP:': codigo_output, 'Actividad:': actividad_output, 'Domicilio:': domicilio_output, 'Facturación:': facturacion, 'Empleados:': empleados,
                     'Deuda (miles):': deuda_nosis_ult, 'Ganancias?:': ganancias_output, 'IVA?:': iva_output, 'Es empleador?:': empleador_output,
                     'Ultima Situación BCRA:': BCRA_ult, 'Situación BCRA:': BCRA_sit, 'Antecedentes Fiscales:': antecedentes_fiscales_output, 'Concursos:': concurso_output, 
                     'Aportes:': aportes, 'Cheques cantidad:': cheques_cant, 'Cheques situación:': cheques_output, 'Legales:': legal_output, 'Referencias:': referencias_output}
 
      base_key = 'appHJKYgvmLkpv022'
      table_name = 'Scoring'
      AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
      airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)

      #insertar id del Cliente de la tabla
      id = id_airtable
      datos_cliente = airtable.search('Clientes',id)[0]['fields']

      directores = []
      try:
         directores.append(datos_cliente.get('CUIT Dir 1')[0])
         directores.append(datos_cliente.get('Dir1'))
         directores.append(str(datos_cliente.get('% D1')[0])+'%')
      except TypeError:
         pass
      try:
         directores.append(datos_cliente.get('CUIT Dir 2')[0])
         directores.append(datos_cliente.get('Dir2'))
         directores.append(str(datos_cliente.get('% D2')[0])+'%')
      except TypeError:
         pass
      try:
         directores.append(datos_cliente.get('CUIT Dir 3')[0])
         directores.append(datos_cliente.get('Dir3'))
         directores.append(str(datos_cliente.get('% D3')[0])+'%')
      except TypeError:
         pass
      try:
         directores.append(datos_cliente.get('CUIT Dir 4')[0])
         directores.append(datos_cliente.get('Dir4'))
         directores.append(str(datos_cliente.get('% D4')[0])+'%')
      except TypeError:
         pass
      try:
         directores.append(datos_cliente.get('CUIT Dir 5')[0])
         directores.append(datos_cliente.get('Dir5'))
         directores.append(str(datos_cliente.get('% D5')[0])+'%')
      except TypeError:
         pass
      
      session['nosis_soc'] = nosis_sociedad
      session['nosistabla'] = nosis_output
      session['nosis_deuda'] = nosis_deuda
      session['deuda_bancos'] = deuda_bancos
      session['final_aportes'] = final_aportes
      try:
         nosis_tabla_final = nosis_tabla.tolist()
      except AttributeError:
         nosis_tabla_final = nosis_tabla
      session['nosis_fechas'] = nosis_tabla_final
      session['datos_dir'] = directores

      return render_template("nosisresult.html", nosisresult = dict_nosis)


@app.route('/nosisairtable/', methods=["GET", "POST"])
@login_required
def nosisairtable():
   nosis_sociedad = session.get('nosis_soc', None)
   datos_airtable = request.form['datos_airtable']
   directores = session.get('datos_dir', None)
   #nosis_sociedad = request.form['nosis_soc']
   if nosis_sociedad == 'personal':
      if datos_airtable == 'scoring':
         nosisairtable = session.get('nosistabla', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Scoring'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #insertar id de la tabla
         id = request.form['nosis_sociedad_id']
         session['nosis_sociedad_id'] = id
         record = {'B.1': nosisairtable[0],
                  'Codigo AFIP': nosisairtable[1],
                  'Nosis': int(nosisairtable[2]),
                  'Deuda Total Nosis': float(nosisairtable[3].replace(",", "")),
                  'Razon Social': nosisairtable[4],
                  'Actividad': nosisairtable[5],
                  'Domicilio': nosisairtable[6],
                  'Antecedentes Fiscales': int(nosisairtable[7]),
                  'Antecedentes Concursos': int(nosisairtable[8]),
                  'Deuda Previsional': int(nosisairtable[9]),
                  'Antecedentes Crediticios': int(nosisairtable[10]),
                  'Cheques Rechazados': int(nosisairtable[11]),
                  'Sit BCRA': int(nosisairtable[12]),
                  'Inscripcion AFIP':  nosisairtable[13],
                  'Empleador': int(nosisairtable[14]),
                  'Ganancias': int(nosisairtable[15]),
                  'IVA': int(nosisairtable[16]),
                  'Cheques': int(nosisairtable[17]),
                  'Juicios': int(nosisairtable[18]),
                  'Referencias': int(nosisairtable[19]),
                  'Empleador dir1': nosisairtable[20],
                  'Compromisos dir1': nosisairtable[21],
                  'NSE dir1': nosisairtable[22]
                  }
         airtable.update_by_field('Id', id, record)
         return render_template("nosisairtable.html", airtableresult = record)
      
      elif datos_airtable == 'extra':
         nosis_personales = session.get('nosis_personales', None)
         nosisper = session.get('deuda_nosis', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Nosis Personales'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #queda fijo, siempre 1
         id = '1'
         record = {'fecha01': nosis_personales[0],'fecha02': nosis_personales[1],'fecha03': nosis_personales[2],
                  'fecha04': nosis_personales[3],'fecha05': nosis_personales[4],'fecha06': nosis_personales[5],
                  'fecha07': nosis_personales[6],'fecha08': nosis_personales[7],'fecha09': nosis_personales[8],
                  'fecha10': nosis_personales[9],'fecha11': nosis_personales[10],'fecha12': nosis_personales[11],
                  'fecha13': nosis_personales[12],'fecha14': nosis_personales[13],'fecha15': nosis_personales[14],
                  'fecha16': nosis_personales[15],'fecha17': nosis_personales[16],'fecha18': nosis_personales[17],
                  'fecha19': nosis_personales[18],'fecha20': nosis_personales[19],'fecha21': nosis_personales[20],
                  'fecha22': nosis_personales[21],'fecha23': nosis_personales[22],'fecha24': nosis_personales[23],
                  'deuda01': nosisper[0],'deuda02': nosisper[1],'deuda03': nosisper[2],'deuda04': nosisper[3],
                  'deuda05': nosisper[4],'deuda06': nosisper[5],'deuda07': nosisper[6],'deuda08': nosisper[7],
                  'deuda09': nosisper[8],'deuda10': nosisper[9],'deuda11': nosisper[10],'deuda12': nosisper[11],
                  'deuda13': nosisper[12],'deuda14': nosisper[13],'deuda15': nosisper[14],'deuda16': nosisper[15],
                  'deuda17': nosisper[16],'deuda18': nosisper[17],'deuda19': nosisper[18],'deuda20': nosisper[19],
                  'deuda21': nosisper[20],'deuda22': nosisper[21],'deuda23': nosisper[22],'deuda24': nosisper[23]
               }
         airtable.update_by_field('Id', id, record)

         table_name = 'Bancos Personales'
         deudabanco = session.get('deuda_bancos', None)
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #queda fijo, siempre 1
         id = '1'
         record = {'Banco1': deudabanco[0],'Banco2': deudabanco[1],'Banco3': deudabanco[2],'Banco4': deudabanco[3],'Banco5': deudabanco[4],
                  'Banco6': deudabanco[5],'Banco7': deudabanco[6],'Banco8': deudabanco[7],'Banco9': deudabanco[8],
                  'Deuda 01-06':deudabanco[9].replace(",", ""),'Deuda 01-05':deudabanco[10].replace(",", ""),
                  'Deuda 01-04':deudabanco[11].replace(",", ""),'Deuda 01-03':deudabanco[12].replace(",", ""),
                  'Deuda 01-02':deudabanco[13].replace(",", ""),'Deuda 01-01':deudabanco[14].replace(",", ""),      
                  'Deuda 02-06':deudabanco[15].replace(",", ""),'Deuda 02-05':deudabanco[16].replace(",", ""),
                  'Deuda 02-04':deudabanco[17].replace(",", ""),'Deuda 02-03':deudabanco[18].replace(",", ""),
                  'Deuda 02-02':deudabanco[19].replace(",", ""),'Deuda 02-01':deudabanco[20].replace(",", ""), 
                  'Deuda 03-06':deudabanco[21].replace(",", ""),'Deuda 03-05':deudabanco[22].replace(",", ""),
                  'Deuda 03-04':deudabanco[23].replace(",", ""),'Deuda 03-03':deudabanco[24].replace(",", ""),
                  'Deuda 03-02':deudabanco[25].replace(",", ""),'Deuda 03-01':deudabanco[26].replace(",", ""),
                  'Deuda 04-06':deudabanco[27].replace(",", ""),'Deuda 04-05':deudabanco[28].replace(",", ""),
                  'Deuda 04-04':deudabanco[29].replace(",", ""),'Deuda 04-03':deudabanco[30].replace(",", ""),
                  'Deuda 04-02':deudabanco[31].replace(",", ""),'Deuda 04-01':deudabanco[32].replace(",", ""),
                  'Deuda 05-06':deudabanco[33].replace(",", ""),'Deuda 05-05':deudabanco[34].replace(",", ""),
                  'Deuda 05-04':deudabanco[35].replace(",", ""),'Deuda 05-03':deudabanco[36].replace(",", ""),
                  'Deuda 05-02':deudabanco[37].replace(",", ""),'Deuda 05-01':deudabanco[38].replace(",", ""),
                  'Deuda 06-06':deudabanco[39].replace(",", ""),'Deuda 06-05':deudabanco[40].replace(",", ""),
                  'Deuda 06-04':deudabanco[41].replace(",", ""),'Deuda 06-03':deudabanco[42].replace(",", ""),
                  'Deuda 06-02':deudabanco[43].replace(",", ""),'Deuda 06-01':deudabanco[44].replace(",", ""),
                  'Deuda 07-06':deudabanco[45].replace(",", ""),'Deuda 07-05':deudabanco[46].replace(",", ""),
                  'Deuda 07-04':deudabanco[47].replace(",", ""),'Deuda 07-03':deudabanco[48].replace(",", ""),
                  'Deuda 07-02':deudabanco[49].replace(",", ""),'Deuda 07-01':deudabanco[50].replace(",", ""),
                  'Deuda 08-06':deudabanco[51].replace(",", ""),'Deuda 08-05':deudabanco[52].replace(",", ""),
                  'Deuda 08-04':deudabanco[53].replace(",", ""),'Deuda 08-03':deudabanco[54].replace(",", ""),
                  'Deuda 08-02':deudabanco[55].replace(",", ""),'Deuda 08-01':deudabanco[56].replace(",", ""),
                  'Deuda 09-06':deudabanco[57].replace(",", ""),'Deuda 09-05':deudabanco[58].replace(",", ""),
                  'Deuda 09-04':deudabanco[59].replace(",", ""),'Deuda 09-03':deudabanco[60].replace(",", ""),
                  'Deuda 09-02':deudabanco[61].replace(",", ""),'Deuda 09-01':deudabanco[62].replace(",", ""),
                  'Sit 01-06':deudabanco[63].replace("sit-", ""),'Sit 01-05':deudabanco[64].replace("sit-", ""),
                  'Sit 01-04':deudabanco[65].replace("sit-", ""),'Sit 01-03':deudabanco[66].replace("sit-", ""),
                  'Sit 01-02':deudabanco[67].replace("sit-", ""),'Sit 01-01':deudabanco[68].replace("sit-", ""),      
                  'Sit 02-06':deudabanco[69].replace("sit-", ""),'Sit 02-05':deudabanco[70].replace("sit-", ""),
                  'Sit 02-04':deudabanco[71].replace("sit-", ""),'Sit 02-03':deudabanco[72].replace("sit-", ""),
                  'Sit 02-02':deudabanco[73].replace("sit-", ""),'Sit 02-01':deudabanco[74].replace("sit-", ""), 
                  'Sit 03-06':deudabanco[75].replace("sit-", ""),'Sit 03-05':deudabanco[76].replace("sit-", ""),
                  'Sit 03-04':deudabanco[77].replace("sit-", ""),'Sit 03-03':deudabanco[78].replace("sit-", ""),
                  'Sit 03-02':deudabanco[79].replace("sit-", ""),'Sit 03-01':deudabanco[80].replace("sit-", ""),
                  'Sit 04-06':deudabanco[81].replace("sit-", ""),'Sit 04-05':deudabanco[82].replace("sit-", ""),
                  'Sit 04-04':deudabanco[83].replace("sit-", ""),'Sit 04-03':deudabanco[84].replace("sit-", ""),
                  'Sit 04-02':deudabanco[85].replace("sit-", ""),'Sit 04-01':deudabanco[86].replace("sit-", ""),
                  'Sit 05-06':deudabanco[87].replace("sit-", ""),'Sit 05-05':deudabanco[88].replace("sit-", ""),
                  'Sit 05-04':deudabanco[89].replace("sit-", ""),'Sit 05-03':deudabanco[90].replace("sit-", ""),
                  'Sit 05-02':deudabanco[91].replace("sit-", ""),'Sit 05-01':deudabanco[92].replace("sit-", ""),
                  'Sit 06-06':deudabanco[93].replace("sit-", ""),'Sit 06-05':deudabanco[94].replace("sit-", ""),
                  'Sit 06-04':deudabanco[95].replace("sit-", ""),'Sit 06-03':deudabanco[96].replace("sit-", ""),
                  'Sit 06-02':deudabanco[97].replace("sit-", ""),'Sit 06-01':deudabanco[98].replace("sit-", ""),
                  'Sit 07-06':deudabanco[99].replace("sit-", ""),'Sit 07-05':deudabanco[100].replace("sit-", ""),
                  'Sit 07-04':deudabanco[101].replace("sit-", ""),'Sit 07-03':deudabanco[102].replace("sit-", ""),
                  'Sit 07-02':deudabanco[103].replace("sit-", ""),'Sit 07-01':deudabanco[104].replace("sit-", ""),
                  'Sit 08-06':deudabanco[105].replace("sit-", ""),'Sit 08-05':deudabanco[106].replace("sit-", ""),
                  'Sit 08-04':deudabanco[107].replace("sit-", ""),'Sit 08-03':deudabanco[108].replace("sit-", ""),
                  'Sit 08-02':deudabanco[109].replace("sit-", ""),'Sit 08-01':deudabanco[110].replace("sit-", ""),
                  'Sit 09-06':deudabanco[111].replace("sit-", ""),'Sit 09-05':deudabanco[112].replace("sit-", ""),
                  'Sit 09-04':deudabanco[113].replace("sit-", ""),'Sit 09-03':deudabanco[114].replace("sit-", ""),
                  'Sit 09-02':deudabanco[115].replace("sit-", ""),'Sit 09-01':deudabanco[116].replace("sit-", "")}

         airtable.update_by_field('Id', id, record)
         return render_template("nosisairtablepersonales.html", airtableresult = record)
      
      else:
         nosisairtable = session.get('nosistabla', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Scoring'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #insertar id de la tabla
         id = request.form['nosis_sociedad_id']
         session['nosis_sociedad_id'] = id
         record = {'B.1': nosisairtable[0],
                  'Codigo AFIP': nosisairtable[1],
                  'Nosis': int(nosisairtable[2]),
                  'Deuda Total Nosis': float(nosisairtable[3].replace(",", "")),
                  'Razon Social': nosisairtable[4],
                  'Actividad': nosisairtable[5],
                  'Domicilio': nosisairtable[6],
                  'Antecedentes Fiscales': int(nosisairtable[7]),
                  'Antecedentes Concursos': int(nosisairtable[8]),
                  'Deuda Previsional': int(nosisairtable[9]),
                  'Antecedentes Crediticios': int(nosisairtable[10]),
                  'Cheques Rechazados': int(nosisairtable[11]),
                  'Sit BCRA': int(nosisairtable[12]),
                  'Inscripcion AFIP':  nosisairtable[13],
                  'Empleador': int(nosisairtable[14]),
                  'Ganancias': int(nosisairtable[15]),
                  'IVA': int(nosisairtable[16]),
                  'Cheques': int(nosisairtable[17]),
                  'Juicios': int(nosisairtable[18]),
                  'Referencias': int(nosisairtable[19]),
                  'Empleador dir1': nosisairtable[20],
                  'Compromisos dir1': nosisairtable[21],
                  'NSE dir1': nosisairtable[22]
                  }
         airtable.update_by_field('Id', id, record)
         
         nosis_personales = session.get('nosis_personales', None)
         nosisper = session.get('deuda_nosis', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Nosis Personales'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #queda fijo, siempre 1
         id = '1'
         record = {'fecha01': nosis_personales[0],'fecha02': nosis_personales[1],'fecha03': nosis_personales[2],
                  'fecha04': nosis_personales[3],'fecha05': nosis_personales[4],'fecha06': nosis_personales[5],
                  'fecha07': nosis_personales[6],'fecha08': nosis_personales[7],'fecha09': nosis_personales[8],
                  'fecha10': nosis_personales[9],'fecha11': nosis_personales[10],'fecha12': nosis_personales[11],
                  'fecha13': nosis_personales[12],'fecha14': nosis_personales[13],'fecha15': nosis_personales[14],
                  'fecha16': nosis_personales[15],'fecha17': nosis_personales[16],'fecha18': nosis_personales[17],
                  'fecha19': nosis_personales[18],'fecha20': nosis_personales[19],'fecha21': nosis_personales[20],
                  'fecha22': nosis_personales[21],'fecha23': nosis_personales[22],'fecha24': nosis_personales[23],
                  'deuda01': nosisper[0],'deuda02': nosisper[1],'deuda03': nosisper[2],'deuda04': nosisper[3],
                  'deuda05': nosisper[4],'deuda06': nosisper[5],'deuda07': nosisper[6],'deuda08': nosisper[7],
                  'deuda09': nosisper[8],'deuda10': nosisper[9],'deuda11': nosisper[10],'deuda12': nosisper[11],
                  'deuda13': nosisper[12],'deuda14': nosisper[13],'deuda15': nosisper[14],'deuda16': nosisper[15],
                  'deuda17': nosisper[16],'deuda18': nosisper[17],'deuda19': nosisper[18],'deuda20': nosisper[19],
                  'deuda21': nosisper[20],'deuda22': nosisper[21],'deuda23': nosisper[22],'deuda24': nosisper[23]
               }
         airtable.update_by_field('Id', id, record)

         table_name = 'Bancos Personales'
         deudabanco = session.get('deuda_bancos', None)
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #queda fijo, siempre 1
         id = '1'
         record = {'Banco1': deudabanco[0],'Banco2': deudabanco[1],'Banco3': deudabanco[2],'Banco4': deudabanco[3],'Banco5': deudabanco[4],
                  'Banco6': deudabanco[5],'Banco7': deudabanco[6],'Banco8': deudabanco[7],'Banco9': deudabanco[8],
                  'Deuda 01-06':deudabanco[9].replace(",", ""),'Deuda 01-05':deudabanco[10].replace(",", ""),
                  'Deuda 01-04':deudabanco[11].replace(",", ""),'Deuda 01-03':deudabanco[12].replace(",", ""),
                  'Deuda 01-02':deudabanco[13].replace(",", ""),'Deuda 01-01':deudabanco[14].replace(",", ""),      
                  'Deuda 02-06':deudabanco[15].replace(",", ""),'Deuda 02-05':deudabanco[16].replace(",", ""),
                  'Deuda 02-04':deudabanco[17].replace(",", ""),'Deuda 02-03':deudabanco[18].replace(",", ""),
                  'Deuda 02-02':deudabanco[19].replace(",", ""),'Deuda 02-01':deudabanco[20].replace(",", ""), 
                  'Deuda 03-06':deudabanco[21].replace(",", ""),'Deuda 03-05':deudabanco[22].replace(",", ""),
                  'Deuda 03-04':deudabanco[23].replace(",", ""),'Deuda 03-03':deudabanco[24].replace(",", ""),
                  'Deuda 03-02':deudabanco[25].replace(",", ""),'Deuda 03-01':deudabanco[26].replace(",", ""),
                  'Deuda 04-06':deudabanco[27].replace(",", ""),'Deuda 04-05':deudabanco[28].replace(",", ""),
                  'Deuda 04-04':deudabanco[29].replace(",", ""),'Deuda 04-03':deudabanco[30].replace(",", ""),
                  'Deuda 04-02':deudabanco[31].replace(",", ""),'Deuda 04-01':deudabanco[32].replace(",", ""),
                  'Deuda 05-06':deudabanco[33].replace(",", ""),'Deuda 05-05':deudabanco[34].replace(",", ""),
                  'Deuda 05-04':deudabanco[35].replace(",", ""),'Deuda 05-03':deudabanco[36].replace(",", ""),
                  'Deuda 05-02':deudabanco[37].replace(",", ""),'Deuda 05-01':deudabanco[38].replace(",", ""),
                  'Deuda 06-06':deudabanco[39].replace(",", ""),'Deuda 06-05':deudabanco[40].replace(",", ""),
                  'Deuda 06-04':deudabanco[41].replace(",", ""),'Deuda 06-03':deudabanco[42].replace(",", ""),
                  'Deuda 06-02':deudabanco[43].replace(",", ""),'Deuda 06-01':deudabanco[44].replace(",", ""),
                  'Deuda 07-06':deudabanco[45].replace(",", ""),'Deuda 07-05':deudabanco[46].replace(",", ""),
                  'Deuda 07-04':deudabanco[47].replace(",", ""),'Deuda 07-03':deudabanco[48].replace(",", ""),
                  'Deuda 07-02':deudabanco[49].replace(",", ""),'Deuda 07-01':deudabanco[50].replace(",", ""),
                  'Deuda 08-06':deudabanco[51].replace(",", ""),'Deuda 08-05':deudabanco[52].replace(",", ""),
                  'Deuda 08-04':deudabanco[53].replace(",", ""),'Deuda 08-03':deudabanco[54].replace(",", ""),
                  'Deuda 08-02':deudabanco[55].replace(",", ""),'Deuda 08-01':deudabanco[56].replace(",", ""),
                  'Deuda 09-06':deudabanco[57].replace(",", ""),'Deuda 09-05':deudabanco[58].replace(",", ""),
                  'Deuda 09-04':deudabanco[59].replace(",", ""),'Deuda 09-03':deudabanco[60].replace(",", ""),
                  'Deuda 09-02':deudabanco[61].replace(",", ""),'Deuda 09-01':deudabanco[62].replace(",", ""),
                  'Sit 01-06':deudabanco[63].replace("sit-", ""),'Sit 01-05':deudabanco[64].replace("sit-", ""),
                  'Sit 01-04':deudabanco[65].replace("sit-", ""),'Sit 01-03':deudabanco[66].replace("sit-", ""),
                  'Sit 01-02':deudabanco[67].replace("sit-", ""),'Sit 01-01':deudabanco[68].replace("sit-", ""),      
                  'Sit 02-06':deudabanco[69].replace("sit-", ""),'Sit 02-05':deudabanco[70].replace("sit-", ""),
                  'Sit 02-04':deudabanco[71].replace("sit-", ""),'Sit 02-03':deudabanco[72].replace("sit-", ""),
                  'Sit 02-02':deudabanco[73].replace("sit-", ""),'Sit 02-01':deudabanco[74].replace("sit-", ""), 
                  'Sit 03-06':deudabanco[75].replace("sit-", ""),'Sit 03-05':deudabanco[76].replace("sit-", ""),
                  'Sit 03-04':deudabanco[77].replace("sit-", ""),'Sit 03-03':deudabanco[78].replace("sit-", ""),
                  'Sit 03-02':deudabanco[79].replace("sit-", ""),'Sit 03-01':deudabanco[80].replace("sit-", ""),
                  'Sit 04-06':deudabanco[81].replace("sit-", ""),'Sit 04-05':deudabanco[82].replace("sit-", ""),
                  'Sit 04-04':deudabanco[83].replace("sit-", ""),'Sit 04-03':deudabanco[84].replace("sit-", ""),
                  'Sit 04-02':deudabanco[85].replace("sit-", ""),'Sit 04-01':deudabanco[86].replace("sit-", ""),
                  'Sit 05-06':deudabanco[87].replace("sit-", ""),'Sit 05-05':deudabanco[88].replace("sit-", ""),
                  'Sit 05-04':deudabanco[89].replace("sit-", ""),'Sit 05-03':deudabanco[90].replace("sit-", ""),
                  'Sit 05-02':deudabanco[91].replace("sit-", ""),'Sit 05-01':deudabanco[92].replace("sit-", ""),
                  'Sit 06-06':deudabanco[93].replace("sit-", ""),'Sit 06-05':deudabanco[94].replace("sit-", ""),
                  'Sit 06-04':deudabanco[95].replace("sit-", ""),'Sit 06-03':deudabanco[96].replace("sit-", ""),
                  'Sit 06-02':deudabanco[97].replace("sit-", ""),'Sit 06-01':deudabanco[98].replace("sit-", ""),
                  'Sit 07-06':deudabanco[99].replace("sit-", ""),'Sit 07-05':deudabanco[100].replace("sit-", ""),
                  'Sit 07-04':deudabanco[101].replace("sit-", ""),'Sit 07-03':deudabanco[102].replace("sit-", ""),
                  'Sit 07-02':deudabanco[103].replace("sit-", ""),'Sit 07-01':deudabanco[104].replace("sit-", ""),
                  'Sit 08-06':deudabanco[105].replace("sit-", ""),'Sit 08-05':deudabanco[106].replace("sit-", ""),
                  'Sit 08-04':deudabanco[107].replace("sit-", ""),'Sit 08-03':deudabanco[108].replace("sit-", ""),
                  'Sit 08-02':deudabanco[109].replace("sit-", ""),'Sit 08-01':deudabanco[110].replace("sit-", ""),
                  'Sit 09-06':deudabanco[111].replace("sit-", ""),'Sit 09-05':deudabanco[112].replace("sit-", ""),
                  'Sit 09-04':deudabanco[113].replace("sit-", ""),'Sit 09-03':deudabanco[114].replace("sit-", ""),
                  'Sit 09-02':deudabanco[115].replace("sit-", ""),'Sit 09-01':deudabanco[116].replace("sit-", "")}
         airtable.update_by_field('Id', id, record)

         return render_template("nosisairtable.html", airtableresult = record)

   else:
      
      for n in range(0,15):
         try:
            globals()['director_%s' % n] = directores[n]
         except IndexError:
            globals()['director_%s' % n] = '-'
      
      dict_directores =  {'Director 1:': [director_0, director_1, director_2], 'Director 2:': [director_3, director_4, director_5], 'Director 3:': [director_6, director_7, director_8],
                        'Director 4:': [director_9, director_10, director_11], 'Director 5:': [director_12, director_13, director_14]}

      if datos_airtable == 'scoring':
         nosisairtable = session.get('nosistabla', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Scoring'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #insertar id de la tabla
         id = request.form['nosis_sociedad_id']
         session['nosis_sociedad_id'] = id
         record = {'B.1': nosisairtable[0],
                  'Codigo AFIP': nosisairtable[1],
                  'Nosis': int(nosisairtable[2]),
                  'Deuda Total Nosis': float(nosisairtable[3].replace(",", "")),
                  'Razon Social': nosisairtable[4],
                  'Actividad': nosisairtable[5],
                  'Domicilio': nosisairtable[6],
                  'Antecedentes Fiscales': int(nosisairtable[7]),
                  'Antecedentes Concursos': int(nosisairtable[8]),
                  'Deuda Previsional': int(nosisairtable[9]),
                  'Antecedentes Crediticios': int(nosisairtable[10]),
                  'Cheques Rechazados': int(nosisairtable[11]),
                  'Sit BCRA': int(nosisairtable[12]),
                  'Inscripcion AFIP':  nosisairtable[13],
                  'Empleador': int(nosisairtable[14]),
                  'Ganancias': int(nosisairtable[15]),
                  'IVA': int(nosisairtable[16]),
                  'Empleados': nosisairtable[17],
                  'Facturacion': nosisairtable[18],
                  'Cheques': int(nosisairtable[19]),
                  'Juicios': int(nosisairtable[20]),
                  'Referencias': int(nosisairtable[21])
                  }
         airtable.update_by_field('Id', id, record)
         session['datos_dir2'] = dict_directores
         return render_template("nosisairtable.html", airtableresult = record, directores = dict_directores)

      elif datos_airtable == 'extra':
         nosis_tabla = session.get('nosis_fechas', None)
         nosis_deuda = session.get('nosis_deuda', None)
         deudabanco = session.get('deuda_bancos', None)
         final_aportes = session.get('final_aportes', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Nosis Sociedades'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #id de la tabla, no se guarda, siempre 1
         id = '1'
         record = {'Fecha 1': nosis_tabla[0],'Fecha 2': nosis_tabla[1],'Fecha 3': nosis_tabla[2],
                  'Fecha 4': nosis_tabla[3],'Fecha 5': nosis_tabla[4],'Fecha 6': nosis_tabla[5],
                  'Fecha 7': nosis_tabla[6],'Fecha 8': nosis_tabla[7],'Fecha 9': nosis_tabla[8],
                  'Fecha 10': nosis_tabla[9],'Fecha 11': nosis_tabla[10],'Fecha 12': nosis_tabla[11],
                  'Fecha 13': nosis_tabla[12],'Fecha 14': nosis_tabla[13],'Fecha 15': nosis_tabla[14],
                  'Fecha 16': nosis_tabla[15],'Fecha 17': nosis_tabla[16],'Fecha 18': nosis_tabla[17],
                  'Fecha 19': nosis_tabla[18],'Fecha 20': nosis_tabla[19],'Fecha 21': nosis_tabla[20],
                  'Fecha 22': nosis_tabla[21],'Fecha 23': nosis_tabla[22],'Fecha 24': nosis_tabla[23],
                  'Deuda 1': nosis_deuda[0],'Deuda 2': nosis_deuda[1],'Deuda 3': nosis_deuda[2],'Deuda 4': nosis_deuda[3],
                  'Deuda 5': nosis_deuda[4],'Deuda 6': nosis_deuda[5],'Deuda 7': nosis_deuda[6],'Deuda 8': nosis_deuda[7],
                  'Deuda 9': nosis_deuda[8],'Deuda 10': nosis_deuda[9],'Deuda 11': nosis_deuda[10],'Deuda 12': nosis_deuda[11],
                  'Deuda 13': nosis_deuda[12],'Deuda 14': nosis_deuda[13],'Deuda 15': nosis_deuda[14],'Deuda 16': nosis_deuda[15],
                  'Deuda 17': nosis_deuda[16],'Deuda 18': nosis_deuda[17],'Deuda 19': nosis_deuda[18],'Deuda 20': nosis_deuda[19],
                  'Deuda 21': nosis_deuda[20],'Deuda 22': nosis_deuda[21],'Deuda 23': nosis_deuda[22],'Deuda 24': nosis_deuda[23],
                  'Banco1': deudabanco[0],'Banco2': deudabanco[1],'Banco3': deudabanco[2],'Banco4': deudabanco[3],'Banco5': deudabanco[4],
                  'Banco6': deudabanco[5],'Banco7': deudabanco[6],'Banco8': deudabanco[7],'Banco9': deudabanco[8],
                  'Deuda 01-06':deudabanco[9].replace(",", ""),'Deuda 01-05':deudabanco[10].replace(",", ""),
                  'Deuda 01-04':deudabanco[11].replace(",", ""),'Deuda 01-03':deudabanco[12].replace(",", ""),
                  'Deuda 01-02':deudabanco[13].replace(",", ""),'Deuda 01-01':deudabanco[14].replace(",", ""),      
                  'Deuda 02-06':deudabanco[15].replace(",", ""),'Deuda 02-05':deudabanco[16].replace(",", ""),
                  'Deuda 02-04':deudabanco[17].replace(",", ""),'Deuda 02-03':deudabanco[18].replace(",", ""),
                  'Deuda 02-02':deudabanco[19].replace(",", ""),'Deuda 02-01':deudabanco[20].replace(",", ""), 
                  'Deuda 03-06':deudabanco[21].replace(",", ""),'Deuda 03-05':deudabanco[22].replace(",", ""),
                  'Deuda 03-04':deudabanco[23].replace(",", ""),'Deuda 03-03':deudabanco[24].replace(",", ""),
                  'Deuda 03-02':deudabanco[25].replace(",", ""),'Deuda 03-01':deudabanco[26].replace(",", ""),
                  'Deuda 04-06':deudabanco[27].replace(",", ""),'Deuda 04-05':deudabanco[28].replace(",", ""),
                  'Deuda 04-04':deudabanco[29].replace(",", ""),'Deuda 04-03':deudabanco[30].replace(",", ""),
                  'Deuda 04-02':deudabanco[31].replace(",", ""),'Deuda 04-01':deudabanco[32].replace(",", ""),
                  'Deuda 05-06':deudabanco[33].replace(",", ""),'Deuda 05-05':deudabanco[34].replace(",", ""),
                  'Deuda 05-04':deudabanco[35].replace(",", ""),'Deuda 05-03':deudabanco[36].replace(",", ""),
                  'Deuda 05-02':deudabanco[37].replace(",", ""),'Deuda 05-01':deudabanco[38].replace(",", ""),
                  'Deuda 06-06':deudabanco[39].replace(",", ""),'Deuda 06-05':deudabanco[40].replace(",", ""),
                  'Deuda 06-04':deudabanco[41].replace(",", ""),'Deuda 06-03':deudabanco[42].replace(",", ""),
                  'Deuda 06-02':deudabanco[43].replace(",", ""),'Deuda 06-01':deudabanco[44].replace(",", ""),
                  'Deuda 07-06':deudabanco[45].replace(",", ""),'Deuda 07-05':deudabanco[46].replace(",", ""),
                  'Deuda 07-04':deudabanco[47].replace(",", ""),'Deuda 07-03':deudabanco[48].replace(",", ""),
                  'Deuda 07-02':deudabanco[49].replace(",", ""),'Deuda 07-01':deudabanco[50].replace(",", ""),
                  'Deuda 08-06':deudabanco[51].replace(",", ""),'Deuda 08-05':deudabanco[52].replace(",", ""),
                  'Deuda 08-04':deudabanco[53].replace(",", ""),'Deuda 08-03':deudabanco[54].replace(",", ""),
                  'Deuda 08-02':deudabanco[55].replace(",", ""),'Deuda 08-01':deudabanco[56].replace(",", ""),
                  'Deuda 09-06':deudabanco[57].replace(",", ""),'Deuda 09-05':deudabanco[58].replace(",", ""),
                  'Deuda 09-04':deudabanco[59].replace(",", ""),'Deuda 09-03':deudabanco[60].replace(",", ""),
                  'Deuda 09-02':deudabanco[61].replace(",", ""),'Deuda 09-01':deudabanco[62].replace(",", ""),
                  'Sit 01-06':deudabanco[63].replace("sit-", ""),'Sit 01-05':deudabanco[64].replace("sit-", ""),
                  'Sit 01-04':deudabanco[65].replace("sit-", ""),'Sit 01-03':deudabanco[66].replace("sit-", ""),
                  'Sit 01-02':deudabanco[67].replace("sit-", ""),'Sit 01-01':deudabanco[68].replace("sit-", ""),      
                  'Sit 02-06':deudabanco[69].replace("sit-", ""),'Sit 02-05':deudabanco[70].replace("sit-", ""),
                  'Sit 02-04':deudabanco[71].replace("sit-", ""),'Sit 02-03':deudabanco[72].replace("sit-", ""),
                  'Sit 02-02':deudabanco[73].replace("sit-", ""),'Sit 02-01':deudabanco[74].replace("sit-", ""), 
                  'Sit 03-06':deudabanco[75].replace("sit-", ""),'Sit 03-05':deudabanco[76].replace("sit-", ""),
                  'Sit 03-04':deudabanco[77].replace("sit-", ""),'Sit 03-03':deudabanco[78].replace("sit-", ""),
                  'Sit 03-02':deudabanco[79].replace("sit-", ""),'Sit 03-01':deudabanco[80].replace("sit-", ""),
                  'Sit 04-06':deudabanco[81].replace("sit-", ""),'Sit 04-05':deudabanco[82].replace("sit-", ""),
                  'Sit 04-04':deudabanco[83].replace("sit-", ""),'Sit 04-03':deudabanco[84].replace("sit-", ""),
                  'Sit 04-02':deudabanco[85].replace("sit-", ""),'Sit 04-01':deudabanco[86].replace("sit-", ""),
                  'Sit 05-06':deudabanco[87].replace("sit-", ""),'Sit 05-05':deudabanco[88].replace("sit-", ""),
                  'Sit 05-04':deudabanco[89].replace("sit-", ""),'Sit 05-03':deudabanco[90].replace("sit-", ""),
                  'Sit 05-02':deudabanco[91].replace("sit-", ""),'Sit 05-01':deudabanco[92].replace("sit-", ""),
                  'Sit 06-06':deudabanco[93].replace("sit-", ""),'Sit 06-05':deudabanco[94].replace("sit-", ""),
                  'Sit 06-04':deudabanco[95].replace("sit-", ""),'Sit 06-03':deudabanco[96].replace("sit-", ""),
                  'Sit 06-02':deudabanco[97].replace("sit-", ""),'Sit 06-01':deudabanco[98].replace("sit-", ""),
                  'Sit 07-06':deudabanco[99].replace("sit-", ""),'Sit 07-05':deudabanco[100].replace("sit-", ""),
                  'Sit 07-04':deudabanco[101].replace("sit-", ""),'Sit 07-03':deudabanco[102].replace("sit-", ""),
                  'Sit 07-02':deudabanco[103].replace("sit-", ""),'Sit 07-01':deudabanco[104].replace("sit-", ""),
                  'Sit 08-06':deudabanco[105].replace("sit-", ""),'Sit 08-05':deudabanco[106].replace("sit-", ""),
                  'Sit 08-04':deudabanco[107].replace("sit-", ""),'Sit 08-03':deudabanco[108].replace("sit-", ""),
                  'Sit 08-02':deudabanco[109].replace("sit-", ""),'Sit 08-01':deudabanco[110].replace("sit-", ""),
                  'Sit 09-06':deudabanco[111].replace("sit-", ""),'Sit 09-05':deudabanco[112].replace("sit-", ""),
                  'Sit 09-04':deudabanco[113].replace("sit-", ""),'Sit 09-03':deudabanco[114].replace("sit-", ""),
                  'Sit 09-02':deudabanco[115].replace("sit-", ""),'Sit 09-01':deudabanco[116].replace("sit-", ""),
                  'Fecha Aportes 1':final_aportes[0], 'Fecha Aportes 2':final_aportes[1],
                  'Fecha Aportes 3':final_aportes[2], 'Fecha Aportes 4':final_aportes[3],
                  'Fecha Aportes 5':final_aportes[4], 'Fecha Aportes 6':final_aportes[5],
                  'Fecha Aportes 7':final_aportes[6], 'Fecha Aportes 8':final_aportes[7],
                  'Fecha Aportes 9':final_aportes[8], 'Fecha Aportes 10':final_aportes[9],
                  'Fecha Aportes 11':final_aportes[10],'Fecha Aportes 12':final_aportes[11],
                  'Seguridad Aportes 1':final_aportes[12], 'Seguridad Aportes 2':final_aportes[13],
                  'Seguridad Aportes 3':final_aportes[14], 'Seguridad Aportes 4':final_aportes[15],
                  'Seguridad Aportes 5':final_aportes[16], 'Seguridad Aportes 6':final_aportes[17],
                  'Seguridad Aportes 7':final_aportes[18], 'Seguridad Aportes 8':final_aportes[19],
                  'Seguridad Aportes 9':final_aportes[20], 'Seguridad Aportes 10':final_aportes[21],
                  'Seguridad Aportes 11':final_aportes[22],'Seguridad Aportes 12':final_aportes[23],
                  'Obra Aportes 1':final_aportes[24], 'Obra Aportes 2':final_aportes[25],
                  'Obra Aportes 3':final_aportes[26], 'Obra Aportes 4':final_aportes[27],
                  'Obra Aportes 5':final_aportes[28], 'Obra Aportes 6':final_aportes[29],
                  'Obra Aportes 7':final_aportes[30], 'Obra Aportes 8':final_aportes[31],
                  'Obra Aportes 9':final_aportes[32], 'Obra Aportes 10':final_aportes[33],
                  'Obra Aportes 11':final_aportes[34],'Obra Aportes 12':final_aportes[35],
                  'Patronal Aportes 1':final_aportes[36], 'Patronal Aportes 2':final_aportes[37],
                  'Patronal Aportes 3':final_aportes[38], 'Patronal Aportes 4':final_aportes[39],
                  'Patronal Aportes 5':final_aportes[40], 'Patronal Aportes 6':final_aportes[41],
                  'Patronal Aportes 7':final_aportes[42], 'Patronal Aportes 8':final_aportes[43],
                  'Patronal Aportes 9':final_aportes[44], 'Patronal Aportes 10':final_aportes[45],
                  'Patronal Aportes 11':final_aportes[46],'Patronal Aportes 12':final_aportes[47],
                  'Consulta 1':final_aportes[48], 'Consulta 2':final_aportes[49],
                  'Consulta 3':final_aportes[50], 'Consulta 4':final_aportes[51],
                  'Consulta 5':final_aportes[52], 'Consulta 6':final_aportes[53],
                  'Semestre 1':final_aportes[54], 'Semestre 2':final_aportes[55],
                  'Semestre 3':final_aportes[56], 'Semestre 4':final_aportes[57],
                  'Semestre 5':final_aportes[58], 'Semestre 6':final_aportes[59]}
         airtable.update_by_field('Id', id, record)
         session['datos_dir2'] = dict_directores
         return render_template("nosisairtable.html", airtableresult = record, directores = dict_directores)

      else:
         nosisairtable = session.get('nosistabla', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Scoring'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #insertar id de la tabla
         id = request.form['nosis_sociedad_id']
         session['nosis_sociedad_id'] = id
         record = {'B.1': nosisairtable[0],
                  'Codigo AFIP': nosisairtable[1],
                  'Nosis': int(nosisairtable[2]),
                  'Deuda Total Nosis': float(nosisairtable[3].replace(",", "")),
                  'Razon Social': nosisairtable[4],
                  'Actividad': nosisairtable[5],
                  'Domicilio': nosisairtable[6],
                  'Antecedentes Fiscales': int(nosisairtable[7]),
                  'Antecedentes Concursos': int(nosisairtable[8]),
                  'Deuda Previsional': int(nosisairtable[9]),
                  'Antecedentes Crediticios': int(nosisairtable[10]),
                  'Cheques Rechazados': int(nosisairtable[11]),
                  'Sit BCRA': int(nosisairtable[12]),
                  'Inscripcion AFIP':  nosisairtable[13],
                  'Empleador': int(nosisairtable[14]),
                  'Ganancias': int(nosisairtable[15]),
                  'IVA': int(nosisairtable[16]),
                  'Empleados': nosisairtable[17],
                  'Facturacion': nosisairtable[18],
                  'Cheques': int(nosisairtable[19]),
                  'Juicios': int(nosisairtable[20]),
                  'Referencias': int(nosisairtable[21])
                  }
         airtable.update_by_field('Id', id, record)

         nosis_tabla = session.get('nosis_fechas', None)
         nosis_deuda = session.get('nosis_deuda', None)
         final_aportes = session.get('final_aportes', None)
         deudabanco = session.get('deuda_bancos', None)
         base_key = 'appHJKYgvmLkpv022'
         AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
         table_name = 'Nosis Sociedades'
         airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
         #id de la tabla, no se guarda, siempre 1
         id = '1'
         record = {'Fecha 1': nosis_tabla[0],'Fecha 2': nosis_tabla[1],'Fecha 3': nosis_tabla[2],
                  'Fecha 4': nosis_tabla[3],'Fecha 5': nosis_tabla[4],'Fecha 6': nosis_tabla[5],
                  'Fecha 7': nosis_tabla[6],'Fecha 8': nosis_tabla[7],'Fecha 9': nosis_tabla[8],
                  'Fecha 10': nosis_tabla[9],'Fecha 11': nosis_tabla[10],'Fecha 12': nosis_tabla[11],
                  'Fecha 13': nosis_tabla[12],'Fecha 14': nosis_tabla[13],'Fecha 15': nosis_tabla[14],
                  'Fecha 16': nosis_tabla[15],'Fecha 17': nosis_tabla[16],'Fecha 18': nosis_tabla[17],
                  'Fecha 19': nosis_tabla[18],'Fecha 20': nosis_tabla[19],'Fecha 21': nosis_tabla[20],
                  'Fecha 22': nosis_tabla[21],'Fecha 23': nosis_tabla[22],'Fecha 24': nosis_tabla[23],
                  'Deuda 1': nosis_deuda[0],'Deuda 2': nosis_deuda[1],'Deuda 3': nosis_deuda[2],'Deuda 4': nosis_deuda[3],
                  'Deuda 5': nosis_deuda[4],'Deuda 6': nosis_deuda[5],'Deuda 7': nosis_deuda[6],'Deuda 8': nosis_deuda[7],
                  'Deuda 9': nosis_deuda[8],'Deuda 10': nosis_deuda[9],'Deuda 11': nosis_deuda[10],'Deuda 12': nosis_deuda[11],
                  'Deuda 13': nosis_deuda[12],'Deuda 14': nosis_deuda[13],'Deuda 15': nosis_deuda[14],'Deuda 16': nosis_deuda[15],
                  'Deuda 17': nosis_deuda[16],'Deuda 18': nosis_deuda[17],'Deuda 19': nosis_deuda[18],'Deuda 20': nosis_deuda[19],
                  'Deuda 21': nosis_deuda[20],'Deuda 22': nosis_deuda[21],'Deuda 23': nosis_deuda[22],'Deuda 24': nosis_deuda[23],
                  'Banco1': deudabanco[0],'Banco2': deudabanco[1],'Banco3': deudabanco[2],'Banco4': deudabanco[3],'Banco5': deudabanco[4],
                  'Banco6': deudabanco[5],'Banco7': deudabanco[6],'Banco8': deudabanco[7],'Banco9': deudabanco[8],
                  'Deuda 01-06':deudabanco[9].replace(",", ""),'Deuda 01-05':deudabanco[10].replace(",", ""),
                  'Deuda 01-04':deudabanco[11].replace(",", ""),'Deuda 01-03':deudabanco[12].replace(",", ""),
                  'Deuda 01-02':deudabanco[13].replace(",", ""),'Deuda 01-01':deudabanco[14].replace(",", ""),      
                  'Deuda 02-06':deudabanco[15].replace(",", ""),'Deuda 02-05':deudabanco[16].replace(",", ""),
                  'Deuda 02-04':deudabanco[17].replace(",", ""),'Deuda 02-03':deudabanco[18].replace(",", ""),
                  'Deuda 02-02':deudabanco[19].replace(",", ""),'Deuda 02-01':deudabanco[20].replace(",", ""), 
                  'Deuda 03-06':deudabanco[21].replace(",", ""),'Deuda 03-05':deudabanco[22].replace(",", ""),
                  'Deuda 03-04':deudabanco[23].replace(",", ""),'Deuda 03-03':deudabanco[24].replace(",", ""),
                  'Deuda 03-02':deudabanco[25].replace(",", ""),'Deuda 03-01':deudabanco[26].replace(",", ""),
                  'Deuda 04-06':deudabanco[27].replace(",", ""),'Deuda 04-05':deudabanco[28].replace(",", ""),
                  'Deuda 04-04':deudabanco[29].replace(",", ""),'Deuda 04-03':deudabanco[30].replace(",", ""),
                  'Deuda 04-02':deudabanco[31].replace(",", ""),'Deuda 04-01':deudabanco[32].replace(",", ""),
                  'Deuda 05-06':deudabanco[33].replace(",", ""),'Deuda 05-05':deudabanco[34].replace(",", ""),
                  'Deuda 05-04':deudabanco[35].replace(",", ""),'Deuda 05-03':deudabanco[36].replace(",", ""),
                  'Deuda 05-02':deudabanco[37].replace(",", ""),'Deuda 05-01':deudabanco[38].replace(",", ""),
                  'Deuda 06-06':deudabanco[39].replace(",", ""),'Deuda 06-05':deudabanco[40].replace(",", ""),
                  'Deuda 06-04':deudabanco[41].replace(",", ""),'Deuda 06-03':deudabanco[42].replace(",", ""),
                  'Deuda 06-02':deudabanco[43].replace(",", ""),'Deuda 06-01':deudabanco[44].replace(",", ""),
                  'Deuda 07-06':deudabanco[45].replace(",", ""),'Deuda 07-05':deudabanco[46].replace(",", ""),
                  'Deuda 07-04':deudabanco[47].replace(",", ""),'Deuda 07-03':deudabanco[48].replace(",", ""),
                  'Deuda 07-02':deudabanco[49].replace(",", ""),'Deuda 07-01':deudabanco[50].replace(",", ""),
                  'Deuda 08-06':deudabanco[51].replace(",", ""),'Deuda 08-05':deudabanco[52].replace(",", ""),
                  'Deuda 08-04':deudabanco[53].replace(",", ""),'Deuda 08-03':deudabanco[54].replace(",", ""),
                  'Deuda 08-02':deudabanco[55].replace(",", ""),'Deuda 08-01':deudabanco[56].replace(",", ""),
                  'Deuda 09-06':deudabanco[57].replace(",", ""),'Deuda 09-05':deudabanco[58].replace(",", ""),
                  'Deuda 09-04':deudabanco[59].replace(",", ""),'Deuda 09-03':deudabanco[60].replace(",", ""),
                  'Deuda 09-02':deudabanco[61].replace(",", ""),'Deuda 09-01':deudabanco[62].replace(",", ""),
                  'Sit 01-06':deudabanco[63].replace("sit-", ""),'Sit 01-05':deudabanco[64].replace("sit-", ""),
                  'Sit 01-04':deudabanco[65].replace("sit-", ""),'Sit 01-03':deudabanco[66].replace("sit-", ""),
                  'Sit 01-02':deudabanco[67].replace("sit-", ""),'Sit 01-01':deudabanco[68].replace("sit-", ""),      
                  'Sit 02-06':deudabanco[69].replace("sit-", ""),'Sit 02-05':deudabanco[70].replace("sit-", ""),
                  'Sit 02-04':deudabanco[71].replace("sit-", ""),'Sit 02-03':deudabanco[72].replace("sit-", ""),
                  'Sit 02-02':deudabanco[73].replace("sit-", ""),'Sit 02-01':deudabanco[74].replace("sit-", ""), 
                  'Sit 03-06':deudabanco[75].replace("sit-", ""),'Sit 03-05':deudabanco[76].replace("sit-", ""),
                  'Sit 03-04':deudabanco[77].replace("sit-", ""),'Sit 03-03':deudabanco[78].replace("sit-", ""),
                  'Sit 03-02':deudabanco[79].replace("sit-", ""),'Sit 03-01':deudabanco[80].replace("sit-", ""),
                  'Sit 04-06':deudabanco[81].replace("sit-", ""),'Sit 04-05':deudabanco[82].replace("sit-", ""),
                  'Sit 04-04':deudabanco[83].replace("sit-", ""),'Sit 04-03':deudabanco[84].replace("sit-", ""),
                  'Sit 04-02':deudabanco[85].replace("sit-", ""),'Sit 04-01':deudabanco[86].replace("sit-", ""),
                  'Sit 05-06':deudabanco[87].replace("sit-", ""),'Sit 05-05':deudabanco[88].replace("sit-", ""),
                  'Sit 05-04':deudabanco[89].replace("sit-", ""),'Sit 05-03':deudabanco[90].replace("sit-", ""),
                  'Sit 05-02':deudabanco[91].replace("sit-", ""),'Sit 05-01':deudabanco[92].replace("sit-", ""),
                  'Sit 06-06':deudabanco[93].replace("sit-", ""),'Sit 06-05':deudabanco[94].replace("sit-", ""),
                  'Sit 06-04':deudabanco[95].replace("sit-", ""),'Sit 06-03':deudabanco[96].replace("sit-", ""),
                  'Sit 06-02':deudabanco[97].replace("sit-", ""),'Sit 06-01':deudabanco[98].replace("sit-", ""),
                  'Sit 07-06':deudabanco[99].replace("sit-", ""),'Sit 07-05':deudabanco[100].replace("sit-", ""),
                  'Sit 07-04':deudabanco[101].replace("sit-", ""),'Sit 07-03':deudabanco[102].replace("sit-", ""),
                  'Sit 07-02':deudabanco[103].replace("sit-", ""),'Sit 07-01':deudabanco[104].replace("sit-", ""),
                  'Sit 08-06':deudabanco[105].replace("sit-", ""),'Sit 08-05':deudabanco[106].replace("sit-", ""),
                  'Sit 08-04':deudabanco[107].replace("sit-", ""),'Sit 08-03':deudabanco[108].replace("sit-", ""),
                  'Sit 08-02':deudabanco[109].replace("sit-", ""),'Sit 08-01':deudabanco[110].replace("sit-", ""),
                  'Sit 09-06':deudabanco[111].replace("sit-", ""),'Sit 09-05':deudabanco[112].replace("sit-", ""),
                  'Sit 09-04':deudabanco[113].replace("sit-", ""),'Sit 09-03':deudabanco[114].replace("sit-", ""),
                  'Sit 09-02':deudabanco[115].replace("sit-", ""),'Sit 09-01':deudabanco[116].replace("sit-", ""),
                  'Fecha Aportes 1':final_aportes[0], 'Fecha Aportes 2':final_aportes[1],
                  'Fecha Aportes 3':final_aportes[2], 'Fecha Aportes 4':final_aportes[3],
                  'Fecha Aportes 5':final_aportes[4], 'Fecha Aportes 6':final_aportes[5],
                  'Fecha Aportes 7':final_aportes[6], 'Fecha Aportes 8':final_aportes[7],
                  'Fecha Aportes 9':final_aportes[8], 'Fecha Aportes 10':final_aportes[9],
                  'Fecha Aportes 11':final_aportes[10],'Fecha Aportes 12':final_aportes[11],
                  'Seguridad Aportes 1':final_aportes[12], 'Seguridad Aportes 2':final_aportes[13],
                  'Seguridad Aportes 3':final_aportes[14], 'Seguridad Aportes 4':final_aportes[15],
                  'Seguridad Aportes 5':final_aportes[16], 'Seguridad Aportes 6':final_aportes[17],
                  'Seguridad Aportes 7':final_aportes[18], 'Seguridad Aportes 8':final_aportes[19],
                  'Seguridad Aportes 9':final_aportes[20], 'Seguridad Aportes 10':final_aportes[21],
                  'Seguridad Aportes 11':final_aportes[22],'Seguridad Aportes 12':final_aportes[23],
                  'Obra Aportes 1':final_aportes[24], 'Obra Aportes 2':final_aportes[25],
                  'Obra Aportes 3':final_aportes[26], 'Obra Aportes 4':final_aportes[27],
                  'Obra Aportes 5':final_aportes[28], 'Obra Aportes 6':final_aportes[29],
                  'Obra Aportes 7':final_aportes[30], 'Obra Aportes 8':final_aportes[31],
                  'Obra Aportes 9':final_aportes[32], 'Obra Aportes 10':final_aportes[33],
                  'Obra Aportes 11':final_aportes[34],'Obra Aportes 12':final_aportes[35],
                  'Patronal Aportes 1':final_aportes[36], 'Patronal Aportes 2':final_aportes[37],
                  'Patronal Aportes 3':final_aportes[38], 'Patronal Aportes 4':final_aportes[39],
                  'Patronal Aportes 5':final_aportes[40], 'Patronal Aportes 6':final_aportes[41],
                  'Patronal Aportes 7':final_aportes[42], 'Patronal Aportes 8':final_aportes[43],
                  'Patronal Aportes 9':final_aportes[44], 'Patronal Aportes 10':final_aportes[45],
                  'Patronal Aportes 11':final_aportes[46],'Patronal Aportes 12':final_aportes[47],
                  'Consulta 1':final_aportes[48], 'Consulta 2':final_aportes[49],
                  'Consulta 3':final_aportes[50], 'Consulta 4':final_aportes[51],
                  'Consulta 5':final_aportes[52], 'Consulta 6':final_aportes[53],
                  'Semestre 1':final_aportes[54], 'Semestre 2':final_aportes[55],
                  'Semestre 3':final_aportes[56], 'Semestre 4':final_aportes[57],
                  'Semestre 5':final_aportes[58], 'Semestre 6':final_aportes[59]}
         
         airtable.update_by_field('Id', id, record)
         session['datos_dir2'] = dict_directores
         return render_template("nosisairtable.html", airtableresult = record, directores = dict_directores)


@app.route('/nosisairtableresult/', methods=["GET", "POST"])
@login_required
def nosisairtableresult():
   nosis_sociedad = session.get('nosis_soc', None)
   #datos_airtable = request.form['datos_airtable']
   directores = session.get('datos_dir2', None)

   options = Options()
   options.headless = False
   driver = webdriver.Chrome(executable_path='./Chrome/chromedriver', chrome_options=options)

   # keys
   usuario = '457993'
   contra = '079778'

   start_time = time.time()
   wait = ui.WebDriverWait(driver,30)

   score_dir = []
   nombre_dir = []
   domicilio_dir = []
   NSE_dir = []
   compromisos_dir = []
   empleador_dir = []
   cheques_dir = []
   juicios_dir = []
   concurso_dir = []
   referencias_dir = []

   directores_final = []

   if directores['Director 1:'][0] != '-':
      directores_final.append(directores['Director 1:'][0])
   else:
      pass
   if directores['Director 2:'][0] != '-':
      directores_final.append(directores['Director 2:'][0])
   else:
      pass
   if directores['Director 3:'][0] != '-':
      directores_final.append(directores['Director 3:'][0])
   else:
      pass
   if directores['Director 4:'][0] != '-':
      directores_final.append(directores['Director 4:'][0])
   else:
      pass
   if directores['Director 5:'][0] != '-':
      directores_final.append(directores['Director 5:'][0])
   else:
      pass

   driver.get('http://sac31.nosis.com/net/manager')
   driver.find_element_by_id('Email').send_keys(usuario)
   driver.find_element_by_id('Clave').send_keys(contra)
   try:
      driver.find_element_by_xpath('//*[@id="frmInicioSesion"]/div/div/div[2]/div[2]/button').click()
   except NoSuchElementException:
      driver.find_element_by_id('iniciarSesion').click()
      time.sleep(5)
      
   for d in range(len(directores_final)):
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(directores_final[d])
      driver.find_element_by_xpath('//*[@id="arbol"]/li/div/div[1]/input[3]').send_keys(Keys.ENTER)
      time.sleep(10)
      driver.find_element_by_id('btnConsultar').click()
      wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/b'))
      try:
         time.sleep(15)
      except NoSuchElementException:
         time.sleep(120)
      try:
         driver.find_element_by_id('link-continuar').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]').click()
      except NoSuchElementException:
         pass
      try:
         driver.find_element_by_xpath('//*[@id="ly-master"]/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]').click()
      except NoSuchElementException:
         pass   
      score_dir.append(driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]').text)
      nombre_dir.append(driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/b').text)
      domicilio_dir.append(str(driver.find_element_by_xpath("//*[contains(text(), 'Domicilio fiscal')]/following-sibling::ul").text).split("\n")[0])
      NSE_dir.append(str(driver.find_element_by_xpath("//*[contains(text(), 'Nivel Socioeconómico (NSE):')]").text).split('Nivel Socioeconómico (NSE): ')[1].split(' (')[0])
      try:
         compromisos_dir.append(str(driver.find_element_by_xpath("//*[contains(text(), 'Total de compromisos mensuales sistema financiero: ')]").text).split('Total de compromisos mensuales sistema financiero: ')[1])
      except NoSuchElementException:    
         compromisos_dir.append ('-')
      try:
         empleador_dir.append(str(driver.find_element_by_xpath("//*[contains(text(), 'Empleador: ')]").text).split(' | ')[1])
      except NoSuchElementException:
         empleador_dir.append ('-')
      tabla_cda = driver.find_element_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[4]/div/div/table[2]/tbody').text  
      cheques_dir.append(str(tabla_cda.partition('Cheques Rechazados del BCRA: ')[2][0:6]))
      juicios_dir.append(str(tabla_cda.partition('Juicios - Demandado: ')[2][0:6]))
      concurso_dir.append(str(tabla_cda.partition('Concurso o Quiebra: ')[2][0:6]))
      referencias_dir.append(str(tabla_cda.partition('Referencias Comerciales: ')[2][0:6]))
      
      head_deuda = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/thead'):
         ths = tr.find_elements_by_tag_name('th')
         if ths:
               head_deuda.append([th.text for th in ths])
      
      tabla_deuda = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
               tabla_deuda.append([td.text for td in tds])
      
      tabla_deuda_sit = []
      for tr in driver.find_elements_by_xpath('//*[@id="ly-master"]/div[4]/div[2]/div[5]/div[5]/div[2]/table[2]/tbody'):
         tds = tr.find_elements_by_tag_name('td')
         if tds:
               tabla_deuda_sit.append([td.get_attribute("class") for td in tds])
      
      head_deuda_01 = []
      head_deuda_03 = []
      try:
         for cell in (head_deuda)[0][1:]:
               head_deuda_01.append(int(cell))
         year01 = head_deuda_01[0]
         if head_deuda_01[1]>12:
               year02 = head_deuda_01[1]
         else:
               year02 = year01
         head_deuda_02 = (head_deuda_01)[1:]
         for cell in head_deuda_02:
                  if cell < 10:
                     if cell == 1:
                           year01 = year02
                     head_deuda_03.append(str(year01)+'-0'+str(cell))
                  else:
                     head_deuda_03.append(str(year01)+'-'+str(cell))

         num_deuda_head = np.array(head_deuda_03)[-12:]
         deuda_reshaped_head = num_deuda_head.reshape(1,12)
      except IndexError:
         pass

      try:
         num_deuda = np.array(tabla_deuda)
         deuda_reshaped = num_deuda.reshape(int(num_deuda.size/13),13)
         tabla_deuda_final = pd.DataFrame(deuda_reshaped, columns = ['Banco'] + head_deuda_03[-12:])
      except (IndexError, ValueError, NoSuchElementException):
         pass
      
      try:
         num_deuda_sit = np.array(tabla_deuda_sit)
         deuda_reshaped_sit = num_deuda_sit.reshape(int(num_deuda_sit.size/13),13)
         tabla_deuda_sit_final = pd.DataFrame(deuda_reshaped_sit, columns = ['Banco'] + head_deuda_03[-12:])
      except(IndexError, ValueError, NoSuchElementException):
         pass

      for n in range (1,7):
         try:
               globals()['nosisfechadir%s' % n] = head_deuda_03[5:][n]
         except (NoSuchElementException, IndexError):
               globals()['nosisfechadir%s' % n] = ''
               
      for n in range(1,10):
         try:
               globals()['banco%s' % n] = deuda_reshaped[n+2][0]
         except (NoSuchElementException, IndexError):
               globals()['banco%s' % n] = ''

      for n in range(1,10):
         globals()['deudabanco%s' % n ]=[]
         try:
               globals()['deudabanco%s' % n ].append(deuda_reshaped[n+2][7:])
         except IndexError:
               globals()['deudabanco%s' % n ].append('')
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco1_%s' % n ] = deudabanco1[0][n]
               except IndexError:
                  globals()['deudabanco1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco2_%s' % n ] = deudabanco2[0][n]
               except IndexError:
                  globals()['deudabanco2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco3_%s' % n ] = deudabanco3[0][n]
               except IndexError:
                  globals()['deudabanco3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco4_%s' % n ] = deudabanco4[0][n]
               except IndexError:
                  globals()['deudabanco4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco5_%s' % n ] = deudabanco5[0][n]
               except IndexError:
                  globals()['deudabanco5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco6_%s' % n ] = deudabanco6[0][n]
               except IndexError:
                  globals()['deudabanco6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco7_%s' % n ] = deudabanco7[0][n]
               except IndexError:
                  globals()['deudabanco7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco8_%s' % n ] = deudabanco8[0][n]
               except IndexError:
                  globals()['deudabanco8_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabanco9_%s' % n ] = deudabanco9[0][n]
               except IndexError:
                  globals()['deudabanco9_%s' % n ] = ''
      except IndexError:
         pass

      for n in range(1,10):
         globals()['deudabancosit%s' % n ]=[]
         try:
               globals()['deudabancosit%s' % n ].append(deuda_reshaped_sit[n+2][7:])
         except IndexError:
               globals()['deudabancosit%s' % n ].append('')

      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit1_%s' % n ] = deudabancosit1[0][n]
               except IndexError:
                  globals()['deudabancosit1_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit2_%s' % n ] = deudabancosit2[0][n]
               except IndexError:
                  globals()['deudabancosit2_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit3_%s' % n ] = deudabancosit3[0][n]
               except IndexError:
                  globals()['deudabancosit3_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit4_%s' % n ] = deudabancosit4[0][n]
               except IndexError:
                  globals()['deudabancosit4_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit5_%s' % n ] = deudabancosit5[0][n]
               except IndexError:
                  globals()['deudabancosit5_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit6_%s' % n ] = deudabancosit6[0][n]
               except IndexError:
                  globals()['deudabancosit6_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit7_%s' % n ] = deudabancosit7[0][n]
               except IndexError:
                  globals()['deudabancosit7_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit8_%s' % n ] = deudabancosit8[0][n]
               except IndexError:
                  globals()['deudabancosit8_%s' % n ] = ''
      except IndexError:
         pass
      try:
         for n in range(0,6):
               try:
                  globals()['deudabancosit9_%s' % n ] = deudabancosit9[0][n]
               except IndexError:
                  globals()['deudabancosit9_%s' % n ] = ''
      except IndexError:
         pass
      
      cda_dir = []
      for n in cheques_dir:
         if n == 'Cumple':
               cda_dir.append(0)
         else:
               cda_dir.append(0)

      for n in juicios_dir:
         if n == 'Cumple':
               cda_dir.append(0)
         else:
               cda_dir.append(0)

      for n in concurso_dir:
         if n == 'Cumple':
               cda_dir.append(0)
         else:
               cda_dir.append(0)

      for n in referencias_dir:
         if n == 'Cumple':
               cda_dir.append(0)
         else:
               cda_dir.append(0)
      
      base_key = 'appHJKYgvmLkpv022'
      AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
      table_name = 'Bancos Directores'
      airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
      id = str(d+1)
      record = {'Cheques': cda_dir[0],'Juicios':cda_dir[1],'Concursos': cda_dir[2],'Referencias':cda_dir[3],
               'Fecha 6': nosisfechadir1,'Fecha 5': nosisfechadir2,'Fecha 4': nosisfechadir3,
               'Fecha 3': nosisfechadir4,'Fecha 2': nosisfechadir5,'Fecha 1': nosisfechadir6,
               'Banco1': banco1,'Banco2': banco2,'Banco3': banco3,'Banco4': banco4,'Banco5': banco5,
               'Banco6': banco6,'Banco7': banco7,'Banco8': banco8,'Banco9': banco9,
               'Deuda 01-06':deudabanco1_0.replace(",", ""),'Deuda 01-05':deudabanco1_1.replace(",", ""),
               'Deuda 01-04':deudabanco1_2.replace(",", ""),'Deuda 01-03':deudabanco1_3.replace(",", ""),
               'Deuda 01-02':deudabanco1_4.replace(",", ""),'Deuda 01-01':deudabanco1_5.replace(",", ""),      
               'Deuda 02-06':deudabanco2_0.replace(",", ""),'Deuda 02-05':deudabanco2_1.replace(",", ""),
               'Deuda 02-04':deudabanco2_2.replace(",", ""),'Deuda 02-03':deudabanco2_3.replace(",", ""),
               'Deuda 02-02':deudabanco2_4.replace(",", ""),'Deuda 02-01':deudabanco2_5.replace(",", ""), 
               'Deuda 03-06':deudabanco3_0.replace(",", ""),'Deuda 03-05':deudabanco3_1.replace(",", ""),
               'Deuda 03-04':deudabanco3_2.replace(",", ""),'Deuda 03-03':deudabanco3_3.replace(",", ""),
               'Deuda 03-02':deudabanco3_4.replace(",", ""),'Deuda 03-01':deudabanco3_5.replace(",", ""),
               'Deuda 04-06':deudabanco4_0.replace(",", ""),'Deuda 04-05':deudabanco4_1.replace(",", ""),
               'Deuda 04-04':deudabanco4_2.replace(",", ""),'Deuda 04-03':deudabanco4_3.replace(",", ""),
               'Deuda 04-02':deudabanco4_4.replace(",", ""),'Deuda 04-01':deudabanco4_5.replace(",", ""),
               'Deuda 05-06':deudabanco5_0.replace(",", ""),'Deuda 05-05':deudabanco5_1.replace(",", ""),
               'Deuda 05-04':deudabanco5_2.replace(",", ""),'Deuda 05-03':deudabanco5_3.replace(",", ""),
               'Deuda 05-02':deudabanco5_4.replace(",", ""),'Deuda 05-01':deudabanco5_5.replace(",", ""),
               'Deuda 06-06':deudabanco6_0.replace(",", ""),'Deuda 06-05':deudabanco6_1.replace(",", ""),
               'Deuda 06-04':deudabanco6_2.replace(",", ""),'Deuda 06-03':deudabanco6_3.replace(",", ""),
               'Deuda 06-02':deudabanco6_4.replace(",", ""),'Deuda 06-01':deudabanco6_5.replace(",", ""),
               'Deuda 07-06':deudabanco7_0.replace(",", ""),'Deuda 07-05':deudabanco7_1.replace(",", ""),
               'Deuda 07-04':deudabanco7_2.replace(",", ""),'Deuda 07-03':deudabanco7_3.replace(",", ""),
               'Deuda 07-02':deudabanco7_4.replace(",", ""),'Deuda 07-01':deudabanco7_5.replace(",", ""),
               'Deuda 08-06':deudabanco8_0.replace(",", ""),'Deuda 08-05':deudabanco8_1.replace(",", ""),
               'Deuda 08-04':deudabanco8_2.replace(",", ""),'Deuda 08-03':deudabanco8_3.replace(",", ""),
               'Deuda 08-02':deudabanco8_4.replace(",", ""),'Deuda 08-01':deudabanco8_5.replace(",", ""),
               'Deuda 09-06':deudabanco9_0.replace(",", ""),'Deuda 09-05':deudabanco9_1.replace(",", ""),
               'Deuda 09-04':deudabanco9_2.replace(",", ""),'Deuda 09-03':deudabanco9_3.replace(",", ""),
               'Deuda 09-02':deudabanco9_4.replace(",", ""),'Deuda 09-01':deudabanco9_5.replace(",", ""),
               'Sit 01-06':deudabancosit1_0.replace("sit-", ""),'Sit 01-05':deudabancosit1_1.replace("sit-", ""),
               'Sit 01-04':deudabancosit1_2.replace("sit-", ""),'Sit 01-03':deudabancosit1_3.replace("sit-", ""),
               'Sit 01-02':deudabancosit1_4.replace("sit-", ""),'Sit 01-01':deudabancosit1_5.replace("sit-", ""),      
               'Sit 02-06':deudabancosit2_0.replace("sit-", ""),'Sit 02-05':deudabancosit2_1.replace("sit-", ""),
               'Sit 02-04':deudabancosit2_2.replace("sit-", ""),'Sit 02-03':deudabancosit2_3.replace("sit-", ""),
               'Sit 02-02':deudabancosit2_4.replace("sit-", ""),'Sit 02-01':deudabancosit2_5.replace("sit-", ""), 
               'Sit 03-06':deudabancosit3_0.replace("sit-", ""),'Sit 03-05':deudabancosit3_1.replace("sit-", ""),
               'Sit 03-04':deudabancosit3_2.replace("sit-", ""),'Sit 03-03':deudabancosit3_3.replace("sit-", ""),
               'Sit 03-02':deudabancosit3_4.replace("sit-", ""),'Sit 03-01':deudabancosit3_5.replace("sit-", ""),
               'Sit 04-06':deudabancosit4_0.replace("sit-", ""),'Sit 04-05':deudabancosit4_1.replace("sit-", ""),
               'Sit 04-04':deudabancosit4_2.replace("sit-", ""),'Sit 04-03':deudabancosit4_3.replace("sit-", ""),
               'Sit 04-02':deudabancosit4_4.replace("sit-", ""),'Sit 04-01':deudabancosit4_5.replace("sit-", ""),
               'Sit 05-06':deudabancosit5_0.replace("sit-", ""),'Sit 05-05':deudabancosit5_1.replace("sit-", ""),
               'Sit 05-04':deudabancosit5_2.replace("sit-", ""),'Sit 05-03':deudabancosit5_3.replace("sit-", ""),
               'Sit 05-02':deudabancosit5_4.replace("sit-", ""),'Sit 05-01':deudabancosit5_5.replace("sit-", ""),
               'Sit 06-06':deudabancosit6_0.replace("sit-", ""),'Sit 06-05':deudabancosit6_1.replace("sit-", ""),
               'Sit 06-04':deudabancosit6_2.replace("sit-", ""),'Sit 06-03':deudabancosit6_3.replace("sit-", ""),
               'Sit 06-02':deudabancosit6_4.replace("sit-", ""),'Sit 06-01':deudabancosit6_5.replace("sit-", ""),
               'Sit 07-06':deudabancosit7_0.replace("sit-", ""),'Sit 07-05':deudabancosit7_1.replace("sit-", ""),
               'Sit 07-04':deudabancosit7_2.replace("sit-", ""),'Sit 07-03':deudabancosit7_3.replace("sit-", ""),
               'Sit 07-02':deudabancosit7_4.replace("sit-", ""),'Sit 07-01':deudabancosit7_5.replace("sit-", ""),
               'Sit 08-06':deudabancosit8_0.replace("sit-", ""),'Sit 08-05':deudabancosit8_1.replace("sit-", ""),
               'Sit 08-04':deudabancosit8_2.replace("sit-", ""),'Sit 08-03':deudabancosit8_3.replace("sit-", ""),
               'Sit 08-02':deudabancosit8_4.replace("sit-", ""),'Sit 08-01':deudabancosit8_5.replace("sit-", ""),
               'Sit 09-06':deudabancosit9_0.replace("sit-", ""),'Sit 09-05':deudabancosit9_1.replace("sit-", ""),
               'Sit 09-04':deudabancosit9_2.replace("sit-", ""),'Sit 09-03':deudabancosit9_3.replace("sit-", ""),
               'Sit 09-02':deudabancosit9_4.replace("sit-", ""),'Sit 09-01':deudabancosit9_5.replace("sit-", "")}
      airtable.update_by_field('Id', id, record)
      driver.get('http://www.nosis.com')
      time.sleep(5)
      try:
         driver.find_element_by_xpath('/html/body/header/div/div/div[2]/div/div/div[1]/a').click()
      except NoSuchElementException:
         pass 
      time.sleep(5)
      #driver.get('http://sac33.nosis.com/net/manager')

   driver.close()
   elapsed_time = time.time() - start_time
   
   #hasta aca corre
   for n in range(5-len(score_dir)):
      score_dir.append('0')
      nombre_dir.append('-')
      directores_final.append('-')
      NSE_dir.append('-')
      empleador_dir.append('-')
      compromisos_dir.append('-')

   base_key = 'appHJKYgvmLkpv022'
   table_name = 'Scoring'
   AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'
   airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)

   #insertar id de la tabla
   id = session.get('nosis_sociedad_id', None)

   record = { 'Nosis D1': int(score_dir[0]), 'Nosis D2': int(score_dir[1]), 'Nosis D3': int(score_dir[2]), 'Nosis D4': int(score_dir[3]), 'Nosis D5': int(score_dir[4]),
            'Dir1': nombre_dir[0], 'Dir2': nombre_dir[1], 'Dir3': nombre_dir[2], 'Dir4': nombre_dir[3], 'Dir5': nombre_dir[4], 'Empleador dir1': empleador_dir[0],
            'Empleador dir2': empleador_dir[1], 'Empleador dir3': empleador_dir[2], 'Empleador dir4': empleador_dir[3], 'Empleador dir5': empleador_dir[4],
            'Compromisos dir1': compromisos_dir[0],'Compromisos dir2': compromisos_dir[1],'Compromisos dir3': compromisos_dir[2],'Compromisos dir4': compromisos_dir[3], 
            'Compromisos dir5': compromisos_dir[4], 'NSE dir1': NSE_dir[0], 'NSE dir2': NSE_dir[1], 'NSE dir3': NSE_dir[2], 'NSE dir4': NSE_dir[3], 'NSE dir5': NSE_dir[4] }

   airtable.update_by_field('Id', id, record)

   nosisairtableresult = record
   
   return render_template("nosisairtableresult.html", nosisairtableresult = nosisairtableresult)

@app.route('/afip/')
@login_required
def afip():
    return render_template('afip.html')

@app.route('/afipresult/', methods=["GET", "POST"])
@login_required
def afipresult():
   cuit = request.form['cuit_afip']
   afip_comp = request.form['afip_comp']
   afip_meses = request.form['afip_meses']

   options = Options()
   options.headless = False
   #driver = webdriver.Chrome('./Chrome/chromedriver', chrome_options=options)
   driver = webdriver.Chrome(executable_path='./Chrome/chromedriver', chrome_options=options)
   wait = ui.WebDriverWait(driver,30)
   #keys
   usuario = '20319324101'
   contra = 'fedegr211'
   cuit_long = str(cuit)[0:2]+'-'+str(cuit)[2:10]+'-'+str(cuit)[10:11]

   if afip_comp == 'emitidos' or afip_comp == 'todos':
      emitidos_input = 'true'
   else:
      emitidos_input = 'false'
   
   if afip_comp == 'recibidos' or afip_comp == 'todos':
      recibidos_input = 'true'
   else:
      recibidos_input = 'false'
   
   start_time = time.time()

   #intervalo meses
   elegir_rango = int(afip_meses)
   year = datetime.datetime.today().strftime('%Y')
   month = datetime.datetime.today().strftime('%m')
   rango_mes = range(1, elegir_rango+1)
   lista=[]
   for m in rango_mes:
      if (int(month)-m) == 0:
         meslista = ("01/"+str(12)+"/"+str(int(year)-1)+" - "+"31/"+str(12)+"/"+str(int(year)-1))
         month =int(month)+12
         year = int(year)-1
         lista.insert (0,meslista)
      else:
         if (int(month)-m)<10:
               if (int(month)-m)==1 or (int(month)-m)==3 or (int(month)-m)==5 or (int(month)-m)==7 or (int(month)-m)==8:
                  meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"31/0"+str(int(month)-m)+"/"+str(year))
                  lista.insert (0,meslista)
               elif (int(month)-m)==2:
                  if (int(year))%4==0:
                     if (int(year))%100==0:
                           if (int(year))%400==0:
                              meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"29/0"+str(int(month)-m)+"/"+str(year))
                              lista.insert (0,meslista)
                           else:    
                              meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"28/0"+str(int(month)-m)+"/"+str(year))
                              lista.insert (0,meslista)
                     else:
                           meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"29/0"+str(int(month)-m)+"/"+str(year))
                           lista.insert (0,meslista)
                  else:    
                     meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"28/0"+str(int(month)-m)+"/"+str(year))
                     lista.insert (0,meslista)    
               else:
                  meslista = ("01/0"+str(int(month)-m)+"/"+str(year)+" - "+"30/0"+str(int(month)-m)+"/"+str(year))
                  lista.insert (0,meslista)
         else:
               if (int(month)-m)==11:
                  meslista = ("01/"+str(int(month)-m)+"/"+str(year)+" - "+"30/"+str(int(month)-m)+"/"+str(year))
                  lista.insert (0,meslista)
               else:
                  meslista = ("01/"+str(int(month)-m)+"/"+str(year)+" - "+"31/"+str(int(month)-m)+"/"+str(year))
                  lista.insert (0,meslista)


   dict_emitidos = {}
   dict_recibidos = {}

   #registro en AFIP
   #driver.minimize_window()
   driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
   #driver.minimize_window()
   driver.find_element_by_id('F1:username').send_keys(usuario)
   driver.find_element_by_id('F1:btnSiguiente').click()
   driver.find_element_by_id('F1:password').send_keys(contra)
   driver.find_element_by_id('F1:btnIngresar').click()

   #ingresar a Mis Comprobantes
   driver.find_element_by_xpath('//*[@id="j_idt51"]/div/div[2]/div[2]/div[2]/ul/li[11]/a').click()
   driver.switch_to.window(driver.window_handles[-1])

   #Elegir Empresa
   boton_cuit = driver.find_element_by_xpath("//*[contains(text(), '"+cuit_long+"')]")
   wait.until(lambda driver: boton_cuit)
   time.sleep(2)
   actions = ActionChains(driver)
   #actions.move_to_element(boton_cuit).perform()
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   boton_cuit.location_once_scrolled_into_view
   boton_cuit.click()

   #Comprobantes Emitidos
   #print('Emitidos')
   #Seleccionar Fecha
   if emitidos_input == 'true':
      emitidos_table = []
      suma_emitidos = 0
      for f in lista:
         #driver.minimize_window()
         driver.find_element_by_id('btnEmitidos').click()
         driver.find_element_by_id('fechaEmision').clear()
         driver.find_element_by_id('fechaEmision').send_keys(f)
         driver.find_element_by_xpath('//*[@id="tabConsulta"]/div/div[5]').click()
         wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]'))
         try:
               time.sleep(3)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[5]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[7]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[8]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[9]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[10]').click()
               xy = driver.find_element_by_xpath('//*[@id="contenidoResultados"]/div[1]/div[1]/h3')
         except ElementNotVisibleException:
               time.sleep(15)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[5]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[7]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[8]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[9]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[10]').click()
               xy = driver.find_element_by_xpath('//*[@id="contenidoResultados"]/div[1]/div[1]/h3')
         actions = ActionChains(driver)
         actions.move_to_element_with_offset(xy, 1, 0)
         actions.click()
         actions.perform()
         wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]'))
         try:
               time.sleep(3)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]').click()
               driver.switch_to.window(driver.window_handles[-1])
               if driver.find_element_by_xpath('/html/body/table/tbody').text!='':
                  suma_emitidos += len(driver.find_elements_by_xpath('/html/body/table/tbody/tr'))
               for tr in driver.find_elements_by_xpath('/html/body/table/tbody'):
                  tds = tr.find_elements_by_tag_name('td')
                  if tds:
                     emitidos_table.append([td.text for td in tds])
               driver.close()
               driver.switch_to.window(driver.window_handles[1])
               #driver.minimize_window()
               driver.execute_script("window.history.go(-1)")
               print (f,'emitidos ok')
         except ElementNotVisibleException:
               time.sleep(15)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]').click()
               driver.switch_to.window(driver.window_handles[-1])
               if driver.find_element_by_xpath('/html/body/table/tbody').text!='':
                  suma_emitidos += len(driver.find_elements_by_xpath('/html/body/table/tbody/tr'))
               for tr in driver.find_elements_by_xpath('/html/body/table/tbody'):
                  tds = tr.find_elements_by_tag_name('td')
                  if tds:
                     emitidos_table.append([td.text for td in tds])
               driver.close()
               driver.switch_to.window(driver.window_handles[1])
               #driver.minimize_window()
               driver.execute_script("window.history.go(-1)")
               print (f,'emitidos ok')
      print()
      emitidos_table_final = [] 
      for x in emitidos_table:
         for y in x:
               emitidos_table_final.append(y)
      emitidos_table_final = [w.replace('$  ', '') for w in emitidos_table_final]
      emitidos_table_final = [w.replace('.', '') for w in emitidos_table_final]
      emitidos_table_final = [w.replace(',', '.') for w in emitidos_table_final]
      num_emitidos = np.array(emitidos_table_final)
      emitidos_reshaped = num_emitidos.reshape(suma_emitidos,10)
      nombre_emitidos = str(cuit)+"_"+str(datetime.datetime.today().strftime('%Y%m%d'))+"_emitidos.csv"

      emitidos_final = pd.DataFrame(emitidos_reshaped, columns=['Fecha','Tipo','Nro','CUIT','Emisor','Neto_gravado',
                                                            'Neto_no_gravado','Exento','IVA','Total'])
      emitidos_final['Fecha'] = pd.to_datetime(emitidos_final['Fecha'],format="%d/%m/%Y")
      #emitidos_final.to_csv('/Users/matiasiturralde/Google Drive/Credility/IT/AFIP/Mis Comprobantes/'+str(nombre_emitidos), encoding='utf-8', index=False)
      try:
         emitidos_final[['Total','Total_cambio']] = emitidos_final['Total'].str.split(' TC: ',expand=True)
      except ValueError:
         emitidos_final['Total_cambio'] = '1'
      emitidos_final.replace(to_replace=[None], value='1', inplace=True)
      emitidos_final['Neto_gravado'] = emitidos_final['Neto_gravado'].str.replace('USD ','')
      emitidos_final['Neto_no_gravado'] = emitidos_final['Neto_no_gravado'].str.replace('USD ','')
      emitidos_final['Exento'] = emitidos_final['Exento'].str.replace('USD ','')
      emitidos_final['IVA'] = emitidos_final['IVA'].str.replace('USD ','')
      emitidos_final['Total'] = emitidos_final['Total'].str.replace('USD ','')

      emitidos_final[["Neto_gravado","Neto_no_gravado","Exento",
                     "IVA","Total","Total_cambio"]] = emitidos_final[["Neto_gravado","Neto_no_gravado",
                                                         "Exento","IVA","Total","Total_cambio"]].apply(pd.to_numeric)
      emitidos_final["Comp"] = emitidos_final.Tipo.str[0:3]
      columnas = ['Neto_gravado','Neto_no_gravado','Exento','IVA','Total']
      for n in columnas:
         column_name = n
         mask = emitidos_final.Comp == '3 -'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '8 -'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '13 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '21 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '38 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '43 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '44 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '48 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '53 '
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '110'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '112'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '113'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '114'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
         mask = emitidos_final.Comp == '119'
         emitidos_final.loc[mask, column_name] = emitidos_final.loc[mask, column_name]*(-1)
      emitidos_final["Neto_gravado"] = emitidos_final.Neto_gravado * emitidos_final.Total_cambio
      emitidos_final["Neto_no_gravado"] = emitidos_final.Neto_no_gravado * emitidos_final.Total_cambio
      emitidos_final["Exento"] = emitidos_final.Exento * emitidos_final.Total_cambio
      emitidos_final["IVA"] = emitidos_final.IVA * emitidos_final.Total_cambio
      emitidos_final["Total"] = emitidos_final.Total * emitidos_final.Total_cambio
      emitidos_final['Total_neto'] = emitidos_final.Neto_gravado + emitidos_final.Neto_no_gravado + emitidos_final.Exento
      mask = emitidos_final.Total_neto == 0
      emitidos_final.loc[mask, 'Total_neto'] = emitidos_final.loc[mask, 'Total']
      #emitidos_final.to_csv('/Users/matiasiturralde/Google Drive/Credility/IT/AFIP/Mis Comprobantes/'+str(nombre_emitidos), encoding='utf-8', index=False)
      meses = elegir_rango - 1
      emitidos_sum_mes = emitidos_final['Total_neto'].groupby(emitidos_final['Fecha'].dt.to_period('M')).sum()
      emitidos_final = emitidos_sum_mes.reindex(pd.period_range(pd.Period(str(lista [0][6:10])+"-"+str(lista [0][3:5])), str(lista [meses][6:10])+"-"+str(lista [meses][3:5]),freq='M')).fillna(0.0)
      dict_emitidos = {'Vtas Mes-24': float((emitidos_final[0])/1000),
            'Vtas Mes-23': float((emitidos_final[1])/1000),
            'Vtas Mes-22': float((emitidos_final[2])/1000),
            'Vtas Mes-21': float((emitidos_final[3])/1000),
            'Vtas Mes-20': float((emitidos_final[4])/1000),
            'Vtas Mes-19': float((emitidos_final[5])/1000),
            'Vtas Mes-18': float((emitidos_final[6])/1000),
            'Vtas Mes-17': float((emitidos_final[7])/1000),
            'Vtas Mes-16': float((emitidos_final[8])/1000),
            'Vtas Mes-15': float((emitidos_final[9])/1000),
            'Vtas Mes-14': float((emitidos_final[10])/1000),
            'Vtas Mes-13': float((emitidos_final[11])/1000),
            'Vtas Mes-12': float((emitidos_final[12])/1000),
            'Vtas Mes-11': float((emitidos_final[13])/1000),
            'Vtas Mes-10': float((emitidos_final[14])/1000),
            'Vtas Mes-9': float((emitidos_final[15])/1000),
            'Vtas Mes-8': float((emitidos_final[16])/1000),
            'Vtas Mes-7': float((emitidos_final[17])/1000),
            'Vtas Mes-6': float((emitidos_final[18])/1000),
            'Vtas Mes-5': float((emitidos_final[19])/1000),
            'Vtas Mes-4': float((emitidos_final[20])/1000),
            'Vtas Mes-3': float((emitidos_final[21])/1000),
            'Vtas Mes-2': float((emitidos_final[22])/1000),
            'Vtas Mes-1': float((emitidos_final[23])/1000)}
         #pd.DataFrame(emitidos_reshaped, columns=['Fecha','Tipo','Nro','CUIT','Receptor','Neto_gravado','Neto_no_gravado','Exento','IVA','Total'])

   #Comprobantes Recibidos
   #print('Recibidos')
   #Seleccionar Fecha
   if recibidos_input == 'true':
      recibidos_table = []
      suma_recibidos = 0
      for f in lista:
         driver.find_element_by_id('btnRecibidos').click()
         driver.find_element_by_id('fechaEmision').clear()
         driver.find_element_by_id('fechaEmision').send_keys(f)
         driver.find_element_by_xpath('//*[@id="tabConsulta"]/div/div[5]').click()
         wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]'))
         try:
               time.sleep(4)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[5]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[7]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[8]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[9]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[10]').click()
               xy = driver.find_element_by_xpath('//*[@id="contenidoResultados"]/div[1]/div[1]/h3')
         except ElementNotVisibleException:
               time.sleep(20)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[4]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[5]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[7]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[8]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[9]').click()
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/ul/li[10]').click()
               xy = driver.find_element_by_xpath('//*[@id="contenidoResultados"]/div[1]/div[1]/h3')
         actions = ActionChains(driver)
         actions.move_to_element_with_offset(xy, 1, 0)
         actions.click()
         actions.perform()
         wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]'))
         try:
               time.sleep(4)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]').click()
               driver.switch_to.window(driver.window_handles[-1])
               if driver.find_element_by_xpath('/html/body/table/tbody').text!='':
                  suma_recibidos += len(driver.find_elements_by_xpath('/html/body/table/tbody/tr'))
               for tr in driver.find_elements_by_xpath('/html/body/table/tbody'):
                  tds = tr.find_elements_by_tag_name('td')
                  if tds:
                     recibidos_table.append([td.text for td in tds])
               driver.close()
               driver.switch_to.window(driver.window_handles[1])
               driver.execute_script("window.history.go(-1)")
               print (f,'recibidos ok')
         except (ElementNotVisibleException, WebDriverException):
               time.sleep(20)
               driver.find_element_by_xpath('//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[5]').click()
               driver.switch_to.window(driver.window_handles[-1])
               if driver.find_element_by_xpath('/html/body/table/tbody').text!='':
                  suma_recibidos += len(driver.find_elements_by_xpath('/html/body/table/tbody/tr'))
               for tr in driver.find_elements_by_xpath('/html/body/table/tbody'):
                  tds = tr.find_elements_by_tag_name('td')
                  if tds:
                     recibidos_table.append([td.text for td in tds])
               driver.close()
               driver.switch_to.window(driver.window_handles[1])
               driver.execute_script("window.history.go(-1)")
               print (f,'recibidos ok')
      print()
      recibidos_table_final = [] 
      for x in recibidos_table:
         for y in x:
               recibidos_table_final.append(y)
      recibidos_table_final = [w.replace('$  ', '') for w in recibidos_table_final]
      recibidos_table_final = [w.replace('.', '') for w in recibidos_table_final]
      recibidos_table_final = [w.replace(',', '.') for w in recibidos_table_final]
      num_recibidos = np.array(recibidos_table_final)
      recibidos_reshaped = num_recibidos.reshape(suma_recibidos,10)
      #pd.DataFrame(recibidos_reshaped, columns=['Fecha','Tipo','Nro','CUIT','Emisor','Neto_gravado','Neto_no_gravado','Exento','IVA','Total'])
      nombre_recibidos = str(cuit)+"_"+str(datetime.datetime.today().strftime('%Y%m%d'))+"_recibidos.csv"
      
      recibidos_final = pd.DataFrame(recibidos_reshaped, columns=['Fecha','Tipo','Nro','CUIT','Emisor','Neto_gravado',
                                                            'Neto_no_gravado','Exento','IVA','Total'])
      recibidos_final['Fecha'] = pd.to_datetime(recibidos_final['Fecha'],format="%d/%m/%Y")
      #recibidos_final.to_csv('/Users/matiasiturralde/Google Drive/Credility/IT/AFIP/Mis Comprobantes/'+str(nombre_recibidos), encoding='utf-8', index=False)
      try:
         recibidos_final[['Total','Total_cambio']] = recibidos_final['Total'].str.split(' TC: ',expand=True)
      except ValueError:
         recibidos_final['Total_cambio'] = '1'
      recibidos_final.replace(to_replace=[None], value='1', inplace=True)
      recibidos_final['Neto_gravado'] = recibidos_final['Neto_gravado'].str.replace('USD ','')
      recibidos_final['Neto_no_gravado'] = recibidos_final['Neto_no_gravado'].str.replace('USD ','')
      recibidos_final['Exento'] = recibidos_final['Exento'].str.replace('USD ','')
      recibidos_final['IVA'] = recibidos_final['IVA'].str.replace('USD ','')
      recibidos_final['Total'] = recibidos_final['Total'].str.replace('USD ','')

      recibidos_final[["Neto_gravado","Neto_no_gravado","Exento",
                     "IVA","Total","Total_cambio"]] = recibidos_final[["Neto_gravado","Neto_no_gravado",
                                                         "Exento","IVA","Total","Total_cambio"]].apply(pd.to_numeric)
      recibidos_final["Comp"] = recibidos_final.Tipo.str[0:3]
      columnas = ['Neto_gravado','Neto_no_gravado','Exento','IVA','Total']
      for n in columnas:
         column_name = n
         mask = recibidos_final.Comp == '3 -'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '8 -'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '13 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '21 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '38 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '43 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '44 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '48 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '53 '
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '110'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '112'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '113'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '114'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)
         mask = recibidos_final.Comp == '119'
         recibidos_final.loc[mask, column_name] = recibidos_final.loc[mask, column_name]*(-1)  
      recibidos_final["Neto_gravado"] = recibidos_final.Neto_gravado * recibidos_final.Total_cambio
      recibidos_final["Neto_no_gravado"] = recibidos_final.Neto_no_gravado * recibidos_final.Total_cambio
      recibidos_final["Exento"] = recibidos_final.Exento * recibidos_final.Total_cambio
      recibidos_final["IVA"] = recibidos_final.IVA * recibidos_final.Total_cambio
      recibidos_final["Total"] = recibidos_final.Total * recibidos_final.Total_cambio
      recibidos_final['Total_neto'] = recibidos_final.Neto_gravado + recibidos_final.Neto_no_gravado + recibidos_final.Exento
      mask = recibidos_final.Total_neto == 0
      recibidos_final.loc[mask, 'Total_neto'] = recibidos_final.loc[mask, 'Total']
      meses = elegir_rango - 1
      recibidos_sum_mes = recibidos_final['Total_neto'].groupby(recibidos_final['Fecha'].dt.to_period('M')).sum()
      recibidos_final = recibidos_sum_mes.reindex(pd.period_range(pd.Period(str(lista [0][6:10])+"-"+str(lista [0][3:5])),
                                             str(lista [meses][6:10])+"-"+str(lista [meses][3:5]),freq='M')).fillna(0.0)
      dict_recibidos = {'Costos Mes-24': float((recibidos_final[0])/1000),
                        'Costos Mes-23': float((recibidos_final[1])/1000),
                        'Costos Mes-22': float((recibidos_final[2])/1000),
                        'Costos Mes-21': float((recibidos_final[3])/1000),
                        'Costos Mes-20': float((recibidos_final[4])/1000),
                        'Costos Mes-19': float((recibidos_final[5])/1000),
                        'Costos Mes-18': float((recibidos_final[6])/1000),
                        'Costos Mes-17': float((recibidos_final[7])/1000),
                        'Costos Mes-16': float((recibidos_final[8])/1000),
                        'Costos Mes-15': float((recibidos_final[9])/1000),
                        'Costos Mes-14': float((recibidos_final[10])/1000),
                        'Costos Mes-13': float((recibidos_final[11])/1000),
                        'Costos Mes-12': float((recibidos_final[12])/1000),
                        'Costos Mes-11': float((recibidos_final[13])/1000),
                        'Costos Mes-10': float((recibidos_final[14])/1000),
                        'Costos Mes-9': float((recibidos_final[15])/1000),
                        'Costos Mes-8': float((recibidos_final[16])/1000),
                        'Costos Mes-7': float((recibidos_final[17])/1000),
                        'Costos Mes-6': float((recibidos_final[18])/1000),
                        'Costos Mes-5': float((recibidos_final[19])/1000),
                        'Costos Mes-4': float((recibidos_final[20])/1000),
                        'Costos Mes-3': float((recibidos_final[21])/1000),
                        'Costos Mes-2': float((recibidos_final[22])/1000),
                        'Costos Mes-1': float((recibidos_final[23])/1000)}

   driver.close()
   driver.switch_to.window(driver.window_handles[0])
   driver.close()
   elapsed_time = time.time() - start_time
   #print ('tiempo:', str(datetime.timedelta(seconds = elapsed_time)).partition('.')[0])


   
   return render_template('afipresult.html', emitidos = dict_emitidos, recibidos = dict_recibidos)

@app.route('/afipairtableresult/', methods=["GET", "POST"])
@login_required
def afipairtableresult():
   
   #base_key = 'appHJKYgvmLkpv022'
   #AIRTABLE_API_KEY = 'keyUKuYTCi8eUeHk6'

   #table_name = 'Scoring'
   #airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
   #insertar id de la tabla
   #id = '36'
   #record = dict_emitidos
   #airtable.update_by_field('Id', id, record)

   #table_name = 'Scoring'
   #airtable = Airtable(base_key, table_name, api_key = AIRTABLE_API_KEY)
   #insertar id de la tabla
   #id = '36'
   #record = dict_recibidos
   #airtable.update_by_field('Id', id, record)

   return render_template('afipairtableresult.html')

if __name__ == '__main__':
    app.run(debug=True)
