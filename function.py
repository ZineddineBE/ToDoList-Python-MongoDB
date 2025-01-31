import connectiondb as dbTask
import datetime as dt
import webbrowser
import time
import os

# Définition des couleurs ANSI
RED = "\033[31m"
GREEN = "\033[32m"
BOLD_UNDERLINE_PURPLE = "\033[1;4;35m"
WARNING = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Affiche toutes les taches
def displayAllTasks(tasks):

    if len(tasks) == 0:
        print("\nAucune tâche à afficher.\n")
        return

    for task in tasks:

        match task["statut"]:
            case 1:
                status = "à faire"
            case 2:
                status = "en cours"
            case 3:
                status = "terminé"

        print("\n--------------------------------------------------")
        print(f"Tache: {task["nom"]}\nStatut: {task["statut"]} ({status})")
        print("--------------------------------------------------")
    
    print(f"\nIl y a {BOLD}{len(tasks)} tâche(s){RESET} au total\n")

# Affiche toutes les taches
def displayTask():
    task_name = input(f"\n{BOLD}Quelle est la tâche que vous voulez afficher ?{RESET}\n")
    while not(dbTask.tasks_collection.find_one({"nom": task_name})):
        print(f"\n{WARNING}Cette tâche n'existe pas... Veuillez choisir une tâche qui existe{RESET} 👀\n")
        task_name = input(f"Quelle est la tâche que vous voulez afficher ?\n")

    task = dbTask.tasks_collection.find_one({"nom": task_name})
    match task["statut"]:
        case 1:
            status = "à faire"
        case 2:
            status = "en cours"
        case 3:
            status = "terminé"
    print("\n--------------------------------------------------")
    print(f"Tache: {task["nom"]}\nStatut: {task["statut"]} ({status})")
    print("--------------------------------------------------")

# Affiche les taches selon le paramètre choice
def displayTasksChoice(tasks, choice):
    match choice:
        case "à faire":
            status = 1
        case "en cours":
            status = 2
        case "terminé":
            status = 3

    found = False
    for task in tasks:
        if task["statut"] == status:
            found = True
            print("\n--------------------------------------------------")
            print(f"Tâche: {task['nom']}\nStatut: {task['statut']} ({choice})")
            print("--------------------------------------------------")

    if found:
        print(f"\nIl y a {BOLD}{len(tasks)} tâche(s){RESET} avec le statut {BOLD}'{choice}'{RESET}\n")
    else:
        print(f"\n{WARNING}Aucune tâche n'est {choice}.{RESET}")

# Ajouter une tâche avec le statut 'à faire' par défaut
def addTask():
    task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez ajouter ? ➕{RESET}\n")
    
    while (dbTask.tasks_collection.find_one({"nom": task_name})):
        print(f"\n{WARNING}Cette tâche existe déjà... Ajoutez-en une nouvelle qui n'existe pas{RESET} 👀\n")
        task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez ajouter ?{RESET}\n")

    newTask = {
        "nom": task_name,
        "statut": 1
    }
    
    dbTask.tasks_collection.insert_one(newTask)
    print(f"\n{GREEN}La tâche {task_name} a été ajouté !{RESET} ✅")
        
# Ajouter une tâche avec un statut au choix
def addTaskWithStatus():
    task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez ajouter ?{RESET} ➕\n")
    
    while (dbTask.tasks_collection.find_one({"nom": task_name})):
        print(f"\n{WARNING}Cette tâche existe déjà... Ajoutez-en une nouvelle qui n'existe pas{RESET} 👀\n")
        task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez ajouter ?{RESET}\n")
    
    statutTask = int(input(f"\n{BOLD}Quel est le statut de la tâche que vous voulez ajouter ?\n(1 : A faire | 2 : En cours | 3 : Terminé){RESET}\n"))
    while (statutTask <1 or statutTask >3):
            print(f"\n{WARNING}Le statut de la tâche doit être compris entre 1 et 3{RESET}\n")
            statutTask = int(input(f"{BOLD}Quel est le nouveau statut de la tâche {task_name} ?\n(1 : A faire | 2 : En cours | 3 : Terminé){RESET}\n"))

    newTask = {
        "nom": task_name,
        "statut": statutTask
    }
    
    dbTask.tasks_collection.insert_one(newTask)
    print(f"\n{GREEN}Tâche ajouté ! ✅{RESET}")

