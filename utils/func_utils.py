import file_walker as fw
from pathlib import Path
import pandas as pd
import glob
import os
import re
import textstat
import pysentiment2 as sent
import master_dict_load as mdl


# constantes
REGEX = re.compile('\n *Item.*\d\.\d\d.*\n\n?|\n *ITEM.*\d\.\d\d.*\n\n?')


# funcoes para coletar e separa os items de dentro do html


def limpa_texto(html):
    txt = open(html, "r", encoding='utf-8', errors="ignore").read()
    txt = re.sub('SIGNATURE[\s\S]*', ' ', txt)
    txt = re.sub('\.jpg[\s\S]*', ' ', txt)
    txt = re.sub('[\s\S]*</HEAD>', ' ', txt)
    txt = re.sub("'", ' ', txt)
    txt = re.sub('"', ' ', txt)
    txt = re.sub('<[^>]*>', '\n', txt)
    txt = re.sub('&#\d{1,4};|&#\w{1,4};|&\w{1,4};|&#160;|&nbsp;|\\xa0|\\w\d{1,3}\w', ' ', txt)
    txt = re.sub(' +', ' ', txt)
    txt = re.sub(';', ',', txt)

    txt = re.sub('\n\n *Item\n', '\n\nItem ', txt)
    txt = re.sub('\n\n *ITEM\n', '\n\nITEM ', txt)

    return txt

def lista_item(clean_txt, regex):
    list_item = re.findall(regex, clean_txt)
    list_item = [re.sub('\n+', ' ', li) for li in list_item]
    list_item = [re.sub('\.$|\. |\t+| +', ' ', li) for li in list_item]
    list_item = [re.sub(',', ' ', li) for li in list_item]
    list_item = [re.sub('\.', '-', li) for li in list_item]

    list_item = [li.strip() for li in list_item]

    return list_item

def lista_conteudo(clean_txt, regex):
    lista_conteudo = re.split(regex, clean_txt)
    lista_conteudo = lista_conteudo[1:]
    lista_conteudo = [re.sub('\n+', ' ', lc) for lc in lista_conteudo]
    lista_conteudo = [re.sub('\t+| +', ' ', lc) for lc in lista_conteudo]

    return lista_conteudo



# calculo de indicadores
def conteudo_limpo(conteudo, tipo):
    if tipo == "contagem":
        _conteudo_limpo = re.sub('\$|\([\d\w]{1,4}\)|\d|<.*>|[,;]|-', ' ', conteudo)
        _conteudo_limpo = re.sub('\([\w\d]{1,5}\)|[\.<>\\\/,;?(){}*&¨#@!=_\-+:|]|\d|No', ' ', _conteudo_limpo)
        _conteudo_limpo = re.sub(' +', ' ', _conteudo_limpo)

        return _conteudo_limpo

    elif tipo == "leitura":
        _conteudo_limpo = re.sub('\$|\([\d\w]{1,4}\)|\d|<.*>|[,;]|-', ' ', conteudo)
        _conteudo_limpo = re.sub('\([\w\d]{1,5}\)|[<>\\\/,;?(){}*&¨%$#@!=_\-+:|º]|\d|No|(\w\. *){1,5}', ' ', _conteudo_limpo)
        _conteudo_limpo = re.sub('^ *\.', '', _conteudo_limpo)
        _conteudo_limpo = re.sub('( *\. *)+', '. ', _conteudo_limpo)
        _conteudo_limpo = re.sub(' +', ' ', _conteudo_limpo)

        return _conteudo_limpo


def qtd_sentimento(conteudo, dict):
    l_neg = [word.lower() for word in dict['negative']]
    l_pos = [word.lower() for word in dict['positive']]
    l_unc = [word.lower() for word in dict['uncertainty']]
    l_lit = [word.lower() for word in dict['litigious']]
    l_strong = [word.lower() for word in dict['strong_modal']]
    l_weak = [word.lower() for word in dict['weak_modal']]
    l_const = [word.lower() for word in dict['constraining']]

    conteudo_limpo_cont = conteudo_limpo(conteudo, "contagem")
    l_conteudo = conteudo_limpo_cont.split(' ')

    qtd_neg = len([word.lower()  for word in l_conteudo if word in l_neg])
    qtd_pos = len([word.lower()  for word in l_conteudo if word in l_pos])
    qtd_unc = len([word.lower()  for word in l_conteudo if word in l_unc])
    qtd_lit = len([word.lower()  for word in l_conteudo if word in l_lit])
    qtd_strong = len([word.lower()  for word in l_conteudo if word in l_strong])
    qtd_weak = len([word.lower()  for word in l_conteudo if word in l_weak])
    qtd_const = len([word.lower()  for word in l_conteudo if word in l_const])
    qtd_signo = len(re.findall('\$|%', conteudo))
    qtd_conteudo = len(conteudo_limpo_cont)

    return [qtd_neg, qtd_pos, qtd_unc, qtd_lit, qtd_strong, qtd_weak, qtd_const, qtd_signo, qtd_conteudo]


def indicador_leitura(conteudo):

    conteudo_limpo_leitura = conteudo_limpo(conteudo, "leitura")
    try:
        i_1 = round(textstat.flesch_kincaid_grade(conteudo_limpo_leitura), 1)
        i_2 = round(textstat.smog_index(conteudo_limpo_leitura), 1)
        i_3 = round(textstat.coleman_liau_index(conteudo_limpo_leitura), 1)
        i_4 = round(textstat.automated_readability_index(conteudo_limpo_leitura), 1)
        i_5 = round(textstat.dale_chall_readability_score(conteudo_limpo_leitura), 1)
        i_6 = round(textstat.difficult_words(conteudo_limpo_leitura), 1)
        i_7 = round(textstat.linsear_write_formula(conteudo_limpo_leitura), 1)
        i_8 = round(textstat.gunning_fog(conteudo_limpo_leitura), 1)
        i_9 = round(textstat.fernandez_huerta(conteudo_limpo_leitura), 1)
        i_10 = round(textstat.szigriszt_pazos(conteudo_limpo_leitura), 1)
        i_11 = round(textstat.gutierrez_polini(conteudo_limpo_leitura), 1)
        i_12 = round(textstat.crawford(conteudo_limpo_leitura), 1)
        i_13 = round(textstat.osman(conteudo_limpo_leitura), 1)
        i_14 = round(textstat.gulpease_index(conteudo_limpo_leitura), 1)
    except:
        i_1 = i_2 = i_3 = i_4 = i_5 = i_6 = i_7 = i_8 = i_9 = i_11 = i_12 = i_13 = i_14 = 0

    return [i_1, i_2, i_3, i_4, i_5, i_6, i_7, i_8, i_9, i_10, i_11, i_12, i_13, i_14]



# limpeza linha final para exportacao

def linha_formatada(empresa, doc, conteudo, lista_qtd, lista_indicador):
    """ NOTA - a ordem das variaveis salvas e:
    empresa; 8k; item; qtd_neg; qtd_pos; qtd_unc; qtd_lit; qtd_strong; qtd_weak; qtd_const;
    qtd_signo; qtd_conteudo; flesch_kincaid; smog; coleman_liau; automated_readability;
    dale_chall; difficult_words; linsear_write; gunning_fog; fernandez_huerta;
    szigriszt_pazos; gutierrez_polini; crawford; osman; gulpease_index """

    _linha = f'{empresa}; {doc}; {conteudo}; {lista_qtd}; {lista_indicador}'
    _linha = re.sub('\[|]', '', _linha)
    _linha = re.sub(',', ';', _linha)
    _linha = re.sub('\.', ',', _linha)

    return _linha