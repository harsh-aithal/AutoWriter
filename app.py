import os
import streamlit as st
import openai
from docx import Document
import json
from dotenv import load_dotenv

# -------- Remove user data file load/save for session-specific --------
# Session-specific: No loading/saving from/to disk

load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AutoWriter", layout="centered")
st.title("AutoWriter - Resume Generator")

# Initialize session states
for key in ['user_data', 'education_entries', 'experience_entries', 'project_entries', 'certification_entries']:
    if key not in st.session_state:
        st.session_state[key] = {} if key == 'user_data' else []

tab1, tab2 = st.tabs(["1. Enter Personal Details", "2. Generate Resume (Quick Apply)"])

with tab1:
    st.header("Step 1: Enter Personal Information")

    st.subheader("Basic Info")
    user_data = st.session_state.user_data

    user_data['name'] = st.text_input("Full Name", value=user_data.get('name', ''))
    user_data['phone'] = st.text_input("Phone Number", value=user_data.get('phone', ''))
    user_data['email'] = st.text_input("Email", value=user_data.get('email', ''))
    user_data['address'] = st.text_input("Address", value=user_data.get('address', ''))
    user_data['linkedin'] = st.text_input("LinkedIn URL (Optional)", value=user_data.get('linkedin', ''))
    user_data['github'] = st.text_input("GitHub URL (Optional)", value=user_data.get('github', ''))
    user_data['experience'] = st.slider("Years of Experience", 0, 40, user_data.get('experience', 2))
    user_data['skills'] = st.text_area("Key Skills", value=user_data.get('skills', ''))
    user_data['achievements'] = st.text_area("Achievements", value=user_data.get('achievements', ''))

    st.session_state.user_data = user_data

    st.subheader("Education")
    if st.button("Add Education"):
        st.session_state.education_entries.append({"institution": "", "major": "", "date": "", "cgpa": ""})
    for i, edu in enumerate(st.session_state.education_entries):
        with st.expander(f"Education {i+1}"):
            edu['institution'] = st.text_input("Institution", value=edu.get("institution", ""), key=f"edu_inst_{i}")
            edu['major'] = st.text_input("Major", value=edu.get("major", ""), key=f"edu_major_{i}")
            edu['date'] = st.text_input("End Date (MM/YYY)", value=edu.get("date", ""), key=f"edu_date_{i}")
            edu['cgpa'] = st.text_input("CGPA", value=edu.get("cgpa", ""), key=f"edu_cgpa_{i}")
            if st.button(f"Delete Education {i+1}", key=f"delete_edu_{i}"):
                del st.session_state.education_entries[i]
                st.rerun()
                break

    st.subheader("Work Experience")
    if st.button("Add Experience"):
        st.session_state.experience_entries.append({"company": "", "role": "", "summary": "", "dates": ""})
    for i, exp in enumerate(st.session_state.experience_entries):
        with st.expander(f"Experience {i+1}"):
            exp['company'] = st.text_input("Company", value=exp.get("company", ""), key=f"exp_company_{i}")
            exp['role'] = st.text_input("Role", value=exp.get("role", ""), key=f"exp_role_{i}")
            exp['summary'] = st.text_area("Summary", value=exp.get("summary", ""), key=f"exp_summary_{i}")
            exp['dates'] = st.text_input("Start Date (MM/YYYY) - End Date (MM/YYYY)", value=exp.get("dates", ""), key=f"exp_dates_{i}")
            if st.button(f"Delete Experience {i+1}", key=f"delete_exp_{i}"):
                del st.session_state.experience_entries[i]
                st.rerun()
                break

    st.subheader("Projects")
    if st.button("Add Project"):
        st.session_state.project_entries.append({"name": "", "description": "", "tools": ""})
    for i, proj in enumerate(st.session_state.project_entries):
        with st.expander(f"Project {i+1}"):
            proj['name'] = st.text_input("Project Name", value=proj.get("name", ""), key=f"proj_name_{i}")
            proj['description'] = st.text_area("Description", value=proj.get("description", ""), key=f"proj_description_{i}")
            proj['tools'] = st.text_input("Tools Used", value=proj.get("tools", ""), key=f"proj_tools_{i}")
            if st.button(f"Delete Project {i+1}", key=f"delete_proj_{i}"):
                del st.session_state.project_entries[i]
                st.rerun()
                break

    st.subheader("Certifications")
    if st.button("Add Certification"):
        st.session_state.certification_entries.append({"name": "", "issuer": "", "date": ""})
    for i, cert in enumerate(st.session_state.certification_entries):
        with st.expander(f"Certification {i+1}"):
            cert['name'] = st.text_input("Certificate Name", value=cert.get("name", ""), key=f"cert_name_{i}")
            cert['issuer'] = st.text_input("Issued By", value=cert.get("issuer", ""), key=f"cert_issuer_{i}")
            cert['date'] = st.text_input("Issue Date (MM/YYY)", value=cert.get("date", ""), key=f"cert_date_{i}")
            if st.button(f"Delete Certificate {i+1}", key=f"delete_cert_{i}"):
                del st.session_state.certification_entries[i]
                st.rerun()
                break
    st.success("Details saved. Go to next tab to generate resume.")
    if st.button("Clear All Data"):
        for key in ['user_data', 'education_entries', 'experience_entries', 'project_entries', 'certification_entries']:
            st.session_state[key] = {} if key == 'user_data' else []
        st.rerun()

