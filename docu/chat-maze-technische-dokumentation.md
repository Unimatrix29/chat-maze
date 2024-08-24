# Chat Maze: Technische Dokumentation

- Einführung
- Spezifikation
- Spielablauf
- Aufbau des Projekts
    - Verbindung mit Chat GPT
    - Verarbeitung von Antworten
    - GUI
- Spieleinstellungen
    - Steuerung
    - Schwierigkeitsgrade
    - Prompts
    - Maze-Aufbau
- Links

## Einführung 

Dieses Dokument dient dafür, Funktionsweise und Merkmale vom Projekt Chat Maze neugierigen Entwicklern zu erklären. Es wird vorausgesetzt, dass man bereits Grundlagen der objektorientierten Programmierung kennengelernt hat, sowie Syntax und Verwendung von externen Bibliotheken in Pythonanwendungen. Zunächst wird der grundlegender Programmablauf dargestellt, mithilfe dessen es ein bisschen weniger Aufwand beim Nachvollziehen von Aufbau und Zusammenhängen zwischen Klassen in weiteren Kapiteln geben sollte. Danach werden einzelne Features bzw. Klassen, ihre Methoden und Implementierung beschrieben, was potentiellen Weiterentwicklern und tieferem Verständnis des Projekts helfen sollte.
In Erklärungen können folgende Begriffe auftauchen, die zum ersten Mal verwirrend sein mögen:

- Ein Spieler - ein Mensch, der die Weganweisungen gibt und so eine Figur steuert.
- Eine Figur - ein Quadrat auf dem Bildschirm, das eine ChatGPT-Rolle repräsentiert.
- Eine Rolle - ein Verhandlungsmuster, das dem ChatGPT vor jedem Spiel übergeben wird.

Es werden ab und zu Code-Beispiele gegeben, die auf echtem Code von diesem Projekt basieren. Diese stellen eine einfachere und manchmal die erste Implementation von zu besprechenden Features dar, damit man eine Vorstellung bekommt, was im wirklichen Code vorkommt.
In diesem Projekt wurden mehrere externe Bibliotheken wie OpenAI und pygame verwendet, die hier nicht ausführlich erklärt werden, weil sie bereits eigene Dokumentationen besitzen (siehe Abschnitt “Links”).

## Spezifikation (TODO)

Für das Projekt sind folgende Anwendungen erforderlich:
- Python 3
- Anaconda Environment (installation guide in User-Doku)
- Chat GPT API-Key (als config.json in /src zu speichern)

## Spielablauf

Da für jedes Feature oft mehrere Klassen zuständig sind, wäre es zunächst total sinnvoll, sich den gesamten Spielablauf anzuschauen. Man kann alle Aktivitäten in folgenden Kategorien unterteilen:

- Erfassung von Benutzereingaben (Text oder Sprache)
- Verbindung mit ChatGPT
- Erarbeitung von Antworten
- Spielverwaltung (Anwendung von Strafen, Bewegung von Figuren und Labyrinthwechsel)
- Graphische Darstellung von Labyrinthen und Chatabläufen

Folgendes Diagramm stellt den in diesem Projekt implementierten Kernprozess dar:

# TODO

Wie es schon wahrscheinlich aufgefallen ist, ist das ganze Spiel eine dauerhafte Schleife. Diese Schleife kann sowohl beim Erreichen vom Ende des gespielten Labyrinths, als auch manuell durch ein Restart-Kommando (/restart oder /newgame) unterbrochen werden.Damit man sehen kann, was überhaupt im Spiel passiert, gibt es eine Methode update_screen() der Klasse Screen, die für eigentliches Zeichnen des GUIs zuständig ist. Diese wird dauerhaft nebenläufig dem o.b. Kernprozess ausgeführt. Wenn das Spiel zu Ende ist, wird ein der vorhandenen Endscreens (auch animierte) gezeigt, wo man einen Schwierigkeitsgrad auswählen und somit ein neues Spiel starten kann.
Die Hauptklasse, die alle Bausteine des Projekts zusammenführt, ist GameLoop. Der o.g. Kernprozess läuft innerhalb der run() Methode dieser Klasse ab. Sobald das Spielfenster geschlossen wird, wird die Schleife in run() nach laufender Iteration unterbrochen und alle verwendete Threads mit close() geschlossen.

