import mlflow
import os

os.environ['DATABRICKS_TOKEN'] = 'dapi5f79cde79ef829ae84e3a0ce388cb40c'

model_name = f"netflix.rag_chatbot.netflix_chatbot_model"
model_version = "1"


mlflow.set_tracking_uri("databricks") 
mlflow.set_registry_uri("databricks-uc")

model_uri = mlflow.get_tracking_uri()

client = mlflow.tracking.MlflowClient(model_uri)

model_details = client.get_registered_model(model_name)
model_version_details = client.get_model_version(model_details.name, model_version)

loaded_model = mlflow.pyfunc.load_model(model_version_details.source)

prediction = loaded_model.predict({"query": "Do you know The Summer I Turned Pretty"})
print(prediction)

