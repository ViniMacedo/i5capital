import urllib.error
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import html5lib
from datetime import datetime
import json
import openpyxl
import tabula as tb
import os
from tkinter import filedialog as dlg
from tkinter import *
from urllib.error import HTTPError


def scraping():
    txt_and["text"]="Processo iniciado, por favor aguarde."
    arq_htlm=dlg.askopenfilename()  # usuario escolhe o seu arquivo
    myFile= open(arq_htlm, encoding="utf-8")  # arquivo HTML retirado do safra
    content=myFile.read()
    soup=BeautifulSoup(content, "html.parser")  # fazendo o soup do arquivo


    # Inicio do Scraping
    dados_rf=[]  # lista para armazenar os dados retirados
    dados= soup.findAll("tr",attrs={"ng-repeat": "row in $data"})  #pegando todas tabelas da página que possuem esse att
    for dado in dados:  # Para cada tabela pegando linha por linha
        children= dado.findChildren("td", recursive=False)  # Pegando em cada linha os dados de interesse
        emissor=children[2].text.split(sep="\n")[1].strip()  # Emissor
        app_min=children[3].text.strip()  # Aplicacao min
        resgate=children[4].text.strip()  # resgate
        rent_mes=children[5].text.strip()  # rent mes
        rent_ano=children[6].text.strip()  # rent ano
        rent_dozemeses=children[7].text.strip()  # rent 12 meses
        taxa_adm=children[8].text.strip()  # taxa de adm
        pdf=dado.find("a")  # pegando o link do PDF
        pdf=pdf["href"]
        print(pdf)
        txt_and["text"] = pdf
        simple_path="tabula-RPB.json"  # pegando o arquivo de template
        abs_path=os.path.abspath(simple_path)
        try:
            table = tb.read_pdf_with_template(pdf, "tabula-RPB (1).json")
            if len(table) >= 1:
                tabela = table[0]
                cnpj = tabela.columns[0]
                cnpj = cnpj.split(" - ")
                cnpj = cnpj[1]
                tabela1 = table[1]
                if len(tabela1.columns) == 1:
                    categoria = tabela1.iat[0, 0]
                    categoria = categoria.split("ANBIMA ")
                    categoria = categoria[1]
                else:
                    categoria = tabela1.iat[0, 1]

                tabela2 = table[2]
                if len(tabela2.index) > 4:
                    vol_in = tabela2.iat[1, 4]
                    print(vol_in)
                    vol_dozemeses = tabela2.iat[2, 4]
                    print(vol_dozemeses)
                    vol_vintequatromeses = tabela2.iat[3, 4]
                    print(vol_vintequatromeses)
                    vol_trintaseismeses = tabela2.iat[4, 4]
                    print(vol_trintaseismeses)
                    dados_rf.append(
                        [emissor, cnpj, categoria, app_min, resgate, rent_mes, rent_ano, rent_dozemeses, taxa_adm,
                         vol_in, vol_dozemeses, vol_vintequatromeses, vol_trintaseismeses, pdf])
                else:
                    vol_in = tabela2.iat[0, 4]
                    print(vol_in)
                    vol_dozemeses = tabela2.iat[1, 4]
                    print(vol_dozemeses)
                    vol_vintequatromeses = tabela2.iat[2, 4]
                    print(vol_vintequatromeses)
                    vol_trintaseismeses = tabela2.iat[3, 4]
                    print(vol_trintaseismeses)
                    dados_rf.append(
                        [emissor, cnpj, categoria, app_min, resgate, rent_mes, rent_ano, rent_dozemeses, taxa_adm,
                         vol_in,
                         vol_dozemeses, vol_vintequatromeses, vol_trintaseismeses, pdf])

        except urllib.error.HTTPError:
            print("Não foi possível localizar o pdf!")
            cnpj = 'Sem PDF'
            categoria = 'Sem PDF'
            vol_in = 'Sem PDF'
            vol_dozemeses = 'Sem PDF'
            vol_vintequatromeses = 'Sem PDF'
            vol_trintaseismeses = 'Sem PDF'
            dados_rf.append(
                [emissor, cnpj, categoria, app_min, resgate, rent_mes, rent_ano, rent_dozemeses, taxa_adm, vol_in,
                 vol_dozemeses, vol_vintequatromeses, vol_trintaseismeses, pdf])
            pass
        except:
            print("desculpe ocorreu um erro inesperado!")
            vol_in = 'Erro'
            vol_dozemeses = 'Erro'
            vol_vintequatromeses = 'Erro'
            vol_trintaseismeses = 'Erro'
            cnpj = "Erro"
            categoria = "Erro"
            dados_rf.append(
                [emissor,cnpj,categoria, app_min, resgate, rent_mes, rent_ano, rent_dozemeses, taxa_adm, vol_in, vol_dozemeses,
                 vol_vintequatromeses, vol_trintaseismeses,pdf])
            pass

    # TRATAMENTO DE DADOS
    # 1 transformamos a lista em um dataframe com as colunas esperadas
    transformer=pd.DataFrame(dados_rf,columns=["Fundo","CNPJ","Categoria","Aplicação Mínima (R$)","Resgate (liquidação)","Rent.mês","Rent.ano",
                                               "Rent. 12 meses","Taxa de ADM (a.a)", "Vol.Início", "Vol. 12 meses", "Vol. 24 meses", "Vol.36 meses","PDF"])
    print(transformer)
    nome_arq=arq.get()
    transformer.to_excel(nome_arq+".xlsx", index=False)  # tornando tudo em um excel

    txt_and["text"] = "Processo finalizado, você já pode fechar o programa."



modal=Tk()
modal.title("Automação Fundos de Investimentos")


txt_excel=Label(modal,text="Primeiro escolha o nome para a pasta excel que será gerada: ")
txt_excel.grid(column=0,row=0, padx=10, pady=10)

arq=StringVar()
n_arq=Entry(modal,width=20,textvariable=arq)
n_arq.grid(column=0,row=1, padx=10, pady=10)


txt_orient=Label(modal,text="Clique no botão para escolher o arquivo de onde será retirada as informações.")
txt_orient.grid(column=0,row=2, padx=10, pady=10)


bt=Button(modal,text="Executar", command=scraping)
bt.grid(column=0,row=3, padx=10, pady=10)

txt_and=Label(modal,text="")
txt_and.grid(column=0,row=4, padx=10, pady=10)

modal.mainloop()