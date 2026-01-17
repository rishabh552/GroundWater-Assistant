"""Jal-Rakshak: Groundwater Risk Advisor Streamlit Web Interface."""
import streamlit as st
from streamlit_folium import st_folium

from backend.config import APP_TITLE, APP_SUBTITLE, PDF_DIR, VECTORSTORE_DIR
from backend.retriever import GroundwaterRetriever
from backend.llm import load_model, generate_response
from backend.prompts import SYSTEM_PROMPT, format_query
from backend.translator import translate_to_english, translate_response, get_language_name
from backend.agent import Agency
from backend.map_utils import generate_tamil_nadu_map
from backend.report_generator import create_pdf


# Page configuration
st.set_page_config(
    page_title="Jal-Rakshak",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global Styles - Deep Ocean Theme */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 90%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers with Gradient */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6, p, li, span, div {
        color: #e2e8f0;
    }
    
    /* Sidebar adjustments */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    
    /* Input Fields - Modern Glass */
    .stTextInput > div > div > input {
        border-radius: 12px;
        background-color: rgba(30, 41, 59, 0.5);
        color: #ffffff;
        border: 1px solid #334155;
        padding: 15px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        background-color: rgba(30, 41, 59, 0.8);
    }
    
    /* Buttons - Neon Glow */
    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(90deg, #0ea5e9, #3b82f6);
        color: white;
        border: none;
        padding: 0.7rem 2.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
    }
    
    /* Modern Cards (Glassmorphism) */
    .risk-box, .warning-box, .source-citation {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 1.5rem 0;
    }
    
    /* Risk Levels with Glow */
    .risk-low { 
        border-left: 4px solid #4ade80; 
        box-shadow: inset 10px 0 20px -10px rgba(74, 222, 128, 0.1); 
    }
    .risk-moderate { 
        border-left: 4px solid #facc15; 
        box-shadow: inset 10px 0 20px -10px rgba(250, 204, 21, 0.1); 
    }
    .risk-high { 
        border-left: 4px solid #fb923c; 
        box-shadow: inset 10px 0 20px -10px rgba(251, 146, 60, 0.1); 
    }
    .risk-very-high { 
        border-left: 4px solid #f87171; 
        box-shadow: inset 10px 0 20px -10px rgba(248, 113, 113, 0.1); 
    }
    
    .source-citation {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #64748b;
    }
    
    .warning-box {
        background: rgba(69, 10, 10, 0.3);
        border-left: 4px solid #f87171;
        color: #fca5a5;
    }
    
    /* Agent Thoughts */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Code Blocks */
    code {
        color: #38bdf8 !important;
        background-color: #0f172a !important;
        border: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_llm():
    """Load and cache the LLM model."""
    with st.spinner("Loading AI model (first time takes ~2 minutes)..."):
        return load_model()


@st.cache_resource
def load_retriever():
    """Load and cache the retriever."""
    retriever = GroundwaterRetriever()
    try:
        retriever.load()
        return retriever
    except FileNotFoundError:
        return None


def check_setup():
    """Check if the system is properly set up."""
    issues = []
    
    # Check for vectorstore
    if not VECTORSTORE_DIR.exists() or not any(VECTORSTORE_DIR.iterdir()):
        issues.append("📁 No documents indexed. Please run `python ingest.py` first.")
    
    # Check for PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        issues.append(f"📄 No PDF files found in `{PDF_DIR}`. Please add CGWB reports.")
    
    return issues


def main():
    # Header
    st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
    
    # Check setup
    issues = check_setup()
    if issues:
        st.warning("⚠️ Setup Required")
        for issue in issues:
            st.error(issue)
        
        st.info("""
        **Quick Start:**
        1. Download a CGWB groundwater report PDF
        2. Place it in `data/pdfs/` folder
        3. Run `python ingest.py --all`
        4. Refresh this page
        """)
        return
    
    # Load models
    retriever = load_retriever()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Jal-Rakshak** helps farmers across Tamil Nadu 
        assess groundwater availability before drilling borewells.
        
        **Data Source:**
        - CGWB Ground Water Reports
        - State Ground Water Data Centre
        - Tamil Nadu PWD Firka Categorization
        
        **Risk Levels:**
        - 🟢 Safe - Low Risk
        - 🟡 Semi-Critical - Moderate Risk
        - 🟠 Critical - High Risk
        - 🔴 Over-Exploited - Very High Risk
        - 🟣 Saline - Not Suitable
""")
        st.divider()
        
        st.header("🛠️ Tech Stack")
        st.markdown('''
        - **LLM**: IBM Granite 3.0 2B
        - **Acceleration**: NVIDIA CUDA GPU
        - **Embeddings**: Sentence-Transformers
        - **Vector Store**: FAISS
        - **Parsing**: IBM Docling
        - **Translation**: Google Translate
        ''')

        
        st.divider()
        
        # Show indexed documents
        st.header("📚 Indexed Documents")
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        for pdf in pdf_files:
            st.text(f"• {pdf.name}")
    
    # Main query interface
    st.header("🔍 Check Groundwater Status")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Display chat history
    if st.session_state["chat_history"]:
        st.subheader("💬 Conversation History")
        for i, msg in enumerate(st.session_state["chat_history"]):
            if msg["role"] == "user":
                st.markdown(f"**🧑 You:** {msg['content']}")
            else:
                with st.expander(f"🤖 Jal-Rakshak Response #{i//2 + 1}", expanded=(i == len(st.session_state['chat_history']) - 1)):
                    st.markdown(msg["content"])
        st.divider()

    # Interactive Map Section
    with st.expander("🗺️ Interactive Risk Map", expanded=False):
        st.markdown("Click on a location to see its risk status.")
        m = generate_tamil_nadu_map()
        map_data = st_folium(m, width="100%", height=400)
    
    # Handle Map Click
    if map_data and map_data.get("last_object_clicked_tooltip"):
        clicked_text = map_data["last_object_clicked_tooltip"]
        # Tooltip format is "Name: Status", we split to get Name
        if ":" in clicked_text:
            clicked_district = clicked_text.split(":")[0].strip()
            st.session_state["selected_district"] = clicked_district
    
    # Pre-fill query from map click if available
    initial_query = st.session_state.get("selected_district", "")
    
    # Use a form to align button and input, and allow Enter key to submit
    with st.form(key="search_form"):
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_input(
                "Enter Block/Firka/District Name (English, Tamil, or Hindi)",
                value=f"Groundwater status in {initial_query}" if initial_query else "",
                placeholder="e.g., Salem, சேலம், सलेम",
                help="Type in English, Tamil, or Hindi - we'll translate automatically!",
                key="query_input"
            )
        
        with col2:
            # Add some spacing to align button with input box (label offset)
            st.markdown("<br>", unsafe_allow_html=True) 
            search_button = st.form_submit_button("🔍 Check Status", type="primary", use_container_width=True)
    
    # Process query
    if (search_button or st.session_state.get("selected_district")) and query:
        # Store location for PDF report before clearing
        location_for_report = initial_query if initial_query else "Tamil_Nadu"
        
        # Clear the session state trigger so it doesn't loop
        if st.session_state.get("selected_district"):
             del st.session_state["selected_district"]
             
        with st.spinner("Searching documents and analyzing..."):
            # Translate query to English if needed
            english_query, detected_lang = translate_to_english(query)
            
            if detected_lang != 'en':
                st.info(f"🌐 Detected {get_language_name(detected_lang)} - translating...")
            
            # Retrieve relevant context using English query
            results = retriever.search(english_query)
            
            if not results:
                no_data_msg = "No relevant data found for this query. Try a different block name."
                if detected_lang != 'en':
                    no_data_msg = translate_response(no_data_msg, detected_lang)
                st.warning(no_data_msg)
                return
            
            # Load Agent components
            llm = load_llm()
            agent = Agency(llm, retriever)
            
            # Run Agent Loop
            response_container = st.empty()
            thoughts_expander = st.expander("Agent Thinking Process", expanded=True)
            
            final_response = ""
            
            with thoughts_expander:
                for step in agent.run(english_query):
                    status = step["status"]
                    content = step["content"]
                    
                    if status == "thinking":
                        st.info(content)
                    elif status == "thought":
                        st.markdown(f"**Thought:** {content}")
                    elif status == "action":
                        st.code(content, language="python")
                    elif status == "observation":
                        st.success(f"Output: {content}")
                    elif status == "final":
                        final_response = content
            
            # Translate response back to user's language if needed
            if detected_lang != 'en' and final_response:
                final_response = translate_response(final_response, detected_lang)
            
            # Add to chat history
            st.session_state["chat_history"].append({"role": "user", "content": query})
            st.session_state["chat_history"].append({"role": "assistant", "content": final_response})
            
            # Store response in session state so it persists after map interactions
            st.session_state["last_response"] = final_response
            st.session_state["last_query"] = english_query
            st.session_state["last_location"] = location_for_report
    
    # Display response OUTSIDE the query block (from session state, persists after map clicks)
    if st.session_state.get("last_response"):
        st.divider()
        st.subheader("Agent Response")
        st.markdown(st.session_state["last_response"])
        
        # PDF Report Button (use session state for persistence)
        response_for_pdf = st.session_state["last_response"]
        # Helper to guess risk based on response text (case-insensitive check)
        risk_heuristic = "Unknown"
        response_lower = response_for_pdf.lower()
        if "over-exploited" in response_lower or "overexploited" in response_lower:
            risk_heuristic = "Over-Exploited"
        elif "semi-critical" in response_lower or "semicritical" in response_lower:
            risk_heuristic = "Semi-Critical"
        elif "critical" in response_lower:
            risk_heuristic = "Critical"
        elif "safe" in response_lower:
            risk_heuristic = "Safe"
        
        pdf_bytes = create_pdf(
            query=st.session_state.get("last_query", ""), 
            location=st.session_state.get("last_location", "Tamil_Nadu"), 
            risk_level=risk_heuristic, 
            full_response=response_for_pdf
        )
        
        st.download_button(
            label="📄 Download Official Feasibility Report (PDF)",
            data=pdf_bytes,
            file_name=f"Jal_Rakshak_Report_{st.session_state.get('last_location', 'Tamil_Nadu')}.pdf",
            mime="application/pdf"
        )

    
    # Footer
    st.divider()
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Disclaimer:</strong> This tool provides indicative risk assessments based on 
        government reports. Groundwater levels fluctuate seasonally. Always consult local 
        groundwater officials before making drilling decisions.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
