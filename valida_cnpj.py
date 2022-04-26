import re
import requests 
import time
import csv
import pandas as pd
import os
import datetime


def consultaReceita():
  CNPJ = input('Digite um CNPJ:')
  CNPJ = re.sub('[0-9]', '', CNPJ)

  URL = ('https://www.receitaws.com.br/v1/cnpj/' + CNPJ)

  r = requests.get(url = URL)
  data = r.json()
  status = data['status']
  f = open("RelCNPJ.txt", "a")
  if status == 'OK':
    situacao = data['situacao']
    if situacao == 'ATIVA':
      print('A situação do CNPJ '+CNPJ+' é '+ str(situacao))      
    else:
      f.write('\n A situação do CNPJ '+CNPJ+' é '+ str(situacao))
  elif status == 'ERROR':
    mensagem = data['message']
    if (len(mensagem) > 20):
      f.write('\n'+CNPJ+ ' CNPJ Rejeitado pela Receita')
    else:
      f.write('\n'+CNPJ+ ' CNPJ Inválido')    
  f.close()



#consultaReceita()

def geraCsv(filename):
    df = pd.read_excel(filename, sheet_name=None)
    for key, value in df.items():
        return df[key].to_csv('%s.csv' % key)


def valida_base_cnpj(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        csv_list = list(reader)
        for cnpj in csv_list:     
            #entre [] deve ser informado o indice da coluna que contém o numero de CNPJ no arquivo .csv
            CNPJ = re.sub('[^0-9]+', '', str(cnpj[1]))

            if (len(CNPJ) > 5):
                #tempo 21 segundos mínimo entre cada pesquisa para manter a regra de plano gratuito da plataforma
                time.sleep(21)
                print(datetime.datetime.now())
                URL = ('https://www.receitaws.com.br/v1/cnpj/' + CNPJ)
                r = requests.get(url = URL)
                data = r.json()
                status = data['status']
                f = open("RelCNPJ.txt", "a")
                if status == 'OK':
                    situacao = data['situacao']
                    if situacao == 'ATIVA':
                        print('A situação do CNPJ '+CNPJ+' é '+ str(situacao))                        
                    else:
                        f.write('\n A situação do CNPJ '+CNPJ+' é '+ str(situacao))
                        print('A situação do CNPJ '+CNPJ+' é '+ str(situacao))
                elif status == 'ERROR':
                    mensagem = data['message']
                if (len(mensagem) > 20):
                    f.write('\n'+CNPJ+ ' CNPJ Rejeitado pela Receita')
                    print('A situação do CNPJ '+CNPJ+' é '+ str(situacao))
                else:
                    f.write('\n'+CNPJ+ ' CNPJ Inválido')
                    print('A situação do CNPJ '+CNPJ+' é '+ str(situacao))                
                f.close()


geraCsv('contratantes.xlsx')            
valida_base_cnpj('Exportar Planilha.csv')
