# 🛡️ NEOMA Blockchain Lab - Beauty Contest dApp
### *Projet par Camélia El Rhabi*

![Version](https://img.shields.io/badge/Version-1.0.0-rose)
![Python](https://img.shields.io/badge/Python-3.13-F7E7CE)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FFB6C1)

## 📋 Présentation du Projet
Ce portail est une application décentralisée (dApp) permettant de participer au célèbre **Concours de Beauté de Keynes** (Keynesian Beauty Contest) via un protocole de **Commit-Reveal** sur la blockchain.

L'objectif est de choisir un nombre entre 0 et 100 qui se rapproche le plus des **2/3 de la moyenne de tous les nombres choisis** par la classe.

## 🏗️ Architecture du Système
Pour garantir l'intégrité et la confidentialité des votes, le système utilise un mécanisme cryptographique en deux phases :

1. **Phase de Commit** : L'utilisateur génère une preuve de son choix en hachant son `ID|Nombre|Secret` avec l'algorithme **SHA-256**. Seul le hash est envoyé au registre (ledger), gardant le choix secret.
2. **Phase de Reveal** : Une fois la deadline passée, l'utilisateur révèle son nombre et son secret. Le système vérifie que le hash correspond à l'engagement initial avant de comptabiliser le vote.

## 💻 Tech Stack
* **Frontend** : Streamlit (Design personnalisé Rose Pastel & Beige)
* **Backend** : Google Apps Script API (Shared Ledger)
* **Cryptographie** : SHA-256 (Bibliothèque `hashlib`)
* **Police d'écriture** : Aeonik Pro (Lexend Deca)

## 🚀 Installation et Lancement

1. Clonez le répertoire :
   ```bash
   git clone [https://github.com/votre-username/neoma-blockchain-portal.git](https://github.com/votre-username/neoma-blockchain-portal.git)
