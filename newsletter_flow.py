import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
api_key = os.getenv("LANGFLOW_API_KEY")
url = "https://lang.kondhost.com/api/v1/run/fd16a9c3-9a1f-49be-a2be-a9343a79d07c"  # The complete API endpoint URL for this flow
#import pdb; pdb.set_trace()

def call_langflow(flow_subject, flow_url):
	# Request payload configuration
	payload = {
	    "output_type": "chat",
	    "input_type": "text",
	    "tweaks": {
	        "Prompt-XX1NB": {
	            "template": "Gere uma newsletter com base nas informações dada abaixo. \
			Use um texto fluido, e nao inclua titulos ou texto conversacionais, somente a newsletter pronta. \
			Faça o texto com tags htmls somente no texto. \
			Não inclua caracteres de codigo como ``` ou tags como html, header, body, etc. \
			Texto com tags de forma direta, ex. <h1>Tudo sobre etc</h1>. \
			\n\nConteúdo de referência: {references} \
			\n\n---\n\nTema, em poucas palavras: {theme}\n\n---\n\nNewsletter",
	            "tool_placeholder": ""
	        },
	        "TextInput-dgofj": {
	            "input_value": "Assunto qualquer."
	        },
	        "ChatOutput-YOs2U": {
	            "data_template": "{text}",
	            "sender": "Machine",
	            "sender_name": "AI",
	            "session_id": "",
	            "should_store_message": True
	        },
	        "ParserComponent-IqLRA": {
	            "mode": "Parser",
	            "pattern": "Text: {text}",
	            "sep": "\n"
	        },
	        "URLComponent-4i3kh": {
	            "autoset_encoding": True,
	            "check_response_status": False,
	            "continue_on_failure": True,
	            "filter_text_html": True,
	            "format": "Text",
	            "headers": [
	                {
	                    "key": "User-Agent",
	                    "value": "langflow"
	                }
	            ],
	            "max_depth": 1,
	            "prevent_outside": True,
	            "timeout": 30,
	            "urls": [
	                "https://docs.langflow.org/"
	            ],
	            "use_async": True
	        },
	        "GoogleGenerativeAIModel-Aops8": {
	            "api_key": "MY_API_KEY",
	            "max_output_tokens": None,
	            "model_name": "gemini-2.0-flash",
	            "n": None,
	            "stream": False,
	            "temperature": 0.1,
	            "tool_model_enabled": False,
	            "top_k": None,
	            "top_p": None
	        }
	    }
	}
	payload["session_id"] = str(uuid.uuid4())
	payload["tweaks"]["TextInput-dgofj"]["input_value"] = flow_subject
	payload["tweaks"]["URLComponent-4i3kh"]["urls"] = [flow_url]
	payload["tweaks"]["GoogleGenerativeAIModel-Aops8"]["api_key"] = google_api_key

	headers = {"x-api-key": api_key}

	try:
	    # Send API request
	    response = requests.request("POST", url, json=payload, headers=headers)
	    response.raise_for_status()  # Raise exception for bad status codes

	    # Print response
	    #print(response.text)
	    #import pdb; pdb.set_trace()
	    #return response.text

	    data = response.json()
	    texto = data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
	    return texto
	    #return response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]

	except requests.exceptions.RequestException as e:
	    return f"Error making API request: {e}"
	except ValueError as e:
	    return f"Error parsing response: {e}"
