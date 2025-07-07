import streamlit as st
import requests
import json

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
        
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            suggestions_text = result['choices'][0]['message']['content']
            # Parse JSON from response
            suggestions = json.loads(suggestions_text)
            return suggestions
        else:
            st.error(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error getting suggestions: {str(e)}")
        return None

# Enterprise Header
st.markdown("""
<div style="background: linear-gradient(135deg, #502DD5 0%, #32B3F1 100%); padding: 2rem 0; margin: -2rem -2rem 2rem -2rem; border-radius: 0;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <h1 style="color: white; font-size: 2.5rem; font-weight: 300; margin: 0; letter-spacing: -0.5px;">The Only Purple, Not The Weird Fade</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0.5rem 0 0 0; font-weight: 300;">Streamline your manufacturing setup with intelligent machine management</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for machines if not exists
if 'machines' not in st.session_state:
    st.session_state.machines = []

# Initialize total machine count if not exists
if 'total_machines' not in st.session_state:
    st.session_state.total_machines = 0

# Initialize manual form state
if 'show_manual_form' not in st.session_state:
    st.session_state.show_manual_form = False

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

# Function to update total machine count
def update_total_machines():
    """Calculate and update the total number of machines"""
    total = sum(machine.get('quantity', 1) for machine in st.session_state.machines)
    st.session_state.total_machines = total

# Update total machines count on app load
if 'total_machines' not in st.session_state:
    update_total_machines()

# Machine editing interface (outside the form)
if st.session_state.machines and ('editing_machine' in st.session_state and st.session_state.editing_machine is not None):
    edit_idx = st.session_state.editing_machine
    machine = st.session_state.machines[edit_idx]
    
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h3 style="color: #502DD5; margin: 0 0 1.5rem 0; font-weight: 500;">Edit Machine Configuration</h3>
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
    st.write("**Machine Photo:**")
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
    
    st.markdown("</div>", unsafe_allow_html=True)

# Manual Machine Addition Form
if st.session_state.show_manual_form:
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">✏️</span>
            </div>
            <div>
                <h3 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Add New Machine</h3>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Enter the details for your new machine</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        machine_type = st.text_input(
            "Machine Type *",
            placeholder="e.g., CNC Lathe, Milling Machine, Welding Station",
            help="Enter the type or name of the machine"
        )
        quantity = st.number_input(
            "Quantity *",
            min_value=1,
            value=1,
            help="How many of this machine do you have?"
        )
    
    with col2:
        model = st.text_input(
            "Model",
            placeholder="e.g., Haas VF-2, Bridgeport Series I",
            help="Optional: Enter the specific model number"
        )
        info = st.text_input(
            "Additional Info",
            placeholder="e.g., Serial number, year, modifications",
            help="Optional: Any additional information about this machine"
        )
    
    # Machine photo upload
    st.write("**Machine Photo (Optional):**")
    machine_photo = st.file_uploader(
        "Upload a photo of this machine",
        type=["jpg", "jpeg", "png"],
        help="Upload a photo to help us understand your setup better"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("✅ Save Machine", use_container_width=True, type="primary"):
            if machine_type.strip():  # Check if machine type is provided
                new_machine = {
                    "type": machine_type.strip(),
                    "model": model.strip(),
                    "info": info.strip(),
                    "quantity": quantity,
                    "photo": machine_photo
                }
                st.session_state.machines.append(new_machine)
                st.session_state.show_manual_form = False
                show_celebration()
                st.rerun()
            else:
                st.error("❌ Please enter a machine type")
    
    with col2:
        if st.button("➕ Add Another", use_container_width=True):
            if machine_type.strip():
                new_machine = {
                    "type": machine_type.strip(),
                    "model": model.strip(),
                    "info": info.strip(),
                    "quantity": quantity,
                    "photo": machine_photo
                }
                st.session_state.machines.append(new_machine)
                show_celebration()
                st.rerun()
            else:
                st.error("❌ Please enter a machine type")
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_manual_form = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Enterprise Machine Setup Section
st.markdown("""
<div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
            <span style="color: white; font-size: 1.2rem;">🚀</span>
        </div>
        <div>
            <h2 style="color: #2c3e50; margin: 0; font-weight: 600; font-size: 1.5rem;">Get Started</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.95rem;">Choose your preferred method to add machines</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI Suggestions Card
st.markdown("""
<div style="background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%); border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
            <span style="color: white; font-size: 1rem;">🤖</span>
        </div>
        <div>
            <h3 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">AI-Powered Suggestions</h3>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Get industry-specific machine recommendations</p>
        </div>
    </div>
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
                st.error("❌ Could not get AI suggestions. Please try again or use manual entry.")

with col3:
    if st.button("➕ Add Machine Manually", key="add_machine_form", help="Add a new machine manually to your list.", use_container_width=True):
        st.session_state.show_manual_form = True
        show_celebration()
        st.rerun()

# Update total machines count before displaying
update_total_machines()

# Machine Inventory Section
st.markdown(f"""
<div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
            <span style="color: white; font-size: 1rem;">📋</span>
        </div>
        <div>
            <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Machine Inventory</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Review and manage your machine list • Total: {st.session_state.total_machines} machines</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Show machine summary with edit/remove options
if st.session_state.machines:
    for i, machine in enumerate(st.session_state.machines):
        st.markdown(f"""
        <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin: 0.5rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #502DD5; font-size: 1.1rem;">{machine['type']}</div>
                    <div style="color: #6c757d; font-size: 0.9rem; margin-top: 0.25rem;">
                        Model: {machine['model'] if machine['model'] else 'Not specified'} • Qty: {machine['quantity']}
                    </div>
                    {f'<div style="color: #868e96; font-size: 0.85rem; margin-top: 0.25rem;">{machine["info"]}</div>' if machine['info'] else ''}
                    {'<span style="color: #32B3F1; font-size: 0.9rem;">📸 Photo uploaded</span>' if machine.get('photo') else ''}
                </div>
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
    <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 2rem; text-align: center; color: #6c757d;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">📋</div>
        <div style="font-weight: 500; margin-bottom: 0.5rem;">No machines added yet</div>
        <div style="font-size: 0.9rem;">Click "Add Machine Manually" to start building your inventory, or use AI suggestions for industry-specific machines.</div>
    </div>
    """, unsafe_allow_html=True)

# Main Form Section
with st.form(key="onboarding_form"):
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">📝</span>
            </div>
            <div>
                <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Additional Information</h2>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Provide additional context for your setup</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    notes = st.text_area(
        "Additional Notes",
        placeholder="Any additional information about your setup, requirements, or special considerations...",
        height=100
    )
    
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">📸</span>
            </div>
            <div>
                <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Documentation & Photos</h2>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Upload relevant documentation and visual assets</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    other_photos = st.file_uploader(
        "Upload additional photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload any relevant photos: whiteboard diagrams, factory layouts, safety equipment, certifications, or other important documentation."
    )
    
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">🏭</span>
            </div>
            <div>
                <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Line Layout</h2>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Share your production line configuration</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    layout_option = st.radio(
        "How would you like to share your line layout?",
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
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">👤</span>
            </div>
            <div>
                <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Contact Information</h2>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Primary contact details for your setup</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Enter your full name")
    with col2:
        email = st.text_input("Email Address", placeholder="Enter your email address")
    
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, #502DD5, #32B3F1); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="color: white; font-size: 1rem;">👥</span>
            </div>
            <div>
                <h2 style="color: #2c3e50; margin: 0; font-weight: 500; font-size: 1.2rem;">Team Collaboration</h2>
                <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem;">Invite team members to the onboarding process</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    invite_teammate = st.checkbox("Invite a teammate to this onboarding?")
    teammate_name = ""
    teammate_email = ""
    if invite_teammate:
        col1, col2 = st.columns(2)
        with col1:
            teammate_name = st.text_input("Teammate's Name", placeholder="Enter teammate's full name")
        with col2:
            teammate_email = st.text_input("Teammate's Email", placeholder="Enter teammate's email address")
    
    # Submit button with enterprise styling
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <button type="submit" style="background: linear-gradient(135deg, #502DD5, #32B3F1); color: white; border: none; padding: 1rem 3rem; border-radius: 8px; font-size: 1.1rem; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(80, 45, 213, 0.3); transition: all 0.3s ease;">
            Submit Onboarding Information
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    submit = st.form_submit_button("Submit", use_container_width=True)

if submit:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d4edda, #c3e6cb); border: 1px solid #c3e6cb; border-radius: 12px; padding: 2rem; margin: 2rem 0; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
        <h2 style="color: #155724; margin: 0 0 0.5rem 0; font-weight: 600;">Onboarding Submitted Successfully!</h2>
        <p style="color: #155724; margin: 0; font-size: 1.1rem;">Thank you for providing your information. We're excited to help you get started!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
    
    # Enterprise Summary Section
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #2c3e50; margin: 0 0 1.5rem 0; font-weight: 600; font-size: 1.5rem;">📋 Setup Summary</h2>
        <p style="color: #7f8c8d; margin: 0 0 2rem 0;">Here's what we'll be working with for your installation:</p>
    """, unsafe_allow_html=True)
    
    # Layout option summary
    layout_summary = layout_option
    if layout_option == "I have existing sketches to upload" and layout_sketches:
        layout_summary += f" ({len(layout_sketches)} files)"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem;">
            <h3 style="color: #502DD5; margin: 0 0 1rem 0; font-weight: 500;">👤 Contact Information</h3>
        """, unsafe_allow_html=True)
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        if invite_teammate:
            st.write(f"**Teammate:** {teammate_name} ({teammate_email})")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem;">
            <h3 style="color: #502DD5; margin: 0 0 1rem 0; font-weight: 500;">🔧 Machine Inventory ({st.session_state.total_machines} total)</h3>
        """, unsafe_allow_html=True)
        for i, machine in enumerate(st.session_state.machines):
            machine_info = f"• {machine['type']}"
            if machine['model']:
                machine_info += f" ({machine['model']})"
            machine_info += f": {machine['quantity']}"
            if machine['info']:
                machine_info += f" - {machine['info']}"
            st.write(machine_info)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if notes:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; margin-top: 1rem;">
            <h3 style="color: #502DD5; margin: 0 0 1rem 0; font-weight: 500;">📝 Additional Notes</h3>
        """, unsafe_allow_html=True)
        st.write(notes)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; margin-top: 1rem;">
        <h3 style="color: #502DD5; margin: 0 0 1rem 0; font-weight: 500;">🏭 Line Layout</h3>
        <p style="margin: 0;">{}</p>
    </div>
    """.format(layout_summary), unsafe_allow_html=True)
    
    # Asset Summary
    machine_photo_count = sum(1 for machine in st.session_state.machines if machine.get('photo'))
    other_photo_count = (len(other_photos) if other_photos else 0) + (len(layout_sketches) if layout_sketches else 0)
    
    st.markdown(f"""
    <div style="background: #f8f9fa; border-radius: 8px; padding: 1.5rem; margin-top: 1rem;">
        <h3 style="color: #502DD5; margin: 0 0 1rem 0; font-weight: 500;">📸 Uploaded Assets</h3>
        <p style="margin: 0.5rem 0;"><strong>Machine photos:</strong> {machine_photo_count}</p>
        <p style="margin: 0.5rem 0;"><strong>Other photos:</strong> {other_photo_count}</p>
        <p style="margin: 0.5rem 0;"><strong>Total assets:</strong> {machine_photo_count + other_photo_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Meet Your Guidewheel Buddy Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #502DD5 0%, #32B3F1 100%); border-radius: 12px; padding: 2rem; margin: 2rem 0; text-align: center; color: white;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤝</div>
        <h2 style="color: white; margin: 0 0 1rem 0; font-weight: 600;">Meet Your Guidewheel Buddy</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem; line-height: 1.6;">
            <strong>Alex</strong> will reach out to guide your setup and answer any questions. 
            He's worked with 100+ factories and loves seeing machines come to life in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Message
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🎉</div>
        <h2 style="color: #2c3e50; margin: 0 0 0.5rem 0; font-weight: 600;">Welcome to the Guidewheel Family!</h2>
        <p style="color: #7f8c8d; margin: 0; font-size: 1.1rem;">We're excited to help you get started with intelligent machine management.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display uploaded photos in a grid
    machine_photos_to_show = [machine for machine in st.session_state.machines if machine.get('photo')]
    if machine_photos_to_show or other_photos or layout_sketches:
        st.markdown("""
        <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h3 style="color: #2c3e50; margin: 0 0 1.5rem 0; font-weight: 500;">📸 Uploaded Assets</h3>
        """, unsafe_allow_html=True)
        
        if machine_photos_to_show:
            st.subheader("Machine Photos:")
            cols = st.columns(3)
            for i, machine in enumerate(machine_photos_to_show):
                with cols[i % 3]:
                    st.image(machine['photo'], caption=f"{machine['type']}", use_column_width=True)
        
        if other_photos:
            st.subheader("Additional Photos:")
            cols = st.columns(3)
            for i, photo in enumerate(other_photos):
                with cols[i % 3]:
                    st.image(photo, caption=f"Photo {i+1}", use_column_width=True)
        
        if layout_sketches:
            st.subheader("Line Layout Sketches:")
            cols = st.columns(3)
            for i, sketch in enumerate(layout_sketches):
                with cols[i % 3]:
                    st.image(sketch, caption=f"Layout {i+1}", use_column_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True) 