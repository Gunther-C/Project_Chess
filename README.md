
# Project_Chess
### **_Logiciel Tournoi d'échec_**
Tournoi évolutif, création sans élimination directe.  
Joueur, évolutif, Inscription club ou tournoi.  

![Project_Chess](https://github.com/Gunther-C/Dossier-Zip/assets/162619333/cc89cfb6-e777-4b84-bd0a-b8ea1d68c1fd)
###
##
## Joueur, Joueuse
___
### Critères d'inscription :
    1. Nom
    2. Prénom 
    3. Date de naissance 
    4. Identifiant national   
    5. Point acquis au niveau national
### Déroulement / possibilités :
    1. Inscription en club (mise en base de données)
    2. Inscription pour un tournoi (avec ou sans inscription en club)
    3. Recherche individuelle d'un joueur, joueuse inscrit au club (par nom ou identifiant national)  
    4. Liste des joueurs, joueuses inscrits dans le club
#
## Tournoi
___
### Création :
    1. Nom
    2. adresse 
    3. Date de début
    4. Nombre de tour(s)   
    5. Choix des joueurs, joueuses

### **_Option Sélection des joueurs, joueuses :_**
- **Joueurs du club,**    
- **Joueurs extérieurs au club,**    
- **Joueurs du club et joueurs extérieurs au club,**    
#
## Options supplémentaires du logiciel
___
### **_Alerte / Assistance :_**
- **à l'inscription d'un joueur, joueuse**    
- **à la recherche d'un joueur, joueuse**     
- **à la création d'un tournoi**      
- **erreurs système**  
> Ce logiciel est muni de nombreuses alertes détaillées  
afin de vous assister dans vos actions, voici trois exemples : 
>- le choix d'un nombre pair de participants à la création d'un tournoi, 
>- Un début de tournoi qui ne peut être antérieur à la date du jour, 
>- Un identifiant national non-valide. 
### **_Debug :_**
- **Rapport d'évaluation du système**   
> Analyse en temps réel du système, recherche et indexation des erreurs potentielles
### **_Raccourci bureau :_**
- **Fichier "Project_Chess.bat"**   
> Faite les installations requises ci-dessous. Ensuite,  
> Allez dans le dossier Project_Chess et clique droite sur le fichier "Project_Chess.bat" pour créer un raccourci bureau.  
> Vous n'aurez plus besoin de l'invité de commande pour ouvrir l'application.
> 
> **_(Ce raccourci peut ne pas fonctionner sous linux ou os)_**
#
___
___
#
## Installation  
___
####
### Python 3.12.2 >>>
####
_Téléchargement de Python_ :  
Rendez-vous sur la page de téléchargement officielle de Python : Télécharger Python1.
Choisissez la version de Python que vous souhaitez installer (par exemple, Python 3.12.2).
Sélectionnez votre système d’exploitation (Windows, Linux/UNIX, macOS, ou autre).
Cliquez sur le lien de téléchargement correspondant.
####
_Installation de Python_ :  
Une fois le téléchargement terminé, exécutez le fichier d’installation.
Suivez les instructions à l’écran pour installer Python sur votre système.
Assurez-vous d’ajouter Python à votre chemin d’accès système (cochez la case “Add Python to PATH” lors de l’installation sur Windows).
####
_Vérification de l’installation, Ouvrez **_votre terminal_** et Tapez :_  
 
>       python --version 
Et appuyez sur Entrée. Vous devriez voir la version de Python installée **_" Python 3.12.2. Ou plus "_**  

#
## Installation du projet sur votre machine 
___
####
### Récuperer le dossier du projet >>>
_Clone du projet_ :
####
```bash
  git clone https://github.com/Gunther-C/Project_Chess.git
```
### Installer l'environement virtuel >>>
- Décompresser le dossier sur votre bureau
- Ensuite, ouvrez votre terminal  

**_Voici les commandes à taper l'une après l'autre :_**  
_Taper une commande puis valider avec entrée et ainsi de suite_

>        cd < Le nom du dossier >  

>        python -m venv .venv  
_(n'oubliez pas le '.' au deuxième .venv)_

>_(pour la ligne de commande qui suit, selon votre système)_
> 1.     .venv\Scripts\activate.bat   
> 2.     source .venv/Scripts/Activate
> 3.     source .venv/bin/activate  
>_(Vous trouverez plus d'informations sur le site de [Stackoverflow](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows/18713789#18713789))_  
####

_(Résultat)_  
>- (.venv) doit apparaitre dans le chemin du project de l'invité de commande  
>
> 
>- taper la commande " _pip freeze_ " , pip doit ètre vide
###
### Installation des modules complémentaires >>>
####
> **_Vérifier la version de pip "pip24.0" :_**  
> 
>       pip --version (mettre à jour si besoin) pip install --upgrade pip24.0  

> **_Installer les modules nécessaires :_**  
> 
>       pip install -r requirements.txt (Vérifiez avec "pip freeze")

**_(N’oubliez pas que pour les utilisateurs POSIX (comme Mac OS X et Linux), il est recommandé d’utiliser un environnement virtuel pour gérer vos projets Python)._**  
#
## _Ouverture du logiciel_ (Fichier main.py)
_Toujours sur votre invité de commande : Mettez-vous dans le dossier du "Projet" si vous n'y êtes pas déjà,_  
_Puis taper ce qui suit ci-dessous, ensuite validé avec la touche entrée._ 
>       python main.py 

**_ou ,_**
> _(Si votre système d'exploitation le permet),_   
> 
>       Vous pouvez créer un raccourci bureau.  
>       Voyer la rubrique " Options supplémentaires du logiciel "

### _À vous de jouer_
___
### 🔗 Links 
 
[![linkedin](https://www.linkedin.com/in/gunther-chevestrier-813344255?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
