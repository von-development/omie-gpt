from typing import Optional, Dict, Union, TypedDict, Sequence, Annotated
import requests
from langchain.pydantic_v1 import BaseModel, Field, BaseTool
from langchain_core.tools import tool, StructuredTool
import os
import requests
from langchain.tools import BaseTool

class ClientesFiltro(BaseTool):
    codigo_cliente_omie: Optional[int] = Field(None, description='Código de Cliente / Fornecedor', example=12345)
    codigo_cliente_integracao: Optional[str] = Field(None, description='Código de Integração com sistemas legados', example='INT-123')
    cnpj_cpf: Optional[str] = Field(None, description='CNPJ / CPF', example='12345678901234')
    nome_fantasia: Optional[str] = Field(None, description='Nome Fantasia', example='XYZ Ltda')
    razao_social: Optional[str] = Field(None, description='Razão Social', example='Empresa XYZ')
    endereco: Optional[str] = Field(None, description='Endereço', example='Rua ABC, 123')
    bairro: Optional[str] = Field(None, description='Bairro', example='Centro')
    cidade: Optional[str] = Field(None, description='Código da Cidade', example='12345')
    estado: Optional[str] = Field(None, description='Sigla do Estado', example='SP')
    cep: Optional[str] = Field(None, description='CEP', example='12345-678')
    contato: Optional[str] = Field(None, description='Nome para contato', example='João Silva')
    email: Optional[str] = Field(None, description='E-Mail', example='contato@empresa.com')

class InputListarClientes(BaseTool):
    pagina: int = Field(default=1, description='Número da página a ser consultada')
    registros_por_pagina: int = Field(default=40, description='Número de registros por página')
    apenas_importado_api: str = Field(default="N", description='Apenas registros importados pela API (S ou N)')
    clientesFiltro: Optional[ClientesFiltro] = Field(None, description='Filtros opcionais para a listagem de clientes')

@tool("listar_clientes", args_schema=InputListarClientes, return_direct=True)
def listar_clientes(input: InputListarClientes) -> Union[Dict, str]:
    """
    Returns the list of clients for a given set of parameters from the Omie API.
    """
    # Define the URL and authentication parameters
    url = 'https://app.omie.com.br/api/v1/geral/clientes/'
    app_key = '3568546098117'
    app_secret = 'd063098e99c6535528c08a26ab77aff2'

    # Define the parameters for the API request
    params = {
        "call": "ListarClientes",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "pagina": pagina,
            "registros_por_pagina": registros_por_pagina,
            "apenas_importado_api": apenas_importado_api,
            "clientesFiltro": clientesFiltro.dict(exclude_unset=True) if clientesFiltro else {}
        }]
    }

    # Send the request and print the response
    response = requests.post(url, json=params)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        # Raise an exception if the request failed
        raise Exception(f'Request to API {url} failed: {response.status_code}')

# Exemplo de chamada de função para testar o código:

# Chamada sem filtro
try:
    input_data = InputListarClientes()
    resultado_sem_filtro = listar_clientes(input_data)
    print("Resultado sem filtro:", resultado_sem_filtro)
except Exception as e:
    print(e)

# Chamada com filtro por razão social "Renan"
try:
    filtro = ClientesFiltro(razao_social="Renan")
    input_data = InputListarClientes(clientesFiltro=filtro)
    resultado_com_filtro = listar_clientes(input_data)
    print("Resultado com filtro:", resultado_com_filtro)
except Exception as e:
    print(e)
