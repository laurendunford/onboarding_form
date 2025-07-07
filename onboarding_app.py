import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Guidewheel Onboarding",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, Figma-inspired design
st.markdown("""
<style>
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Modern typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.main .block-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    max-width: 1200px;
    padding: 0 1rem;
}

/* Header styles */
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a1a1a;
    text-align: center;
    margin: 2rem 0 3rem 0;
}

/* Card styles */
.modern-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}

.modern-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.card-header {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-subtitle {
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}

/* Button styles */
.modern-button {
    background: linear-gradient(135deg, #502DD5 0%, #7C3AED 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.modern-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(80, 45, 213, 0.3);
}

.secondary-button {
    background: #f8fafc;
    color: #374151;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.secondary-button:hover {
    background: #f1f5f9;
    border-color: #9ca3af;
}

/* Form styles */
.stTextInput > div > div > input {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 0.75rem;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #502DD5;
    box-shadow: 0 0 0 3px rgba(80, 45, 213, 0.1);
}

.stTextArea > div > div > textarea {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 0.75rem;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: #502DD5;
    box-shadow: 0 0 0 3px rgba(80, 45, 213, 0.1);
}

/* Selectbox styles */
.stSelectbox > div > div > div {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.stSelectbox > div > div > div:focus-within {
    border-color: #502DD5;
    box-shadow: 0 0 0 3px rgba(80, 45, 213, 0.1);
}

/* Machine item styles */
.machine-item {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.2s ease;
}

.machine-item:hover {
    background: #f1f5f9;
    border-color: #d1d5db;
}

.machine-title {
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 0.25rem;
}

.machine-details {
    color: #6b7280;
    font-size: 0.9rem;
}

/* Success and info styles */
.success-message {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    font-weight: 500;
}

.info-message {
    background: #eff6ff;
    color: #1e40af;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #3b82f6;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        font-size: 2rem;
        margin: 1.5rem 0 2rem 0;
    }
    
    .modern-card {
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .card-header {
        font-size: 1.25rem;
    }
}

/* Grid layout */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
}

/* Progress indicator */
.progress-bar {
    background: #f1f5f9;
    border-radius: 8px;
    height: 8px;
    margin: 1rem 0;
    overflow: hidden;
}

.progress-fill {
    background: linear-gradient(135deg, #502DD5 0%, #7C3AED 100%);
    height: 100%;
    border-radius: 8px;
    transition: width 0.3s ease;
}

/* Animation classes */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Custom checkbox */
.stCheckbox > div > div {
    background: #f8fafc;
    border: 1px solid #d1d5db;
    border-radius: 6px;
}

.stCheckbox > div > div:checked {
    background: #502DD5;
    border-color: #502DD5;
}

/* File uploader */
.stFileUploader > div > div {
    border: 2px dashed #d1d5db;
    border-radius: 8px;
    background: #f8fafc;
    transition: all 0.2s ease;
}

.stFileUploader > div > div:hover {
    border-color: #502DD5;
    background: #f0f4ff;
}

/* Radio buttons */
.stRadio > div > div {
    background: #f8fafc;
    border: 1px solid #d1d5db;
    border-radius: 8px;
}

.stRadio > div > div:checked {
    background: #502DD5;
    border-color: #502DD5;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# LLM API configuration
def get_machine_suggestions(industry):
    """Get machine suggestions from LLM based on industry"""
    try:
        # Using a free LLM API (you can replace with OpenAI, Anthropic, etc.)
        api_url = "https://api.openai.com/v1/chat/completions"
        
        prompt = f"""Based on the {industry} industry, suggest 6-8 common machines that would be found in a typical manufacturing facility. 
        For each machine, provide:
        - Machine type (e.g., Lathe, Milling Machine, CNC Router)
        - Typical quantity (1-3)
        - Brief description of its use in this industry
        
        Return as JSON array with format:
        [{{"type": "Machine Type", "model": "", "info": "Brief description", "quantity": 1}}]
        
        Focus on machines that are essential for {industry} manufacturing."""
        
        # For demo purposes, using a fallback if API is not configured
        if not st.secrets.get("OPENAI_API_KEY"):
            # Fallback suggestions based on industry
            fallback_suggestions = {
                "Automotive": [
                    {"type": "CNC Lathe", "model": "", "info": "Precision turning for automotive parts", "quantity": 2},
                    {"type": "Milling Machine", "model": "", "info": "Complex machining operations", "quantity": 1},
                    {"type": "Welding Station", "model": "", "info": "Metal joining and fabrication", "quantity": 2},
                    {"type": "Press Brake", "model": "", "info": "Sheet metal bending", "quantity": 1},
                    {"type": "Laser Cutter", "model": "", "info": "Precision cutting of metal sheets", "quantity": 1},
                    {"type": "Quality Control Station", "model": "", "info": "Measurement and inspection", "quantity": 1}
                ],
                "Aerospace": [
                    {"type": "5-Axis CNC Mill", "model": "", "info": "Complex aerospace component machining", "quantity": 1},
                    {"type": "EDM Machine", "model": "", "info": "Precision electrical discharge machining", "quantity": 1},
                    {"type": "Coordinate Measuring Machine", "model": "", "info": "High-precision measurement", "quantity": 1},
                    {"type": "Composite Layup Station", "model": "", "info": "Composite material processing", "quantity": 1},
                    {"type": "Heat Treatment Oven", "model": "", "info": "Material hardening and tempering", "quantity": 1},
                    {"type": "Ultrasonic Testing Station", "model": "", "info": "Non-destructive testing", "quantity": 1}
                ],
                "Electronics": [
                    {"type": "PCB Assembly Line", "model": "", "info": "Circuit board assembly", "quantity": 1},
                    {"type": "SMT Machine", "model": "", "info": "Surface mount technology placement", "quantity": 1},
                    {"type": "Reflow Oven", "model": "", "info": "PCB component soldering", "quantity": 1},
                    {"type": "Testing Station", "model": "", "info": "Electronic component testing", "quantity": 2},
                    {"type": "3D Printer", "model": "", "info": "Prototype and enclosure printing", "quantity": 1},
                    {"type": "Laser Marking System", "model": "", "info": "Component identification", "quantity": 1}
                ],
                "Food & Beverage": [
                    {"type": "Filling Machine", "model": "", "info": "Product packaging and filling", "quantity": 1},
                    {"type": "Conveyor System", "model": "", "info": "Product movement and sorting", "quantity": 2},
                    {"type": "Pasteurization Unit", "model": "", "info": "Food safety processing", "quantity": 1},
                    {"type": "Packaging Machine", "model": "", "info": "Product sealing and labeling", "quantity": 1},
                    {"type": "Quality Control Lab", "model": "", "info": "Food safety testing", "quantity": 1},
                    {"type": "Cleaning Station", "model": "", "info": "Equipment sanitization", "quantity": 1}
                ],
                "Pharmaceutical": [
                    {"type": "Tablet Press", "model": "", "info": "Pharmaceutical tablet manufacturing", "quantity": 1},
                    {"type": "Capsule Filling Machine", "model": "", "info": "Capsule production", "quantity": 1},
                    {"type": "Coating Machine", "model": "", "info": "Tablet coating and finishing", "quantity": 1},
                    {"type": "Blending Station", "model": "", "info": "Powder mixing and blending", "quantity": 1},
                    {"type": "Quality Control Lab", "model": "", "info": "Product testing and validation", "quantity": 1},
                    {"type": "Clean Room Equipment", "model": "", "info": "Sterile manufacturing environment", "quantity": 1}
                ],
                "General Manufacturing": [
                    {"type": "CNC Lathe", "model": "", "info": "General purpose turning operations", "quantity": 2},
                    {"type": "Milling Machine", "model": "", "info": "Versatile machining operations", "quantity": 1},
                    {"type": "Drill Press", "model": "", "info": "Hole drilling and tapping", "quantity": 1},
                    {"type": "Band Saw", "model": "", "info": "Material cutting and shaping", "quantity": 1},
                    {"type": "Welding Station", "model": "", "info": "Metal joining and fabrication", "quantity": 1},
                    {"type": "Quality Control Station", "model": "", "info": "Measurement and inspection", "quantity": 1}
                ]
            }
            return fallback_suggestions.get(industry, fallback_suggestions["General Manufacturing"])
        
        headers = {
            "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a manufacturing expert. Provide accurate, industry-specific machine suggestions."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            suggestions_text = result['choices'][0]['message']['content']
            try:
                # Parse JSON from response
                suggestions = json.loads(suggestions_text)
                return suggestions
            except json.JSONDecodeError:
                st.warning("AI response format issue, using fallback suggestions.")
                return None
        else:
            st.warning(f"API Error: {response.status_code}. Using fallback suggestions.")
            return None
            
    except Exception as e:
        st.warning(f"Error getting suggestions: {str(e)}. Using fallback suggestions.")
        return None

# Initialize session state
if 'machines' not in st.session_state:
    st.session_state.machines = []

# Celebration messages for machine additions
celebration_messages = [
    "🎉 Another machine joins the team!",
    "🛠️ You're building a powerhouse!",
    "🔧 That one's a beauty. Welcome aboard!",
    "🚀 Let's keep the momentum rolling!",
    "💪 That machine is ready to work!"
]

if 'celebration_index' not in st.session_state:
    st.session_state.celebration_index = 0

def show_celebration():
    """Show celebration message and balloons, then rotate to next message"""
    message = celebration_messages[st.session_state.celebration_index]
    st.success(message)
    st.balloons()
    # Rotate to next celebration message
    st.session_state.celebration_index = (st.session_state.celebration_index + 1) % len(celebration_messages)

# Main header
st.markdown('<h1 class="main-header">Guidewheel Onboarding</h1>', unsafe_allow_html=True)

# Machine editing interface (outside the form)
if st.session_state.machines and ('editing_machine' in st.session_state and st.session_state.editing_machine is not None):
    edit_idx = st.session_state.editing_machine
    machine = st.session_state.machines[edit_idx]
    
    st.markdown("""
    <div class="modern-card fade-in">
        <div class="card-header">✏️ Edit Machine</div>
        <div class="card-subtitle">Update the details for this machine</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        machine["type"] = st.text_input(
            "Machine Type",
            value=machine["type"],
            placeholder="e.g., Lathe, Milling Machine, CNC Router",
            key=f"edit_type_{edit_idx}"
        )
        machine["quantity"] = st.number_input(
            "Quantity",
            min_value=1,
            value=machine["quantity"],
            key=f"edit_qty_{edit_idx}"
        )
    
    with col2:
        machine["model"] = st.text_input(
            "Model",
            value=machine["model"],
            placeholder="e.g., Haas VF-2, Bridgeport Series I",
            key=f"edit_model_{edit_idx}"
        )
        machine["info"] = st.text_input(
            "Additional Info",
            value=machine["info"],
            placeholder="Serial number, year, modifications, etc.",
            key=f"edit_info_{edit_idx}"
        )
    
    # Machine photo upload
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">📸 Machine Photo</div>
        <div class="card-subtitle">Upload a photo to help us identify this machine</div>
    </div>
    """, unsafe_allow_html=True)
    
    machine["photo"] = st.file_uploader(
        f"Upload photo of Machine {edit_idx + 1}",
        type=["jpg", "jpeg", "png"],
        key=f"machine_photo_{edit_idx}"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Save Changes", key=f"save_{edit_idx}", use_container_width=True):
            show_celebration()
            st.session_state.editing_machine = None
            st.rerun()
    with col2:
        if st.button("❌ Cancel", key=f"cancel_{edit_idx}", use_container_width=True):
            st.session_state.editing_machine = None
            st.rerun()

# AI Suggestions Section
st.markdown("""
<div class="modern-card fade-in">
    <div class="card-header">🤖 AI-Powered Machine Suggestions</div>
    <div class="card-subtitle">Select your industry and let AI suggest relevant machines for your facility</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    industry = st.selectbox(
        "Select your industry:",
        ["General Manufacturing", "Automotive", "Aerospace", "Electronics", "Food & Beverage", "Pharmaceutical"],
        help="Choose your industry for AI-powered machine suggestions"
    )

with col2:
    if st.button("🤖 Get AI Suggestions", help="Get industry-specific machine suggestions powered by AI", use_container_width=True):
        with st.spinner("🤖 AI is analyzing your industry..."):
            suggestions = get_machine_suggestions(industry)
            if suggestions:
                st.session_state.machines = suggestions
                st.success(f"✨ AI magic activated! {len(suggestions)} {industry} machines added.")
                st.balloons()
                st.rerun()
            else:
                # If AI fails, use fallback suggestions
                fallback_suggestions = {
                    "Automotive": [
                        {"type": "CNC Lathe", "model": "", "info": "Precision turning for automotive parts", "quantity": 2},
                        {"type": "Milling Machine", "model": "", "info": "Complex machining operations", "quantity": 1},
                        {"type": "Welding Station", "model": "", "info": "Metal joining and fabrication", "quantity": 2},
                        {"type": "Press Brake", "model": "", "info": "Sheet metal bending", "quantity": 1},
                        {"type": "Laser Cutter", "model": "", "info": "Precision cutting of metal sheets", "quantity": 1},
                        {"type": "Quality Control Station", "model": "", "info": "Measurement and inspection", "quantity": 1}
                    ],
                    "Aerospace": [
                        {"type": "5-Axis CNC Mill", "model": "", "info": "Complex aerospace component machining", "quantity": 1},
                        {"type": "EDM Machine", "model": "", "info": "Precision electrical discharge machining", "quantity": 1},
                        {"type": "Coordinate Measuring Machine", "model": "", "info": "High-precision measurement", "quantity": 1},
                        {"type": "Composite Layup Station", "model": "", "info": "Composite material processing", "quantity": 1},
                        {"type": "Heat Treatment Oven", "model": "", "info": "Material hardening and tempering", "quantity": 1},
                        {"type": "Ultrasonic Testing Station", "model": "", "info": "Non-destructive testing", "quantity": 1}
                    ],
                    "Electronics": [
                        {"type": "PCB Assembly Line", "model": "", "info": "Circuit board assembly", "quantity": 1},
                        {"type": "SMT Machine", "model": "", "info": "Surface mount technology placement", "quantity": 1},
                        {"type": "Reflow Oven", "model": "", "info": "PCB component soldering", "quantity": 1},
                        {"type": "Testing Station", "model": "", "info": "Electronic component testing", "quantity": 2},
                        {"type": "3D Printer", "model": "", "info": "Prototype and enclosure printing", "quantity": 1},
                        {"type": "Laser Marking System", "model": "", "info": "Component identification", "quantity": 1}
                    ],
                    "Food & Beverage": [
                        {"type": "Filling Machine", "model": "", "info": "Product packaging and filling", "quantity": 1},
                        {"type": "Conveyor System", "model": "", "info": "Product movement and sorting", "quantity": 2},
                        {"type": "Pasteurization Unit", "model": "", "info": "Food safety processing", "quantity": 1},
                        {"type": "Packaging Machine", "model": "", "info": "Product sealing and labeling", "quantity": 1},
                        {"type": "Quality Control Lab", "model": "", "info": "Food safety testing", "quantity": 1},
                        {"type": "Cleaning Station", "model": "", "info": "Equipment sanitization", "quantity": 1}
                    ],
                    "Pharmaceutical": [
                        {"type": "Tablet Press", "model": "", "info": "Pharmaceutical tablet manufacturing", "quantity": 1},
                        {"type": "Capsule Filling Machine", "model": "", "info": "Capsule production", "quantity": 1},
                        {"type": "Coating Machine", "model": "", "info": "Tablet coating and finishing", "quantity": 1},
                        {"type": "Blending Station", "model": "", "info": "Powder mixing and blending", "quantity": 1},
                        {"type": "Quality Control Lab", "model": "", "info": "Product testing and validation", "quantity": 1},
                        {"type": "Clean Room Equipment", "model": "", "info": "Sterile manufacturing environment", "quantity": 1}
                    ],
                    "General Manufacturing": [
                        {"type": "CNC Lathe", "model": "", "info": "General purpose turning operations", "quantity": 2},
                        {"type": "Milling Machine", "model": "", "info": "Versatile machining operations", "quantity": 1},
                        {"type": "Drill Press", "model": "", "info": "Hole drilling and tapping", "quantity": 1},
                        {"type": "Band Saw", "model": "", "info": "Material cutting and shaping", "quantity": 1},
                        {"type": "Welding Station", "model": "", "info": "Metal joining and fabrication", "quantity": 1},
                        {"type": "Quality Control Station", "model": "", "info": "Measurement and inspection", "quantity": 1}
                    ]
                }
                fallback = fallback_suggestions.get(industry, fallback_suggestions["General Manufacturing"])
                st.session_state.machines = fallback
                st.success(f"✨ Using industry-specific suggestions! {len(fallback)} {industry} machines added.")
                st.balloons()
                st.rerun()

with col3:
    if st.button("➕ Add Machine Manually", key="add_machine_form", help="Add a new machine manually to your list.", use_container_width=True):
        st.session_state.machines.append({"type": "", "model": "", "info": "", "quantity": 1})
        show_celebration()
        st.rerun()

# Machine Inventory Section
st.markdown("""
<div class="modern-card fade-in">
    <div class="card-header">🔧 Machine Inventory</div>
    <div class="card-subtitle">Review and manage your machine list</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.machines:
    for i, machine in enumerate(st.session_state.machines):
        st.markdown(f"""
        <div class="machine-item fade-in">
            <div class="machine-title">Machine {i+1}: {machine['type']}</div>
            <div class="machine-details">
                Model: {machine['model'] if machine['model'] else 'Not specified'} | 
                Quantity: {machine['quantity']} | 
                {machine['info'] if machine['info'] else 'No additional info'}
                {' 📸' if machine.get('photo') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Edit {i+1}", key=f"form_edit_{i}", use_container_width=True):
                st.session_state.editing_machine = i
                st.rerun()
        with col2:
            if st.button(f"Remove {i+1}", key=f"form_remove_{i}", use_container_width=True):
                st.session_state.machines.pop(i)
                st.rerun()
else:
    st.markdown("""
    <div class="info-message">
        💡 Start by adding machines using AI suggestions or manually. This will help us understand your facility better.
    </div>
    """, unsafe_allow_html=True)

# Main Form
with st.form(key="onboarding_form"):
    st.markdown("""
    <div class="modern-card fade-in">
        <div class="card-header">📝 Additional Information</div>
        <div class="card-subtitle">Help us understand your setup better</div>
    </div>
    """, unsafe_allow_html=True)
    
    notes = st.text_area(
        "Optional notes:",
        placeholder="Any additional information about your facility, processes, or specific requirements...",
        height=100
    )
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">📸 Facility Photos</div>
        <div class="card-subtitle">Upload photos to help us understand your setup better</div>
    </div>
    """, unsafe_allow_html=True)
    
    other_photos = st.file_uploader(
        "Upload photos (whiteboards, factory layout, safety equipment, etc.):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload any relevant photos: whiteboard diagrams, factory layouts, safety equipment, certifications, or other important documentation."
    )
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">🎨 Line Layout</div>
        <div class="card-subtitle">How would you like to share your production line layout?</div>
    </div>
    """, unsafe_allow_html=True)
    
    layout_option = st.radio(
        "Layout sharing method:",
        ["I have existing sketches to upload", "Skip for now"],
        help="Choose whether you want to upload existing sketches/diagrams or skip for now."
    )
    
    layout_sketches = None
    if layout_option == "I have existing sketches to upload":
        layout_sketches = st.file_uploader(
            "Upload your line layout sketches/diagrams:",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Upload any existing sketches, diagrams, or drawings of your production line layout."
        )
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">👤 Contact Information</div>
        <div class="card-subtitle">Let us know how to reach you</div>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input("Your Name:")
    email = st.text_input("Your Email:")
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">👥 Invite Teammate</div>
        <div class="card-subtitle">Would you like to invite a teammate to this onboarding?</div>
    </div>
    """, unsafe_allow_html=True)
    
    invite_teammate = st.checkbox("Invite a teammate to this onboarding?")
    teammate_name = ""
    teammate_email = ""
    if invite_teammate:
        show_celebration()
        teammate_name = st.text_input("Teammate's Name:")
        teammate_email = st.text_input("Teammate's Email:")
    
    submit = st.form_submit_button("Submit Onboarding", use_container_width=True, type="primary")

# Success Section
if submit:
    st.markdown("""
    <div class="success-message fade-in">
        🎉 Onboarding submitted successfully! Welcome to Guidewheel!
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
    
    st.markdown("""
    <div class="modern-card fade-in">
        <div class="card-header">📋 Your Setup Summary</div>
        <div class="card-subtitle">Here's what we'll be working with</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout option summary
    layout_summary = layout_option
    if layout_option == "I have existing sketches to upload" and layout_sketches:
        layout_summary += f" ({len(layout_sketches)} files)"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">👤 Contact Information</div>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        if invite_teammate:
            st.write(f"**Teammate:** {teammate_name} ({teammate_email})")
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">🔧 Machine Inventory</div>
        </div>
        """, unsafe_allow_html=True)
        for i, machine in enumerate(st.session_state.machines):
            machine_info = f"• {machine['type']}"
            if machine['model']:
                machine_info += f" ({machine['model']})"
            machine_info += f": {machine['quantity']}"
            if machine['info']:
                machine_info += f" - {machine['info']}"
            st.write(machine_info)
    
    if notes:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">📝 Additional Notes</div>
        </div>
        """, unsafe_allow_html=True)
        st.write(notes)
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">🎨 Line Layout</div>
    </div>
    """, unsafe_allow_html=True)
    st.write(layout_summary)
    
    # Count photos
    machine_photo_count = sum(1 for machine in st.session_state.machines if machine.get('photo'))
    other_photo_count = (len(other_photos) if other_photos else 0) + \
                       (len(layout_sketches) if layout_sketches else 0)
    
    st.markdown("""
    <div class="modern-card">
        <div class="card-header">📸 Uploaded Assets</div>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"• Machine photos: {machine_photo_count}")
    st.write(f"• Other photos: {other_photo_count}")
    st.write(f"• Total photos: {machine_photo_count + other_photo_count}")
    
    st.markdown("""
    <div class="modern-card fade-in">
        <div class="card-header">🤝 Meet Your Guidewheel Buddy</div>
        <div class="card-subtitle">Alex will reach out to guide your setup and answer any questions</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 12px; margin: 2rem 0;">
        <h3 style="color: #1a1a1a; margin-bottom: 1rem;">🎉 Welcome to the Guidewheel family!</h3>
        <p style="color: #6b7280; font-size: 1.1rem;">We're excited to help you get started with your manufacturing journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display uploaded photos
    machine_photos_to_show = [machine for machine in st.session_state.machines if machine.get('photo')]
    if machine_photos_to_show:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">📸 Machine Photos</div>
        </div>
        """, unsafe_allow_html=True)
        for i, machine in enumerate(machine_photos_to_show):
            st.image(machine['photo'], caption=f"Machine {i+1}: {machine['type']}", width=300)
    
    if other_photos:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">📸 Facility Photos</div>
        </div>
        """, unsafe_allow_html=True)
        for i, photo in enumerate(other_photos):
            st.image(photo, caption=f"Photo {i+1}", width=300)
    
    if layout_sketches:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">🎨 Line Layout Sketches</div>
        </div>
        """, unsafe_allow_html=True)
        for i, sketch in enumerate(layout_sketches):
            st.image(sketch, caption=f"Layout Sketch {i+1}", width=300)

