import utils.func_utils as util
import file_walker as fw
import master_dict_load as mdl
from utils.func_utils import REGEX

if __name__ == '__main__':

    csv = 'utils/Loughran-McDonald_MasterDictionary_1993-2021.csv'
    dict_mcdonald = mdl.load_dictionary(csv)

    for f in fw.walk("baixados"):
        for f2 in fw.walk(f.full_path):
            for f3 in fw.walk(f2.full_path):
                for f4 in fw.walk(f3.full_path):
                    if f4.name == "filing-details":

                        txt_limpo = util.limpa_texto(f4.full_path)
                        lista_item = util.lista_item(txt_limpo, REGEX)
                        lista_conteudo = util.lista_conteudo(txt_limpo, REGEX)

                        for l_i, l_c in zip(lista_item, lista_conteudo):

                            l_indicador = util.indicador_leitura(l_c)
                            l_qtd = util.qtd_sentimento(l_c, dict_mcdonald)
                            resultado = util.linha_formatada(f.name, f3.name, l_i, l_qtd, l_indicador)

                            print(resultado)

                            with open('coleta/coleta.csv', 'a') as fp:
                                fp.write(resultado+'\n')



