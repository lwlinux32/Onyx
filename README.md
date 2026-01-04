# Onyx

An AI that doesnt need any API's or any reverse engineering but has no limits made with GPT4All.



## Features

- **🚀 Local AI Power**: Runs locally using GPT4All models. No API keys or internet required after model download.
- **💎 Sleek UI**: Beautiful Rich terminal interface with Onyx-themed dark aesthetics.
- **🎭 Personality System**: Switch between different personalities like "Super Coder", "CLI Expert", or create your own.
- **⚙️ Dynamic Engine Switching**: View available local models and their RAM usage, and switch engines on the fly.
- **🛠️ Configurable**: Adjustable temperature, max tokens, and model settings.
- **⚙️ Offline working**: When you download the model, you dont need any wifi to chat.
## Getting Ready

1. **Requirements**
- Python 3.8+ installed and the libraries gpt4all, rich, pyyaml and requests 
- 4GB+ RAM (8GB+ recommended for better models)
- Internet connection (initial model download only)
- Libraries gpt4all, rich, pyyaml and requests  
   If they are ready, then you're good to go!
## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/lwlinux32/Onyx.git
    cd Onyx
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    ### Note: "Externally managed enviroment"(PEP 6xx) or the "HINT:this package was installed by debian." errors solved(if needed)
     ** pip has a LOT of errors in linux so,the solvings for the install are followed by: **  
   
    #### Breaking the system packages
 by using the   ```--break-system-packages ``` and   ```--ignore-installed ``` your errors will be gone! But, breaking the system packages can make other errors so it is NOT recommended. The command will be:
    ```bash
     pip install requirements.txt -r --break-system-packages --ignore-installed
    ```
#### Create a Virtual Environment (recommended) 
      
    *Debian/Ubuntu/Arch/Fedora:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
     ```
    
    *Termux:*
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    *(You will see `(venv)` appear in your terminal prompt)*

## Usage

Run the main application:

```bash
python main.py
```

### Menu Options

1.  **Chat with AI**: Start a conversation with the current persona.
2.  **Change Persona**: Switch the AI's personality.
3.  **Settings**: Adjust model parameters (Temp, Max Tokens) or load a specific model file.
4.  **Change AI Engine**: View detailed list of available GPT4All models (with RAM usage) and switch the active engine.
5.  **Exit**: Close the application.






