import streamlit as st

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Machine Onboarding Form</h1>', unsafe_allow_html=True)

# Initialize session state for machines if not exists
if 'machines' not in st.session_state:
    st.session_state.machines = []

# Machine management buttons (outside the form)
st.markdown("""
### 🏭 Add Your Machines
Add each machine you want to include in your onboarding. You can use the magic button to pre-fill common machines, or add them one by one.
""")
col1, col2 = st.columns([2, 1])
with col1:
    if st.button("🎯 Magic: Add Common Machines", help="Quickly add a list of common machines to get started."):
        default_machines = [
            {"type": "Lathe", "model": "", "info": "", "quantity": 2},
            {"type": "Milling Machine", "model": "", "info": "", "quantity": 1},
            {"type": "Drill Press", "model": "", "info": "", "quantity": 1},
            {"type": "CNC Router", "model": "", "info": "", "quantity": 1},
            {"type": "Band Saw", "model": "", "info": "", "quantity": 1},
            {"type": "Welding Station", "model": "", "info": "", "quantity": 1}
        ]
        st.session_state.machines = default_machines
        st.markdown('<div class="stSuccess">✨ Magic activated! Common machines added.</div>', unsafe_allow_html=True)
        st.rerun()
with col2:
    st.markdown("<div style='height: 1.5em'></div>", unsafe_allow_html=True)
    if st.button("➕ **Add a New Machine**", key="add_machine", help="Add a new machine to your list."):
        st.session_state.machines.append({"type": "", "model": "", "info": "", "quantity": 1})
        st.rerun()

# Machine editing interface (outside the form)
if st.session_state.machines and ('editing_machine' in st.session_state and st.session_state.editing_machine is not None):
    edit_idx = st.session_state.editing_machine
    machine = st.session_state.machines[edit_idx]
    
    st.subheader(f"Editing Machine {edit_idx + 1}")
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
        if st.button("✅ Save Changes", key=f"save_{edit_idx}"):
            st.success(f"Machine {edit_idx + 1} updated!")
            st.session_state.editing_machine = None
            st.rerun()
    with col2:
        if st.button("❌ Cancel", key=f"cancel_{edit_idx}"):
            st.session_state.editing_machine = None
            st.rerun()

with st.form(key="onboarding_form"):
    st.header("Machine Information")
    
    # Show machine summary with edit/remove options
    if st.session_state.machines:
        st.write("**Your Machines:**")
        for i, machine in enumerate(st.session_state.machines):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                machine_summary = f"• Machine {i+1}: {machine['type']}"
                if machine['model']:
                    machine_summary += f" ({machine['model']})"
                machine_summary += f" - Qty: {machine['quantity']}"
                if machine['info']:
                    machine_summary += f" - {machine['info']}"
                if machine.get('photo'):
                    machine_summary += " 📸"
                st.write(machine_summary)
            with col2:
                if st.button(f"Edit {i+1}", key=f"form_edit_{i}"):
                    st.session_state.editing_machine = i
                    st.rerun()
            with col3:
                if st.button(f"Remove {i+1}", key=f"form_remove_{i}"):
                    st.session_state.machines.pop(i)
                    st.rerun()
    else:
        st.markdown('<div class="stInfo">Click "Add Machine" to start adding your machines, or use the Magic button for common machines.</div>', unsafe_allow_html=True)
    notes = st.text_area(
        "Optional notes:",
        placeholder="Any additional information...",
        height=80
    )
    st.header("Other Photos")
    st.write("Upload additional photos to help us understand your setup better:")
    
    other_photos = st.file_uploader(
        "📸 Upload photos (whiteboards, factory layout, safety equipment, etc.):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload any relevant photos: whiteboard diagrams, factory layouts, safety equipment, certifications, or other important documentation."
    )
    
    st.header("Line Layout")
    layout_option = st.radio(
        "How would you like to share your line layout?",
        ["I'll sketch it on a whiteboard", "I have existing sketches to upload", "Skip for now"],
        help="Choose whether you want to sketch your layout on a whiteboard during setup, or upload existing sketches/diagrams."
    )
    
    layout_sketches = None
    if layout_option == "I have existing sketches to upload":
        layout_sketches = st.file_uploader(
            "Upload your line layout sketches/diagrams:",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Upload any existing sketches, diagrams, or drawings of your production line layout."
        )
    elif layout_option == "I'll sketch it on a whiteboard":
        st.markdown('<div class="stInfo">🎨 Perfect! We\'ll have a whiteboard ready during your setup session for you to sketch your line layout.</div>', unsafe_allow_html=True)
    
    st.header("Contact Information")
    name = st.text_input("Your Name:")
    email = st.text_input("Your Email:")
    
    st.header("Invite Teammate")
    invite_teammate = st.checkbox("Invite a teammate to this onboarding?")
    teammate_name = ""
    teammate_email = ""
    
    if invite_teammate:
        teammate_name = st.text_input("Teammate's Name:")
        teammate_email = st.text_input("Teammate's Email:")
    
    submit = st.form_submit_button("Submit")

