# Healthcare Task Prioritization App

This Streamlit application assists healthcare workers in prioritizing patient care tasks based on patient condition, vitals, and lab results. It leverages Vertex AI's Gemini API on Google Cloud.

## Setup Instructions

1. Clone this repository.
2. Set up Google Cloud credentials and enable Vertex AI API.
3. Configure environment variables for `GCP_PROJECT` and `GCP_REGION`.
4. Build and deploy the app on Cloud Run.

## Run Locally

```bash
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
pip install -r requirements.txt
GCP_PROJECT='your-project-id' GCP_REGION='your-region' streamlit run app.py
```
