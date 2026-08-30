# Question 4: Capstone Reproducibility Drill

This repository demonstrates end-to-end reproducibility using MLflow and DVC as part of the DA3408 Assignment 1 Capstone.


### 1. Initialize the Repository
```bash
git init
dvc init
```

### 2. Generate and Version the Dataset
```bash
python generate_data.py
dvc remote add -d myremote s3://aseel-da3408-dvc-820298843056-eu-north-1-an/q4-data
dvc add dataset.csv
```

### 3. Commit to Git & Push to S3
```bash
git add dataset.csv.dvc .dvc/config environment.yml generate_data.py train.py README.md
git commit -m "Initial commit for Q4"
dvc push
```

### 4. Train the Model
Extract the Git commit hash and DVC dataset hash using shell commands, and pass them as environment variables to the training script:
```bash
export GIT_COMMIT=$(git rev-parse HEAD)
export DVC_HASH=$(grep md5 dataset.csv.dvc | head -n 1 | awk '{print $2}')
python train.py
```
*(This logs the metrics, seed, Git commit hash, and DVC artifact hash to MLflow).*

### 5. Transition to Staging
1. Start the MLflow UI on a new port: `mlflow ui --backend-store-uri sqlite:///q4_mlflow.db --port 5001`
2. Open `http://127.0.0.1:5001` in your browser.
3. Click the **Models** tab at the top.
4. Click on **Capstone_Final_Model**, click its latest version, and change its stage to **Staging**.
5. Push your final code changes to GitHub.

---

## Phase 2: Partner B Reproduction

### 1. Clone the Code
```bash
git clone <partner_a_github_url>
cd <repo_folder>
git checkout <partner_a_commit_hash>
```

### 2. Export S3 Credentials

```bash
export AWS_ACCESS_KEY_ID="<provided_by_partner_a>"
export AWS_SECRET_ACCESS_KEY="<provided_by_partner_a>"
export AWS_DEFAULT_REGION="eu-north-1"
```

### 3. Pull the Data via DVC
```bash
dvc checkout
```
*(This pulls `dataset.csv` from S3 based on the hash in `dataset.csv.dvc`)*

### 4. Create the Environment
```bash
conda env create -f environment.yml
conda activate da13
```


### 5. Reproduce the Run
```bash
export GIT_COMMIT=$(git rev-parse HEAD)
export DVC_HASH=$(grep md5 dataset.csv.dvc | head -n 1 | awk '{print $2}')
python train.py
```

### 6. Verify and Log
```bash 
mlflow ui --backend-store-uri sqlite:///q4_mlflow.db --port 5001```

