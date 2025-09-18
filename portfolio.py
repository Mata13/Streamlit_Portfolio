import streamlit as st
import pandas as pd
from pyairtable import Api  # Solo para el formulario de contacto
from datetime import datetime
import base64
import os

# Configuración de la página
st.set_page_config(
    page_title="Marc - Portfolio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargamos la fecha actual
today = datetime.today().strftime("%Y")

# Cargamos librerías de MaterializeCSS, Material Icons y Font Awesome usando markdown
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">', unsafe_allow_html=True)
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
            unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" integrity="sha512-Evv84Mr4kqVGRNSgIGL/F/aIDqQb7xQ2vcrdIwxfjThSH8CSR7PBEakCr51Ck+w+/U6swU2Im1vVX0SVk9ABhg==" crossorigin="anonymous" referrerpolicy="no-referrer" />', unsafe_allow_html=True)

# Adicionamos estilos personalizados para mejorar el diseño
customStyle = """
	<style type = "text/css">
		/* Aumenta el tamaño de las cards */
		.card.large{
			height:550px!important;
		}
		/* Aumenta el contenido disponible */
		.card.large .card-content{
			max-height:fit-content!important;
		}
		/* Aumenta la fuente de los tabs de Streamlit */
		button[data-baseweb="tab"] p{
			font-size:20px!important;
		}
		/* Remueve el espacio en el encabezado por defecto de las apps de Streamlit */
		div[data-testid="stAppViewBlockContainer"]{
			padding-top:0px;
		}
    /* Color gradiente del fondo de la pantalla, si lo comentas se cambia el color a blanco */
    .stApp {
      background: linear-gradient(90deg, hsla(186, 33%, 94%, 1) 0%, hsla(216, 41%, 79%, 1) 100%) !important;
    }
  </style>
"""

# Cargamos los estilos
st.html(customStyle)

# ========== NUEVA FUNCIÓN PARA CONVERTIR IMÁGENES A BASE64 ==========


def image_to_base64(image_path):
    """Convierte una imagen a base64 para embedding en HTML"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode()

                # Detectar el tipo de imagen por extensión
                if image_path.lower().endswith(('.png', '.PNG')):
                    return f"data:image/png;base64,{img_base64}"
                elif image_path.lower().endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
                    return f"data:image/jpeg;base64,{img_base64}"
                elif image_path.lower().endswith(('.gif', '.GIF')):
                    return f"data:image/gif;base64,{img_base64}"
                elif image_path.lower().endswith(('.webp', '.WEBP')):
                    return f"data:image/webp;base64,{img_base64}"
                else:
                    # Por defecto asumimos JPEG
                    return f"data:image/jpeg;base64,{img_base64}"
        else:
            st.warning(f"⚠️ Imagen no encontrada: {image_path}")
            return None
    except Exception as e:
        st.error(f"❌ Error procesando imagen {image_path}: {e}")
        return None

# ========== FUNCIONES PARA CSV (SIN CAMBIOS) ==========


@st.cache_data(ttl=82800)  # Cache por 23 horas
def load_csv(table_name):
    """Carga un CSV desde la carpeta Data"""
    try:
        df = pd.read_csv(f"Data/{table_name}.csv")
        return df
    except Exception as e:
        st.error(f"Error cargando {table_name}.csv: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=82800)  # Cache por 23 horas
def get_profile_data():
    """Obtiene el primer registro del CSV profile y procesa la imagen"""
    try:
        profile_df = load_csv("profile")
        if not profile_df.empty:
            profile = profile_df.iloc[0].to_dict()

            # Procesar campo Picture para extraer solo el nombre del archivo
            picture_raw = profile.get("Picture", "")
            if isinstance(picture_raw, str) and picture_raw.strip():
                profile["Picture"] = picture_raw.split()[0]  # 'perfil.jpg'
            else:
                profile["Picture"] = "placeholder.jpg"

            return profile
        return {}
    except Exception as e:
        st.error(f"Error cargando perfil: {e}")
        return {}

# ========== FUNCIÓN PARA CONTACTO (MANTIENE AIRTABLE) ==========


# Verificación de API Key solo para contacto
if "AIRTABLE_API_KEY" not in st.secrets:
    st.error(
        "⚠️ No se encontró la API key en los secrets. El formulario de contacto no funcionará.")
    AIRTABLE_API_KEY = None
else:
    AIRTABLE_API_KEY = st.secrets.AIRTABLE_API_KEY

# Seleccionamos el base id de Airtable (solo para contacto)
AIRTABLE_BASE_ID = 'appGyrt1M9uOvi9cr'


def create_contact(name, email, phone, notes):
    """Crea un nuevo contacto en Airtable"""
    if not AIRTABLE_API_KEY:
        st.error("No se puede enviar el mensaje: API key no configurada")
        return False

    try:
        api = Api(AIRTABLE_API_KEY)
        table = api.table(AIRTABLE_BASE_ID, 'contacts')
        table.create({"Name": name, "Email": email,
                     "PhoneNumber": phone, "Notes": notes})
        return True
    except Exception as e:
        st.error(f"Error enviando mensaje: {e}")
        return False

# ========== CARGA DE DATOS DESDE CSV ==========


# Extraemos los valores recuperados del CSV "profile"
profile = get_profile_data()

# Valores de la sección "Profile"
name = profile.get('Name', 'Nombre no disponible')
profileDescription = profile.get('Description', 'Descripción no disponible')
profileTagline = profile.get('Tagline', 'Tagline no disponible')
linkedInLink = profile.get('Linkedin', '#')
githubLink = profile.get('GitHub', '#')
instagramLink = profile.get('Instagram', '#')

# ========== PROCESAMIENTO DE IMAGEN DE PERFIL CON BASE64 ==========
picture_filename = profile.get('Picture', 'placeholder.jpg')
picture_path = f"Images/{picture_filename}"
picture_base64 = image_to_base64(picture_path)

# Si no se pudo cargar la imagen, usar un placeholder o mostrar error
if picture_base64 is None:
    picture_base64 = ""  # Imagen vacía, se puede manejar en el HTML
    st.warning(f"⚠️ No se pudo cargar la imagen de perfil: {picture_path}")

# Creamos la plantilla de "Perfil" con las clases CSS de MaterializeCSS
profileHTML = f"""
  <div class="row center-align profile-card">
    <h1> {name} <span class = "blue-text text-darken-3"> Portfolio </span></h1>
    <h5> {profileTagline} </h5>
  </div>
  <div class="row profile-card">
    <div class="col s12">
      <div class="card hoverable">
        <div class="card-content">
          <div class="row valign-wrapper">
            <!-- Imagen con tamaño controlado -->
            <div class="col s12 m3 center-align">
              {f'<img src="{picture_base64}" alt="Profile picture" class="circle responsive-img profile-img">' if picture_base64 else '<div class="circle responsive-img profile-img" style="background-color: #e0e0e0; display: flex; align-items: center; justify-content: center;"><i class="material-icons" style="font-size: 4rem; color: #9e9e9e;">person</i></div>'}
            </div>

            <!-- Descripción con clase para estilizar -->
            <div class="col s12 m9">
              <span class="card-title">About me</span>
              <p class="profile-desc">{profileDescription}</p>
              <div class="card-action social-icons">
                <a href="{linkedInLink}" class="blue-text text-darken-3" target="_blank"><i class="fa-brands fa-linkedin fa-2xl"></i></a>
                <a href="{githubLink}" class="blue-text text-darken-3" target="_blank"><i class="fa-brands fa-github fa-2xl"></i></a>
                <a href="{instagramLink}" class="blue-text text-darken-3" target="_blank"><i class="fa-brands fa-instagram fa-2xl"></i></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

# CSS responsivo específico para perfil y mejoras de iconos y texto
st.markdown(
    """
    <style>
    /* Base styling */
    .profile-card .profile-img {
        width: 250px;
        height: 250px;
        object-fit: cover;
    }
    .profile-card .profile-desc {
        font-size: 1.5rem;
        line-height: 1.6;
    }
    /* Espaciado horizontal entre iconos */
    .social-icons a {
        margin-right: 1rem;
        display: inline-block;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .profile-card .profile-img {
            width: 150px !important;
            height: 150px !important;
        }
        .profile-card .profile-desc {
            font-size: 1.3rem !important;
            line-height: 1.5 !important;
        }
    }
    @media (max-width: 480px) {
        .profile-card .profile-img {
            width: 100px !important;
            height: 100px !important;
        }
        .profile-card .profile-desc {
            font-size: 1.2rem !important;
            line-height: 1.4 !important;
        }
        .profile-card h1 {
            font-size: 1.8rem !important;
        }
        .profile-card h5 {
            font-size: 1rem !important;
        }
        /* Ajuste de iconos en móvil: menos espacio y tamaño reducido */
        .social-icons a {
            margin-right: 0.5rem !important;
        }
        .social-icons i {
            font-size: 1.5rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostramos el HTML generado
st.html(profileHTML)

# Creamos los tabs de Streamlit
tabSkills, tabPortfolio, tabEducation, tabSTEM, tabContact = st.tabs(
    ['My skills', 'My projects', 'Education', 'STEM Content Creation & Outreach', 'Contact'])

# Cards "Skills" con las clases CSS de MaterializeCSS
with tabSkills:
    # Construimos el HTML de todas las cards de skill
    cards = []

    # CSS personalizado solo para esta sección
    st.markdown("""
    <style>
        /* Estilos base para la descripción */
        .skill-card .card-content p {
            font-size: 1.3rem !important;
            line-height: 1.5;
            max-height: none;
            overflow-y: hidden;
            padding-right: 0;
        }

        /* Ajustes para móviles (hasta 600px) */
        @media (max-width: 600px) {
            .skill-card .card-content p {
                font-size: 1.1rem !important;
                max-height: 120px; /* Aumenté la altura para móviles */
                overflow-y: auto;
                padding-right: 10px;
            }
        }

        /* Ajustes para tablets (entre 601px y 992px) */
        @media (min-width: 601px) and (max-width: 992px) {
            .skill-card .card-content p {
                font-size: 1.2rem !important;
                max-height: 180px; /* Aumenté la altura para tablets */
                overflow-y: auto;
                padding-right: 10px;
            }
        }

        /* Ajustes para pantallas medianas/grandes (entre 993px y 1996px) */
        @media (min-width: 993px) and (max-width: 1996px) {
            .skill-card .card-content p {
                font-size: 1.3rem !important;
                max-height: 220px; /* Aumenté la altura para este rango */
                overflow-y: auto;
                padding-right: 10px;
            }
        }

        /* Ajustes de margen para móviles */
        @media (max-width: 600px) {
            .skill-card {
                margin-bottom: 20px !important;
            }
        }

        /* Scrollbar personalizada (opcional) */
        .skill-card ::-webkit-scrollbar {
            width: 5px;
        }
        .skill-card ::-webkit-scrollbar-thumb {
            background-color: #0288d1;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Obtenemos los datos de skills desde CSV
    skills_df = load_csv('skills')

    for _, skill in skills_df.iterrows():
        # Obtenemos datos con valores por defecto
        skill_name = skill.get('Name', 'Habilidad sin nombre')
        skill_description = skill.get('Notes', 'Descripción no disponible')

        # Plantilla mejorada
        card_html = f"""
        <div class = "col s12 m4 l3 skill-card">  <div class="card small light-blue darken-3 hoverable">
                <div class = "card-content white-text">
                    <span class = "card-title"> {skill_name} </span>
                    <p>
                      {skill_description}
                    </p>
                </div>
            </div>
        </div>
        """
        cards.append(card_html)

    # Unimos todas las cards en un grid responsive
    container = f"""
    <div class = "row">
      {''.join(cards)}
    </div>
    """

    # Mostramos los skills
    st.html(container)

# Cards "Projects" con las clases CSS de MaterializeCSS
with tabPortfolio:
    projects = ""

    # CSS personalizado solo para esta sección
    st.markdown("""
    <style>
    /* Estilos para el contenedor de las cards */
    .projects-container {
        display: flex;
        flex-wrap: wrap; /* Permite que las cards pasen a la siguiente línea */
        gap: 15px; /* Espacio entre las cards */
    }

    /* Estilos base para la card */
    .project-card {
        width: calc(33.333% - 15px); /* Aproximadamente 3 cards por fila en pantallas grandes */
        margin-bottom: 20px; /* Espacio vertical entre filas de cards */
    }

    /* Ajustes para pantallas medianas */
    @media (max-width: 992px) {
        .project-card {
            width: calc(50% - 15px); /* 2 cards por fila en pantallas medianas */
        }
    }

    /* Ajustes para móviles */
    @media (max-width: 600px) {
        .project-card {
            width: 100%; /* 1 card por fila en móviles */
        }
    }

    /* Estilos del contenido de la card */
    .project-description {
        font-size: 1.3rem !important;
        line-height: 1.6;
        max-height: 150px;
        overflow-y: auto;
        padding-right: 10px;
    }

    /* Scrollbar personalizada */
    .project-card ::-webkit-scrollbar {
        width: 5px;
    }
    .project-card ::-webkit-scrollbar-thumb {
        background-color: #0288d1;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Obtenemos los datos de projects desde CSV
    projects_df = load_csv('projects')

    for _, project_data in projects_df.iterrows():
        # Extracción de datos
        projectName = project_data.get('Name', 'Project Name')
        projectDescription = project_data.get(
            'Description', 'No description available')

        # Manejo de Skills y Knowledge (vienen separados por comas en tu CSV)
        projectSkils_raw = project_data.get('Skills', '')
        projectKnowledge_raw = project_data.get('Knowledge', '')

        # Convertir a lista usando comas como separador
        if isinstance(projectSkils_raw, str):
            projectSkils = [s.strip()
                            for s in projectSkils_raw.split(',') if s.strip()]
        else:
            projectSkils = []

        if isinstance(projectKnowledge_raw, str):
            projectKnowledge = [
                k.strip() for k in projectKnowledge_raw.split(',') if k.strip()]
        else:
            projectKnowledge = []

        projectLink = project_data.get('Link', '#')

        # ========== PROCESAMIENTO DE IMAGEN DEL PROYECTO CON BASE64 ==========
        image_raw = project_data.get('Image', '')
        if isinstance(image_raw, str) and image_raw.strip():
            # Nos quedamos sólo con el nombre antes del espacio o paréntesis
            image_file = image_raw.split()[0]
            project_image_path = f"Images/{image_file}"
            project_image_base64 = image_to_base64(project_image_path)
        else:
            project_image_base64 = None

        # Si no se pudo cargar la imagen, usar placeholder
        if project_image_base64 is None:
            # Crear un placeholder visual
            image_html = '''
            <div style="height:200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        display: flex; align-items: center; justify-content: center; color: white;">
                <i class="material-icons" style="font-size: 4rem;">image</i>
            </div>
            '''
        else:
            image_html = f'''
            <img src="{project_image_base64}" style="object-fit: cover; height:100%; width:100%;">
            '''

        # Generación de chips
        skillsHTML = "".join(
            [f'<div class="chip green lighten-4">{p}</div>' for p in projectSkils])
        knowledgeHTML = "".join(
            [f'<div class="chip blue lighten-4">{p}</div>' for p in projectKnowledge])

        # Plantilla mejorada
        projectHTML = f"""
        <div class="card hoverable" style="height: auto; min-height: 400px;">
            <div class="card-image" style="height:200px; overflow:hidden;">
                <a href="{projectLink}" target="_blank">
                    {image_html}
                </a>
            </div>
            <div class="card-content" style="padding: 20px;">
                <span class="card-title" style="font-size: 1.5rem !important; margin-bottom: 15px;">{projectName}</span>
                <p class="project-description">{projectDescription}</p>
                <div class="row hide-on-small-only">
                    <div class="col s12 m6">
                        <h6 style="font-weight: 600;">Knowledge Applied:</h6>
                        {knowledgeHTML}
                    </div>
                    <div class="col s12 m6">
                        <h6 style="font-weight: 600;">Skills Demonstrated:</h6>
                        {skillsHTML}
                    </div>
                </div>
            </div>
            <div class="card-action right-align" style="padding: 15px 20px;">
                <a href="{projectLink}" class="waves-effect waves-light btn-small blue darken-3 white-text" style="border-radius: 20px: padding: 0 20px;" target="_blank">
                  <i class="material-icons left">launch</i>View Project
                </a>
            </div>
        </div>
        """
        projects += f'<div class="project-card">{projectHTML}</div>'

    projectsHTML = f"""
    <div class="projects-container">
        {projects}
    </div>
    """

    # Mostramos los Projects
    st.html(projectsHTML)

# Cards "Education" con las clases CSS de MaterializeCSS
with tabEducation:
    # Construimos las cards de educación
    edu_cards = []

    # Obtenemos los datos de education desde CSV
    education_df = load_csv('education')

    # Agrupamos por Name y Degree para manejar múltiples filas de Knowledge
    grouped_education = {}

    for _, edu in education_df.iterrows():
        uni_name = edu.get('Name', '').strip()
        degree = edu.get('Degree', '').strip()
        date = edu.get('Date', '')
        knowledge_item = edu.get('Knowledge', '').strip()

        # Crear clave única para cada combinación de universidad y grado
        key = f"{uni_name}|{degree}"

        if key not in grouped_education:
            grouped_education[key] = {
                'Name': uni_name,
                'Degree': degree,
                'Date': date,
                'Knowledge': []
            }

        # Agregar conocimiento si no está vacío
        if knowledge_item:
            # Dividir en subpárrafos por el símbolo '#'
            sub_paragraphs = [p.strip()
                              for p in knowledge_item.split('#') if p.strip()]
            grouped_education[key]['Knowledge'].extend(sub_paragraphs)

    # Crear cards para cada entrada educativa agrupada
    for edu_data in grouped_education.values():
        uni_name = edu_data['Name'] if edu_data['Name'] else 'Institución no especificada'
        degree = edu_data['Degree'] if edu_data['Degree'] else 'Grado no especificado'
        date = edu_data['Date'] if edu_data['Date'] else 'Fecha no especificada'
        knowledge = edu_data['Knowledge'] if edu_data['Knowledge'] else [
            'Conocimientos no especificados']

        # Plantilla de card
        card_html = f"""
        <div class="col s12 m6 l6">
            <div class="card hoverable">
                <!-- Sección superior - Encabezado -->
                <div class="card-content light-blue lighten-4">
                    <div class="row" style="margin-bottom: 0;">
                        <div class="col s9">
                            <span class="card-title blue-grey-text text-darken-4" style="font-weight: 700;">{uni_name}</span>
                            <p class="blue-grey-text text-darken-2" style="margin-top: 8px;">
                                <i class="fas fa-graduation-cap"></i> {degree}<br>
                                <i class="fas fa-calendar-alt"></i> {date}
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Sección inferior - Conocimientos -->
                <div class="card-content">
                    <div class="collection" style="border: none;">
                        {''.join([f'<div class="collection-item grey lighten-5" style="border: none; margin: 4px 0; border-radius: 4px;"><p style="margin:0;">{k}</p></div>' for k in knowledge])}
                    </div>
                </div>
            </div>
        </div>
        """
        edu_cards.append(card_html)

    # Contenedor principal
    container = f"""
    <div class="row">
        {''.join(edu_cards)}
    </div>
    """

    # CSS personalizado
    st.markdown("""
    <style>
        .education-card {
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
            font-size: 1.3rem;
        }
        .card .collection-item {
            padding: 10px 20px !important;
            font-size: 1.2rem;
        }
        .card-title {
            font-size: 1.8rem !important;
        }
        .fa-graduation-cap, .fa-calendar-alt {
            margin-right: 8px !important;
            color: #0288d1 !important;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Mostramos el contenido de Education
    st.html(container)

# Cards "STEM Content Creation & Outreach" con las clases CSS de MaterializeCSS
with tabSTEM:
    stem_cards = []

    # Obtenemos los datos de STEM desde CSV
    stem_df = load_csv('STEM')

    for _, stem in stem_df.iterrows():
        # Obtenemos datos desde CSV
        title = stem.get('Name', 'Título no disponible')
        description = stem.get('Description', 'Descripción no disponible')
        instagram_link = stem.get('Instagram', '#')

        # Plantilla de la card
        card_html = f"""
        <div class="col s12 m6 l4">
            <div class="card hoverable">
                <!-- Sección superior - Título y Descripción -->
                <div class="card-content light-blue lighten-4">
                    <div class="row" style="margin-bottom: 0;">
                        <div class="col s12">
                            <span class="card-title blue-grey-text text-darken-4" style="font-weight: 700;">{title}</span>
                        </div>
                    </div>
                </div>

                <!-- Sección inferior - Instagram -->
                <div class="card-content">
                    <div class="row valign-wrapper">
                        <div class="col s12 center">
                            <p class="blue-grey-text text-darken-2" style="margin-top: 8px; font-size: 1.3rem;">
                                {description}
                            </p>
                            <a href="{instagram_link}" target="_blank" class="btn waves-effect pink accent-3 white-text">
                                <i class="fab fa-instagram"></i> Follow me!
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        stem_cards.append(card_html)

    # Contenedor fuera del bucle
    container = f"""
    <div class="row">
        {''.join(stem_cards)}
    </div>
    """

    st.html(container)

# Formulario de "Contact" con las clases CSS de MaterializeCSS (MANTIENE AIRTABLE)
with tabContact:
    st.info("If you think I can help you with some of your projects or entrepreneurships, send me a message I'll contact you as soon as I can. I'm always glad to help")
    with st.container(border=True):
        parName = st.text_input("Your name")
        parEmail = st.text_input("Your email")
        parPhoneNumber = st.text_input(
            "WhatsApp phone number, with country code")
        parNotes = st.text_area("What can I do for you")
        btnEnviar = st.button("Send", type="primary")

    if btnEnviar:  # acción al hacer click en enviar
        if parName and parEmail and parNotes:  # Validación básica
            success = create_contact(
                parName, parEmail, parPhoneNumber, parNotes)
            if success:
                st.toast("Message sent")  # muestra el mensaje
                st.success("✅ Tu mensaje ha sido enviado correctamente!")
            else:
                st.error("❌ Hubo un error al enviar el mensaje. Intenta de nuevo.")
        else:
            st.warning(
                "⚠️ Por favor completa al menos el nombre, email y mensaje.")

st.markdown('<script src = "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>', unsafe_allow_html=True)
