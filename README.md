
# Project_Chess
### **_Logiciel Tournoi d'échec_**
Récupérer des infos sur https://books.toscrape.com/ puis les stocker par classifications, dossiers, fichiers.csv
##
## Fonction / Objectif
### Mode de récupération :
- Historique complet du site
- Catégories et ses produits
- Produit

### Type de récupération :
#### Données de l'article
    1. Catégorie 
    2. Nom 
    3. Lien 
    4. Descriptif 
    5. Code   
    6. Prix HT
    7. Prix TTC
    8. Evaluation
    9. Lien photo

#### Objet de l'article
    1. Photo  

#
## Installation  
####
**_Sous Windows (option bas de page)_** :
####
### Python 3.12.2 =>  
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
 
        python --version 
Et appuyez sur Entrée. Vous devriez voir la version de Python installée **_" Python 3.12.2. Ou plus "_**  

#
## Installation du projet sur votre machine 
####
### Récuperer le dossier du projet =>
_Clone du projet_ :
####
```bash
  git clone https://github.com/Gunther-C/Project-BooksOnline.git
```
![Capture d'écran](https://github.com/Gunther-C/Dossier-Zip/assets/162619333/b7a4d2b9-e37b-41e7-acda-8553e34e1e1f)
###
### Installer l'environement virtuel =>
    > Décompresser le dossier sur votre bureau
    > Ensuite ouvrez votre terminal
####
Aller dans le dossier répertoire du projet / Créer l'environment / activer :  

        cd < Le nom du dossier >

    (Le Chemin doit comporter le nom du dossier)
####
_(Créer l'environment)_  

        python -m venv env
####
_(Activer)_  

        env\Scripts\activate.bat

    Avec PowerShell et Cyguin (Activate avec une majuscule):
        source env/Scripts/Activate

    Sinon : 
        source env/bin/activate

_Vous trouverez plus d'informations sur le site de [Stackoverflow](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows/18713789#18713789)._  
####
_(Résultat)_  
1. (env) doit apparaitre  
    _(env) /cygdrive/c/Users/(nom utilisateur)/desktop/(nom du dossier Project-Books...)$_
2. Tapper la commande " _pip freeze_ " , pip doit ètre vide
###
### Installation des modules complémentaires =>
####
**_Vérifier la version de pip "pip24.0"_**

        pip --version 

    (Mettre a jour si besoin)        

        pip install --upgrade pip24.0  
###
**_Installer les modules nécessaires_**  

        pip install -r requirements.txt

        (Vérifiez avec "pip freeze")

(N’oubliez pas que pour les utilisateurs POSIX (comme Mac OS X et Linux), il est recommandé d’utiliser un environnement virtuel pour gérer vos projets Python.)  
#
## _Exemples_ ( Fichier main.py )
_Mettez-vous dans le dossier du "Project" puis tapper_ :

        python main.py
###
**_Toutes les catégories et leurs produits_**

        Arg_1 = directory_N
**_Une catégorie et ses produits_**

        Arg_1 = category_N (recherche aléatoire)
        ou
        Arg_1 = category_N,  Arg_2 = <nom de la catégorie>
**_Un produit_**

        Arg_1 = product_N (recherche aléatoire)
        ou
        Arg_1 = product_N,  Arg_2 = <nom du produit>
 
- **Inutile de mettre plus que les 4 premiers mots d'un produit'**  
- **Dans tous les cas ne pas renseigner les parenthèses et leur contenu**  
#
#
**_Sous Windows, vous pouvez installer Cyguin_** :
####
Cygwin est idéal pour les tests et le développement, car il permet d’utiliser les utilitaires UNIX/Linux sur Windows, il est compatible avec les anciennes versions de Windows, contrairement à l’environnement WSL proposé par Windows,  
####
_Téléchargement_ :  
Rendez-vous sur le site officiel de Cygwin.
Cliquez sur la rubrique “Install Cygwin” située à gauche.
Choisissez l’exécutable à télécharger en fonction de votre version de Windows (32 ou 64 bits).  
####
_Installation_ :  
Lancez le fichier exécutable téléchargé.
Acceptez toutes les invites et avertissements affichés à l’écran, notamment ceux du Contrôle d’accès des utilisateurs de Windows.
Le programme d’installation s’ouvrira. Cliquez sur “Suivant” pour continuer la configuration.
Une invite vous permettra de sélectionner une source de téléchargement. Dans la plupart des cas, l’option par défaut “Installer depuis Internet” convient et doit être conservée.  
####
 
**_Rendez-vous dans votre dossier Cyguin puis suivez ces étapes_**

        Dossier home ->   
        Ouvré le dossier portant votre nom d'utilisateur -> 
        Ouvré le fichier " .bash_profile " avec notPad ou autre -> 
        En bas de page taper "cd /cygdrive/c/Users/<le nom de votre dossier utilisateur>/desktop/" ->
        Enregistré

##
##
### 🔗 Links

[![linkedin](https://www.linkedin.com/in/gunther-chevestrier-813344255?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
