
from models.output_schema import OutputSchema
from api.omie_api import fetch_contas_pagar
from tools.listar_contas_pagar import listar_contas_pagar
from tools.resumo_financeiro import resumo_financeiro
from tools.listar_clientes import listar_clientes
from agents.decision_agent import run_agent
from dotenv import load_dotenv, find_dotenv
from chain import GenerativeUIState, StateGraph, create_graph
from state import ChatInputType
from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Literal
import logging

logging.basicConfig(level=logging.INFO) 

def main():
    # Initialize the Decision Agent
    print("Welcome to the Financial Assistant! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Ending the conversation. Goodbye!")
            break
        
        # Run the agent with the user input
        agent_response = run_agent({'input': user_input})
        
        # Print the agent's response
        print(f"Agent: {agent_response}")

if __name__ == "__main__":
    main()


#def main():
    # Initialize the Decision Agent
    #agent = run_agent({'input': 'Quais as variaveis da Listar contas a pagar? Faca uma chamada filtre das datas 10/11/2023 ate 12/12/2023, retorne os dados e faca sua analise financeira'})
   # print(agent)
    
#resposta = run_agent({'input': 'Faca uma chamada para a API e com os default fields e retorne os dados'})
#print(resposta)


#if __name__ == "__main__":
   #HeHell main()