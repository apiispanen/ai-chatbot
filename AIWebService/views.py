# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, jsonify, request
from AIWebService import app, apiconfig, config, helpers, classification 
import openai, json

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

openai.api_key = apiconfig.API_KEY
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
            # if prompt.lower() == "what is the best manual grinder for metal?":
            #     query = "The best manual grinder for metal is the Timesavers Model MGV Grinder. You can find more information here: https://directmachines.com/timesavers%20model%20mgv%20grinder.html"
            # if prompt.lower() == "how much is a powermatic saw?":
            #     query = "The powermatic 31A belt/disc sander is $2099, learn more here: https://directmachines.com/powermatic-31a-belt-disc-sander-1-5hp-1ph-115-230v.html"
            # if prompt.lower() == "would an ironworker be able to punch metal?":
            #     query = "Yes! Ironworkers would be able to punch metal - try Piranha ironworkers here: https://directmachines.com/ironworkers/piranha-ironworkers.html"

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
        if "spinnr" in prompt.lower():
            return jsonify({"message": config.spinnrQuestionMessage})
        elif "spinny" in prompt.lower():
            prompt = prompt.replace("spinny", "")
        prompt = helpers.AddEmojiRequestToPrompt(prompt)
        completions = openai.Completion.create(
            engine=config.engine,
            prompt=prompt,
            max_tokens=config.max_tokens,
            top_p=config.top_p
        )
        message = completions.choices[0].text.strip()
        message = helpers.remove_extra_emojis(message)
        query = classification.query_intent(prompt)
        print("query: ", query)
        return jsonify({"message": message, "query":query})

    except openai.exceptions.OpenAIError as e:
        # Check if the exception was due to a timeout
        if "timeout" in str(e).lower():
            return jsonify({"message": config.timeOutErrorMessage})
        # For any other OpenAIError
        return jsonify({"message": config.anyOtherExceptionErrorMessage})
    except Exception as e:
        # For any other exception
        return jsonify({"message": config.anyOtherExceptionErrorMessage})

@app.route('/api/VideoIntelligenceAPITester',  methods=['GET', 'POST'])
def VideoIntelligenceAPITester():
    try:
        if request.method == 'POST':
            path = request.form['path']
            content_analysis_dict = helpers.analyze_explicit_content(path)
            return render_template('VideoIntelligenceAPITester.html',
                title='Video Intelligence API Tester',
                year=datetime.now().year,
                message='Use /api/VideoIntelligenceAPI for actual API calls.',
                response=content_analysis_dict)
        else:
            return render_template('VideoIntelligenceAPITester.html',
                title='Video Intelligence API Tester',
                year=datetime.now().year,
                message='Use /api/VideoIntelligenceAPI for actual API calls.')
    except Exception as e:
        # For any other exception
        return jsonify({"message": config.anyOtherExceptionErrorMessage})
    


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/query', methods=['POST'])
# def handle_query():
#     data = request.get_json()