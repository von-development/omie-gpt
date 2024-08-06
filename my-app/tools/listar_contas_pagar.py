import os
import requests


from langchain.tools import tool
from langchain_core.tools import tool, StructuredTool
from langchain_core.utils.function_calling import convert_to_openai_function

from typing import Optional, Dict, Union, TypedDict, Sequence, Annotated, List
from langchain.pydantic_v1 import BaseModel, Field 


class InputListarContasP(BaseModel):
    """
    Arguments for listar-contas-pagar 

    """
    pagina: int = Field(description='Número da página a ser consultada')
    registros_por_pagina: int = Field(description='Número de registros por página')
    apenas_importado_api: str = Field(description='Apenas registros importados pela API so pode ser S ou N')

    ordenar_por: Optional[str] = Field(description='Ordem de exibição dos dados', example='DATA_PAGAMENTO')
    ordem_descrescente: Optional[str] = Field(description='Exibir em Ordem Crescente ou Decrescente', example='S')
    filtrar_por_data_de: Optional[str] = Field(description='Data de início do filtro', example='dd/mm/aaaa')
    filtrar_por_data_ate: Optional[str] = Field(description='Data de fim do filtro', example='dd/mm/aaaa')
    filtrar_apenas_inclusao: Optional[str] = Field(description='Filtra os registros exibidos apenas os incluídos', example='S')
    filtrar_apenas_alteracao: Optional[str] = Field(description='Filtra os registros exibidos apenas os alterados', example='S')
    filtrar_por_emissao_de: Optional[str] = Field(description='Data de alteração inicial (Filtrar os registros a partir da data especificada)', example='dd/mm/aaaa')
    filtrar_por_registro_de: Optional[str] = Field(description='Filtra os registros a partir da data especificada', example='dd/mm/aaaa')
    filtrar_por_emissao_ate: Optional[str] = Field(description='Data de alteração final (Filtra os registros até a data especificada)', example='dd/mm/aaaa')
    filtrar_por_registro_ate: Optional[str] = Field(description='Filtra os registros até a data especificada', example='dd/mm/aaaa')
    filtrar_conta_corrente: Optional[int] = Field(description='Filtrar os lançamentos de Contas a Pagar por código da conta corrente')
    filtrar_cliente: Optional[int] = Field(description='Filtrar os lançamentos de Contas a Pagar por código do cliente')
    filtrar_por_cpf_cnpj: Optional[str] = Field(description='Filtrar os títulos por CPF/CNPJ', example='Apenas números')
    filtrar_por_status: Optional[str] = Field(description='Filtrar por status', example='CANCELADO, PAGO, LIQUIDADO, EMABERTO')
    filtrar_por_projeto: Optional[int] = Field(description='Código do Projeto')
    
@tool("listar-contas-pagar", args_schema=InputListarContasP, return_direct=True)
def listar_contas_pagar(
    pagina: int, registros_por_pagina: int, apenas_importado_api: str,
    ordenar_por: str = None, ordem_descrescente: str = None,
    filtrar_por_data_de: str = None, filtrar_por_data_ate: str = None,
    filtrar_apenas_inclusao: str = None, filtrar_apenas_alteracao: str = None,
    filtrar_por_emissao_de: str = None, filtrar_por_registro_de: str = None,
    filtrar_por_emissao_ate: str = None, filtrar_por_registro_ate: str = None,
    filtrar_conta_corrente: int = None, filtrar_cliente: int = None,
    filtrar_por_cpf_cnpj: str = None
) -> Union[Dict, str]:
    """
    Returns the list of accounts payable for a given set of parameters from the Omie API.
        dict: The parsed JSON response from the API.
    """
    # Define the URL and authentication parameters
    url = 'http://app.omie.com.br/api/v1/financas/contapagar/'
    app_key = '3568546098117'
    app_secret = 'd063098e99c6535528c08a26ab77aff2'
    
  

    # Define the parameters for the API request
    params = {
        "call": "ListarContasPagar",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "pagina": pagina,
            "registros_por_pagina": registros_por_pagina,
            "apenas_importado_api": apenas_importado_api,
        }]
    }

    optional_params = {
        "ordenar_por": ordenar_por,
        "ordem_descrescente": ordem_descrescente,
        "filtrar_por_data_de": filtrar_por_data_de,
        "filtrar_por_data_ate": filtrar_por_data_ate,
        "filtrar_apenas_inclusao": filtrar_apenas_inclusao,
        "filtrar_apenas_alteracao": filtrar_apenas_alteracao,
        "filtrar_por_emissao_de": filtrar_por_emissao_de,
        "filtrar_por_registro_de": filtrar_por_registro_de,
        "filtrar_por_emissao_ate": filtrar_por_emissao_ate,
        "filtrar_por_registro_ate": filtrar_por_registro_ate,
        "filtrar_conta_corrente": filtrar_conta_corrente,
        "filtrar_cliente": filtrar_cliente,
        "filtrar_por_cpf_cnpj": filtrar_por_cpf_cnpj
    }

    for key, value in optional_params.items():
        if value is not None:
            params["param"][0][key] = value

    # Send the request and print the response
    response = requests.post(url, json=params)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        # Raise an exception if the request failed
        raise Exception(f'Request to API {url} failed: {response.status_code}')
    
