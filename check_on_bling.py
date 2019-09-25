# -*- coding: utf-8 -*-
import requests, json, datetime
import user_inf.bling_automation as b_inf
from calendar import monthrange

class Request_Bling:
    def __init__(self):
        self.apikey = b_inf.blinKey()
        self.url = "https://bling.com.br/Api/v2"

    def get_orders_of_this_month(self,idsituacao=15):
        now = datetime.datetime.now()
        past = now - datetime.timedelta(weeks=2)
        return self.get_orders_of_month( past.month, past.year, idsituacao, now.month, now.year )

    def get_orders_of_month(self, month_start=1, year_start=2019, idsituacao=15, month_finish=False,year_finish=False):
        month_finish = month_start if month_finish else month_start
        year_finish = year_start if year_finish else year_start

        req_start_date = "01/{}/{}".format(month_start,year_start)
        req_end_date   = "{}/{}/{}".format(monthrange(year_finish,month_finish)[1],month_finish,year_finish)
        req_filter = "filters=dataEmissao[{} TO {}]; idSituacao[{}]".format(
            req_start_date, req_end_date, idsituacao)
        return self.get_all_pages("pedidos", req_filter)

    def prepare_url(self, first_param="pedidos", page="1" ):
        return "{}/{}/{}/json/{}".format(
            self.url,
            first_param,
            "page={}".format(str(page)),
            "&apikey={}".format(self.apikey)
        )

    def get_all_pages(self,first_param,req_filter):
        '''
        If(There is nothing or error)  => list []
        If(there is info)              => list [...]
        '''
        other_request, list_, page = True, [], 0
        #print("Request bar:")
        while other_request : 
            response = json.loads(requests.get(self.prepare_url(first_param,page+1),req_filter).content)
            itens = self.itens_in_request(response, first_param)
            if itens :
                print("|",end="",flush=True)
                page += 1
                for iten in itens:
                    list_.append(iten)
            else:
                other_request = False
                print("Request All months Finished")

        return list_

    def itens_in_request(self,response,itens):
        '''
        If (Error or nothing to show) => Bolean False 
        If (something in the list) => List 
        '''
        if( response['retorno'].__contains__('erros') ):
            return False

        list_=[]
        for iten in response['retorno'][itens]:
            list_.append(iten)
        return list_

if __name__ == "__main__":
    rb = Request_Bling()
    resp = rb.get_orders_of_this_month()
    print(len(resp))
    print("-------")
    ids = []
    Execute_this_script_="function getElementByXpath(path){return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;}"
    for item in resp:
        try:
            item['pedido']['itens']
            print('Tem Produtos')
        except:
            print('Não tem Produtos - Organizar pedido Nº ' + item['pedido']['numero'])
            Execute_this_script_ = Execute_this_script_  + '''
            getElementByXpath('//tr[@numerovenda="{numero_pedido}"]/td/input[@type="checkbox"]').click();
            '''.format( numero_pedido = item['pedido']['numero'])
            ids.append(item['pedido']['numero'])
    Execute_this_script_ = Execute_this_script_  + '''getElementByXpath('//*[@id="div_side_acoes"]/div/ul/li[a="Excluir selecionados"]/a').click();'''
