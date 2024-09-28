# Welcome to Chat Maze 

Dear Player,

Are you ready for an exciting adventure? In Chat Maze, you are challenged to guide various characters with unique personalities out of a complex labyrinth. Your mission: to show them the right path and lead them safety.

Each character in this labyrinth has their own quirks – be it a snobbish prince, a rhyming poet, or a madman. Your instructions are their only way out of the tangled paths. But be warned, the characters can be as challenging and unpredictable as the labyrinth itself.

Have fun!

## User Doukumentation

- Specification 
- Game Setup
- How to play

#### Specification

- [Python 3.12.3](https://www.python.org/downloads/) 
- [Anaconda 24.5.0](https://www.anaconda.com/) or higher
- [OpenAI API key](https://platform.openai.com/api-keys) (they are **not** free )

#### Game Setup

1. Clone [Repository]()
2. Go to the chat-maze/src directory and create a JSON file called **config.json**. This file will contain the necessary API key for connecting with OpenAI's API.
3. Enter the following line of code and replace **YOUR API KEY** with your actual API key.
4.

        {
            "api_key" : "YOUR API KEY"
        }
        
5. Open the Anaconda console and navigate to the chat-maze directory.
6. Run the following command to create a new conda environment with all necessary dependencies.
7.      

        conda env create -f environment.yml

#### How to play

To run the game, go to the chat-maze/src directory and in the console enter the following 

    python main.py

After choosing a dificulty you can run
    
    /commands

to see a list of all commands. Or run 

    /help
    
to get help with your current level. 