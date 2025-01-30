# 📝 ToDoList-Python-MongoDB

Une application simple et efficace de gestion de **To-Do List** en **Python** avec **MongoDB**, permettant d'**ajouter, modifier, compléter, supprimer et afficher** des tâches facilement.

---

## 🚀 Fonctionnalités

✔️ Ajouter de nouvelles tâches  
✔️ Modifier des tâches existantes  
✔️ Marquer une tâche comme terminée  
✔️ Supprimer des tâches  
✔️ Affichage des tâches avec différents statuts  
✔️ Stockage persistant des tâches dans **MongoDB**  

---

## 📌 Prérequis

Avant d'exécuter l'application, assurez-vous d'avoir installé :

- **Python 3.x**  
- **MongoDB** (installé et en cours d'exécution)  
- **MongoDB Compass** (optionnel, pour visualiser et gérer les données plus facilement)  
- Les **bibliothèques Python** suivantes :
  - `pymongo` (pour la connexion à MongoDB)
  - `os` (pour la gestion des variables d'environnement)
  - `time` (pour gérer les temporisations)
  - `webbrowser` (pour ouvrir des liens web)
  - `datetime` (pour gérer les dates)

---

## 📥 Installation

1. **Clonez ce dépôt** :
    ```bash
    git clone https://github.com/ZineddineBE/ToDoList-Python-MongoDB.git
    cd ToDoList-Python-MongoDB
    ```

2. **Installez les dépendances** :
    ```bash
    pip install pymongo
    ```

---

## 🔧 Configuration

1. **Démarrer MongoDB** : Assurez-vous que **MongoDB** est bien installé et en cours d'exécution.  
2. **Importer les tâches initiales** :  
   Avant d'utiliser le programme, importez les tâches contenues dans le fichier `todolist.json` dans MongoDB en exécutant la commande suivante :

    ```bash
    mongoimport --db todolist_db --collection tasks --file tasks.json --jsonArray
    ```

3. **(Optionnel) Utiliser MongoDB Compass** :  
   Si vous souhaitez **visualiser et gérer les données** plus facilement, vous pouvez installer **MongoDB Compass** et l'utiliser pour **importer le fichier `todolist.json`** manuellement :
   - Ouvrez **MongoDB Compass**  
   - Connectez-vous à votre base de données (`mongodb://localhost:27017/` par défaut)  
   - Sélectionnez la base **todolist_db**  
   - Allez dans l'onglet **tasks** et cliquez sur **Import Data**  
   - Sélectionnez le fichier **tasks.json** et importez-le  

4. **Configurer la connexion MongoDB** :  
   Modifiez le fichier `connectiondb.py` si nécessaire pour adapter la connexion à votre base de données.

---

## ▶️ Utilisation

Lancez l'application en exécutant le fichier principal :

```bash
python main.py
