from typing import Optional, Dict, Union, TypedDict, Sequence, Annotated
import requests
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool, StructuredTool
import json


class InputResumoFinanceiro(BaseModel):
    """
    Arguments for the get_financial_summary tool. 
    """
    dDia: str = Field(description='The day for which to get the financial summary', examples=['dd/mm/aaaa'])
    lApenasResumo: bool = Field(description='Whether to get only the summary', example=True)

@tool("resumo-financas", args_schema=InputResumoFinanceiro, return_direct=False)
def resumo_financeiro(dDia: str, lApenasResumo: bool) -> Union[Dict, str]:
    '''
    Returns the list of accounts payable for a given day from the Omie API.
        dict: The parsed JSON response from the API.
    '''
    # Define the URL and authentication parameters
    url = 'https://app.omie.com.br/api/v1/financas/resumo/'
    app_key = '3568546098117'
    app_secret = 'd063098e99c6535528c08a26ab77aff2'

    # Define the parameters for the API request
    params = {
        "call": "ObterResumoFinancas",
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [{
            "dDia": dDia,
            "lApenasResumo": lApenasResumo
        }]
    }

    # Send the request and print the response
    response = requests.post(url, json=params)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Raise an exception if the request failed
        raise Exception(f'Request to API {url} failed: {response.status_code}')