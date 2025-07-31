import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="📊 Tableau de Bord - Inventaire Entreprise",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour une interface moderne
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #C73E1D;
        --background-light: #F8FAFC;
        --text-dark: #1E293B;
        --border-color: #E2E8F0;
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        padding: 2.5rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(46, 134, 171, 0.3);
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        border-radius: 15px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-color), var(--accent-color));
    }
    
    /* Sidebar Styles */
    .sidebar-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
    }
    
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
    }
    
    /* Welcome Section */
    .welcome-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpolygon points='50 0 60 40 100 50 60 60 50 100 40 60 0 50 40 40'/%3E%3C/g%3E%3C/svg%3E");
        animation: rotate 60s linear infinite;
        z-index: 0;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .welcome-content {
        position: relative;
        z-index: 1;
    }
    
    /* Upload Area */
    .upload-area {
        background: white;
        border: 3px dashed var(--primary-color);
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: var(--secondary-color);
        background: var(--background-light);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
        text-align: center;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Charts Container */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Status Messages */
    .success-message {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .info-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 134, 171, 0.4);
    }
    
    /* Data Table */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 2rem 1rem;
        }
        
        .welcome-container {
            padding: 2rem 1rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def show_welcome_screen():
    """Afficher l'écran d'accueil attractif"""
    
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-content">
            <h1>🚀 Bienvenue dans votre Tableau de Bord d'Inventaire</h1>
            <p style="font-size: 1.2rem; margin: 1.5rem 0; opacity: 0.9;">
                Analysez, visualisez et gérez votre inventaire avec des outils puissants et intuitifs
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fonctionnalités principales
    st.markdown("## ✨ Fonctionnalités Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Visualisations</h3>
            <p>Graphiques interactifs et tableaux de bord dynamiques</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Filtres Avancés</h3>
            <p>Filtrez vos données selon vos besoins spécifiques</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Analyses</h3>
            <p>Corrélations, distributions et analyses croisées</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💾</div>
            <h3>Export</h3>
            <p>Téléchargez vos analyses et rapports en CSV</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Instructions de démarrage
    st.markdown("## 🎯 Comment Commencer")
    
    st.markdown("""
    <div class="upload-area">
        <h3>📁 Téléchargez votre fichier Excel</h3>
        <p>Utilisez le panneau latéral pour charger votre fichier d'inventaire</p>
        <p style="font-size: 0.9rem; color: #666; margin-top: 1rem;">
            Formats supportés: .xlsx, .xls
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Format de fichier attendu
    with st.expander("📋 Format de fichier recommandé", expanded=False):
        st.markdown("""
        **Colonnes principales attendues :**
        
        | Colonne | Description | Type |
        |---------|-------------|------|
        | `Code Produit` | Identifiant unique du produit | Texte |
        | `Libellé Produit` | Description du produit | Texte |
        | `Montant (DA)` | Valeur en dinars algériens | Numérique |
        | `Qte (kg)` | Quantité en kilogrammes | Numérique |
        | `LIEU` | Lieu de stockage | Texte |
        | `UNITE` | Unité de travail | Texte |
        | `NATURE` | Type/nature du produit | Texte |
        | `FAMILLE DE PRODUIT` | Catégorie du produit | Texte |
        
        > 💡 **Conseil :** Votre fichier peut contenir d'autres colonnes. L'application s'adaptera automatiquement !
        """)

@st.cache_data
def load_data(uploaded_file):
    """Chargement et mise en cache des données avec gestion d'erreurs améliorée"""
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(uploaded_file)
        
        # Validation basique
        if df.empty:
            st.error("❌ Le fichier est vide")
            return None
            
        # Nettoyage des noms de colonnes
        df.columns = df.columns.str.strip()
        
        # Informations sur le dataset
        st.success(f"✅ Fichier chargé avec succès : {len(df)} lignes, {len(df.columns)} colonnes")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
        st.info("💡 Vérifiez que votre fichier est un format Excel valide (.xlsx ou .xls)")
        return None

def format_number(num):
    """Formatage des nombres pour l'affichage avec style français"""
    if pd.isna(num):
        return "N/A"
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return f"{num:,.0f}".replace(",", " ")

def create_summary_metrics(df):
    """Création des métriques de résumé avec style amélioré"""
    st.markdown("## 📊 Vue d'Ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculs des métriques
    total_produits = len(df)
    total_montant = df['Montant (DA)'].sum() if 'Montant (DA)' in df.columns else 0
    total_quantite = df['Qte  (kg)'].sum() if 'Qte  (kg)' in df.columns else 0
    nb_lieux = df['LIEU'].nunique() if 'LIEU' in df.columns else 0
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--primary-color); margin: 0;">📦 Total Produits</h3>
            <h2 style="margin: 0.5rem 0; color: var(--text-dark);">{}</h2>
            <p style="color: #666; margin: 0;">articles référencés</p>
        </div>
        """.format(format_number(total_produits)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--secondary-color); margin: 0;">💰 Valeur Totale</h3>
            <h2 style="margin: 0.5rem 0; color: var(--text-dark);">{} DA</h2>
            <p style="color: #666; margin: 0;">montant inventaire</p>
        </div>
        """.format(format_number(total_montant)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--accent-color); margin: 0;">⚖️ Quantité Totale</h3>
            <h2 style="margin: 0.5rem 0; color: var(--text-dark);">{} kg</h2>
            <p style="color: #666; margin: 0;">poids total</p>
        </div>
        """.format(format_number(total_quantite)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: var(--success-color); margin: 0;">📍 Lieux</h3>
            <h2 style="margin: 0.5rem 0; color: var(--text-dark);">{}</h2>
            <p style="color: #666; margin: 0;">emplacements</p>
        </div>
        """.format(nb_lieux), unsafe_allow_html=True)

def create_filters(df):
    """Création d'une interface de filtres améliorée"""
    st.sidebar.markdown("""
    <div class="sidebar-header">
        🔍 Filtres de Données
    </div>
    """, unsafe_allow_html=True)
    
    filters = {}
    
    with st.sidebar:
        # Section Filtres Principaux
        st.markdown("### 🎯 Filtres Principaux")
        
        # Filtre par lieu
        if 'LIEU' in df.columns:
            lieux = ['Tous'] + sorted(df['LIEU'].dropna().unique().tolist())
            filters['lieu'] = st.selectbox(
                "📍 Lieu de stockage", 
                lieux,
                help="Filtrer par lieu de stockage"
            )
        
        # Filtre par unité de travail
        if 'UNITE' in df.columns:
            unites = ['Toutes'] + sorted(df['UNITE'].dropna().unique().tolist())
            filters['unite'] = st.selectbox(
                "🏭 Unité de travail", 
                unites,
                help="Filtrer par unité de travail"
            )
        
        # Filtre par nature
        if 'NATURE' in df.columns:
            natures = ['Toutes'] + sorted(df['NATURE'].dropna().unique().tolist())
            filters['nature'] = st.selectbox(
                "🔖 Nature", 
                natures,
                help="Filtrer par type de produit"
            )
        
        # Section Filtres Avancés
        st.markdown("### ⚙️ Filtres Avancés")
        
        # Filtre par plage de montant
        if 'Montant (DA)' in df.columns and not df['Montant (DA)'].isna().all():
            montant_min = float(df['Montant (DA)'].min())
            montant_max = float(df['Montant (DA)'].max())
            
            if montant_min != montant_max:
                filters['montant_range'] = st.slider(
                    "💸 Plage de montant (DA)",
                    montant_min, montant_max,
                    (montant_min, montant_max),
                    help="Définir une plage de valeurs"
                )
        
        # Filtre par famille de produit
        if 'FAMILLE DE PRODUIT' in df.columns:
            familles = ['Toutes'] + sorted(df['FAMILLE DE PRODUIT'].dropna().unique().tolist())
            filters['famille'] = st.selectbox(
                "🏷️ Famille de produit", 
                familles,
                help="Filtrer par famille de produit"
            )
        
        # Bouton de réinitialisation
        if st.button("🔄 Réinitialiser les filtres", help="Effacer tous les filtres"):
            st.experimental_rerun()
    
    return filters

def apply_filters(df, filters):
    """Application des filtres avec gestion d'erreurs"""
    filtered_df = df.copy()
    
    try:
        if 'lieu' in filters and filters['lieu'] != 'Tous':
            filtered_df = filtered_df[filtered_df['LIEU'] == filters['lieu']]
        
        if 'unite' in filters and filters['unite'] != 'Toutes':
            filtered_df = filtered_df[filtered_df['UNITE'] == filters['unite']]
        
        if 'nature' in filters and filters['nature'] != 'Toutes':
            filtered_df = filtered_df[filtered_df['NATURE'] == filters['nature']]
        
        if 'famille' in filters and filters['famille'] != 'Toutes':
            filtered_df = filtered_df[filtered_df['FAMILLE DE PRODUIT'] == filters['famille']]
        
        if 'montant_range' in filters:
            min_val, max_val = filters['montant_range']
            filtered_df = filtered_df[
                (filtered_df['Montant (DA)'] >= min_val) & 
                (filtered_df['Montant (DA)'] <= max_val)
            ]
    
    except Exception as e:
        st.error(f"Erreur lors de l'application des filtres : {str(e)}")
        return df
    
    return filtered_df

def create_visualizations(df):
    """Création des visualisations avec style amélioré"""
    
    st.markdown("## 📈 Visualisations")
    
    # Vérifier la présence des colonnes nécessaires
    if 'LIEU' not in df.columns or 'Montant (DA)' not in df.columns:
        st.warning("⚠️ Colonnes requises manquantes pour les visualisations complètes")
        return
    
    # Section 1: Analyse par lieu
    st.markdown("### 📍 Analyse par Lieu de Stockage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres
        lieu_analysis = df.groupby('LIEU').agg({
            'Montant (DA)': 'sum',
            df.columns[0]: 'count'  # Utiliser la première colonne pour compter
        }).reset_index()
        lieu_analysis.columns = ['LIEU', 'Montant_Total', 'Nombre_Produits']
        
        fig_bar = px.bar(
            lieu_analysis, 
            x='LIEU', 
            y='Montant_Total',
            title="💰 Valeur d'inventaire par lieu",
            color='Montant_Total',
            color_continuous_scale='viridis',
            template='plotly_white'
        )
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            height=450,
            showlegend=False,
            font=dict(size=12)
        )
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Graphique en secteurs
        fig_pie = px.pie(
            lieu_analysis,
            values='Nombre_Produits',
            names='LIEU',
            title="📊 Répartition des produits par lieu",
            template='plotly_white'
        )
        fig_pie.update_layout(height=450, font=dict(size=12))
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Top produits
    st.markdown("### 🏆 Top Produits par Valeur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 produits par montant
        if 'Libellé Produit' in df.columns:
            top_products = df.nlargest(10, 'Montant (DA)')
            
            fig_top = px.bar(
                top_products,
                x='Montant (DA)',
                y='Libellé Produit',
                orientation='h',
                title="🥇 Top 10 - Produits les plus chers",
                color='Montant (DA)',
                color_continuous_scale='reds',
                template='plotly_white'
            )
            fig_top.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=11)
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_top, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Analyse par famille de produit
        if 'FAMILLE DE PRODUIT' in df.columns:
            famille_analysis = df.groupby('FAMILLE DE PRODUIT').agg({
                'Montant (DA)': 'sum',
                'Qte  (kg)': 'sum' if 'Qte  (kg)' in df.columns else 'count'
            }).reset_index().sort_values('Montant (DA)', ascending=True)
            
            fig_famille = px.bar(
                famille_analysis,
                x='Montant (DA)',
                y='FAMILLE DE PRODUIT',
                orientation='h',
                title="📦 Valeur par famille de produit",
                color='Qte  (kg)' if 'Qte  (kg)' in df.columns else 'Montant (DA)',
                color_continuous_scale='blues',
                template='plotly_white'
            )
            fig_famille.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=11)
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_famille, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def create_data_table(df):
    """Création du tableau de données avec interface améliorée"""
    st.markdown("## 📋 Tableau de Données Détaillé")
    
    # Interface de contrôle améliorée
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_rows = st.selectbox(
            "📊 Lignes à afficher", 
            [10, 25, 50, 100, len(df)],
            help="Nombre de lignes à afficher dans le tableau"
        )
    
    with col2:
        sort_column = st.selectbox(
            "🔄 Trier par", 
            df.columns.tolist(),
            help="Colonne utilisée pour le tri"
        )
    
    with col3:
        sort_order = st.selectbox(
            "📈 Ordre", 
            ["Décroissant", "Croissant"],
            help="Ordre de tri"
        )
    
    with col4:
        columns_to_show = st.multiselect(
            "👁️ Colonnes visibles",
            df.columns.tolist(),
            default=df.columns.tolist()[:6],  # 6 premières colonnes par défaut
            help="Sélectionner les colonnes à afficher"
        )
    
    # Affichage du tableau filtré
    if columns_to_show:
        ascending_order = sort_order == "Croissant"
        
        try:
            display_df = df[columns_to_show].sort_values(
                sort_column, 
                ascending=ascending_order
            ).head(show_rows)
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(
                display_df, 
                use_container_width=True, 
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Section de téléchargement
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                # Préparation du CSV
                csv_buffer = io.StringIO()
                display_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                csv_data = csv_buffer.getvalue()
                
                st.download_button(
                    label="📥 Télécharger (CSV)",
                    data=csv_data,
                    file_name=f'inventaire_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    help="Télécharger les données filtrées au format CSV"
                )
        
        except Exception as e:
            st.error(f"Erreur lors de l'affichage du tableau : {str(e)}")
    else:
        st.warning("⚠️ Veuillez sélectionner au moins une colonne à afficher")

def create_pivot_analysis(df):
    """Création d'analyses de tableau croisé dynamique avec heatmap améliorée"""
    st.markdown("### 🔄 Tableau Croisé Dynamique & Heatmap")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚙️ Configuration")
        
        # Colonnes disponibles pour les analyses
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not categorical_cols or not numeric_cols:
            st.warning("⚠️ Données insuffisantes pour l'analyse croisée")
            return
        
        # Sélecteurs pour le tableau croisé
        index_col = st.selectbox(
            "📋 Lignes (Index)", 
            categorical_cols,
            help="Colonne pour les lignes du tableau"
        )
        
        columns_col = st.selectbox(
            "📊 Colonnes", 
            categorical_cols,
            help="Colonne pour les colonnes du tableau"
        )
        
        values_col = st.selectbox(
            "💰 Valeurs", 
            numeric_cols,
            help="Colonne pour les valeurs à agréger"
        )
        
        aggfunc = st.selectbox(
            "📈 Fonction d'agrégation",
            ["sum", "mean", "count", "median", "std"],
            help="Comment agréger les données"
        )
    
    with col2:
        st.markdown("#### 🎨 Options d'Affichage")
        
        color_scale = st.selectbox(
            "🎨 Palette de couleurs",
            ["Viridis", "RdBu", "Blues", "Reds", "YlOrRd", "Plasma"],
            help="Palette de couleurs pour la heatmap"
        )
        
        show_values = st.checkbox("📝 Afficher les valeurs", value=True)
        show_heatmap = st.checkbox("🌡️ Afficher la Heatmap", value=True)
        show_totals = st.checkbox("🔢 Afficher les totaux", value=True)
    
    # Création du tableau croisé dynamique
    try:
        if index_col and columns_col and values_col:
            # Création du pivot table
            pivot_table = pd.pivot_table(
                df, 
                index=index_col, 
                columns=columns_col, 
                values=values_col, 
                aggfunc=aggfunc,
                fill_value=0
            )
            
            # Ajout des totaux si demandé
            if show_totals:
                pivot_table['Total'] = pivot_table.sum(axis=1)
                totals_row = pivot_table.sum(axis=0)
                totals_row.name = 'Total'
                pivot_table = pd.concat([pivot_table, totals_row.to_frame().T])
            
            # Affichage du tableau
            st.markdown("#### 📊 Résultats du Tableau Croisé")
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(
                pivot_table.style.background_gradient(cmap='RdYlBu', axis=None)
                                .format("{:.2f}"),
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Affichage de la heatmap si demandé
            if show_heatmap:
                st.markdown("#### 🌡️ Heatmap Interactive")
                
                # Préparation des données pour la heatmap
                heatmap_data = pivot_table.copy()
                if show_totals and 'Total' in heatmap_data.columns:
                    heatmap_data = heatmap_data.drop('Total', axis=1)
                    if 'Total' in heatmap_data.index:
                        heatmap_data = heatmap_data.drop('Total', axis=0)
                
                # Création de la heatmap avec Plotly
                fig_heatmap = px.imshow(
                    heatmap_data,
                    text_auto=show_values,
                    aspect="auto",
                    title=f"Heatmap : {index_col} vs {columns_col} ({values_col})",
                    color_continuous_scale=color_scale.lower(),
                    template='plotly_white'
                )
                
                fig_heatmap.update_layout(
                    height=max(400, len(heatmap_data) * 30),
                    font=dict(size=10)
                )
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig_heatmap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Bouton de téléchargement
            csv_buffer = io.StringIO()
            pivot_table.to_csv(csv_buffer, encoding='utf-8-sig')
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📥 Télécharger le tableau croisé",
                data=csv_data,
                file_name=f'tableau_croise_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
            
    except Exception as e:
        st.error(f"❌ Erreur lors de la création du tableau croisé : {str(e)}")

def create_advanced_analysis(df):
    """Analyses avancées avec interface améliorée"""
    st.markdown("## 🔬 Analyses Avancées")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Tableau Croisé", 
        "📊 Corrélations", 
        "📈 Distribution", 
        "🎨 Graphique Personnalisé"
    ])
    
    with tab1:
        create_pivot_analysis(df)
    
    with tab2:
        st.markdown("### 📊 Matrice de Corrélation")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            # Sélection des colonnes pour la corrélation
            selected_cols = st.multiselect(
                "Sélectionner les colonnes numériques",
                numeric_cols.tolist(),
                default=numeric_cols.tolist()[:5]  # 5 premières par défaut
            )
            
            if len(selected_cols) > 1:
                corr_matrix = df[selected_cols].corr()
                
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="🔗 Matrice de Corrélation",
                    color_continuous_scale='RdBu',
                    template='plotly_white'
                )
                fig_corr.update_layout(height=500)
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig_corr, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("💡 Sélectionnez au moins 2 colonnes pour calculer les corrélations")
        else:
            st.warning("⚠️ Pas assez de colonnes numériques pour l'analyse de corrélation")
    
    with tab3:
        st.markdown("### 📈 Analyse de Distribution")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_col = st.selectbox(
                    "Choisir une colonne numérique",
                    numeric_cols.tolist()
                )
            
            with col2:
                chart_type = st.selectbox(
                    "Type de graphique",
                    ["Histogramme", "Box Plot", "Violin Plot"]
                )
            
            if selected_col:
                if chart_type == "Histogramme":
                    fig_dist = px.histogram(
                        df,
                        x=selected_col,
                        nbins=30,
                        title=f"📊 Distribution de {selected_col}",
                        marginal="box",
                        template='plotly_white'
                    )
                elif chart_type == "Box Plot":
                    fig_dist = px.box(
                        df,
                        y=selected_col,
                        title=f"📦 Box Plot de {selected_col}",
                        template='plotly_white'
                    )
                else:  # Violin Plot
                    fig_dist = px.violin(
                        df,
                        y=selected_col,
                        title=f"🎻 Violin Plot de {selected_col}",
                        template='plotly_white'
                    )
                
                fig_dist.update_layout(height=500)
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig_dist, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Statistiques descriptives
                st.markdown("#### 📋 Statistiques Descriptives")
                stats_df = df[selected_col].describe().to_frame().T
                st.dataframe(stats_df, use_container_width=True)
        else:
            st.warning("⚠️ Aucune colonne numérique disponible pour l'analyse de distribution")
    
    with tab4:
        st.markdown("### 🎨 Créateur de Graphique Personnalisé")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚙️ Configuration du Graphique")
            
            x_axis = st.selectbox("📊 Axe X", df.columns.tolist(), key="custom_x")
            y_axis = st.selectbox("📈 Axe Y", df.columns.tolist(), key="custom_y")
            
            chart_type = st.selectbox(
                "📋 Type de graphique", 
                ["Scatter", "Bar", "Line", "Box", "Histogram"]
            )
        
        with col2:
            st.markdown("#### 🎨 Personnalisation")
            
            color_by = st.selectbox(
                "🌈 Couleur par", 
                ["Aucune"] + df.columns.tolist()
            )
            
            title = st.text_input(
                "📝 Titre du graphique",
                value=f"{chart_type} : {x_axis} vs {y_axis}"
            )
        
        if st.button("🚀 Générer le graphique", type="primary"):
            try:
                color_col = None if color_by == "Aucune" else color_by
                
                if chart_type == "Scatter":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Bar":
                    # Agrégation pour les graphiques en barres
                    if df[x_axis].dtype == 'object':
                        agg_df = df.groupby(x_axis)[y_axis].sum().reset_index()
                        fig = px.bar(agg_df, x=x_axis, y=y_axis, title=title)
                    else:
                        fig = px.bar(df, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Line":
                    fig = px.line(df, x=x_axis, y=y_axis, color=color_col, title=title)
                elif chart_type == "Box":
                    fig = px.box(df, x=x_axis, y=y_axis, color=color_col, title=title)
                else:  # Histogram
                    fig = px.histogram(df, x=x_axis, color=color_col, title=title)
                
                fig.update_layout(template='plotly_white', height=500)
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la création du graphique : {str(e)}")

def create_data_overview(df):
    """Création d'un aperçu des données"""
    st.markdown("## 🔍 Aperçu des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Informations Générales")
        
        info_data = {
            "Nombre de lignes": len(df),
            "Nombre de colonnes": len(df.columns),
            "Mémoire utilisée": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            "Valeurs manquantes": df.isnull().sum().sum(),
            "Colonnes numériques": len(df.select_dtypes(include=[np.number]).columns),
            "Colonnes textuelles": len(df.select_dtypes(include=['object']).columns)
        }
        
        for key, value in info_data.items():
            st.metric(key, value)
    
    with col2:
        st.markdown("### 📋 Types de Colonnes")
        
        types_df = pd.DataFrame({
            'Colonne': df.columns,
            'Type': df.dtypes.astype(str),
            'Valeurs Uniques': [df[col].nunique() for col in df.columns],
            'Valeurs Manquantes': [df[col].isnull().sum() for col in df.columns]
        })
        
        st.dataframe(types_df, use_container_width=True, height=400)

def main():
    """Fonction principale avec interface utilisateur améliorée"""
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        📊 Tableau de Bord - Inventaire Entreprise
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar pour l'upload
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            📁 Chargement des Données
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier Excel",
            type=['xlsx', 'xls'],
            help="Téléchargez votre fichier d'inventaire au format Excel"
        )
        
        # Informations sur l'application
        with st.expander("ℹ️ À propos de l'application"):
            st.markdown("""
            **Version:** 2.0  
            **Développé pour:** Analyse d'inventaire  
            **Formats supportés:** Excel (.xlsx, .xls)  
            **Fonctionnalités:**
            - Visualisations interactives
            - Filtres avancés
            - Analyses statistiques
            - Export des données
            """)
    
    # Chargement et traitement des données
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None and not df.empty:
            # Création des filtres
            filters = create_filters(df)
            
            # Application des filtres
            filtered_df = apply_filters(df, filters)
            
            # Vérification des données filtrées
            if len(filtered_df) == 0:
                st.markdown("""
                <div class="info-message">
                    ⚠️ Aucune donnée ne correspond aux filtres sélectionnés. 
                    Essayez de modifier vos critères de filtrage.
                </div>
                """, unsafe_allow_html=True)
                return
            
            # Affichage du nombre d'éléments filtrés
            if len(filtered_df) != len(df):
                st.markdown(f"""
                <div class="success-message">
                    🔍 Affichage de {len(filtered_df)} éléments sur {len(df)} 
                    ({len(filtered_df)/len(df)*100:.1f}% des données)
                </div>
                """, unsafe_allow_html=True)
            
            # Sections principales
            create_summary_metrics(filtered_df)
            
            # Onglets pour organiser le contenu
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Visualisations", 
                "📋 Données", 
                "🔬 Analyses", 
                "🔍 Aperçu"
            ])
            
            with tab1:
                create_visualizations(filtered_df)
            
            with tab2:
                create_data_table(filtered_df)
            
            with tab3:
                create_advanced_analysis(filtered_df)
            
            with tab4:
                create_data_overview(filtered_df)
        
        else:
            st.error("❌ Impossible de charger le fichier. Vérifiez le format et le contenu.")
    
    else:
        # Écran d'accueil
        show_welcome_screen()

if __name__ == "__main__":
    main()
