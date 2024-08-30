# User Documentation

- Specification 
- Game Setup
- How to play

### Specification

- [Python 3.12.3](https://www.python.org/downloads/) 
- [Anaconda 24.5.0](https://www.anaconda.com/) or higher
- [OpenAI API key](https://platform.openai.com/api-keys) (they are **not** free)

### Game Setup

1. Clone [this repository]().
2. Go to the `../chat-leap/src` directory and create a file called **config.json**. This file must contain the following and the only one necessary line for connecting to OpenAI's API. Replace **YOUR API KEY** with your actual API key:
```
    {
        "api_key" : "YOUR API KEY"
    }
```        
3. Open the Anaconda console and navigate to the `./chat-leap` directory.
4. Run the following command to create a new conda environment with all necessary dependencies:   
```
    conda env create -f environment.yml
```
### How to play

To start the game, go to the `../chat-leap/src` directory and enter the following command into console:
```
    python main.py
```
After choosing a difficulty try following commands:
- `/commands` - to see a list of all commands.
- `/help` - to get help with your current level.