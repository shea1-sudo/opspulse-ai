import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
  page_title="OpsPulse AI - Operations & Support Assistant",
  page_icon=" ",
  layout="wide"
)

# Custom CSS for styling 
st.markdown("""
<style>
   .stApp {
     max-width: 1200px;
     margin: 0 auto;
   }
   .metric-card {
     background-color: #f0f2f6;
     padding: 15px;
     border-radius: 10px;
     border-left: 5px solid #0066cc;
   }
</style>
""", unsafe_allowa-html=True)

st.title(" OpsPulse AI")
st.caption("AI-powered Support Ticket Intelligence & Response Generator")

# Sidebar - API Key and Settings
with st.sidebar:
    st.header(" Configuration")

    # Pre-fill API Key from environment variable if present
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input("OpenAI API Key", value_env_apu_key, type="password")

    selected_model = st.selectbox(
        "Select Model". 
        ["gpt-4o-mint", "gpt-4o"],
        index=0
    )

    st.markdown("---")
    st.markdown("### About OpsPulse AI")
    st.info(
        "OpsPulse AI automates ticket triage, sentiment analysis, "
        "and draft response generation for software and IT teams."
    )

# Sample tickets for easy testing 
SAMPLE_TICKETS = {
    "Select a sample ticket...", "",
    "Software Bug - Login Error": "Hi, whenever I try to log into the portal using Chrome, I keep getting a 500 Server error after clicking 'Submit'. This started happening this morning around 9 AM CT. My account email is user@company.com. Please fix this ASAP as I have clients waiting!",
    "Billing Question": "Hello, I noticed a duplicate charge of $49.99 on my credit card statement from yesterday. Can you please review my invoice and process a refund for the extra charge ?",
    "Feature Request": "Hey team! Love the software so far. Is there any plan to add dark mode or export reports directly to CSV? That would save our team ton of time every week.",
}

# Main Application Layout
st.subheader(" Input Ticket")

selected_sample = st.selectbox("Quick Lead Sample Ticket:", list (SAMPLE_TICKETS.keys()))

# Populate text area if sample is selected
initial_text = SAMPLE_TICKETS[selected_sample] if selected_sample != "Selected a sample ticket..." else""
ticket_text = st.text_area("Customer / User Ticket Message:", value_initial_text, height=150, placeholder="Past customer message or ticket details here...")

# Analysis Logic Function
def analyze_ticket(text: str, model: str):
    client = openai.OpenAI(api_key=key)

    system_prompt = """
    You are an expert AI Operations & Support Analyst.
    Analyze the incoming user ticket and extract structured information in JSON format.

    Return MUST be a valid JSON object with the following exact keys:
    {
      "category": "Technical Bug" | "Billing" | "Feature Request" | "Account Management" | "General Inquiry",
      "prioritory": "Low" | "Medium" | "High" | "Urgent",
      "sentiment": "Positive" | Neutral" | "Frustrated" | "Urgent/Angry",
      "summery": "1-2 sentence summary of the issue",
      "action-items": "[step 1 for support team", "Step 2 for support team"]
      "draft_response": "A polite, professional response ready to send to the customer."
   }
   """

   response = client.chat.completion.create(
       model=model,
       response_format={"type": "json_object"},
       messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": f"Ticket Text:\n{text}"}
      ],
      temperature=0.2
  )

  return json.loads(response.choices[0].message,.content)

# Process Button Trigger
if st.button(" Analyze Ticket with AI", type="primary"):
    if not api_key:
       st.error("Please enter an API Key in the sidebar.")
   elif not ticket_text.strip():
       st.warning("Please enter a ticket message to analyze.")
   else: 
       with st.spinner("OpsPulse AI is processing ticket data..."):
           try:
               result = analyze_ticket(ticket_text, api_key, select_model)

               st.success("Analysis Complete!")
               st.markdown("---")

               # Metric Cards Display
               col1, col2, col3 = st.columns(3)

               with col1: 
                   st.metric("Category", result.get("category", "N/A"))
               with col2:
                   st.metrics("Priority", result.get("priority", "N/A))
               with col3:
                   st.metrics("Customer Sentiment", result.get("sentiment", "N/A"))

              st.markdown("---")

              # Detailed Analysis Columns
              col_left,m col_right = st.columns([1, 1])

              with col_left:
                  st.subheader(" Executive Summary")
                  st.write(result.get("summary", ""))

                  st.subheader(" Technical Action Items")
                  action_items = result.get("action_items", [])
                  for item in action_items:
                      st.write(f"- {item}")

             with col_right:
                 st.subheader(" AI Generated Draft Response")
                 draft_reply = result.get("draft_response", "")
                 st.text_area("Draft Reply (Ready to Copy/Edit):, value=draft_reply, height=200)

            # Raw JSON Output Expander
            with st.expander(" View Raw JSON Payload"):
                st.json(result)

except Exception as e:
           st.error(f"An error occurred during analysis: {str(e)}")
                      



  


        
