import os
import streamlit as st
import openai
from docx import Document
import base64
import json

def save_user_data():
    with open("userdata.json", "w") as f:
        json.dump({
            "user_data": st.session_state.user_data,
            "education_entries": st.session_state.education_entries,
            "experience_entries": st.session_state.experience_entries,
            "project_entries": st.session_state.project_entries,
            "certification_entries": st.session_state.certification_entries
        }, f)

def load_user_data():
    if os.path.exists("userdata.json"):
        with open("userdata.json", "r") as f:
            data = json.load(f)
            st.session_state.user_data = data.get("user_data", {})
            st.session_state.education_entries = data.get("education_entries", [])
            st.session_state.experience_entries = data.get("experience_entries", [])
            st.session_state.project_entries = data.get("project_entries", [])
            st.session_state.certification_entries = data.get("certification_entries", [])

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AutoWriter", layout="centered")
if "details_saved" not in st.session_state:
    st.session_state["details_saved"] = False

if not st.session_state.get("data_loaded", False):
    load_user_data()
    st.session_state["data_loaded"] = True
st.title("AutoWriter - Resume Generator")

# Initialize session states
for key in ['user_data', 'education_entries', 'experience_entries', 'project_entries', 'certification_entries']:
    if key not in st.session_state:
        st.session_state[key] = []

tab1, tab2 = st.tabs(["1. Enter Personal Details", "2. Generate Resume (Quick Apply)"])

with tab1:
    st.header("Step 1: Enter Personal Information")

    st.subheader("Basic Info")
    user_data = st.session_state.user_data if st.session_state.user_data else {}

    user_data['name'] = st.text_input("Full Name", value=user_data.get('name', ''))
    user_data['phone'] = st.text_input("Phone Number", value=user_data.get('phone', ''))
    user_data['email'] = st.text_input("Email", value=user_data.get('email', ''))
    user_data['address'] = st.text_input("Address", value=user_data.get('address', ''))
    user_data['linkedin'] = st.text_input("LinkedIn URL", value=user_data.get('linkedin', ''))
    user_data['github'] = st.text_input("GitHub URL", value=user_data.get('github', ''))
    user_data['experience'] = st.slider("Years of Experience", 0, 40, user_data.get('experience', 2))
    user_data['skills'] = st.text_area("Key Skills", value=user_data.get('skills', ''))
    user_data['achievements'] = st.text_area("Achievements", value=user_data.get('achievements', ''))

    st.session_state.user_data = user_data

    # Education
    st.subheader("Education")
    if st.button("Add Education"):
        st.session_state.education_entries.append({"institution": "", "major": "", "date": "", "cgpa": ""})
    for i, edu in enumerate(st.session_state.education_entries):
        with st.expander(f"Education {i+1}"):
            edu['institution'] = st.text_input(f"Institution", value=edu.get("institution", ""), key=f"edu_inst_{i}")
            edu['major'] = st.text_input(f"Major", value=edu.get("major", ""), key=f"edu_major_{i}")
            edu['date'] = st.text_input(f"Date", value=edu.get("date", ""), key=f"edu_date_{i}")
            edu['cgpa'] = st.text_input(f"CGPA", value=edu.get("cgpa", ""), key=f"edu_cgpa_{i}")

            if st.button(f"Delete Education {i+1}", key=f"delete_edu_{i}"):
                del st.session_state.education_entries[i]
                st.rerun() 
                break

    # Experience
    st.subheader("Work Experience")
    if st.button("Add Experience"):
        st.session_state.experience_entries.append({"company": "", "role": "", "summary": "", "dates": ""})
    for i, exp in enumerate(st.session_state.experience_entries):
        with st.expander(f"Experience {i+1}"):
            exp['company'] = st.text_input(f"Company", value=exp.get("company", ""), key=f"exp_company_{i}")
            exp['role'] = st.text_input(f"Role", value=exp.get("role", ""), key=f"exp_role_{i}")
            exp['summary'] = st.text_area(f"Summary", value=exp.get("summary", ""), key=f"exp_summary_{i}")
            exp['dates'] = st.text_input(f"Start Date (MM/YYYY) - End Date (MM/YYYY)", value=exp.get("dates", ""), key=f"exp_dates_{i}")

            if st.button(f"Delete Experience {i+1}", key=f"delete_exp_{i}"):
                del st.session_state.experience_entries[i]
                st.rerun()
                break

    # Projects
    st.subheader("Projects")
    if st.button("Add Project"):
        st.session_state.project_entries.append({"name": "", "description": "", "tools": ""})
    for i, proj in enumerate(st.session_state.project_entries):
        with st.expander(f"Project {i+1}"):
            proj['name'] = st.text_input(f"Project Name", value=proj.get("name", ""), key=f"proj_name_{i}")
            proj['description'] = st.text_area(f"Description", value=proj.get("description", ""), key=f"proj_description_{i}")
            proj['tools'] = st.text_input(f"Tools Used", value=proj.get("tools", ""), key=f"proj_tools_{i}")

            if st.button(f"Delete Project {i+1}", key=f"delete_proj_{i}"):
                del st.session_state.project_entries[i]
                st.rerun()  # Needed to update the UI after deletion
                break

    # Certifications
    st.subheader("Certifications")
    if st.button("Add Certification"):
        st.session_state.certification_entries.append({"name": "", "issuer": "", "date": ""})
    for i, cert in enumerate(st.session_state.certification_entries):
        with st.expander(f"Certification {i+1}"):
            cert['name'] = st.text_input(f"Certificate Name", value=cert.get("name", ""), key=f"cert_name_{i}")
            cert['issuer'] = st.text_input(f"Issued By", value=cert.get("issuer", ""), key=f"cert_issuer_{i}")
            cert['date'] = st.text_input(f"Issue Date", value=cert.get("date", ""), key=f"cert_date_{i}")

            if st.button(f"Delete Certificate {i+1}", key=f"delete_cert_{i}"):
                del st.session_state.certification_entries[i]
                st.rerun()  # Needed to update the UI after deletion
                break

    if st.button("Save Details"):
        save_user_data()
        st.session_state["details_saved"] = True

    if st.session_state.get("details_saved"):
        st.success("Details saved. Go to next tab to generate resume.")

    if st.button("Clear All Data"):
        for key in ['user_data', 'education_entries', 'experience_entries', 'project_entries', 'certification_entries']:
            st.session_state[key] = []
        if os.path.exists("userdata.json"):
            os.remove("userdata.json")
        st.session_state["details_saved"] = False
        st.session_state["data_loaded"] = False
        st.rerun()

