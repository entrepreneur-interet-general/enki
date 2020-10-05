Guide utilisateur pour le script d'import des utilisateurs VSSO

Installation de Python et des packages:

  Sur Windows :

  Python
  Se rendre a cette adresse : https://www.python.org/downloads/windows/
  Télécharger et installer la dernière release de la version 3 de python (ex: Latest Python 3 Release - Python 3.8.1)
    Télécharger l'installeur en .exe (ex : Windows x86-64 executable installer)
    Important : Selectionner l'option 'ajouter python 3.7 a votre PATH'

  Packages
  Ouvrir une console (Menu windows, rechercher 'cmd', entrée)

  Configuration du proxy Orion lancer les commandes (en changeant le login et le mot de passe) : 
    set HTTPS_PROXY=http://login:password@10.253.35.2:3128
    set NO_PROXY=localhost,127.0.0.1,minint.fr,mi

  pip install requests
  pip install python-keycloak

  Sur Ubuntu :

  Python:
  Ouvrir le terminal puis lancer les commandes suivantes (nécessite le mot de passe root)

  Configuration du proxy Orion lancer les commandes (en changeant le login et le mot de passe) :
    export HTTPS_PROXY=http://login:password@10.253.35.2:3128
    export NO_PROXY=localhost,127.0.0.1,minint.fr,mi

  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt install python3.7

  Packages
  pip install requests
  pip install python-keycloack


Lancement du script d'import d'utilisateur:

  Placer le fichier CSV d'utilisateur dans le même dossier que le script

  Ouvrir le fichier de configuration 'creation-utilisateur.conf' avec notePad puis editer les variables correspondantes (nom de serveur, mots de passes, nom du fichier csv)
  Ouvrir une console (Windows : Menu windows, rechercher 'cmd', entrée / Linux rechercher terminal) et se placer dans le répertoire du script avec la commande cd
    OU
  Depuis l'explorateur de fichiers dans le repertoire contenant le script :
    SHIFT + click droit > ouvrir shell windows ici
  
  executer le script de cette manière :
  python creationUsersFromCSV.py


Rapport de script:

Le script s'execute et affiche chaque création d'utilisateur, et affiche les erreurs s'il en survient
Un fichier csv est généré en fin de script, définissant le bilan des créations utilisateur sous forme de csv

