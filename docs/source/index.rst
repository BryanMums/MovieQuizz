.. MovieQuizz documentation master file, created by
   sphinx-quickstart on Fri Jun  3 16:40:15 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MovieQuizz's documentation!
======================================


This is the official documentation page for the MovieQuizz bot developed by Infinit8.

-------------------
Project description
-------------------
The Movie Quizz Bot will ask you very hard questions about movies to test your knowledge. Questions come from a JSON
file hand written with love. You can challenge your friends and determine who is the best by consulting your rank through
our great ranking system. The top 10 players will be displayed with the ranking command (see below).

---------
Contents
---------

.. toctree::

   Moviequizz class and methods <classbot>
   API communication (api_call method) <apicall>

------------
Make it work
------------

If you clone the git repo, you have to follow these steps to make it work :

**Clone the git**

#. Create a **config.py** file in the moviequizz folder
#. Set a **DEBUG** var (True or False)
#. Set a **TOKEN** var with your slack bot token key

**pip install**

The package is installable from the repo with git :

#. Create a virtual environment
#. pip install git+https://github.com/BryanMums/MovieQuizz.git
#. The MovieQuizzBot package will install...
#. **python -m moviequizz** to launch it ! Enjoy :)

--------
Commands
--------

There are the available commands for the Movie Quizz Bot :

* ask : ask a question about a movie
* rank : show your position and score in the worldwide ranking system of the bot
* ranking : show the top 10 world best players
* help : show this list

--------------
Special thanks
--------------
Special thanks to our great friend and colleague Alexandre Serex who gave use a great base for slack communication
and message sending.

Alexandre Serex' git_.

.. _git:  https://github.com/cyrilmanuel/picbot

------------------
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

