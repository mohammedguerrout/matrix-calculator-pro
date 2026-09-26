# 🧮 Calculatrice Matricielle Pro ✨

Une application de bureau complète en **Python** (avec **CustomTkinter**) permettant d'effectuer toutes les opérations matricielles courantes dans une interface moderne, élégante et personnalisable.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-8338EC)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Description

**Calculatrice Matricielle Pro** est une application graphique développée en Python permettant de manipuler des matrices carrées (de 2×2 à 8×8) et d'effectuer dessus des opérations mathématiques avancées, avec un historique complet, une sauvegarde/chargement au format JSON, et un export CSV des résultats.

---

## ✨ Fonctionnalités

### Opérations sur une seule matrice (A)
- 📉 **Déterminant**
- 🔄 **Matrice adjointe**
- ✨ **Matrice inverse**
- 🔁 **Transposée**
- Σ **Trace**
- 🏗️ **Rang**
- 🔺 **Puissance A^n** (positive ou négative)
- ✖️ **Multiplication par un scalaire**

### Opérations sur deux matrices (A et B)
- ➕ Addition (A + B)
- ➖ Soustraction (A − B)
- ✖️ Multiplication (A × B)

### Outils supplémentaires
- 🎲 Remplissage aléatoire
- 🔷 Génération de la matrice identité
- ⬛ Remplissage par une matrice nulle
- ↩️ Annulation (Undo) de la dernière modification
- 🕘 Historique complet des opérations avec possibilité de les revoir
- 💾 Sauvegarde et chargement de matrices au format `.json`
- 📤 Export des résultats au format `.csv`
- 📋 Copie du résultat dans le presse-papiers
- ☀️ / 🌙 Mode clair et sombre
- 🎨 Choix de couleurs d'accentuation
- ⌨️ Raccourcis clavier et navigation au clavier entre les cellules

---

## ⌨️ Raccourcis clavier

| Raccourci | Action |
|---|---|
| `Ctrl + D` | Déterminant |
| `Ctrl + I` | Matrice identité |
| `Ctrl + T` | Transposée |
| `Ctrl + R` | Effacer la grille |
| `Ctrl + G` | Remplissage aléatoire |
| `Ctrl + Z` | Annuler |
| `Ctrl + S` | Sauvegarder |
| `Ctrl + O` | Charger |
| `Ctrl + Q` | Quitter |
| `↑ ↓ ← →` | Navigation entre les cellules |

---

## 🛠️ Technologies utilisées

- [Python 3](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — interface graphique moderne
- `tkinter` (messagebox, filedialog)
- `json`, `csv`, `random`, `time` — bibliothèques standard

---

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/VOTRE_NOM_UTILISATEUR/matrix-calculator-pro.git
   cd matrix-calculator-pro
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Sur Linux/Mac
   venv\Scripts\activate         # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install customtkinter
   ```

4. **Lancer l'application**
   ```bash
   python main.py
   ```

---

## 📂 Structure du projet

```
matrix-calculator-pro/
│
├── main.py          # Fichier principal de l'application
├── README.md         # Documentation du projet
├── LICENSE            # Licence MIT
└── .gitignore         # Fichiers ignorés par Git
```

---

## 🖼️ Aperçu

> *(Ajoutez ici une ou plusieurs captures d'écran de l'application une fois publiée)*

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Faites un *fork* du projet
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commitez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une *Pull Request*

---

## 📜 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Mohammed Guerrout**

