import sys
import time
from rich.live import Live
from rich.markdown import Markdown
from core.config import ConfigManager
from core.engine import ModelEngine
from core.personas import PersonaManager
from interface.cli import UI, console

def chat_loop(engine: ModelEngine, config: ConfigManager, persona_mgr: PersonaManager):
    current_persona = config.settings.persona
    UI.print_system(f"Starting chat with persona: [bold]{current_persona}[/bold]")
    UI.print_system("Type 'exit', 'quit', or 'back' to return to menu.")
    
    while True:
        try:
            user_input = console.input(f"\n[bold blue]You[/bold blue] > ")
            if user_input.lower() in ('exit', 'quit', 'back'):
                break
            
            # Streaming response
            response_text = ""
            with Live(Markdown("..."), refresh_per_second=10) as live:
                for token in engine.generate_response(user_input, stream=True):
                    response_text += token
                    live.update(Markdown(response_text))
            
            # Add a final newline
            console.print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            UI.print_error(str(e))

def settings_menu(config: ConfigManager, engine: ModelEngine):
    while True:
        console.print("\n[bold]Current Settings:[/bold]")
        console.print(f"Model: {config.settings.model_name}")
        console.print(f"Max Tokens: {config.settings.max_tokens}")
        console.print(f"Temperature: {config.settings.temperature}")
        
        choice = console.input("\nType 'temp [value]', 'tokens [value]', 'model [name]' or 'back': ")
        parts = choice.split()
        
        if not parts:
             continue
             
        cmd = parts[0].lower()
        if cmd == 'back':
            break
        
        try:
            if cmd == 'temp':
                val = float(parts[1])
                config.update(temperature=val)
                UI.print_system(f"Temperature set to {val}")
            elif cmd == 'tokens':
                val = int(parts[1])
                config.update(max_tokens=val)
                UI.print_system(f"Max Tokens set to {val}")
            elif cmd == 'model':
                # Simplified for now
                name = parts[1]
                UI.print_system(f"Attempting to load {name}...")
                if engine.load_model(name):
                    UI.print_system("Model loaded successfully.")
                else:
                    UI.print_error("Failed to load model.")
            else:
                UI.print_error("Unknown command.")
        except IndexError:
            UI.print_error("Missing value.")
        except ValueError:
            UI.print_error("Invalid value.")

def main():
    # Initialize
    config = ConfigManager()
    persona_mgr = PersonaManager()
    engine = ModelEngine(config)
    
    # Pre-load model if configured? 
    # Or wait until first chat to save startup time. 
    # Let's load on startup to be ready.
    UI.print_header()
    UI.print_system("Initializing Engine...")
    is_loaded = engine.load_model()
    
    if not is_loaded:
        UI.print_error("Could not load default model. Please check settings or download a model.")
        # We don't exit, we let them go to menu to maybe download? 
        # (Download not fully implemented yet in auto-mode, but they can select files)

    while True:
        UI.print_header()
        choice = UI.show_menu()
        
        if choice == "1":
            if not engine.model:
                 if not engine.load_model():
                     UI.print_error("No model loaded.")
                     time.sleep(2)
                     continue
            chat_loop(engine, config, persona_mgr)
            
        elif choice == "2":
            personas = persona_mgr.list_personas()
            new_persona = UI.select_persona(personas)
            config.update(persona=new_persona)
            UI.print_system(f"Persona updated to {new_persona}")
            time.sleep(1)
            
        elif choice == "3":
            settings_menu(config, engine)
            
        elif choice == "4":
            UI.print_system("Fetching available models (this may take a few seconds)...")
            models = engine.fetch_available_models()
            selected_filename = UI.show_model_selection(models)
            
            if selected_filename:
                UI.print_system(f"Switching to {selected_filename}...")
                if engine.load_model(selected_filename):
                    UI.print_system("Model loaded successfully.")
                else:
                    UI.print_error("Failed to load model.")
                    
        elif choice == "5":
            UI.print_system("Goodbye!")
            break

if __name__ == "__main__":
    main()
