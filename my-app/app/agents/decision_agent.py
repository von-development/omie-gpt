from tools.listar_contas_pagar import listar_contas_pagar
from tools.resumo_financeiro import resumo_financeiro
from langchain.pydantic_v1 import BaseModel
#from state import DecisionAgentState


from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.utils.function_calling import format_tool_to_openai_function

from langchain.schema.agent import AgentFinish
from langchain.agents.format_scratchpad import format_to_openai_functions

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv, find_dotenv 
from langchain_core.tools import tool




_ = load_dotenv(find_dotenv())




tools = [listar_contas_pagar, resumo_financeiro]


prompt = ChatPromptTemplate.from_messages([
    ('system', """
    I am a helpful assistant that can make API calls to Omie. I have three main capabilities: **listar_contas_pagar**, **resumo_financeiro**, and **listar_clientes**.

    For **listar_contas_pagar**, the parameters below are REQUIRED every time you call the API:
    - **pagina**: 1
    - **registros_por_pagina**: 40
    - **apenas_importado_api**: N


    However, I can also provide a financial summary for a specific day with **resumo_financeiro**. For this, you need to provide the exact date in the format **dd/mm/yyyy**.

    For all tools, I have the capability to add filters depending on the user's input. If you provide additional parameters, I can add them to the API call to filter the results. For example, you can specify a date range, a specific client, or a particular account type, and more.

    If the API call returns multiple pages of results, I will notify you and ask if you would like to filter the results further or proceed to the next page. This way, you can refine your search and avoid having to navigate through multiple pages of results.

    What would you like to do? Provide the parameters for the API call, and I'll take care of the rest!

    Language: If prompted in Portuguese, respond in Portuguese.
    """
     ),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad'),

    ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_functions(x["intermediate_steps"]),
            
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools)

pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
)
