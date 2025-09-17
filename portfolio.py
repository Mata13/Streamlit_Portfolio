import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Mi Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for MaterializeCSS styling


def load_css():
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    
    .profile-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .skill-chip {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        margin: 4px;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .project-card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
    }
    
    .section-title {
        color: #667eea;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
    }
    
    .profile-image {
        border-radius: 50%;
        width: 200px;
        height: 200px;
        object-fit: cover;
        border: 5px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .contact-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .education-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data functions


@st.cache_data
def load_profile_data():
    try:
        df = pd.read_csv('Data/profile.csv')
        return df.iloc[0].to_dict()
    except Exception as e:
        st.error(f"Error loading profile data: {e}")
        return {}


@st.cache_data
def load_skills_data():
    try:
        return pd.read_csv('Data/skills.csv')
    except Exception as e:
        st.error(f"Error loading skills data: {e}")
        return pd.DataFrame()


@st.cache_data
def load_projects_data():
    try:
        return pd.read_csv('Data/projects.csv')
    except Exception as e:
        st.error(f"Error loading projects data: {e}")
        return pd.DataFrame()


@st.cache_data
def load_education_data():
    try:
        return pd.read_csv('Data/education.csv')
    except Exception as e:
        st.error(f"Error loading education data: {e}")
        return pd.DataFrame()


@st.cache_data
def load_stem_data():
    try:
        return pd.read_csv('Data/STEM.csv')
    except Exception as e:
        st.error(f"Error loading STEM data: {e}")
        return pd.DataFrame()

# Main app


def main():
    load_css()

    # Load data
    profile = load_profile_data()
    skills_df = load_skills_data()
    projects_df = load_projects_data()
    education_df = load_education_data()
    stem_df = load_stem_data()

    # Sidebar navigation
    st.sidebar.title("🚀 Navegación")
    page = st.sidebar.selectbox(
        "Selecciona una sección:",
        ["🏠 Inicio", "💼 Proyectos", "🎓 Educación", "🔬 STEM", "📞 Contacto"]
    )

    if page == "🏠 Inicio":
        show_home(profile, skills_df)
    elif page == "💼 Proyectos":
        show_projects(projects_df)
    elif page == "🎓 Educación":
        show_education(education_df)
    elif page == "🔬 STEM":
        show_stem(stem_df)
    elif page == "📞 Contacto":
        show_contact(profile)


def show_home(profile, skills_df):
    # Header section
    st.markdown("""
    <div class="main-header">
        <div class="container">
            <h1 style="color: white; text-align: center; font-size: 3rem; margin: 0;">
                ¡Bienvenido a mi Portfolio! 🚀
            </h1>
            <p style="color: white; text-align: center; font-size: 1.2rem; margin-top: 1rem;">
                Desarrollador Full Stack | Data Scientist | Innovador
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Profile section
    col1, col2 = st.columns([1, 2])

    with col1:
        if profile and 'image' in profile:
            image_name = profile['image']
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="static/public/{image_name}" class="profile-image" alt="Profile Picture">
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="profile-card">
            <h2 style="color: #667eea; margin-bottom: 1rem;">
                {profile.get('name', 'Tu Nombre')} 👋
            </h2>
            <h4 style="color: #666; margin-bottom: 1.5rem;">
                {profile.get('title', 'Tu Título Profesional')}
            </h4>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #444;">
                {profile.get('description', 'Tu descripción profesional aquí...')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Skills section
    st.markdown('<h2 class="section-title">🛠️ Habilidades Técnicas</h2>',
                unsafe_allow_html=True)

    if not skills_df.empty:
        # Group skills by category
        categories = skills_df['category'].unique()

        for category in categories:
            st.markdown(f"### {category}")
            category_skills = skills_df[skills_df['category'] == category]

            skills_html = ""
            for _, skill in category_skills.iterrows():
                skills_html += f'<span class="skill-chip">{skill["skill"]} - {skill["level"]}</span>'

            st.markdown(
                f'<div style="margin: 1rem 0;">{skills_html}</div>', unsafe_allow_html=True)


def show_projects(projects_df):
    st.markdown('<h1 class="section-title">💼 Mis Proyectos</h1>',
                unsafe_allow_html=True)

    if not projects_df.empty:
        for _, project in projects_df.iterrows():
            st.markdown(f"""
            <div class="project-card">
                <div style="padding: 2rem;">
                    <h3 style="color: #667eea; margin-bottom: 1rem;">
                        {project.get('title', 'Título del Proyecto')}
                    </h3>
                    <p style="color: #666; margin-bottom: 1rem;">
                        <strong>Tecnologías:</strong> {project.get('technologies', 'N/A')}
                    </p>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">
                        {project.get('description', 'Descripción del proyecto...')}
                    </p>
                    <div style="display: flex; gap: 1rem;">
                        <a href="{project.get('github_url', '#')}" target="_blank" 
                           style="background: #667eea; color: white; padding: 10px 20px; 
                                  border-radius: 5px; text-decoration: none;">
                            <i class="material-icons" style="vertical-align: middle;">code</i> GitHub
                        </a>
                        <a href="{project.get('demo_url', '#')}" target="_blank" 
                           style="background: #764ba2; color: white; padding: 10px 20px; 
                                  border-radius: 5px; text-decoration: none;">
                            <i class="material-icons" style="vertical-align: middle;">launch</i> Demo
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay proyectos disponibles en este momento.")


def show_education(education_df):
    st.markdown('<h1 class="section-title">🎓 Educación</h1>',
                unsafe_allow_html=True)

    if not education_df.empty:
        for _, edu in education_df.iterrows():
            st.markdown(f"""
            <div class="education-card">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">
                    {edu.get('degree', 'Título')}
                </h3>
                <h4 style="color: #764ba2; margin-bottom: 0.5rem;">
                    {edu.get('institution', 'Institución')}
                </h4>
                <p style="color: #666; margin-bottom: 1rem;">
                    <i class="material-icons" style="vertical-align: middle; font-size: 1rem;">date_range</i>
                    {edu.get('period', 'Período')}
                </p>
                <p style="line-height: 1.6;">
                    {edu.get('description', 'Descripción de la educación...')}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay información educativa disponible.")


def show_stem(stem_df):
    st.markdown('<h1 class="section-title">🔬 Experiencia STEM</h1>',
                unsafe_allow_html=True)

    if not stem_df.empty:
        for _, stem in stem_df.iterrows():
            st.markdown(f"""
            <div class="project-card">
                <div style="padding: 2rem;">
                    <h3 style="color: #667eea; margin-bottom: 1rem;">
                        {stem.get('title', 'Título STEM')}
                    </h3>
                    <p style="color: #666; margin-bottom: 1rem;">
                        <strong>Área:</strong> {stem.get('area', 'N/A')} | 
                        <strong>Fecha:</strong> {stem.get('date', 'N/A')}
                    </p>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">
                        {stem.get('description', 'Descripción de la experiencia STEM...')}
                    </p>
                    {f'<p style="color: #667eea;"><strong>Resultados:</strong> {stem.get("results", "")}</p>' if stem.get("results") else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay experiencia STEM disponible.")


def show_contact(profile):
    st.markdown('<h1 class="section-title">📞 Contacto</h1>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="contact-info">
            <h3 style="margin-bottom: 1.5rem;">
                <i class="material-icons" style="vertical-align: middle;">contact_mail</i>
                Información de Contacto
            </h3>
            <p style="margin-bottom: 1rem;">
                <i class="material-icons" style="vertical-align: middle;">email</i>
                <strong>Email:</strong> {profile.get('email', 'tu@email.com')}
            </p>
            <p style="margin-bottom: 1rem;">
                <i class="material-icons" style="vertical-align: middle;">phone</i>
                <strong>Teléfono:</strong> {profile.get('phone', '+1234567890')}
            </p>
            <p style="margin-bottom: 1rem;">
                <i class="material-icons" style="vertical-align: middle;">location_on</i>
                <strong>Ubicación:</strong> {profile.get('location', 'Tu Ciudad, País')}
            </p>
            <div style="margin-top: 2rem;">
                <a href="{profile.get('linkedin', '#')}" target="_blank" 
                   style="color: white; margin-right: 1rem; font-size: 1.5rem;">
                    LinkedIn
                </a>
                <a href="{profile.get('github', '#')}" target="_blank" 
                   style="color: white; margin-right: 1rem; font-size: 1.5rem;">
                    GitHub
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <h3 style="color: #667eea; margin-bottom: 1.5rem;">
                <i class="material-icons" style="vertical-align: middle;">send</i>
                Envíame un mensaje
            </h3>
        """, unsafe_allow_html=True)

        # Contact form
        with st.form("contact_form"):
            name = st.text_input("Nombre")
            email = st.text_input("Email")
            subject = st.text_input("Asunto")
            message = st.text_area("Mensaje", height=150)

            if st.form_submit_button("Enviar Mensaje"):
                if name and email and message:
                    st.success(
                        "¡Mensaje enviado correctamente! Te contactaré pronto.")
                else:
                    st.error("Por favor, completa todos los campos obligatorios.")

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
