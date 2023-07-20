# Supervision d'Onduleurs Emeraude solaire

## Mise en place du projet
Clonez le dépôt git.

### Connexion à un onduleur
Ajoutez manuellement les informations de l'onduleur compatible Sunspec dans le fichier `config.py` dans le `debugPanel/sunData/`.

*Ce programme ne fonctionne qu'avec les onduleurs capables de se connecter au réseau ou bien avec leur propre réseau.*

### Exécution
Pour mettre en place le serveur : lancez le script python main.py à la racine de ce dépot.
Le panneau de configuration sera ensuite disponnible sur `localhost:8080`.

### Dépendances
- Python
- Flask
- Pysunspec2


## TODO
- detecter les champs input qui ne marche pas et les griser et ajouter feedback user
- raffraichir le champ qui vient d'être mise à jour
- regler le probleme de la curve qui s'apelle module
- test maitre esclave
- essayé d'acceder en sunspec à un onduleur où c'est pas activé
- démarage du systeme, scanner ip : trouver onduleur, scann slave id 0 à 255 et faire une page de panneau de config par onduleur trouvé
- cache pour que ça foncitonne au lancement et thread qui cherche des onduleurs