# Supprimer une tâche
def deleteTask():
    task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez supprimer ?{RESET} ❌\n")

    while not(dbTask.tasks_collection.find_one({"nom": task_name})):
        print(f"\n{WARNING}Cette tâche n'existe pas... Veuillez choisir une tâche qui existe pour la supprimer{RESET} 👀\n")
        task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez supprimer ?{RESET} ❌\n")

    task = { "nom": task_name }
    dbTask.tasks_collection.delete_one(task)
    print(f"\n{RED}La tâche '{task_name}' a été supprimé !{RESET} ✔\n")

# Mettre à jour une tâche
def updateTask():
    task_name = input(f"\n{BOLD}Quel est le nom de la tâche que vous voulez modifier ?{RESET} 🖊\n")
    task = dbTask.tasks_collection.find_one({"nom": task_name})

    while task is None:
        print(f"\n{WARNING}Cette tâche n'existe pas... Veuillez choisir une tâche existante.{RESET} 👀\n")
        task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez modifier ?{RESET} 🖊\n")
        task = dbTask.tasks_collection.find_one({"nom": task_name})

    new_task_name = input(f"\n{BOLD}Quel est le nouveau nom de cette tâche ?\n(Ancien nom : {task_name}){RESET}\n")

    while dbTask.tasks_collection.find_one({"nom": new_task_name}):
        print(f"\n{WARNING}Ce nom de tâche existe déjà... Veuillez choisir un autre nom.{RESET} 👀\n")
        new_task_name = input(f"\n{BOLD}Quel est le nouveau nom de cette tâche ?\n(Ancien nom : {task_name}){RESET}\n")

    new_status = input(f"\n{BOLD}Quel est le nouveau statut de la tâche '{task_name}' ?\n(Ancien statut : {task['statut']})\n(1 : À faire | 2 : En cours | 3 : Terminé){RESET}\n")

    while not new_status.isdigit() or int(new_status) < 1 or int(new_status) > 3:
        print(f"\n{WARNING}Le statut doit être compris entre 1 et 3.{RESET} 🚨\n")
        new_status = input(f"{BOLD}Quel est le nouveau statut de la tâche '{task_name}' ?\n(Ancien statut : {task['statut']})\n(1 : À faire | 2 : En cours | 3 : Terminé){RESET}\n")

    new_status = int(new_status)

    match task['statut']:
        case 1:
            old_status = "à faire"
        case 2:
            old_status = "en cours"
        case 3:
            old_status = "terminé"

    match new_status:
        case 1:
            status = "à faire"
        case 2:
            status = "en cours"
        case 3:
            status = "terminé"

    # Mise à jour de la tâche dans la base de données
    dbTask.tasks_collection.update_one(
        {"nom": task_name},  # Filtre pour trouver la bonne tâche
        {"$set": {"nom": new_task_name, "statut": new_status}}  # Nouvelles valeurs
    )

    print(f"\n{GREEN}Le nom de la tâche '{task_name}' a été modifié en '{new_task_name}' !{RESET} ✅")
    print(f"{GREEN}Le statut est passé de '{task['statut']}' ({old_status}) à '{new_status}' ({status}) !{RESET} ✔\n")

# Compléter une tâche (la marquer comme terminée avec la date du jour)
def completeTask():
    task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez completer ?{RESET} 🟢\n")

    while not(dbTask.tasks_collection.find_one({"nom": task_name})):
        print(f"\n{WARNING}Cette tâche n'existe pas... Veuillez choisir une tâche qui existe pour la completer{RESET} 👀\n")
        task_name = input(f"{BOLD}Quel est le nom de la tâche que vous voulez completer ?{RESET} 🟢\n")
    
    task = dbTask.tasks_collection.find_one({"nom": task_name})
    new_task_status = { "$set": { 'statut': 3, "date": str(dt.date.today())} }
    dbTask.tasks_collection.update_one(task, new_task_status)
    print(f"\n{GREEN}La tâche '{task_name}' a été complété !{RESET} ✅\n")
    