with tab2:
    st.header("Step 2: Paste Job Description & Generate Resume")
    job_description = st.text_area("Paste Job Title & Description here")

    if st.button("Generate Resume"):
        with st.spinner("Generating resume..."):
            user = st.session_state.user_data
            required_fields = ['name', 'phone', 'email']
            if not all(user.get(field) for field in required_fields):
                st.error("Please complete all required personal details before generating the resume.")
            else:
                education_str = "\n".join(
                    f"{e['institution']} | {e['major']} | {e['date']} | CGPA: {e['cgpa']}"
                    for e in st.session_state.education_entries if e['institution'].strip()
                )
                experience_str = "\n".join(
                    f"{e['company']} | {e['role']} | {e['summary']} | {e['dates']}"
                    for e in st.session_state.experience_entries if e['company'].strip()
                )
                projects_str = "\n".join(
                    f"{p['name']} | {p['description']} | Tools Used: {p['tools']}"
                    for p in st.session_state.project_entries if p['name'].strip()
                )
                certifications_str = "\n".join(
                    f"{c['name']} | Issued By: {c['issuer']} | Date: {c['date']}"
                    for c in st.session_state.certification_entries if c['name'].strip()
                )

                prompt = f"""
                You are an expert resume writer. Tailor the resume below based on the provided job description.

                Follow these strict instructions:

                1. Structure the resume in this exact order:
                    - Personal Details (Name, Phone, Email, LinkedIn, GitHub)
                    - Professional Summary (3–4 lines tailored to the job)
                    - Key Skills (from user's skills + relevant keywords from JD)
                    - Work Experience (impact-driven, ATS-friendly, tailored)
                        - Role
                        - Company
                        - Date
                    - Projects (highlight relevant tools/tech from JD)
                    - Education
                    - Certifications (if any)
                    - Achievements (only if not already in Experience/Projects)

                2. Tailor the resume using the job description:
                    - Insert relevant keywords, tools, or skills from the JD.
                    - Highlight achievements with measurable results.
                    - Reword content to better match job requirements.
                    - Make the resume clean, concise, and professional.

                3. Formatting Rules:
                    - No markdown symbols (** ## etc.)
                    - Use simple section headers and line breaks.
                    - Do NOT include the job description or extra commentary.
                    - Output only the resume text.

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
                Generate only the tailored resume content.
                """

                try:
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5,
                        max_tokens=1600
                    )
                    resume_text = response.choices[0].message.content.strip()
                    st.session_state.final_resume = resume_text

                    st.subheader("Generated Resume")
                    edited_text = st.text_area("This is AI generated content, make sure to review and edit it properly before using it anywhere.", value=resume_text, height=400)

                    # Clean up formatting and export
                    doc = Document()
                    for line in edited_text.splitlines():
                        if line.strip():
                            doc.add_paragraph(line.strip())

                    file_safe_name = user['name'].strip().replace(' ', '_') or "Resume"
                    filename = f"{file_safe_name}_resume.docx"
                    doc.save(filename)

                    with open(filename, "rb") as f:
                        st.download_button(
                            label="Download as Word (.docx)",
                            data=f.read(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    os.remove(filename)

                except Exception as e:
                    st.error(f"Error generating resume: {e}")