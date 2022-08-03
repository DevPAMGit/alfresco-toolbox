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