## Aufbau des Projekts 

### Verbindung mit ChatGPT

#### API-Anfragen

Um eine Verbindung mit [OpenAIs API](https://platform.openai.com/docs/overview) herzustellen und somit mit ChatGPT, wird ein HTTPS-Client benötigt. Dieser lässt sich sehr einfach über die Python-Bibliothek „openai“ von OpenAI erstellen. Für genauere Details siehe die [API-Referenz](https://platform.openai.com/docs/api-reference/introduction) von OpenAI.

Die Aufgabe der Client-Erstellung übernimmt die Klasse „ApiClientCreator“ mit der Methode „getclient“. Dem Client muss ein gültiger [API-Key](https://platform.openai.com/docs/quickstart) übergeben werden. Dieser wird aus einer JSON-Datei geladen. Der Standardname der Datei ist „config.json“. Möchte man die Datei anders benennen, muss der neue Dateiname beim Aufruf von „getclient“ als Argument übergeben werden. Des Weiteren kann optional auch noch eine Timeout-Zeit für die HTTPS-Anfrage mitübergeben werden. Der Standard hier ist 60 Sekunden.
Nun, da uns ein [API-Client](https://platform.openai.com/docs/api-reference/authentication) zur Verfügung steht, können wir uns der Kommunikation mit der API widmen. Die API stellt mehrere Möglichkeiten und Funktionen zur Verfügung, um mit den einzelnen Sprachmodellen zu interagieren. In unserem Spiel verwenden wir die [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-, sowie die [Text-zu-Audio](https://platform.openai.com/docs/guides/text-to-speech)- und die [Audio-zu-Text](https://platform.openai.com/docs/guides/speech-to-text)-Funktionen der einzelnen Modelle von OpenAI. Verwaltet und durchgeführt werden die einzelnen Anfragen von der „ChatGPT“-Klasse in „ChatGPT_Controller.py“. Dieser Klasse muss beim Aufrufen der zuvor erstellte Client übergeben werden. In einer Liste wird der Kommunikationsverlauf mit dem Text-zu-Text-Modell gespeichert. Standardmäßig werden nur fünf Nachrichten gespeichert. Dabei ist eine Nachricht die Anfrage des Users plus die Antwort des Modells. Die Nachrichten werden im [Response-Format der API](https://platform.openai.com/docs/guides/chat-completions/response-format) gespeichert, wobei nur die „content“- und „role“-Informationen gespeichert werden. Wenn mehr als fünf Nachrichten gespeichert werden sollen, kann beim Aufruf als zweites Argument die maximale Nachrichtenanzahl mitübergeben werden.

Schauen wir uns zuerst den [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-Aufruf an. Dieser erfolgt in „texttotext()“. Die Methode hat vier Argumente, von denen zwei optional sind. Das „_retry“-Argument ist für das Error-Handling beim API-Call vonnöten. Der Methode kann als Argument der Name des zu verwendenden [ChatGPT-Modells](https://platform.openai.com/docs/models) übergeben werden, das Standardmodell ist „[gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)“. Der Rückgabewert ist das [Response-Objekt der API](https://platform.openai.com/docs/guides/chat-completions/response-format). Das einzige nicht optionale Argument ist die zu sendende Nachricht. Diese Nachricht muss in einem bestimmten Format sein. Um einen gegebenen String in ein für die API nutzbares [Format](https://platform.openai.com/docs/api-reference/chat/create) zu bringen, gibt es die „construct_message()“-Methode. In dieser Methode wird die aktuelle Eingabe des Nutzers, der System-Prompt und der Kommunikationsverlauf in einem Dictionary zusammengeführt, wobei die Keys den entsprechenden Rollen in Bezug auf die API entsprechen. Die möglichen Rollen sind: „system“, „user“ und „assistant“.

**(Wichtig! Diese Rollen haben nichts mit den Charakteren/Rollen unseres Spieles zu tun, sondern sind von der API vorgeschrieben.)**

Der [Text-zu-Audio](https://platform.openai.com/docs/guides/text-to-speech) ist im Grunde nicht sehr unterschiedlich zum [Text-zu-Text](https://platform.openai.com/docs/guides/chat-completions)-Aufruf. Dieser wird durch die „texttoaudio()“-Methode durchgeführt. Auch hier kann wieder der Name eines [Modells](https://platform.openai.com/docs/models) angegeben werden. OpenAI hat hierfür zwei Modelle zur Verfügung: „[tts-1](https://platform.openai.com/docs/models/tts)“ und „[tts-1-hd](https://platform.openai.com/docs/models/tts)“. Zudem kann die Stimme, mit der der Text synthetisiert werden soll, angegeben werden. OpenAI hat hier sechs [Stimmen](https://platform.openai.com/docs/guides/text-to-speech/overview) zur Auswahl. Im Gegensatz zum Text-zu-Text-Aufruf muss für den Text-zu-Audio-Aufruf der zu synthetisierender Text nicht in einem bestimmten Format sein. Entsprechend kann ein einfacher String übergeben werden. Auch hier ist das „retry“-Argument für das Error-Handling beim API-Call vonnöten. Der API-Call gibt ein Audio-Objekt zurück, welches mit der „writeaudiotofile()“-Methode in eine .wav-Datei namens „tts_out.wav“ geschrieben wird. Die Datei wird im /src-Ordner abgelegt. Wenn die Datei nicht existiert, wird sie beim Initialisieren der Klasse erstellt.  

Der [Audio-zu-Text](https://platform.openai.com/docs/guides/speech-to-text)-Aufruf in der „audiototext()“-Methode verwendet den „[transcription“-Endpoint](https://platform.openai.com/docs/api-reference/audio/createTranscription) der API. Auch hier kann wieder ein Modell angegeben werden, auch wenn nur eines zur Verfügung steht, „[whisper-1](https://platform.openai.com/docs/models/whisper)“. Des Weiteren kann ein optionaler Prompt mitübergeben werden, um dem [Modell](https://platform.openai.com/docs/models) einen Kontext der Transkription zu geben und diese potenziell zu verbessern. Auch diese Methode hat das Error-Handling-Argument „retry“. Die Audiodaten werden aus der im /src-Ordner liegenden „userinput.wav“-Datei gelesen. Diese Datei wird, wenn nicht vorhanden, auch beim Initialisieren der Klasse erstellt. Die Methode gibt den transkribierten Text als String zurück.

#### API-Antworten (TODO)

#### Prompting (TODO)

### Verarbeitung von Antworten

Dieses Feature wird durch Kombination verschiedener Klassen und deren Methoden realisiert. Als zentrale Klasse, mit der hier operiert wird, kommt Player vor:

##### Player

     + currentPosition: list[int]
     + name: string
     + isHidden: bool
     + move (mVector: list[int]): None
     + set_position (point: list[int]): None
     + get_rotated_position (count: int): list[int]
     + hide (request: bool): None
     + change_name (newName: string): None


Hier werden zunächst das Feld currentPosition und die Methode move() betrachtet. CurrentPosition repräsentiert aktuelle Position einer Figur im Labyrinth, während die move() Methode einen Bewegungsvektor dazu addiert.
Die eigentliche Verschiebung der Figuren erfolgt innerhalb der move_untill_wall() Methode der GameLoop Klasse. Bei jeder Bewegung werden folgende Punkte eingehalten:

1. Jede Figur kann in 4 Richtungen (nach oben/unten/links/rechts) laufen.
2. Bewegung wird unterbrochen, sobald die Figur vor einer Wand steht oder das Finish erreicht wird.
3. Bewegung wird nicht unterbrochen, wenn die Figur aus einem Labyrinth in ein anderes läuft (mehr dazu im Maze-Aufbau).

Der Bewegungsvektor wird von der Klasse ChatGPT_Movement_Controller anhand der vom ChatGPT gewonnenen Antwort ermittelt. Die Überprüfung eines Feldes auf eine Wand erfolgt durch die Methode check_wall() Klasse GameHandler (mehr zu der Klasse im folgenden Abschnitt “Anwendung von Strafen”). Diese Klasse verfügt außerdem über Methoden check_finish() und check_border(), die ähnlich wie check_wall() funktionieren und zum Erfüllen von 2. und 3. der o.g. Kriterien verwendet werden.
Im folgenden Beispiel wird eine einfache Implementierung der Bewegungsfunktion bis zur nächsten Wand nach unten vorgestellt:

# TODO

Falls das Labyrinth gedreht wurde und das Spiel plötzlich abstürzt (z.B. wegen einer fehlenden Verbindung zwischen Labyrinthen), wäre es hilfreich, die Position der Figur in demselben nicht gedrehten Labyrinth zu kennen, damit man schnell die Fehlstelle beseitigen kann. Genau dafür gibt es die Methode get_rotated_position(), die die “normale” Position einer Figur zurückliefert, indem man die Rotation mit fehlenden Drehungen um 90° im Gegenuhrzeigersinn vervollständigt, bis das Labyrinth zur initiale Ausrichtung kommt (mehr dazu im folgenden Abschnitt “Anwendung von Strafen”).
Wird das vorherige Beispiel um Logging von Position nach jeder Bewegung erweitert, so bekommt man folgenden Code:

# TODO

Bis dahin kann man seine Figur nur bewegen und zuschauen. Um das Spiel ein wenig interessanter zu machen, wurden verschiedene Rollen von ChatGPT hinzugefügt, von denen jede auf eigene Weise angesprochen werden will. Sind die Figuren  mit der Ansprache zufrieden, so folgen sie gegebenen Anweisungen. Sei das nicht der Fall, werden eine oder mehrere Strafen angewendet.

### Anwendung von Strafen

Zunächst ein Überblick über das gesamte Strafsystem. Für Bestrafung ist die Klasse GameHandler zuständig:

##### GameHandler

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

Die meisten Felder, Eigenschaften und Methoden sind bereits im Code genauer erklärt. Hier sind Methoden apply_debuffs(), reduce_debuffs() und alle dahinterstehende private Methoden im Vordergrund, sowie Felder _DIFFICULTY (Liste von Schwierigkeitsgraden und deren Einstellungen), _DEBUFFS (Liste von möglichen Strafen), _DEBUFF_INFOS (Beschreibungen von Strafen) und difficulty (vom Spieler ausgewählter Schwierigkeitsgrad). Die Anwendung von Strafen erfolgt genauso wie Bewegungen von Figuren in der Klasse GameLoop, Methoden run() und rough_request_debuff().
Nachdem ein Bewegungsvektor ermittelt wurde, wird geprüft. ob dieser Vektor ein Schlüsselvektor ist. Die Schlüsselvektoren sind [0, 0] - Standardwert und [-1, -1] - Antwort auf nicht passende Ansprache, bspw. auf freche Weganweisung, bei der die apply_debuffs() Methode aufgerufen werden und so die Bestrafung passieren muss.
Es sind fünf Strafen vorgegeben:

# TODO

Jede von ihnen hat einen Key-ID, damit man jede Strafe leicht auswählen und ausschließen kann, einen Namen, damit man einen Log oder eine Nachricht im Chat über Anwendung bekommt, und das Wichtigste - die Bestrafungsmethode als eine Art Delegates. Um alle Delegate aufrufen zu können, muss jede ihnen zugewiesene Funktion die gleiche Signatur besitzen. In diesem Projekt greifen alle o.g.  Funktionen auf innere Debuff Eigenschaften (debuffDuration, renderDistance, rotationCounter), aktuellen Labyrinth (maze) und eine Instanz der Player Klasse zu. Unter allen zuzugreifenden Variablen wird nur der Player nicht im GameHandler gespeichert, also der einzige Parameter für die Bestrafungsfunktionen ist der von GameLoop Klasse überzugebender Player. Im folgenden Beispiel eine einfache Implementierung der Anwendung und Logging von drei zufälligen Strafen ohne Wiederholungen auszuschließen:

# TODO

Nachdem der Spieler bestraft wurde, müssen alle Debuff Variablen in GameLoop Klasse durch get_game_stats() aktualisiert werden. Für temporäre Strafen wie Blindness und Invisibility spielt die Methode reduce_debuffs() eine wichtige Rolle. Die Methode dient aber nur als ein Dekrement von debuffDuration und setzt diese temporäre Strafen zurück, wenn ihr Dauer zu Ende ist.
Es ist wichtig, in jeder Iteration vom Bestrafen die Debuff Variablen in der GameLoop Klasse zu aktualisieren (vor allem vor der Bewegung, falls das Labyrinth gedreht wurde).

### GUI

Die Klasse Screen implementiert die grafische Oberfläche von Chat-Maze mithilfe von einfachen Elementen der Pygame Library. Genau genommen besteht das Anwendungsfenster nur aus Rechtecken und Text mit passenden Farben. Die Klasse funktioniert wie folgt: 
Ein Objekt von Screen wird erstellt, dieses enthält aber noch keine Daten oder Funktionalität. Mit dem Aufruf “setup_screen” werden alle benötigten Eigenschaften definiert bzw. errechnet, wie z.B. die Abmaße berstimmter UI Elemente relativ zur Auflösung des aktuellen Bildschirms. Screen hat keinen eigenen thread, dass heißt die Methodenaufrufe zum Verarbeiten von Benutzereingabe, sowie Aktualisierung der dargestellten UI Elemente erfolgen über den Aufruf “update_screen”, über den zusätzlich das aktuelle Maze, die Spielerkoordinaten, und die render-Distanz (dazu später mehr) übergeben werden. Die Methoden, die somit jeden Frame aufgerufen werden, sind zum einen “draw”- Funktionen, die bestimme dynamische Darstellungen wie das Dialogfenster rechts neu “zeichnen”, und zum anderen listener - Funktionen, die auf Eingaben des Benutzers oder auf Antworten von ChatGPT reagieren.

##### setup_screen()

Die bereits erwähnte Methode setup_screen startet die Pygame Application sowie Pygames Audio System 

    pygame.init()
    pygame.mixer.init()
    
und definiert alle konstanten und dynamischen Eigenschaften, mit denen Screen arbeitet. Manche UI Elemente passen sich der Auflösung des Displays an, dafür musszuerst die Größe des aktiven Monitor ausgelesen werden.

    # get size of all connected screens
    self.displaySizes = pygame.display.get_desktop_sizes()
            
    # choosing the right screen based on the screen number and the number of connected screens
    if len(self.displaySizes) >= screenNumber + 1:
        displaySizeX , displaySizeY = self.displaySizes[screenNumber]
    else:
        displaySizeX , displaySizeY = self.displaySizes[0]
        screenNumber = 0

Die Funktion __resize_to_resolution(self, displaySizeX, displaySizeY, screenNumber) passt die Applikation dann an die Auflösung des ausgewählten Monitors an und skaliert die einzelnen UI Elemente. 

Im Folgenden werden vier leere dynamische Strings erstellt, wobei self.user_text den Text, den der Spieler ins Textfeld eingibt repräsentiert. self.message speichert immer den Text der als letztes abgeschickt wurde, also als Nachricht im Chat zu sehen ist. Der String self.response_text enthält den Text den ChatGPT als Antwort auf eine Benutzereingabe generiert und self.last_response speichert jeweils die vorherige Antwort. So kann mithilfe der Methode 

    def __on_response_change(self):
        if self.response_text != self.last_response:
            self.last_response = self.response_text
            return True
        return False

erkannt werden, wann eine neue Antwort an den Spieler eingeht. Dies ist notwendig, da die Zeit der Verarbeitung meistens unterschiedlich lang dauert. Sobald eine Antwort eingeht, kann ein neuer Eintrag im Dialogfenster / Chat erstellt werden.

Das Dictionary self.personality_to_color ordnet registrierten Absendern (Key), wie z.B. dem Spieler oder den verschiedenen Persönlichkeiten von ChatGPT Farben (Value) zu, mit denen sie im Dialogfenster dargestellt werden. Die verwendeten Farben sind in einer separaten Klasse class Colors(Enum) gespeichert. 

##### update_screen()

Die Funktion self.__trigger_game_events() enthält den Python Event Loop, so werden Inputs über die Pygame Applikation erkannt, wie z.B. Tasteneingabe oder Sprache. Sie ist so aufgebaut, dass ein for-Loop über jedes erkannte event aus pygame.event.get()
iteriert. Dort sind alle events enthalten, die zur Zeit des Aufrufs ausgelöst wurden. Danach wird spezifiziert, um welches event es sich genau handelt und welche Bedingungen erfüllt sein müssen, um eine Reaktion zu triggern. So wird z.B self.__return_input() aufgerufen, falls innerhalb des Spiels ein “Enter” erkannt wird und self.active = True, was so viel bedeutet, wie Eingabefeld ist ausgewählt.

    for event in pygame.event.get():
    …
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.__return_input()
                    break
    …

Die Funktion self.__delete_input_listener() löscht den bereits eingegebenen Text in einem bestimmten Zeitintervall falls Backspace gehalten wird.

Als Nächstes werden die am Anfang erwähnten Draw-Funktionen aufgerufen. 
self.__draw_maze(maze, player, render = n) zeichnet das Maze mit dem Spieler und einer gegebenen Renderdistanz n, dass heißt es werden nur die Felder des Maze gezeichnet, die maximal n Felder entfernt sind vom Feld des Spielers. Das Maze besteht im Prinzip aus einem verschachtelten Array, nach diesem Schema:  

    maze = [[Wandkoordinaten], [Spielerkoordinaten], [Zielkoordinaten]]

Dabei haben die Wandkoordinaten die Form eines Zweidimensionalen Arrays, in dem jedes der 16x16 Felder als 0 oder 1 repräsentiert wird, also

    maze[0][y][x]
    
hat entweder den Wert 0 oder 1.
Es wird nun durch jedes Feld iteriert, dabei wird Zeile durch y und Spalte durch x dargestellt wie in einer Tabelle.

    …
    for y in range(16):
        for x in range(16):
    …

Es wird jeweils geprüft, ob eine Wand, der Spieler, oder das Ziel gezeichnet werden soll. Ziel und Wand können wie beschrieben nur gezeichnet werden, wenn sie innerhalb der Renderdistanz liegen. Die Bedingungen dafür sehen wie folgt aus:

###### Wand zeichen:

    maze[0][y][x] == 1

###### Spieler zeichnen: 

    [x, y] == player.currentPosition and (not player.isHidden)

###### Ziel zeichnen:

    [x, y] == maze[2]

Als nächstes wird der Chat gezeichnet mit self.__draw_chat_text(). Dabei wird über das Array self.chat[i] iteriert, was sozusagen die letzten self.chat_max_len Zeilen enthält. Sollten neue Einträge über add_chat_text() hinzukommen, werden die obersten Zeilen einfach von den jeweils nächsten überschrieben. Das Array ist also so lang wie self.chat_max_len. Jede Zeile des Chats, bzw. String im Array mit dem Index i wird untereinander gezeichnet mit einem bestimmten Abstand self.chat_line_offset. self.chat_max_len wird bei setup_screen() ebenfalls der Auflösung angepasst.

    self.screen.blit(self.text_response, (self.chat_horizontal_offset, (self.maze_offset_y + i * self.chat_line_offset)))

Das Hinzufügen eines neuen Textes erfolgt unter anderem beim return einer Benutzereingabe oder nachdem eine Antwort von ChatGPT über self.__chatgpt_response_listener() erkannt wurde. Es wird dann add_chat_text(self, raw_text, author = "") aufgerufen. Es kann auch vorgefertigter Text beispielsweise vom System hinzugefügt werden, in dem Zeilenumbrüche “|” enthalten sind. Sollte das der Fall sein wird der Text so in Paragraphen unterteilt, die jeweils in weitere Paragraphen unterteilt werden, sollten sie eine bestimmte Zeichenlänge überschreiten. 

    if author == "":
        paragraphs = str(raw_text).split("|") 
    else:
        paragraphs = str(author + ": " + raw_text).split("|")
    
    # paragraphs are created by line breaks "|" in the handed over text
    for paragraph in paragraphs:
    
        # each paragraph is splitted in 45 chars long parts
        lines = textwrap.wrap(paragraph, 45)
…
Es wird abhängig vom Autor immer die jeweilige Farbe zwischengespeichert, die für die neu hinzugefügten Zeilen bei der Überschreibung verwendet wird. 

    color = self.personality_to_color.get(author, Colors.GREY.value)

lines enthält also nun alle Zeilen die zum Chat hinzugefügt werden sollen. Jetzt muss für jede neue Zeile jeweils jede alte Zeile einen Index nach unten rutschen, sodass oben immer eine Zeile gelöscht wird und unten immer eine neue hinzukommt.

    irst_line = True
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

Als nächstes in der screen_update() wird die Methode  self.__draw_input_text() aufgerufen, welche den Text darstellt die gerade vom Benutzer eingegeben wird. Dabei wird der rohe Text self.user_text wieder in Zeilen unterteilt falls er eine gewisse Länge überschreitet. 

    lines = textwrap.wrap(self.user_text, 45)
        if lines == []:
            lines = [""]
        max_line = len(lines) - 1

Die Zeilen werden ebenfalls untereinander angeordnet. Zusätzlich wird ein Cursor gezeichnet
self.__draw_input_cursor(current_line, max_line) der current_line (gerendert) als Referenz für die horizontale und max_line als Referenz für die vertikale Position nutzt. Am Schluss wird noch der Rahmen self.input_rect an die gerenderte Höhe und Breite des Eingabetextes angepasst. 

    self.input_rect.width = max(200, first_line.get_width() + 15)
    self.input_rect.height = self.input_rect_normal_height * (max_line + 1) + 5

## Spieleinstellungen

### Steuerung (TODO)

### Schwierigkeitsgrade

Alle Schwierigkeitsgrade werden in der Klasse GameHandler gespeichert und verwendet. Mit der Methode set_level() kann man einen vom Benutzer ausgewählten Grad aus anderen Klassen in diese übergeben. Alle Schwierigkeitsgrade werden im Konstruktor von GameHandler wie folgt definiert:

# TODO

Jeder Grad hat also einen Namen und folgende Eigenschaften:

1. maze_preset_number - Die Gruppe, aus der ein Labyrinth ausgewählt werden muss.
2. debuffs amount - Die Anzahl von Strafen, die beim Bestrafen angewendet werden.
3. debuffs’ duration - Die Dauer von angewendeten Strafen (Anzahl der Bewegungen bis die Strafen ablaufen).

Die Namen werden lediglich zur Lesbar- und Verständlichkeit implementiert, insbesondere für einfachere und anschauliche Unterteilung von Prompts.

### Prompts 

Alle Prompts werden (manuell) serialisiert und in prompts.json Datei folgendermaßen gespeichert:

# TODO 

Hierbei ist zu erwähnen, dass den Namen von Prompts in der Screen Klasse (Feld personaliy_to_color) eine Farbe zugewiesen werden kann, mit der sie im Chat angezeigt werden. Nachdem ein Schwierigkeitsgrad ausgewählt wurde, wird vom GameHandler durch __set_random_prompt() ein zufälliger Prompt aus ausgewählter Gruppe genommen und als Liste [name, prompt_line] gespeichert, weil sie in dieser Form einfacher zuzugreifen sind. Auf ähnliche Art werden alle Labyrinthe gespeichert.

### Maze-Aufbau

#### Kleine Labyrinthe

Genauso wie alle Prompts, werden alle Labyrinthe serialisiert und in maze_presets.json Datei gespeichert. Es sind folgende Punkte beim Erstellen von einfachen (kleinen)Labyrinthen einzuhalten:

- Größe - 16x16 Felder.
- Rahmen - vorhanden. Ausnahmsweise kann der Endpunkt am Rand sein.
- Start- und Endpunkte - jeweils genau ein.
- Anfang - immer innerhalb der Sektion “0”.
- Finish ist mit implementierter Bewegungsmethode (Lauf bis zur nächsten Wand) erreichbar.
- Jeder Name folgt dem Muster: “maze_<difficulty>.<preset>”

Ein einfaches Labyrinth muss somit folgendermaßen aussehen:

# TODO

wobei Felder mit dem Wert “1” als ein Wandblock und mit dem Wert “0” als ein freies Feld betrachtet werden sollen. Labyrinthe dieser Größe eignen sich sehr gut für “EASY” und “NORMAL” Schwierigkeitsgrade. Damit das Spiel ein bisschen interessanter (und gleichzeitig schwerer) wird, wurden komplexe Labyrinthe und deren Verbindungen implementiert.

#### Größere Labyrinthe

Um den Horizont zu erweitern, werden einfachere Labyrinthe zusammengebunden. Größere Labyrinthe müssen somit zusätzliche generelle Eigenschaften besitzen:

- Größe: n x (16x16) Felder.
- Zwischen jeder Sektion besteht mindestens eine Verbindung.
- Beide Start- und Endpunkte müssen in jeder Sektion definiert (jedoch nicht unbedingt erreichbar) sein.
- Es gibt mindestens einen erreichbaren Endpunkt.

Alle Verbindungen (bridges) werden unter Schlüsselwort “connections” in jedem Preset gespeichert. Jede dieser Verbindungen ist wie folgt aufgebaut:

# TODO 

Mit dieser Struktur sind tatsächlich Übergänge aus jedem Punkt zu jeweils einem anderen implementierbar. Der Übergang zwischen einzelnen Sektionen erfolgt in move_until_wall() der Klasse GameLoop beim Aufruf von switch_section() vom GameHandler:

# TODO 

switch_section() sucht also unter einer Liste von Bridges, die aus aktueller Sektion (Key im graph Dictionary) anfangen, einen Startpunkt (Index 1), der mit aktueller Position von Figur übereinstimmt und wechselt aktuelles Labyrinth zu in Bridge gegebener Sektion (Index 0).

#### Animationen

Auf eine ähnliche einfachere Weise werden die Animationen gebaut. Jede Animation besteht aus einzelnen Frames, die nichts anderes als weitere Labyrinthe für eine bestimmte Zeit angezeigt werden. Jeder dieser Frames hat einen Link auf den nächsten, wobei der letzte Frame auf den ersten (0-en) Frame verweist. Da hier kein Spieler bewegt wird, kann man die Verweise (sowie Anzeigedauer) direkt in Sektionen speichern, was das Erstellen und Verwalten von Animationen sehr erleichtert. Somit müssen diese spezielle Labyrinthe wie im Folgenden Code aussehen:

# TODO 

Jede Animation beginnt mit einem Startframe mit dem Namen “FINISH_<preset_number>”, der einmalig nach Bestehen vom Labyrinth gezeigt wird. So muss man zum o.g. Beispiel einen Startframe mit dem Namen “FINISH_0” hinzufügen, damit GameHandler seine Methode switch_idle_maze() ausführen kann:

# TODO

Alle Frames werden durch die Methode run_idle() im GameLoop gewechselt, indem ein Timer-Thread mit der Methode switch_idle_frame() gestartet wird. Dieser Thread führt seine Funktion erst nach einer vorgegebenen Zeit aus, die bereits im aktuellen Labyrinth (unter Index 3) vorhanden ist.

## Links 

[OpenAI](https://platform.openai.com/docs/overview)
[pyGame](https://www.pygame.org/docs/)
[KI_Wekstatt](https://kiwerkstatt.f2.htw-berlin.de/)
