import os
from huggingface_hub import HfApi


HF_TOKEN = os.getenv("HF_TOKEN")
HF_USERNAME = os.getenv("HF_USERNAME")
HF_SPACE_NAME = os.getenv("HF_SPACE_NAME")


REPO_ID = f"{HF_USERNAME}/{HF_SPACE_NAME}"

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing!")

print(f"🚀 Starting upload to {REPO_ID}...")


api = HfApi(token=HF_TOKEN)


api.upload_file(
    path_or_fileobj="models/fcst_model.joblib",
    path_in_repo="models/fcst_model.joblib",
    repo_id=REPO_ID,
    repo_type="space"
)


api.upload_file(
    path_or_fileobj="models/X_future.csv",
    path_in_repo="models/X_future.csv",
    repo_id=REPO_ID,
    repo_type="space"
)


api.upload_file(
    path_or_fileobj="data/air_quality_current.csv", 
    path_in_repo="data/air_quality_current.csv",
    repo_id=REPO_ID,
    repo_type="space"
)

api.upload_file(
    path_or_fileobj="data/air_quality_latest.csv", 
    path_in_repo="data/air_quality_latest.csv",
    repo_id=REPO_ID,
    repo_type="space"
)

print("✅ Upload complete! Hugging Face Space is now rebuilding.")