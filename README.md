# Alfresco Toolbox  
## Description
Script Python dont le but est de faciliter le développement Java d'un AMP Alfresco en générant les classes modèles des types de contenus déclarés.

Il faut au préalable avoir déclarer des types de contenus et les avoir insérer dans le fichier _bootstrap.xml_.

Ensuite, ce script va lire dans ce fichier les éléments déclarés dans comme modèles. 
Et pour chacun il créera les fichiers _.java_ pour chaque **aspects** et **types** déclarés dans chaque fichier modèle.

Par exemple pour un projet Alfresco  *All-in-One* composé de ces données:

| organisation | artifact id  | nom modèle | type | aspect
|--|--|--|--|--|
| org.cd59  | affichage-des-actes | acme:contentModel | acme:document | acme:securityClassified |

Le script génèrera l'arborescence _java_ ci-dessous:
```
.
└── org.cd59
    └── affichagedesactes.modeles
        └── sources
        └── typescontenus.acme
            ├── aspects
            │   └── securityclassified
            │       └── SecurityclassifiedAspectHelperModele.java                
            │       └── SecurityclassifiedAspectModele.java
            └── types
                └── document
                    └── DocumentTypeHelperModele.java
                    └── DocumentTypeModele.java
```

Chaque classe type et aspect dépende de la classe *AlfrescoModeleHelper* qui dépend de la classe *AlfrescoHelper*,
elles aussi générées grâce au script.

## Actions
### Description
Alfresco propose dans son framework la création d'actions permettant d'exécuter des actions sur son environnement.
Ces actions sont sujettes à la création de fichiers et de déclaration de ces derniers dans différents points du projet.
Se faisant ces actions ont été automatisées au sein d'une sous api ("action") qui gère tout ce qui est relatif 
à la déclaration d'action au sein du projet Alfresco.

### Fonctionnement
#### Le script
Cette api fonction en deux temps. 

Le premier est l'**initialisation**, le script va créer un dossier dans lequel nous le développeur pourra déposer ses 
développements (.java) d'action *Alfresco*. Ce dossier (package) sera créé dans le projet platform, dans le package :
organisation.artifact_id.action.

Le second, est la **prise en compte** : L'api va chercher dans le dossier précédemment créer toutes les actions qui ont 
été créées et va les déclarer à qui de droit pour une prise en compte dans l'environnement Alfresco. D'après la 
documentation Alfresco, cette prise en compte reviendrait à :
* Créer le fichier *action-context.xml* si celui-ci n'existe pas.

* Pour chaque fichier de classe Java se définissant comme une action, c'est-à-dire dont la classe étend à la classe 
 **ActionExecuterAbstractBase** Alfresco, le déclarer dans le fichier *action-context.xml*.

* Si un fichier déclare l'utilisation en tant que paramètre la classe **ServiceRegistry**, alors dans sa déclaration le
script ajoutera une propriété faisant référence à celle-ci.

* Ensuite, si cela n'est pas déjà fait, le script va référencer le fichier *action-context.xml* dans le fichier 
*module-context*.

* Enfin, si les informations glanées dans la classe java le permettent, le script va créer si nécessaire le fichier
de propriétés *I18N*, et y renseigner les descriptions, titres et labels des actions. 

Dans un projet où les données seraient :

| organisation | artifact id  | 
|--|--|
| org.cd59  | affichage-des-actes |

L'arborescence ressemblera à cela (les éléments notés d'une étoile sont créées si nécessaires, modifiés sinon. Ceux 
avec deux sont seulement modifiés) :

```
affichage-des-actes
└── affichage-des-actes-platform
    └── src.action
        └── main
            ├── java
            |    └── org.cd59.affichagedesactes.action*
            |        └── Action1.java
            |        └── Action2.java
            |        └── Action3.java
            └── ressources
                └── alfresco
                    └── module.affichage-des-actes-platform
                        ├── context
                        |   └── action-context.xml*
                        ├── messages
                        |   └── action-config.properties*
                        └── module-context.xml**                     
```
