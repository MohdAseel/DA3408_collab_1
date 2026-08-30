import pandas as pd
import numpy as np
import random
import time
import os
import warnings
import logging
import mlflow
import mlflow.sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")
logging.getLogger("mlflow").setLevel(logging.ERROR)

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

def train():
    mlflow.set_tracking_uri("sqlite:///q4_mlflow.db")
    mlflow.set_experiment("Capstone_Reproducibility_Experiment")
    
    with mlflow.start_run():
        print("Loading dataset from local disk...")
        if not os.path.exists("dataset.csv"):
            raise FileNotFoundError("dataset.csv not found! Did you run `dvc checkout` or `generate_data.py`?")
            
        df = pd.read_csv("dataset.csv")
        X = df.drop(columns=['target'])
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=SEED
        )
        
        print("Training model...")
        mlp = MLPClassifier(hidden_layer_sizes=(30,), max_iter=25, random_state=SEED)
        
        start_time = time.time()
        mlp.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        val_acc = accuracy_score(y_test, mlp.predict(X_test))
        

        mlflow.log_param("seed", SEED)
        mlflow.log_param("git_commit", os.environ.get("GIT_COMMIT", "unknown"))
        mlflow.log_param("dvc_dataset_hash", os.environ.get("DVC_HASH", "unknown"))
        
        mlflow.log_metric("val_accuracy", val_acc)
        mlflow.log_metric("training_time", training_time)
        

        mlflow.sklearn.log_model(
            mlp, 
            "model", 
            registered_model_name="Capstone_Final_Model",
            skops_trusted_types=['sklearn.neural_network._stochastic_optimizers.AdamOptimizer']
        )
        
        print(f"Run completed! Validation Accuracy: {val_acc:.4f}")

if __name__ == "__main__":
    train()
