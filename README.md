# 📊 Tableau de Bord d'Analyse d'Inventaire

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/plotly-5.0+-green.svg)

Application web interactive pour l'analyse et la visualisation des données d'inventaire d'entreprise avec Streamlit et Plotly.

## lien vers l'application : https://analyse-stock-cpvaybxkr6yhygnyfxfeka.streamlit.app

## ✨ Fonctionnalités

- 📈 **Visualisations interactives** : Graphiques dynamiques (barres, secteurs, heatmaps, distributions)
- 🔍 **Filtres avancés** : Par lieu, unité, nature, famille et plage de montant
- 🔬 **Analyses avancées** : Tableaux croisés, corrélations, distributions, graphiques personnalisés
- 💾 **Export CSV** : Téléchargez vos analyses et données filtrées
- 🎨 **Interface moderne** : Design responsive avec animations

## 💻 Utilisation

1. **Lancer l'app** avec `streamlit run app.py`
2. **Uploader** votre fichier Excel dans la barre latérale
3. **Filtrer** les données selon vos besoins
4. **Explorer** les visualisations et analyses dans les onglets
5. **Exporter** vos résultats en CSV

## 📊 Format des Données

Colonnes attendues dans votre fichier Excel :

| Colonne | Type | Description |
|---------|------|-------------|
| `Code Produit` | Texte | Identifiant unique |
| `Libellé Produit` | Texte | Description du produit |
| `Montant (DA)` | Numérique | Valeur en DA |
| `Qte (kg)` | Numérique | Quantité en kg |
| `LIEU` | Texte | Lieu de stockage |
| `UNITE` | Texte | Unité de travail |
| `NATURE` | Texte | Type de produit |
| `FAMILLE DE PRODUIT` | Texte | Catégorie |

> 💡 L'application s'adapte automatiquement aux colonnes disponibles


## 🎓 Contexte

Projet développé dans le cadre de mes études en **Data Science et IA** à l'**ENSSEA**.

**Objectif** : Créer une application interactive pour l'analyse d'inventaire avec des visualisations professionnelles et des analyses statistiques avancées.


## 👨‍💻 Auteur

**Boucherite Ahmed Abdeldjalil**
- 🎓 Étudiant Data Science & IA - ENSSEA
- 📧 Email : a.a.boucherite@gmail.com 
- 💼 LinkedIn : [www.linkedin.com/in/abdeldjalil-boucherite-745619378]

---

⭐ Si ce projet vous est utile, donnez-lui une étoile !

*Développé avec ❤️ et Python*
