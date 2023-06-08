# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, jsonify, request
from AIWebService import app, apiconfigd, config, helpers, classification 
from dm_connect import get_product_by_name_or_sku
import openai, json
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

openai.api_key = apiconfigd.API_KEY
@app.route('/api/ChatGPTWebAPITester', methods=['GET', 'POST'])
def chatGPTWebAPITester():
    try:
        if request.method == 'POST':
            prompt = request.form['prompt']
            prompt = helpers.AddEmojiRequestToPrompt(prompt)
            # # completions = openai.Completion.create(
            # #     engine=config.engine,
            # #     prompt=prompt,
            # #     max_tokens=config.max_tokens,
            # #     top_p=config.top_p
            # # )
            # # message = completions.choices[0].text.strip()
            # # message = helpers.remove_extra_emojis(message)
            message = "Dolphin AI Results:"

            ( intent, entities, query) = classification.query_intent(prompt)
            print(query)
            print(prompt.lower())

            print("query: ", query, "intent: ", intent, "entities: ", entities)

            return render_template('ChatGPTWebAPITester.html',
                title='Direct Machines AI Chatbot Tester',
                year=datetime.now().year,
                message='Use /api/ChatGPTWebAPI for actual API calls.',
                response={"Hello": message, "query": query, "intent": intent, "entities": entities})
        else:
            return render_template('ChatGPTWebAPITester.html',
                title='Direct Machines AI Chatbot Tester',
                year=datetime.now().year,
                message='Use /api/ChatGPTWebAPI for actual API calls.')
    
    except openai.error as e:
        # Check if the exception was due to a timeout
        if "timeout" in str(e).lower():
            return jsonify({"message": config.timeOutErrorMessage})
        # For any other OpenAIError
        return jsonify({"message": config.anyOtherExceptionErrorMessage})
    except Exception as e:
        # For any other exception
        return jsonify({"message": config.anyOtherExceptionErrorMessage})

@app.route('/api/ChatGPTWebAPI', methods=['POST'])
def ChatGPTWebAPI():
    try:
        print("ChatGPTWebAPI request.data: ", request.data)
        prompt = json.loads(request.data)['prompt']

        prompt = helpers.AddEmojiRequestToPrompt(prompt)
        completions = openai.Completion.create(
            engine=config.engine,
            prompt=prompt,
            max_tokens=config.max_tokens,
            top_p=config.top_p
        )
        message = completions.choices[0].text.strip()
        message = helpers.remove_extra_emojis(message)
        message=""
        query = classification.query_intent(prompt)
        # if entities == ""
        print("query: ", query)
        return jsonify({"message": message, "query":query})

    except openai.exceptions.OpenAIError as e:
        # Check if the exception was due to a timeout
        if "timeout" in str(e).lower():
            return jsonify({"message": config.timeOutErrorMessage})
        # For any other OpenAIError
        return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})
    except Exception as e:
        # For any other exception
        return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})
    
# from flask import stream_with_context, Response

# @app.route('/api/ChatGPTWebAPI', methods=['POST'])
# def ChatGPTWebAPI():
#     try:
#         print("ChatGPTWebAPI request.data: ", request.data)
#         prompt = json.loads(request.data)['prompt']
        
#         def generate():
#             if "spinnr" in prompt.lower():
#                 yield jsonify({"message": config.spinnrQuestionMessage})
#             elif "spinny" in prompt.lower():
#                 prompt = prompt.replace("spinny", "")
#             prompt = helpers.AddEmojiRequestToPrompt(prompt)
#             completions = openai.Completion.create(
#                 engine=config.engine,
#                 prompt=prompt,
#                 max_tokens=config.max_tokens,
#                 top_p=config.top_p
#             )
#             message = completions.choices[0].text.strip()
#             message = helpers.remove_extra_emojis(message)
#             query = classification.query_intent(prompt)
#             print("query: ", query)
#             yield jsonify({"message": message, "query":query})

#         return Response(stream_with_context(generate()))

#     except openai.exceptions.OpenAIError as e:
#         if "timeout" in str(e).lower():
#             return jsonify({"message": config.timeOutErrorMessage})
#         return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})
#     except Exception as e:
#         return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})

    
@socketio.on('message')
def handle_message(data):
    prompt = data['prompt']
    temperature = config.top_p
    messages = [{"role": "user", "content": prompt}]

    result_dict = classification.query_intent(prompt)
    intent, entities, query = result_dict
    # NOW RUN THE PROMPT:
    print("REsult dict: ", result_dict)
    socketio.emit('response', {"message": f"Intent: {intent},\nEntities: {entities} \nQuery: {query}"}) 
    # response = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=messages,
    #     temperature=temperature,
    #     stream=True  # set stream=True
    # )
    # for chunk in response:
    #     chunk_message = chunk['choices'][0]['delta']  # extract the message
    #     socketio.emit('response', {"message": chunk_message})  # send the chunk message and result_dict to the client


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/query', methods=['POST'])
# def handle_query():
#     data = request.get_json()