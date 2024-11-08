import os
import streamlit as st
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

from google.cloud import storage

def get_storage_url(uri: str):
    # Extract the bucket and blob names from the URI
    if uri.startswith("gs://"):
        path = uri[5:]  # Remove 'gs://' prefix
        bucket_name, blob_name = path.split("/", 1)

        # Initialize a storage client and get the bucket
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # Get the blob and generate a public URL
        blob = bucket.blob(blob_name)
        return blob.public_url
    else:
        raise ValueError(f"Invalid URI: {uri}")


# Google Cloud setup
PROJECT_ID = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("GCP_REGION")
vertexai.init(project=PROJECT_ID, location=LOCATION)

@st.cache_resource
def load_models() -> tuple[GenerativeModel, GenerativeModel]:
    """Load Gemini 1.5 Flash and Pro models."""
    return GenerativeModel("gemini-1.5-flash"), GenerativeModel("gemini-1.5-pro")

def prioritize_tasks(model: GenerativeModel, patient_data: dict, generation_config: GenerationConfig) -> str:
    """Generate a prioritized task list based on patient data."""
    contents = f"""
    Given the following patient data, prioritize the tasks for healthcare workers:
    - Patient Needs: {patient_data['needs']}
    - Lab Results: {patient_data['lab_results']}
    - Incoming Data: {patient_data['incoming_data']}
    """
    
    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        stream=False,
    )
    return responses.text

def get_model_name(model: GenerativeModel) -> str:
    """Get Gemini Model Name"""
    model_name = model._model_name.replace("publishers/google/models/", "")
    return f"`{model_name}`"

st.header("Healthcare Task Prioritization AI", divider="rainbow")
gemini_15_flash, gemini_15_pro = load_models()

# Main tabs for healthcare AI application
tab1, tab2, tab3 = st.tabs(["Task Prioritization", "Marketing Campaign", "Image Analysis"])

# Tab 1: Task Prioritization
with tab1:
    st.subheader("Dynamic Task Prioritization for Healthcare Workers")

    selected_model = st.radio(
        "Select Gemini Model:", [gemini_15_flash, gemini_15_pro],
        format_func=get_model_name, key="selected_model", horizontal=True
    )
    
    patient_needs = st.text_area("Enter Patient Needs:", "e.g., urgent medication, follow-up, etc.")
    lab_results = st.text_area("Enter Lab Results:", "e.g., blood work, imaging results, etc.")
    incoming_data = st.text_area("Enter Any Incoming Data:", "e.g., new symptoms, vital signs, etc.")
    
    prioritize_button = st.button("Prioritize Tasks")
    
    if prioritize_button:
        patient_data = {
            "needs": patient_needs,
            "lab_results": lab_results,
            "incoming_data": incoming_data,
        }
        
        config = GenerationConfig(temperature=0.7, max_output_tokens=1500)
        prioritized_tasks = prioritize_tasks(selected_model, patient_data, config)
        
        st.subheader("Prioritized Task List")
        st.write(prioritized_tasks)

# Tab 2: Marketing Campaign for Healthcare Products/Services
with tab2:
    st.subheader("Generate a Marketing Campaign for Healthcare")

    selected_model = st.radio(
        "Select Gemini Model:",
        [gemini_15_flash, gemini_15_pro],
        format_func=get_model_name,
        key="selected_model_marketing",
        horizontal=True,
    )
    
    product_name = st.text_input("Healthcare Product Name:", "e.g., HealthEase")
    product_category = st.radio(
        "Product Category:", ["Medical Device", "Pharmaceutical", "Service", "Technology"],
        key="product_category", horizontal=True
    )
    
    target_audience = st.radio(
        "Target Audience:", ["Patients", "Healthcare Workers", "Hospitals", "Clinics"],
        key="target_audience", horizontal=True
    )
    
    campaign_goal = st.multiselect(
        "Campaign Goals:", ["Awareness", "Lead Generation", "Sales", "Positive Sentiment"],
        key="campaign_goal", default=["Awareness"]
    )
    
    budget = st.radio(
        "Estimated Budget ($):", ["1,000-5,000", "5,000-10,000", "10,000-20,000", "20,000+"],
        key="estimated_budget", horizontal=True
    )
    
    prompt = f"""
    Generate a marketing campaign for a healthcare product.
    Product Name: {product_name}
    Category: {product_category}
    Target Audience: {target_audience}
    Campaign Goals: {', '.join(campaign_goal)}
    Estimated Budget: {budget}
    """
    
    generate_campaign = st.button("Generate Campaign")
    
    if generate_campaign:
        config = GenerationConfig(temperature=0.8, max_output_tokens=2048)
        campaign_response = prioritize_tasks(selected_model, prompt, config)
        
        st.subheader("Generated Campaign")
        st.write(campaign_response)

# Tab 3: Image Analysis for Healthcare Insights
with tab3:
    st.subheader("Healthcare Image Analysis")

    selected_model = st.radio(
        "Select Gemini Model:",
        [gemini_15_flash, gemini_15_pro],
        format_func=get_model_name,
        key="selected_model_image",
        horizontal=True,
    )

    # Placeholder images (to be replaced with actual healthcare images)
    sample_image_uri = "gs://your-bucket-path/sample-image.jpg"
    sample_image_url = get_storage_url(sample_image_uri)
    
    st.image(sample_image_url, width=350, caption="Sample Healthcare Image")
    
    image_analysis_prompt = """
    Analyze this healthcare image for relevant insights. Determine the key features,
    potential diagnoses, or further investigation steps needed based on the visual data.
    """
    
    analyze_image = st.button("Analyze Image")
    
    if analyze_image:
        sample_image = Part.from_uri(sample_image_uri, mime_type="image/jpeg")
        
        with st.spinner(f"Analyzing image using {get_model_name(selected_model)} ..."):
            response = get_gemini_response(selected_model, [sample_image, image_analysis_prompt])
            st.write(response)
