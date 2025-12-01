import os
from huggingface_hub import HfApi


HF_TOKEN = os.getenv("HF_TOKEN")
HF_USERNAME = os.getenv("HF_USERNAME")
HF_SPACE_NAME = os.getenv("HF_SPACE_NAME")
REPO_ID = f"{HF_USERNAME}/{HF_SPACE_NAME}"

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing!")

print(f"🚀 Starting sync to {REPO_ID}...")
api = HfApi(token=HF_TOKEN)


code_files = [
    "Dockerfile",
    "requirements.txt",
    "entrypoint.sh",
    "README.md",
    "app/main.py",
    "dashboard/streamlit_app.py",
    "training/config.py"
]

print("📦 Uploading Code...")
for file in code_files:
    try:
        api.upload_file(
            path_or_fileobj=file,
            path_in_repo=file,
            repo_id=REPO_ID,
            repo_type="space"
        )
        print(f"✅ Uploaded {file}")
    except Exception as e:
        print(f"⚠️ Could not upload {file}: {e}")


print("📊 Uploading Data & Models...")


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

print("✅ Sync complete! Hugging Face Space is rebuilding.")