import spacy
nlp = spacy.load("en_core_web_sm")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


import pandas as pd
from sklearn.model_selection import train_test_split


def extract_entities(text):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_] = ent.text
    return entities


def generate_query(intent, entities):
    intent = intent.lower()
    if intent == "events":
        location = entities.get("GPE")
        query = f"SELECT * FROM events WHERE location = '{location}'"
    elif intent == "people":
        interests = entities.get("INTERESTS")
        query = f"SELECT * FROM people WHERE interests = '{interests}'"
    else:
        query = ""
    return query


# TIME FOR SOME DATA TRAINING   
data = pd.read_csv("intent_data.csv")
X_train, X_test, y_train, y_test = train_test_split(data["sentence"], data["intent"], test_size=0.2, random_state=42, stratify=data["intent"])
print(X_train)


pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

def predict_intent(text):
    return pipeline.predict([text])[0]



# # NOW LETS RUN THE MODEL FOR INTENTS
# sentence = "Is anything happening on May 5th in Harrisburg?"
# intent = predict_intent(sentence)
# print(f"Predicted intent: {intent}")

# # NEXT, IDENTIFY THE ENTITIES
# entities = extract_entities(sentence)
# print(f"Entities: {entities}")



def query_intent(text):
    # text = request.json.get('text')
    intent = predict_intent(text) # Can be done with the NLP cloud API
    entities = extract_entities(text)
    query = generate_query(intent, entities)
    # results = execute_query(query)
    return query

# Note: GPE is geopolitical entity

# print(query_intent("    "Find people who like hiking and camping"))