import pandas as pd
from sklearn.datasets import make_classification
import os

def create_dataset(filename="dataset.csv"):
    print("Generating simulated dataset...")
    X, y = make_classification(
        n_samples=2000, 
        n_features=20, 
        n_informative=15, 
        n_classes=2, 
        random_state=42
    )
    
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(20)])
    df['target'] = y
    
    df.to_csv(filename, index=False)
    print(f"Successfully generated {filename} with {len(df)} rows.")

if __name__ == "__main__":
    create_dataset()
