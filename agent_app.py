from flask import Flask, request, jsonify
from structured_tools import agent_executor
from cite_recognition_chain import cite_chain

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()  # Get JSON data from POST request
    if not data or 'query_string' not in data:
        return jsonify({'error': 'Invalid request. Please provide a "query_string" in the JSON data.'}), 400

    # Process the query string
    query_string = data['query_string']
    print(query_string)
    # For demonstration, let's just return a JSON object with the original query string
    source:dict = agent_executor.invoke(
            {
            "input": query_string,
            "chat_history": []
        }
    )
    source_output:str = source['output']
    
    end_token = "</s>"
    
    if end_token in source_output:
       source_output = source_output.replace("</s>", "")
    
    # if "False" in source_output:
    #     is_fact_true:bool = False
    # else:
    #     is_fact_true = True
    
    try:
        
        verfiy_citation = cite_chain.invoke(source_output)
        
        verfiy_citation = verfiy_citation.content.strip().lower()
        
        if verfiy_citation  == "yes" or verfiy_citation =="no":
            pass
        else:
            verfiy_citation = "IDK"
            
            
        result = {'query_string':source_output, "is_fact_true":verfiy_citation}

    except:
        
        if "False" in source_output:
            is_fact_true:bool = False
        else:
            is_fact_true = True
    
    finally:

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
