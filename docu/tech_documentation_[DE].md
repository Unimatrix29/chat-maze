# Chat Maze: Technische Dokumentation

- [Einführung](./chat-maze-technische-dokumentation.md#einführung)
- [Spezifikation](./chat-maze-technische-dokumentation.md#spezifikation-todo)
- [Spielablauf](./chat-maze-technische-dokumentation.md#spielablauf)
- Aufbau des Projekts
    - [Verbindung mit Chat GPT](./chat-maze-technische-dokumentation.md#verbindung-mit-chatgpt)
    - [Verarbeitung von Antworten](./chat-maze-technische-dokumentation.md#verarbeitung-von-antworten)
    - [GUI](./chat-maze-technische-dokumentation.md#gui)
      - [setup_screen()](./chat-maze-technische-dokumentation.md#setup_screen)
      - [update_screen()](./chat-maze-technische-dokumentation.md#update_screen)
- Spieleinstellungen
    - [Schwierigkeitsgrade](./chat-maze-technische-dokumentation.md#schwierigkeitsgrade)
    - [Prompts](./chat-maze-technische-dokumentation.md#prompts)
    - [Maze-Aufbau](./chat-maze-technische-dokumentation.md#maze-aufbau)
      - [Kleine Mazes](./chat-maze-technische-dokumentation.md#kleine-labyrinthe)
      - [Größere Mazes](./chat-maze-technische-dokumentation.md#größere-labyrinthe)
      - [Animationen](./chat-maze-technische-dokumentation.md#animationen)
- [Links](./chat-maze-technische-dokumentation.md#links)

## Einführung 

Dieses Dokument dient dafür, Funktionsweise und Merkmale vom Projekt Chat Maze neugierigen Entwicklern zu erklären. Es wird vorausgesetzt, dass man bereits Grundlagen der objektorientierten Programmierung kennengelernt hat, sowie Syntax und Verwendung von externen Bibliotheken in Pythonanwendungen. Zunächst wird der grundlegender Programmablauf dargestellt, mithilfe dessen es ein bisschen weniger Aufwand beim Nachvollziehen von Aufbau und Zusammenhängen zwischen Klassen in weiteren Kapiteln geben sollte. Danach werden einzelne Features bzw. Klassen, ihre Methoden und Implementierung beschrieben, was potentiellen Weiterentwicklern und tieferem Verständnis des Projekts helfen sollte.
In Erklärungen können folgende Begriffe auftauchen, die zum ersten Mal verwirrend sein mögen:

- Ein Spieler - ein Mensch, der die Weganweisungen gibt und so eine Figur steuert.
- Eine Figur - ein Quadrat auf dem Bildschirm, das eine ChatGPT-Rolle repräsentiert.
- Eine Rolle - ein Verhandlungsmuster, das dem ChatGPT vor jedem Spiel übergeben wird.

Es werden ab und zu Code-Beispiele gegeben, die auf echtem Code von diesem Projekt basieren. Diese stellen eine einfachere und manchmal die erste Implementation von zu besprechenden Features dar, damit man eine Vorstellung bekommt, was im wirklichen Code vorkommt.
In diesem Projekt wurden mehrere externe Bibliotheken wie _OpenAI_ und _pygame_ verwendet, die hier nicht ausführlich erklärt werden, weil sie bereits eigene Dokumentationen besitzen (_siehe Abschnitt “Links”_).

## Spezifikation

Für das Projekt sind folgende Anwendungen erforderlich:
- [Python 3.12.3](https://www.python.org/downloads/) 
- [Anaconda 24.5.0](https://www.anaconda.com/) (_oder höher_)
- [OpenAI API key](https://platform.openai.com/api-keys) (_**nicht kostenfrei**_)

### Vorbereitung

Wenn alle Anwendungen installiert worden sind, gehen Sie folgende Schritte durch:
1. Im Verzeichnis `../chat-leap/src` erstellen Sie eine Datei **config.json** und kopieren Sie folgende Zeile dahin, wobei anstatt **YOUR API KEY** Ihr OpenAI API Key zwischen Anführungsstrichen `""` gespeichert wird:
```
    {
        "api_key" : "YOUR API KEY"
    }
```
2. Öffnen Sie Anaconda Prompt und wechseln Sie zum Hauptverzeichnis vom Projekt: `../chat-leap`.
3. Geben Sie folgenden Befehl ein, um das vorbereitete Environment (_lndw_) zu erstellen:   
```
    conda env create -f environment.yml
```
4. Öffnen Sie das Projekt in Ihrem Code Editor und wechseln Sie das voreingestellte Environment zum gerade eben erstellten (_lndw_).

Nun können Sie den Code selber modifizieren und ausführen.
   
## Spielablauf

Da für jedes Feature oft mehrere Klassen zuständig sind, wäre es zunächst total sinnvoll, sich den gesamten Spielablauf anzuschauen. Man kann alle Aktivitäten in folgenden Kategorien unterteilen:

- Erfassung von Benutzereingaben (_Text oder Sprache_)
- Verbindung mit ChatGPT
- Erarbeitung von Antworten
- Spielverwaltung (_Anwendung von Strafen, Bewegung von Figuren und Labyrinthwechsel_)
- Graphische Darstellung von Labyrinthen und Chatabläufen

Folgendes Diagramm stellt den in diesem Projekt implementierten **_Kernprozess_** dar:

![alt-text](./prozess-diagramm.png "Kernprozess")

Wie es schon wahrscheinlich aufgefallen ist, ist das ganze Spiel eine dauerhafte Schleife. Diese Schleife kann sowohl beim Erreichen vom Ende des gespielten Labyrinths, als auch manuell durch ein Restart-Kommando (_/restart oder /newgame_) unterbrochen werden.Damit man sehen kann, was überhaupt im Spiel passiert, gibt es eine Methode *update_screen()* der Klasse _Screen_, die für eigentliches Zeichnen des GUIs zuständig ist. Diese wird dauerhaft nebenläufig dem o.b. Kernprozess ausgeführt. Wenn das Spiel zu Ende ist, wird ein der vorhandenen Endscreens (_auch animierte_) gezeigt, wo man einen Schwierigkeitsgrad auswählen und somit ein neues Spiel starten kann.
Die Hauptklasse, die alle Bausteine des Projekts zusammenführt, ist _GameLoop_. Der o.g. Kernprozess läuft innerhalb der _run()_ Methode dieser Klasse ab. Sobald das Spielfenster geschlossen wird, wird die Schleife in _run()_ nach laufender Iteration unterbrochen und alle verwendete Threads mit _close()_ geschlossen.

## Aufbau des Projekts 

### Verbindung mit ChatGPT

#### API-Anfragen

Um eine Verbindung mit [OpenAIs API](https://platform.openai.com/docs/overview) herzustellen und somit mit ChatGPT, wird ein HTTPS-Client benötigt. Dieser lässt sich sehr einfach über die Python-Bibliothek „_openai_“ von OpenAI erstellen. Für genauere Details siehe die [API-Referenz](https://platform.openai.com/docs/api-reference/introduction) von OpenAI.

Die Aufgabe der Client-Erstellung übernimmt die Klasse „_ApiClientCreator_“ mit der Methode „_getclient()_“. Dem Client muss ein gültiger [API-Key](https://platform.openai.com/docs/quickstart) übergeben werden. Dieser wird aus einer JSON-Datei geladen. Der Standardname der Datei ist „_config.json_“. Möchte man die Datei anders benennen, muss der neue Dateiname beim Aufruf von „_getclient()_“ als Argument übergeben werden. Des Weiteren kann optional auch noch eine Timeout-Zeit für die HTTPS-Anfrage mitübergeben werden. Der Standard hier ist 60 Sekunden.
Nun, da uns ein [API-Client](https://platform.openai.com/docs/api-reference/authentication) zur Verfügung steht, können wir uns der Kommunikation mit der API widmen. Die API stellt mehrere Möglichkeiten und Funktionen zur Verfügung, um mit den einzelnen Sprachmodellen zu interagieren. In unserem Spiel verwenden wir die [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-, sowie die [Text-zu-Audio](https://platform.openai.com/docs/guides/text-to-speech)- und die [Audio-zu-Text](https://platform.openai.com/docs/guides/speech-to-text)-Funktionen der einzelnen Modelle von OpenAI. Verwaltet und durchgeführt werden die einzelnen Anfragen von der „_ChatGPT_“-Klasse in „_ChatGPT_Controller.py_“. Dieser Klasse muss beim Aufrufen der zuvor erstellte Client übergeben werden. In einer Liste wird der Kommunikationsverlauf mit dem Text-zu-Text-Modell gespeichert. Standardmäßig werden nur fünf Nachrichten gespeichert. Dabei ist eine Nachricht die Anfrage des Users plus die Antwort des Modells. Die Nachrichten werden im [Response-Format der API](https://platform.openai.com/docs/guides/chat-completions/response-format) gespeichert, wobei nur die „_content_“- und „_role_“-Informationen gespeichert werden. Wenn mehr als fünf Nachrichten gespeichert werden sollen, kann beim Aufruf als zweites Argument die maximale Nachrichtenanzahl mitübergeben werden.

Schauen wir uns zuerst den [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-Aufruf an. Dieser erfolgt in „_texttotext()_“. Die Methode hat vier Argumente, von denen zwei optional sind. Das „_retry_“-Argument ist für das Error-Handling beim API-Call vonnöten. Der Methode kann als Argument der Name des zu verwendenden [ChatGPT-Modells](https://platform.openai.com/docs/models) übergeben werden, das Standardmodell ist „[gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)“. Der Rückgabewert ist das [Response-Objekt der API](https://platform.openai.com/docs/guides/chat-completions/response-format). Das einzige nicht optionale Argument ist die zu sendende Nachricht. Diese Nachricht muss in einem bestimmten Format sein. Um einen gegebenen String in ein für die API nutzbares [Format](https://platform.openai.com/docs/api-reference/chat/create) zu bringen, gibt es die „construct_message()“-Methode. In dieser Methode wird die aktuelle Eingabe des Nutzers, der System-Prompt und der Kommunikationsverlauf in einem Dictionary zusammengeführt, wobei die Keys den entsprechenden Rollen in Bezug auf die API entsprechen. Die möglichen Rollen sind: „_system_“, „user“ und „_assistant_“.

**(Wichtig! Diese Rollen haben nichts mit den Charakteren/Rollen unseres Spieles zu tun, sondern sind von der API vorgeschrieben.)**

Der [Text-zu-Audio](https://platform.openai.com/docs/guides/text-to-speech) ist im Grunde nicht sehr unterschiedlich zum [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-Aufruf. Dieser wird durch die „_texttoaudio()_“-Methode durchgeführt. Auch hier kann wieder der Name eines [Modells](https://platform.openai.com/docs/models) angegeben werden. OpenAI hat hierfür zwei Modelle zur Verfügung: „[_tts-1_](https://platform.openai.com/docs/models/tts)“ und „[_tts-1-hd_](https://platform.openai.com/docs/models/tts)“. Zudem kann die Stimme, mit der der Text synthetisiert werden soll, angegeben werden. OpenAI hat hier sechs [Stimmen](https://platform.openai.com/docs/guides/text-to-speech/overview) zur Auswahl. Im Gegensatz zum Text-zu-Text-Aufruf muss für den Text-zu-Audio-Aufruf der zu synthetisierender Text nicht in einem bestimmten Format sein. Entsprechend kann ein einfacher String übergeben werden. Auch hier ist das „_retry_“-Argument für das Error-Handling beim API-Call vonnöten. Der API-Call gibt ein Audio-Objekt zurück, welches mit der „_writeaudiotofile()_“-Methode in eine .wav-Datei namens „_tts_out.wav_“ geschrieben wird. Die Datei wird im "_/src_"-Ordner abgelegt. Wenn die Datei nicht existiert, wird sie beim Initialisieren der Klasse erstellt.  

Der [Audio-zu-Text](https://platform.openai.com/docs/guides/speech-to-text)-Aufruf in der „_audiototext()_“-Methode verwendet den ["transcription“-Endpoint](https://platform.openai.com/docs/api-reference/audio/createTranscription) der API. Auch hier kann wieder ein Modell angegeben werden, auch wenn nur eines zur Verfügung steht, ["whisper-1"](https://platform.openai.com/docs/models/whisper). Des Weiteren kann ein optionaler Prompt mitübergeben werden, um dem [Modell](https://platform.openai.com/docs/models) einen Kontext der Transkription zu geben und diese potenziell zu verbessern. Auch diese Methode hat das Error-Handling-Argument „_retry_“. Die Audiodaten werden aus der im "_/src_"-Ordner liegenden „_userinput.wav_“-Datei gelesen. Diese Datei wird, wenn nicht vorhanden, auch beim Initialisieren der Klasse erstellt. Die Methode gibt den transkribierten Text als String zurück.

#### API-Antworten 

Die *chatgpt_movment* Klasse Implementiert nun die Oben erklärten Konzepte. Wie in der Doku schon erklärt, gibt ChatGPT neben einem passenden Antworttext auch eine Richtung für die Bewegung der Spielfigur zurück. Entsprechend wird die Antwort in zwei Teile geteilt und die Richtung mithilfe eines Dictionary in einen Vektor umgewandelt: 
```python
self.move_options = {"up": [0, -1], "down": [0, 1], "left": [-1, 0], "right": [1, 0], "weird": [0, 0], "deny": [-1, -1]}

    content = chat_response.choices[0].message.content
    
    self.chatgpt.set_history("assistant", content)
    
    # Parse the response
    # For reference, see the prompt documentation
    text = content.split("|")

    direction = text[0].lower().strip()
    if direction in self.move_options:
        move_vector = self.move_options[direction]
    else:
        move_vector = self.move_options["deny"]
```
Anschließend werden all die Funktionalitäten in der *__get_chatgpt_response()* Methode in _GameLoop.py_ zusammengefasst und ausgeführt. Um ein einfrieren und stocken der UI zu verhindern läuft diese Methode auf einem separaten Thread:
```python
    movmentChatGPT = chatgpt_movment(chatgpt=chatgpt, model=gpt_model)

    while not self._gameOver_event.is_set():
        try:        
            msg = self._screen_queue.get(False)
            #chatGPT call
            data["mVector"], data["content"] = movmentChatGPT.get_vector(msg, temperatur, prompt)
            
            if self.audio_event.is_set():
                name = self.prompt[0]
                current_voice = voices.get(name, "onyx")
                chatgpt.text_to_audio(data["content"],voice=current_voice)
                self._audio_is_ready_event.set()
            
            data["role"] = "GPT-4o" 
            self._chatgpt_queue.put(data)
```
Hier werden Instanzen der einzelnen Klassen erstellt und die Aufrufe getätigt, sowie das Finale Error-Handling und Informieren des Users. Des weiteren werden hier die Antworten von ChatGPT in Queues gelegt um eine Thread Sichere Kommunikation zu gewährleisten. Dies wird unterstützt durch Events wie „*self.audio_event*“, um auf bestimmte Stadien korrekt reagieren zu können.

### Verarbeitung von Antworten

#### Bewegung der Figur

Dieses Feature wird durch Kombination verschiedener Klassen und deren Methoden realisiert. Als zentrale Klasse, mit der hier operiert wird, kommt _Player_ vor:
```python
class Player():
     + currentPosition: list[int]
     + name: string
     + isHidden: bool
     ----------------
     + move (mVector: list[int]): None
     + set_position (point: list[int]): None
     + get_rotated_position (count: int): list[int]
     + hide (request: bool): None
     + change_name (newName: string): None
```
Hier werden zunächst das Feld _currentPosition_ und die Methode _move()_ betrachtet. _CurrentPosition_ repräsentiert aktuelle Position einer Figur im Labyrinth, während die _move()_ Methode einen Bewegungsvektor dazu addiert.
Die eigentliche Verschiebung der Figuren erfolgt innerhalb der *move_until_wall()* Methode der _GameLoop_ Klasse. Bei jeder Bewegung werden folgende Punkte eingehalten:

1. Jede Figur kann in **_4 Richtungen_** (_nach oben/unten/links/rechts_) laufen.
2. Bewegung wird **_unterbrochen_**, sobald die Figur vor einer Wand steht oder das Finish erreicht wird.
3. Bewegung wird **_nicht unterbrochen_**, wenn die Figur aus einem Labyrinth in ein anderes läuft (_mehr dazu im Maze-Aufbau_).

Der Bewegungsvektor wird von der Klasse *ChatGPT_Movement_Controller* anhand der vom ChatGPT gewonnenen Antwort ermittelt. Die Überprüfung eines Feldes auf eine Wand erfolgt durch die Methode *check_wall()* Klasse _GameHandler_ (_mehr zu der Klasse im folgenden Abschnitt “Anwendung von Strafen”_). Diese Klasse verfügt außerdem über Methoden *check_finish()* und *check_border()*, die ähnlich wie *check_wall()* funktionieren und zum Erfüllen von 2. und 3. der o.g. Kriterien verwendet werden.
Im folgenden Beispiel wird eine einfache Implementierung der Bewegungsfunktion bis zur nächsten Wand nach unten vorgestellt:
```python
    # Running till a wall
    mVector = [0, 1]
    while True:
        if gameHandler.check_finish(player.currentPosition):
            # Setting game variables such as maze and debuffs
            # to their end values
            gameHandler.end_game(player)
            break
        nextStep = [player.currentPosition[0] + mVector[0],
                    player.currentPosition[1] + mVector[1]]
         # Stop moving in front of a wall
        if gameHandler.check_wall(nextStep):
            break
            
        player.move(mVector)
```
Falls das Labyrinth gedreht wurde und das Spiel plötzlich abstürzt (_z.B. wegen einer fehlenden Verbindung zwischen Labyrinthen_), wäre es hilfreich, die Position der Figur in demselben nicht gedrehten Labyrinth zu kennen, damit man schnell die Fehlstelle beseitigen kann. Genau dafür gibt es die Methode *get_rotated_position()*, die die “normale” Position einer Figur zurückliefert, indem man die Rotation mit fehlenden Drehungen um 90° im Gegenuhrzeigersinn vervollständigt, bis das Labyrinth zur initiale Ausrichtung kommt (_mehr dazu im folgenden Abschnitt “Anwendung von Strafen”_).
Wird das vorherige Beispiel um Logging von Position nach jeder Bewegung erweitert, so bekommt man folgenden Code:
```python
    # Running till a wall with position logging
    mVector = [0, 1]
    rotationCounter = 2
    # Applying maze rotation 2 x 90° counterclockwise
    # before starting any movement
    gameHandler.maze_rotation(rotationCounter)
    while True:
        if gameHandler.check_finish(player.currentPosition):
            # Setting game variables such as maze and debuffs
            # to their end values
            gameHandler.end_game(player)
            break
        nextStep = [player.currentPosition[0] + mVector[0],
                    player.currentPosition[1] + mVector[1]]
        # Stop moving in front of a wall
        if gameHandler.check_wall(nextStep):
            break
    
        player.move(mVector)

    # Logging end position into console                    
    position = player.get_rotated_position(4 - rotationCounter)
    print(f"[Movement stopped]\nPlayer position: {position}")
```
Bis dahin kann man seine Figur nur bewegen und zuschauen. Um das Spiel ein wenig interessanter zu machen, wurden verschiedene Rollen von ChatGPT hinzugefügt, von denen jede auf eigene Weise angesprochen werden will. Sind die Figuren  mit der Ansprache zufrieden, so folgen sie gegebenen Anweisungen. _Sei das nicht der Fall,_ werden eine oder mehrere Strafen angewendet.

### Anwendung von Strafen

Zunächst ein Überblick über das gesamte Strafsystem. Für Bestrafung ist die Klasse _GameHandler_ zuständig:
```python
class GameHandler():

    – _DIFFICULTY: dict(str : list[int])
    – _DEBUFFS: dict(int : list[str, func])
    – _DEBUFF_INFOS: dict(str : str)
    – _PROMPT_LIBRARY: dict(str : dict(str : str))
    
    - _difficulty: list[int]
    - _mazeGenerator: MazeGenerator
    - _startMazePreset: str
    - _activeMazePreset: str
    
    + maze: list[list[int]]
    + prompt: list[str]
    
    + debuffDuration: int
    + renderDistance: int
    + rotationCounter: int
    
    + isGameOver: bool
    + set_level (player: Player, level): None
    - __set_random_maze (level: str): None
    - __set_random_prompt (level: str): None
    
    + check_wall (position: list[int): bool
    + check_finish (position: list[int): bool
    + check_border (position: list[int): bool
    + switch_section (player: Player): None
    
    + apply_debuffs (player: Player): list[str]
    + reduce_debuffs (player: Player): None
    + get_game_stats (): list[list[int]
    - __maze_rotation (player: Player, debuffApplied: bool): None
    - __blind (player: Player): None
    - __random_move (player: Player): None
    - __teleport (player: Player): None
    - __set_invisible (player: Player): None

    + restart_game (player: Player): None
    + reset_game (player: Player, isFinished: bool): None
    + switch_idle_maze (): None
```
**Die meisten Felder, Eigenschaften und Methoden sind bereits im Code genauer erklärt.** Hier sind Methoden *apply_debuffs()*, *reduce_debuffs()* und alle dahinterstehende private Methoden im Vordergrund, sowie Felder *_DIFFICULTY* (_Liste von Schwierigkeitsgraden und deren Einstellungen_), *_DEBUFFS* (_Liste von möglichen Strafen_), *_DEBUFF_INFOS* (_Beschreibungen von Strafen_) und difficulty (_vom Spieler ausgewählter Schwierigkeitsgrad_). Die Anwendung von Strafen erfolgt genauso wie Bewegungen von Figuren in der Klasse _GameLoop_, Methoden _run()_ und *rough_request_debuff()*.
Nachdem ein Bewegungsvektor ermittelt wurde, wird geprüft. ob dieser Vektor ein Schlüsselvektor ist. Die Schlüsselvektoren sind [0, 0] - Standardwert und [-1, -1] - Antwort auf nicht passende Ansprache, bspw. auf freche Weganweisung, bei der die *apply_debuffs()* Methode aufgerufen werden und so die Bestrafung passieren muss.
Es sind fünf Strafen vorgegeben:
```python
_DEBUFFS = {
        #  id, [   name,          debuffing method  ]
            1: ["ROTATION",     self.__maze_rotation],
            2: ["BLINDNESS",    self.__blind],
            3: ["INVISIBILITY", self.__set_invisible],
            4: ["RANDOM MOVE",  self.__random_move],
            5: ["TELEPORT",     self.__teleport]
        }
```
Jede von ihnen hat _einen Key-ID_, damit man jede Strafe leicht auswählen und ausschließen kann, _einen Namen_, damit man einen Log oder eine Nachricht im Chat über Anwendung bekommt, und das Wichtigste - _die Bestrafungsmethode_ als eine Art Delegates. Um alle Delegate aufrufen zu können, muss jede ihnen zugewiesene Funktion die gleiche Signatur besitzen. In diesem Projekt greifen alle o.g.  Funktionen auf innere Debuff Eigenschaften (_debuffDuration, renderDistance, rotationCounter_), aktuellen Labyrinth (_maze_) und eine _Instanz_ der _Player_ Klasse zu. Unter allen zuzugreifenden Variablen wird nur der Player nicht im _GameHandler_ gespeichert, also der einzige Parameter für die Bestrafungsfunktionen ist der von _GameLoop_ Klasse überzugebender _Player_. Im folgenden Beispiel eine einfache Implementierung der Anwendung und Logging von drei zufälligen Strafen ohne Wiederholungen auszuschließen:
```python
    def apply_debuffs(self, player: Player):     
        for i in range(3):
           choice = random.randint(5)
    
           _DEBUFFS[choice][1](player)
           
           print(f"{self._DEBUFFS[choice][0]} were applied")
```
Nachdem der Spieler bestraft wurde, müssen alle Debuff Variablen in _GameLoop_ Klasse durch *get_game_stats()* aktualisiert werden. Für temporäre Strafen wie _Blindness_ und _Invisibility_ spielt die Methode *reduce_debuffs()* eine wichtige Rolle. Die Methode dient aber nur als ein Dekrement von _debuffDuration_ und setzt diese temporäre Strafen zurück, wenn ihr Dauer zu Ende ist.
Es ist wichtig, **in jeder Iteration** vom Bestrafen die Debuff Variablen in der _GameLoop_ Klasse zu aktualisieren (_vor allem vor der Bewegung, falls das Labyrinth gedreht wurde_).

### GUI

Die Klasse _Screen_ implementiert die grafische Oberfläche von Chat-Maze mithilfe von einfachen Elementen der _Pygame_ Library. Genau genommen besteht das Anwendungsfenster nur aus Rechtecken und Text mit passenden Farben. Die Klasse funktioniert wie folgt: 
Ein Objekt von _Screen_ wird erstellt, dieses enthält aber noch keine Daten oder Funktionalität. Mit dem Aufruf “*setup_screen()*” werden alle benötigten Eigenschaften definiert bzw. errechnet, wie z.B. die Abmaße bestimmter UI Elemente relativ zur Auflösung des aktuellen Bildschirms. _Screen_ hat keinen eigenen _thread_, dass heißt die Methodenaufrufe zum Verarbeiten von Benutzereingabe, sowie Aktualisierung der dargestellten UI Elemente erfolgen über den Aufruf “*update_screen()*”, über den zusätzlich das aktuelle Maze, die Spielerkoordinaten, und die render-Distanz (_dazu später mehr_) übergeben werden. Die Methoden, die somit jeden Frame aufgerufen werden, sind zum einen “_draw_”- Funktionen, die bestimme dynamische Darstellungen wie das Dialogfenster rechts neu “_zeichnen_”, und zum anderen listener - Funktionen, die auf Eingaben des Benutzers oder auf Antworten von ChatGPT reagieren.

##### setup_screen()

Die bereits erwähnte Methode *setup_screen()* startet die _Pygame_ Application sowie _Pygames Audio System_: 
```python
    pygame.init()
    pygame.mixer.init()
 ```   
und definiert alle konstanten und dynamischen Eigenschaften, mit denen _Screen_ arbeitet. Manche UI Elemente passen sich der Auflösung des Displays an, dafür muss zuerst die Größe des aktiven Monitor ausgelesen werden:
```python
    # get size of all connected screens
    self.displaySizes = pygame.display.get_desktop_sizes()
            
    # choosing the right screen based on the screen number and the number of connected screens
    if len(self.displaySizes) >= screenNumber + 1:
        displaySizeX , displaySizeY = self.displaySizes[screenNumber]
    else:
        displaySizeX , displaySizeY = self.displaySizes[0]
        screenNumber = 0
```
Die Funktion *__resize_to_resolution(self, displaySizeX, displaySizeY, screenNumber)* passt die Applikation dann an die Auflösung des ausgewählten Monitors an und skaliert die einzelnen UI Elemente. 

Im Folgenden werden vier leere dynamische Strings erstellt, wobei *self.user_text* den Text, den der Spieler ins Textfeld eingibt repräsentiert. _self.message_ speichert immer den Text der als letztes abgeschickt wurde, also als Nachricht im Chat zu sehen ist. Der String *self.response_text* enthält den Text den ChatGPT als Antwort auf eine Benutzereingabe generiert und *self.last_response* speichert jeweils die vorherige Antwort. So kann mithilfe der Methode:
```python
    def __on_response_change(self):
        if self.response_text != self.last_response:
            self.last_response = self.response_text
            return True
        return False
```
erkannt werden, wann eine neue Antwort an den Spieler eingeht. Dies ist notwendig, da die Zeit der Verarbeitung meistens unterschiedlich lang dauert. Sobald eine Antwort eingeht, kann ein neuer Eintrag im Dialogfenster / Chat erstellt werden.

Das Dictionary *self.personality_to_color* ordnet registrierten Absendern (_Key_), wie z.B. dem Spieler oder den verschiedenen Persönlichkeiten von ChatGPT Farben (_Value_) zu, mit denen sie im Dialogfenster dargestellt werden. Die verwendeten Farben sind in einer separaten Klasse _Colors_(_Enum_) gespeichert. 

##### update_screen()

Die Funktion *self.__trigger_game_events()* enthält den Python Event Loop, so werden Inputs über die Pygame Applikation erkannt, wie z.B. Tasteneingabe oder Sprache. Sie ist so aufgebaut, dass ein for-Loop über jedes erkannte event aus _pygame.event.get()_ iteriert. Dort sind alle events enthalten, die zur Zeit des Aufrufs ausgelöst wurden. Danach wird spezifiziert, um welches event es sich genau handelt und welche Bedingungen erfüllt sein müssen, um eine Reaktion zu triggern. So wird z.B *self.__return_input()* aufgerufen, falls innerhalb des Spiels ein “Enter” erkannt wird und _self.active = True_, was so viel bedeutet, wie Eingabefeld ist ausgewählt:
```python
    for event in pygame.event.get():
    …
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.__return_input()
                    break
    …
```
Die Funktion *self.__delete_input_listener()* löscht den bereits eingegebenen Text in einem bestimmten Zeitintervall falls Backspace gehalten wird.

Als Nächstes werden die am Anfang erwähnten Draw-Funktionen aufgerufen. 
*self.__draw_maze(maze, player, render = n)* zeichnet das Maze mit dem Spieler und einer gegebenen Renderdistanz n, dass heißt es werden nur die Felder des Maze gezeichnet, die maximal n Felder entfernt sind vom Feld des Spielers. Das Maze besteht im Prinzip aus einem verschachtelten Array, nach diesem Schema:
```python
    maze = [[Wandkoordinaten], [Startkoordinaten], [Zielkoordinaten]]
```
Dabei haben die Wandkoordinaten die Form eines Zweidimensionalen Arrays, in dem jedes der 16x16 Felder als 0 oder 1 repräsentiert wird, also
```python
    maze[0][y][x]    
```
hat entweder den Wert 0 oder 1.
Es wird nun durch jedes Feld iteriert, dabei wird Zeile durch y und Spalte durch x dargestellt wie in einer Tabelle.
```python
    …
    for y in range(16):
        for x in range(16):
    …
```
Es wird jeweils geprüft, ob eine Wand, der Spieler, oder das Ziel gezeichnet werden soll. Ziel und Wand können wie beschrieben nur gezeichnet werden, wenn sie innerhalb der Renderdistanz liegen. Die Bedingungen dafür sehen wie folgt aus:
```python
    # Wand zeichnen:
    maze[0][y][x] == 1
    # Spieler zeichnen: 
    [x, y] == player.currentPosition and (not player.isHidden)
    # Ziel zeichnen:
    [x, y] == maze[2]
```
Als nächstes wird der Chat gezeichnet mit *self.__draw_chat_text()*. Dabei wird über das Array _self.chat[i]_ iteriert, was sozusagen die letzten *self.chat_max_len* Zeilen enthält. Sollten neue Einträge über *add_chat_text()* hinzukommen, werden die obersten Zeilen einfach von den jeweils nächsten überschrieben. Das Array ist also so lang wie *self.chat_max_len*. Jede Zeile des Chats, bzw. String im Array mit dem Index i wird untereinander gezeichnet mit einem bestimmten Abstand *self.chat_line_offset*. *self.chat_max_len* wird bei *setup_screen()* ebenfalls der Auflösung angepasst.
```python
    self.screen.blit(self.text_response, (self.chat_horizontal_offset, (self.maze_offset_y + i * self.chat_line_offset)))
```
Das Hinzufügen eines neuen Textes erfolgt unter anderem beim return einer Benutzereingabe oder nachdem eine Antwort von ChatGPT über *self.__chatgpt_response_listener()* erkannt wurde. Es wird dann *add_chat_text(self, raw_text, author = "")* aufgerufen. Es kann auch vorgefertigter Text beispielsweise vom System hinzugefügt werden, in dem Zeilenumbrüche “|” enthalten sind. Sollte das der Fall sein, wird der Text so in Paragraphen unterteilt, die jeweils in weitere Paragraphen unterteilt werden, sollten sie eine bestimmte Zeichenlänge überschreiten:
```python
    if author == "":
        paragraphs = str(raw_text).split("|") 
    else:
        paragraphs = str(author + ": " + raw_text).split("|")
    
    # paragraphs are created by line breaks "|" in the handed over text
    for paragraph in paragraphs:
    
        # each paragraph is split in 45 chars long parts
        lines = textwrap.wrap(paragraph, 45)
…
```
Es wird abhängig vom Autor immer die jeweilige Farbe zwischengespeichert, die für die neu hinzugefügten Zeilen bei der Überschreibung verwendet wird:
```python
    color = self.personality_to_color.get(author, Colors.GREY.value)
```
_lines_ enthält also nun alle Zeilen die zum Chat hinzugefügt werden sollen. Jetzt muss für jede neue Zeile jeweils jede alte Zeile einen Index nach unten rutschen, sodass oben immer eine Zeile gelöscht wird und unten immer eine neue hinzukommt:
```python
    first_line = True
    …
    for line in lines:
        for i in range(0, self.chat_max_len - 1):
            self.chat[i] = self.chat[i + 1]
            self.chat_color[i] = self.chat_color[i + 1]
        if first_line:
            self.chat[self.chat_max_len - 1] = line
            self.chat_color[self.chat_max_len - 1] = color
        else:
            self.chat[self.chat_max_len - 1] = line
            self.chat_color[self.chat_max_len - 1] = color
        first_line = False
```
Als nächstes in der *screen_update()* wird die Methode *self.__draw_input_text()* aufgerufen, welche den Text darstellt die gerade vom Benutzer eingegeben wird. Dabei wird der rohe Text *self.user_text* wieder in Zeilen unterteilt falls er eine gewisse Länge überschreitet:
```python
    lines = textwrap.wrap(self.user_text, 45)
        if lines == []:
            lines = [""]
        max_line = len(lines) - 1
```
Die Zeilen werden ebenfalls untereinander angeordnet. Zusätzlich wird ein Cursor gezeichnet
*self.__draw_input_cursor(current_line, max_line)* der *current_line* (_gerendert_) als Referenz für die horizontale und *max_line* als Referenz für die vertikale Position nutzt. Am Schluss wird noch der Rahmen *self.input_rect* an die gerenderte Höhe und Breite des Eingabetextes angepasst:
```python
    self.input_rect.width = max(200, first_line.get_width() + 15)
    self.input_rect.height = self.input_rect_normal_height * (max_line + 1) + 5
```
## Spieleinstellungen

### Schwierigkeitsgrade

Alle Schwierigkeitsgrade werden in der Klasse _GameHandler_ gespeichert und verwendet. Mit der Methode *set_level()* kann man einen vom Benutzer ausgewählten Grad aus anderen Klassen in diese übergeben. Alle Schwierigkeitsgrade werden im Konstruktor von _GameHandler_ wie folgt definiert:
```python
    _DIFFICULTY = {
    # name : [maze_preset_number, debuffs amount, debuffs’ duration]
        "TEST"  :   [0, 1, 1],
        "EASY"  :   [1, 0, 0],
        "NORMAL":   [2, 1, 5],
        "HARD"  :   [3, 3, 10]
    }
```
Jeder Grad hat also _einen Namen_ und folgende Eigenschaften:

1. *maze_preset_number* - Die Gruppe, aus der ein Labyrinth ausgewählt werden muss.
2. _debuffs amount_ - Die Anzahl von Strafen, die beim Bestrafen angewendet werden.
3. _debuffs’ duration_ - Die Dauer von angewendeten Strafen (_Anzahl der Bewegungen bis die Strafen ablaufen_).

Die Namen werden lediglich zur Lesbar- und Verständlichkeit implementiert, insbesondere für einfachere und anschauliche Unterteilung von Prompts.

### Prompts 

Alle Prompts werden (_manuell_) serialisiert und unter **_/assets/prompts.json_** Datei folgendermaßen gespeichert:
```python
    {
      "DIFFICULTY 1": {
          "Name1" : "Prompt line 1"
          ,
          "Name2" : "Prompt line 2"
      },
      "DIFFICULTY 2": {
          "Name1" : "Prompt line 1"
          ,
          "Name2" : "Prompt line 2"
      }
    }
```
Hierbei ist zu erwähnen, dass den Namen von Prompts in der _Screen_ Klasse (_Feld personality_to_color_) eine Farbe zugewiesen werden kann, mit der sie im Chat angezeigt werden. Nachdem ein Schwierigkeitsgrad ausgewählt wurde, wird vom _GameHandler_ durch *__set_random_prompt()* ein zufälliger Prompt aus ausgewählter Gruppe genommen und als Liste [*name, prompt_line*] gespeichert, weil sie in dieser Form einfacher zuzugreifen sind. Auf ähnliche Art werden alle Labyrinthe gespeichert.

### Maze-Aufbau

#### Kleine Labyrinthe

Genauso wie alle Prompts, werden alle Labyrinthe serialisiert und unter **_/assets/maze_presets.json_** Datei gespeichert. Es sind folgende Punkte beim Erstellen von einfachen (_kleinen_) Labyrinthen einzuhalten:

1. Größe - 16x16 Felder.
2. Rahmen - vorhanden. Ausnahmsweise kann der Endpunkt am Rand sein.
3. Start- und Endpunkte - jeweils genau ein.
4. Anfang - immer innerhalb der Sektion “0”.
5. Finish ist mit implementierter Bewegungsmethode (Lauf bis zur nächsten Wand) erreichbar.
6. Jeder Name folgt dem Muster: `maze_<difficulty>.<preset>`

Ein einfaches Labyrinth muss somit folgendermaßen aussehen:
```python
    "maze_1.1": {
        "0": [
          [
            # Maze map
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
            [ 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
            [ 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
          ],
            # Start point
            [ 1, 1 ],
            # Finish point
            [ 15, 14 ]
          ]
        },
```
wobei Felder mit dem Wert “1” als ein Wandblock und mit dem Wert “0” als ein freies Feld betrachtet werden sollen. Labyrinthe dieser Größe eignen sich sehr gut für “EASY” und “NORMAL” Schwierigkeitsgrade. Damit das Spiel ein bisschen interessanter (_und gleichzeitig schwerer_) wird, wurden komplexe Labyrinthe und deren Verbindungen implementiert.

#### Größere Labyrinthe

Um den Horizont zu erweitern, werden einfachere Labyrinthe zusammengebunden. Größere Labyrinthe müssen somit _zusätzliche_ generelle Eigenschaften besitzen:

- Größe: n x (16x16) Felder.
- Zwischen jeder Sektion besteht mindestens eine Verbindung.
- Beide Start- und Endpunkte müssen in jeder Sektion definiert (_jedoch nicht unbedingt erreichbar_) sein.
- Es gibt mindestens einen erreichbaren Endpunkt.

Alle Verbindungen (_bridges_) werden unter Schlüsselwort “connections” in jedem Preset gespeichert. Jede dieser Verbindungen ist wie folgt aufgebaut:
```python
    "connections": {
        "<start_section_1>": [
            [
              <target_section_1>,
              <start_point_in_start_section>,
              <target_point_in_target_section>
            ],
            [
              <target_section_2>,
              <start_point_in_start_section>,
              <target_point_in_target_section>
            ]
        ]
```
Mit dieser Struktur sind tatsächlich Übergänge aus jedem Punkt zu jeweils einem anderen implementierbar. Der Übergang zwischen einzelnen Sektionen erfolgt in *move_until_wall()* der Klasse _GameLoop_ beim Aufruf von *switch_section()* vom _GameHandler_:
```python
    def switch_section(self, player: Player):
        """
        Switches active maze according to preset's connection
        setting (graph) to the next one. Works only if the player
        is on a key point of a connection.
        """
        graph = mazeGenerator.get_preset_connections(activeMazePreset)
        
        startSection = _activeMazePreset[-1]
        
        # bridge = [target_section, start_point (active section), end_point]
        # Searching through all connections from the startSection
        for bridge in graph[startSection]:
            # and looking for the one with matching startPoint
            if bridge[1] != playerPosition:
                continue
    
            activeMazePreset = f"{self._activeMazePreset[:-1]}{bridge[0]}"
            maze = _mazeGenerator.get_preset(_activeMazePreset)
            player.set_position(bridge[2])
            
            for i in range(rotationCounter):
                # Rotating target_section by same angle as start_section
                __maze_rotation(player= player, debuffApplied= False)
```
*switch_section()* sucht also unter einer Liste von Bridges, die aus aktueller Sektion (_Key im graph Dictionary_) anfangen, einen Startpunkt (_Index 1_), der mit aktueller Position von Figur übereinstimmt und wechselt aktuelles Labyrinth zu in Bridge gegebener Sektion (_Index 0_).

#### Animationen

Auf eine ähnliche einfachere Weise werden die Animationen gebaut. Jede Animation besteht aus einzelnen Frames, die nichts anderes als weitere Labyrinthe für eine bestimmte Zeit angezeigt werden. Jeder dieser Frames hat einen Link auf den nächsten, wobei der letzte Frame auf den ersten (_0-en_) Frame verweist. Da hier kein Spieler bewegt wird, kann man die Verweise (_sowie Anzeigedauer_) direkt in Sektionen speichern, was das Erstellen und Verwalten von Animationen sehr erleichtert. Somit müssen diese spezielle Labyrinthe wie im Folgenden Code aussehen:
```python
    "IDLE_0": {
      "0": [
          # Frame
          [
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0 ],
            [ 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0 ],
            [ 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0 ],
            [ 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0 ],
            [ 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
          ],
          # Start point (irrelevant but necessary)
          [ -1, -1 ],
          # End point (irrelevant but necessary)
          [ -1, -1 ],
          # Duration
          10,
          # Next frame
          1
      ],
    }
```
Jede Animation beginnt mit einem Startframe mit dem Namen “`FINISH_<preset_number>`”, der einmalig nach Bestehen vom Labyrinth gezeigt wird. So muss man zum o.g. Beispiel einen Startframe mit dem Namen “FINISH_0” hinzufügen, damit _GameHandler_ seine Methode *switch_idle_maze()* ausführen kann:
```python
    def switch_idle_maze(self):
        """
        Switches the current idle maze to the next one connected to it.
        !Used with FINISH and IDLE presets only!
        """
        # e.g. _activeMazePreset = "FINISH_0.0"
        preset = _activeMazePreset[-3]
        nextFrame = maze[4]
        
        _activeMazePreset = f"IDLE_{preset}.{nextFrame}"
        maze = _mazeGenerator.get_preset(_activeMazePreset)
```
Alle Frames werden durch die Methode *run_idle()* im _GameLoop_ gewechselt, indem ein Timer-Thread mit der Methode *switch_idle_frame()* gestartet wird. Dieser Thread führt seine Funktion erst nach einer vorgegebenen Zeit aus, die bereits im aktuellen Labyrinth (_unter Index 3_) vorhanden ist.

## Links 

[OpenAI Dokumentation](https://platform.openai.com/docs/overview)  
[pyGame Dokumentation](https://www.pygame.org/docs/)  
[KI_Werkstatt Website](https://kiwerkstatt.f2.htw-berlin.de/)