# Willkommen in Chat Maze

**See the english version [below](./README.md/#welcome-to-chat-maze)**

## An alle Spieler

Liebe Spieler,

Seid ihr bereit, ein spannendes Abenteuer zu erleben? In Chat Maze werdet ihr herausgefordert, unterschiedliche Figuren mit einzigartigen Persönlichkeiten aus komplexen Labyrinthen zu begleiten. Eure Aufgabe ist, ihnen den richtigen Weg zu zeigen und sie gefahrlos zum Ausgang zu führen.

Jede Figur in diesen Labyrinthen hat seine eingene Persönlichkeit, z.B. versnobter Prinz, reimende Dichterin oder ein Verrückter. Eure Anweisungen sind die einzige Möglichkeit für sie, die verwirrende Labyrinthe zu verlassen. Seid jedoch gewarnt: einige Figuren dürfen genauso anspruchsvoll wie ihre Labyrinthe sein.

Viel Spaß!

### Vor dem ersten Start

Öffnen Sie das Verzeichnis `../chat-leap/data` erstellen Sie die Datei **config.json**. Diese Datei muss nur folgende Zeile mit Ihrem OpenAI API Key enthalten, den Sie anstatt **YOUR API KEY** innerhalb Anführungszeichen `""` hinzufügen sollten:
```
    {
        "api_key" : "YOUR API KEY"
    }
```

### How to play

Um das Spiel zu starten, starten Sie im Verzeichnis `../Chat Maze` die Datei `Chat Maze.exe`.

_Achtung: Chat Maze **erfordert keine** Administrator Rechte oder andere außergewöhnliche Dinge. Sei das nicht der Fall, sollten Sie etwas gefährliches heruntergeladen haben!_

Nach dem Start bekommen Sie eine Willkommensnachricht im Chat, die Sie kurz über Chat Maze anweisen wird. Sie müssen unterschiedliche Figuren helfen, aus ihren Labyrinthen zu fliehen, indem Sie ihnen einfache Weganweisungen geben. Einige von ihnen sind leicht zu führen, während andere ziemlich knifflig mit Ihnen auskommen werden. Viel Spaß, sie alle zu begegnen :3

Hier sind ein paar hilfreiche Befehle:
- `/commands` - listet alle vorhandene Befehle auf.
- `/help` - gibt Hinweis zum Verhandeln mit aktueller Figur.
- `/exit` - schließt das Spielfenster.

## Über das Projekt

Wir sind ein kleines, aber feines Team aus dem Studiengang Ingenieursinformatik der HTW Berlin. Mit Unterschtützung und Betreuung von _Prof. Dr. Erik Rodner_ und _Nils Harnischmacher_ haben an diesem Projekt ganz stark gearbeitet:
|        Wer        |  hat  | was gemacht?                                                         |
| :---------------: | :---: | :------------------------------------------------------------------- |
|    Oskar Fulde    |  -->  | Hat eine vernünftige Verbindung mit ChatGPT über OpenAI eingesetzt   |
|  Nealjade Laluna  |  -->  | Hat all die Persönlichkeiten ausgedacht und ihre Prompts geschrieben |
| Louis Schmolinske |  -->  | Hat das komplette Interface gebastelt und angepasst                  |
|    Robert Koch    |  -->  | Hat alle Strafen, Schwierigkeitsgrade und Maze Features angelegt     |

# Welcome to Chat Maze 

## To all players

Dear Players,

Are you ready for an exciting adventure? In Chat Maze you are challenged to guide various characters with unique personalities out of complex labyrinths. Your goal is to show them the right path and lead them out safety.

Each character in this labyrinth has their own quirks – be it a snobbish prince, a rhyming poet or a madman. Your instructions are their only way out of these tangled mazes. But be warned, some characters can be as challenging and unpredictable as the labyrinth itself.

Have fun!

### Before Playing

Go to the `../chat-leap/data` directory and create a file called **config.json**. This file must contain the following and the only one necessary line for connecting to OpenAI's API. Replace **YOUR API KEY** with your actual API key leaving it withing double quotation marks `""`:
```
    {
        "api_key" : "YOUR API KEY"
    }
```

### How to play

To start the game, go to the `../Chat Maze` directory and start `Chat Maze.exe` file.

_Note: Chat Maze **doesn't require** any administrator's permissions or other serious things to run, otherwise you might've downloaded something dangerous!_

As the game starts you'll see a welcome message which give you a brief guide, what Chat Maze is about. Basically, you have to help various characters to escape mazes they're captured in by giving them a direction to walk along. Some of these characters are pretty easy to get along with, others are quite tricky to communicate. Have fun encountering all of them :3

Here are some useful utility commands you may need:
- `/commands` - to see a list of all commands.
- `/help` - to get help with your current level.
- `/exit` - to close the game.

## About the project

We are a small but fine Team from Computational Science and Engineering course at HTW Berlin. With all the support and guidance from _Prof. Dr. Erik Rodner_ and _Nils Harnischmacher_ in this project was put decent effort and many hard work by:
|        Who        |  did  | what?                                                    |
| :---------------: | :---: | :------------------------------------------------------- |
|    Oskar Fulde    |  -->  | Got along with communicating with ChatGPT via OpenAI API |
|  Nealjade Laluna  |  -->  | Wrote all the personalities and their prompts            |
| Louis Schmolinske |  -->  | Researched and made all the UI/UX elements               |
|    Robert Koch    |  -->  | Figured out penalties, difficulties and mazes' features  |