if submit:
    st.markdown('<div class="stSuccess">🎉 Form submitted successfully!</div>', unsafe_allow_html=True)
    st.balloons()
    
    st.header("Here's the install plan we'll start building for you...")
    
    # Create a summary of their setup
    st.subheader("📋 Your Setup Summary")
    
    # Layout option summary
    layout_summary = layout_option
    if layout_option == "I have existing sketches to upload" and layout_sketches:
        layout_summary += f" ({len(layout_sketches)} files)"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Contact Information:**")
        st.write(f"👤 {name}")
        st.write(f"📧 {email}")
        if invite_teammate:
            st.write(f"👥 Teammate: {teammate_name} ({teammate_email})")
    
    with col2:
        st.write("**Machine Inventory:**")
        for i, machine in enumerate(st.session_state.machines):
            machine_info = f"🔧 {machine['type']}"
            if machine['model']:
                machine_info += f" ({machine['model']})"
            machine_info += f": {machine['quantity']}"
            if machine['info']:
                machine_info += f" - {machine['info']}"
            st.write(machine_info)
    
    if notes:
        st.write("**📝 Additional Notes:**")
        st.write(notes)
    
    st.write("**🎨 Line Layout:**")
    st.write(layout_summary)
    
    st.subheader("📸 Uploaded Assets")
    # Count machine photos
    machine_photo_count = sum(1 for machine in st.session_state.machines if machine.get('photo'))
    
    # Count other photos
    other_photo_count = (len(other_photos) if other_photos else 0) + \
                       (len(layout_sketches) if layout_sketches else 0)
    
    st.write(f"Machine photos: {machine_photo_count}")
    st.write(f"Other photos: {other_photo_count}")
    st.write(f"Total photos uploaded: {machine_photo_count + other_photo_count}")
    
    st.subheader("📊 Raw Data:")
    st.write({
        "Name": name,
        "Email": email,
        "Machines": st.session_state.machines,
        "Notes": notes,
        "Machine Photos": machine_photo_count,
        "Other Photos": len(other_photos) if other_photos else 0,
        "Layout Option": layout_option,
        "Layout Sketches": len(layout_sketches) if layout_sketches else 0,
        "Teammate Invited": invite_teammate,
        "Teammate Name": teammate_name if invite_teammate else "None",
        "Teammate Email": teammate_email if invite_teammate else "None"
    })
    
    st.header("🤝 Meet Your Guidewheel Buddy")
    st.write("**Alex** will reach out to guide your setup and answer any questions. He's worked with 100+ factories and loves seeing machines come to life in real time.")
    
    # Add a nice visual separator
    st.markdown("---")
    st.write("🎉 **Welcome to the Guidewheel family!** We're excited to help you get started.")
    
    # Display uploaded photos
    # Machine photos
    machine_photos_to_show = [machine for machine in st.session_state.machines if machine.get('photo')]
    if machine_photos_to_show:
        st.subheader("Machine Photos:")
        for i, machine in enumerate(machine_photos_to_show):
            st.image(machine['photo'], caption=f"Machine {i+1}: {machine['type']}", width=300)
    
    if other_photos:
        st.subheader("Other Photos:")
        for i, photo in enumerate(other_photos):
            st.image(photo, caption=f"Photo {i+1}", width=300)
    
    if layout_sketches:
        st.subheader("Line Layout Sketches:")
        for i, sketch in enumerate(layout_sketches):
            st.image(sketch, caption=f"Layout Sketch {i+1}", width=300)

