## TP3 - Gestion de la documentation

**Challenge:** Le post-doc génial du groupe est parti. Il travaillait sur un code super classe pour estimer les paramètres d'un modèle à partir de données d'une expérience de macro-biologie quantique en milieu relativiste.
Il a laissé son code, mais il n'a écrit aucune documentation ! A vous de jouer pour le documenter avant la release de la fin de semaine.

----

### Etape 0 : Générer un Software Design Documentation


*   Pourquoi le code a été créé ? Quelles sont les motivations, les challenges ?

*   Description succinte avec des mots simples du concept

*   Implémentation technique, dépendances externes

*   Implication à plus grande échelle ?

*   Autres méthodes existantes ?

----

### Etape 1 : Identifier les utilisateurs

* Est-ce que le code est un framework, une bibliothèque, un executable ?
* Est-ce que le code est en open source, sur une plateforme collaborative ?
* Y-a-t-il plusieurs contributeurs ? Des utilisateurs déjà identifiés ?

---

### Etape 2 : Documenter le code

* En utilisant des docstrings, documenter le code.
  Voir <a href="https://www.python.org/dev/peps/pep-0257">PEP 257</a>,
  <a href="https://www.python.org/dev/peps/pep-0258">PEP 258</a>,
  <a href="https://numpydoc.readthedocs.io/en/latest/format.html">numpydoc</a>,
  <a href="https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings">google</a>
* Rajouter les informations de <a href="https://docs.python.org/3/library/typing.html">type hint</a>
* Le refactoring vous démange ? C'est normal, et c'est sain.
---

### Etape 3 : Construire une documentation haut niveau

conda env create -f environment.yml

* Faisons une documentation utilisateurs en utilisant [sphinx](https://www.sphinx-doc.org/en/master/)

* Dans le dossier TP3, créer un dossier `doc`, et aller dans ce dossier.

* exécuter `sphinx-quickstart`

* Suivre les instructions à l'écran (modifiable plus tard)

* Executer `make html`, et ouvrir `_build/html/index.html`

* A vous de jouer maintenant en éditant les fichiers pour faire une documentation utilisateur. Penser à tout ce qui pourrait être utile: installation, quickstart, tutoriel, descriptions, liens utiles, ...

* Une fois la documentation faite, trouver un/une collègue, et discuter autour de vos docs respectives. La communication c'est important !

---

### Etape 4 : Pour aller plus loin

##### Intégration des tests

Vous ne verrez que cet après-midi les outils de test, mais c'est une bonne pratique de lier la documentation et les tests ensemble.<br/> Par exemple, quand vous lisez la documentation de [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html), les examples affichés sont aussi ceux qui servent à tester le code (unit tests).

    def function(arg):
      """
      A short description.

      A bit longer description.

      Parameters
      ----------
      arg : type
          description

      Returns
      -------
      type
          description

      Raises
      ------
      Exception
          description

      Examples
      --------
      Examples should be written in doctest format, and
      should illustrate how to use the function/class.
      >>>

      """
      pass

Essayer de rajouter des doctests aux fonctions du TP3\.

##### Automatisation de la chaîne

Le maintien de la documentation est plus efficace si la chaîne d'exécution est automatisée. <br/>La façon la plus simple de le faire est d'utiliser l'intégration continue pour re-générer la documentation automatiquement lors de modification du code. <br/>Vous aborderez les notions d'intégration continue demain, mais voici un example minimal sur la CI gitlab pour construire la doc et la publier sur gitlab pages automatiquement:

    image: python:3.9-alpine

    pages:
      script:
      - pip install sphinx
      - sphinx-build -d _build/doctrees . _build/html
      - mv _build/html public
      artifacts:
         paths:
         - public
      only:
      - master
---
