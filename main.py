from flask import Flask, jsonify, request
from flask_cors import CORS
import mlflow
import os


app = Flask(__name__)
CORS(app)

@app.route("/api/getData", methods=['GET'])
def getData():
    question = request.args.get('question')
    os.environ['DATABRICKS_TOKEN'] = 'dapi5f79cde79ef829ae84e3a0ce388cb40c'

    model_name = f"netflix.rag_chatbot.netflix_chatbot_model"
    model_version = "3"

    mlflow.set_tracking_uri("databricks") 
    mlflow.set_registry_uri("databricks-uc")

    model_uri = mlflow.get_tracking_uri()

    client = mlflow.tracking.MlflowClient(model_uri)

    model_details = client.get_registered_model(model_name)
    model_version_details = client.get_model_version(model_details.name, model_version)

    loaded_model = mlflow.pyfunc.load_model(model_version_details.source)

    prediction = loaded_model.predict({"query": question})
    print(prediction)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)