with tab2:
    st.header("Step 2: Paste Job Description & Generate Resume")

    job_description = st.text_area("Paste Job Description here")

    if st.button("Generate Resume"):
        with st.spinner("Generating resume..."):
            user = st.session_state.user_data
            # Format education entries
            education_str = ""
            for edu in st.session_state.education_entries:
                if edu['institution'].strip():
                    education_str += f"{edu['institution']} | {edu['major']} | {edu['date']} | CGPA: {edu['cgpa']}\n"

            # Format experience entries
            experience_str = ""
            for exp in st.session_state.experience_entries:
                if exp['company'].strip():
                    experience_str += f"{exp['company']} | {exp['role']} | {exp['summary']} | {exp['dates']}\n"

            # Format project entries
            projects_str = ""
            for proj in st.session_state.project_entries:
                if proj['name'].strip():
                    projects_str += f"{proj['name']} | {proj['description']} | Tools Used: {proj['tools']}\n"

            # Format certifications
            certifications_str = ""
            for cert in st.session_state.certification_entries:
                if cert['name'].strip():
                    certifications_str += f"{cert['name']} | Issued By: {cert['issuer']} | Date: {cert['date']}\n"
            prompt = f"""
            You are an expert resume writer. Tailor the resume below based on the provided job description.

            Follow these strict instructions:

            1. *Structure the resume in this exact order*:
                - Personal Details (Name, Phone, Email, LinkedIn, GitHub)
                - Professional Summary (3–4 lines tailored to the job)
                - Key Skills (from user's skills + relevant keywords from JD)
                - Work Experience (impact-driven, ATS-friendly, tailored)
                - Projects (highlight relevant tools/tech from JD)
                - Education
                - Certifications (if any)
                - Achievements (only if not already in Experience/Projects)

            2. *Tailor the resume using the job description*:
                - Insert relevant keywords, tools, or skills from the JD.
                - Highlight achievements with measurable results.
                - Reword content to better match job requirements.
                - Make the resume clean, concise, and professional.

            3. *Formatting Rules*:
                - No markdown symbols (** ## etc.)
                - Use simple section headers and line breaks.
                - Do NOT include the job description or extra commentary.
                - Output only the resume text.

            ---

            User Info:
            Name: {user['name']}
            Phone: {user['phone']}
            Email: {user['email']}
            Address: {user['address']}
            LinkedIn: {user['linkedin']}
            GitHub: {user['github']}
            Experience: {user['experience']} years
            Skills: {user['skills']}
            Achievements: {user['achievements']}

            Education:
            {education_str}

            Experience:
            {experience_str}

            Projects:
            {projects_str}

            Certifications:
            {certifications_str}

            Job Description:
            {job_description}

            ---

            Generate only the tailored resume content in the order above.
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert resume writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1200
                )
                resume_text = response["choices"][0]["message"]["content"]

                st.subheader("Generated Resume")
                edited_text = st.text_area("Edit Resume Before Downloading", value=resume_text, height=400)

                # Create .docx
                doc = Document()
                for line in edited_text.strip().split("\n"):
                    doc.add_paragraph(line.strip())
                filename = f"{user['name'].strip().replace(' ', '_')}_resume.docx"
                doc.save(filename)

                # Download button
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download as Word (.docx)",
                        data=f.read(),  # Raw binary data, not base64
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                os.remove(filename)

            except Exception as e:
                st.error(f"Error generating resume: {e}")