def menu():
    print(f"\033[\n1;36mBienvenue sur votre \033[4;1;36mTo Do List{RESET} \033[1;36m{os.getenv("USERNAME")} !{RESET}")

    while True:  # Boucle principale du menu
        print(f"{BOLD_UNDERLINE_PURPLE}\nMenu:\n{RESET}{BOLD}1-Afficher les tâches [+]\n2-Ajouter une tâche [+]\n3-Modifier une tâche\n4-Supprimer une tâche\n5-Compléter une tâche\n6-Quitter 🚪{RESET}\n")

        choice = input(f"{BOLD}Que voulez-vous faire ?{RESET}\n")

        if not choice.isdigit() or int(choice) not in range(1, 7):
            print(f"\n{WARNING}Choix invalide, choisissez un chiffre compris entre 1 et 6{RESET}\n")
            continue  # Redemande un choix valide

        choice = int(choice)

        if choice == 6:
            redirection()
            exit()

        if choice == 1:  # Sous-menu affichage
            while True:
                print(f"\n{BOLD_UNDERLINE_PURPLE}Sous-menu (affichage):{RESET}\n{BOLD}1-Afficher toutes les tâches\n2-Afficher la tâche que vous souhaitez\n3-Afficher les tâches à faire\n4-Afficher les tâches en cours\n5-Afficher les tâches complétées\n6-Retour au menu principal ←{RESET}\n")
                
                choiceDisplay = input(f"{BOLD}Que voulez-vous faire ?{RESET}\n")

                if not choiceDisplay.isdigit() or int(choiceDisplay) not in range(1, 7):
                    print(f"\n{WARNING}Choix invalide, choisissez un chiffre compris entre 1 et 6{RESET}\n")
                    continue

                choiceDisplay = int(choiceDisplay)

                if choiceDisplay == 6:
                    break  # Retour au menu principal

                if choiceDisplay == 1:
                    displayAllTasks(dbTask.tasks)
                elif choiceDisplay == 2:
                    displayTask()
                elif choiceDisplay == 3:
                    displayTasksChoice(dbTask.tasks, "à faire")
                elif choiceDisplay == 4:
                    displayTasksChoice(dbTask.tasks, "en cours")
                elif choiceDisplay == 5:
                    displayTasksChoice(dbTask.tasks, "terminé")

        elif choice == 2:  # Sous-menu ajout
            while True:
                print(f"\n{BOLD_UNDERLINE_PURPLE}Sous-menu (ajout):{RESET}\n{BOLD}1-Ajouter une tâche (par défaut : 'à faire')\n2-Ajouter une tâche (avec n'importe quel statut : 'à faire'/'en cours'/'terminé')'\n3-Retour au menu principal ←{RESET}\n")

                choiceAdd = input(f"{BOLD}Que voulez-vous faire ?\n")

                if not choiceAdd.isdigit() or int(choiceAdd) not in range(1, 4):
                    print(f"\n{WARNING}Choix invalide, choisissez un chiffre compris entre 1 et 3{RESET}\n")
                    continue

                choiceAdd = int(choiceAdd)

                if choiceAdd == 3:
                    break  # Retour au menu principal

                if choiceAdd == 1:
                    addTask()
                elif choiceAdd == 2:
                    addTaskWithStatus()

        elif choice == 3:
            updateTask()
        elif choice == 4:
            deleteTask()
        elif choice == 5:
            completeTask()

# Redirection vers mon linkedin après 5s quand on décide de quitter le programme
def redirection():
    i = 0
    time_redirection = 5

    print(f"\n\033[1;36mMerci d'avoir utilisé mon programme {os.getenv("USERNAME")} !{RESET}")

    for i in range(time_redirection):
        print(f"{GREEN}Redirection vers ma page Linkedin dans {str(time_redirection-i)} s{RESET}", end="\r")
        time.sleep(1)
        i += 1
    webbrowser.open('https://www.linkedin.com/in/zineddine-beouche/')