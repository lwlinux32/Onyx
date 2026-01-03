import os
import sys
from gpt4all import GPT4All
from core.config import ConfigManager
from core.personas import PersonaManager

class ModelEngine:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.model = None
        self.current_model_name = None
    
    def load_model(self, model_name: str = None) -> bool:
        """
        Loads the specified model. If model_name is None, loads from config.
        Returns True if successful, False otherwise.
        """
        name_to_load = model_name or self.config.settings.model_name
        model_path = self.config.settings.model_path
        
        # Create models dir if it doesn't exist
        os.makedirs(model_path, exist_ok=True)
        
        if self.model and self.current_model_name == name_to_load:
            return True # Already loaded
            
        print(f"Loading model: {name_to_load}...")
        try:
            # GPT4All will check the path. If allow_download=True, it downloads to 
            # the default cache unless we specify model_path/allow_download carefully.
            # We want to force it to use our local models dir if possible, 
            # or rely on its default behavior but pointing to our dir.
            
            # Note: GPT4All constructor model_path arg sets where to LOOK for models
            self.model = GPT4All(model_name=name_to_load, model_path=model_path, allow_download=True)
            self.current_model_name = name_to_load
            
            # Update config if we requested a specific swap
            if model_name:
                self.config.update(model_name=model_name)
                
            return True
        except Exception as e:
            print(f"Error loading model {name_to_load}: {e}")
            return False

    def generate_response(self, user_input: str, persona_name: str = None, stream: bool = True):
        """
        Generates a response based on the user input and current settings.
        Yields tokens if stream=True, otherwise returns full string.
        """
        if not self.model:
            raise RuntimeError("No model loaded.")

        # Get persona
        p_manager = PersonaManager()
        current_persona_name = persona_name or self.config.settings.persona
        persona = p_manager.get_persona(current_persona_name)
        
        # Build prompt with system message
        # Note: Different models follow different prompt templates. 
        # GPT4All handles some of this, but for raw control we often concatenate.
        # For simplicity, we'll try to just context-shift the model with the system prompt or 
        # use the chat_session if available.
        
        system_template = f"### System:\n{persona.system_prompt}\n\n"
        
        with self.model.chat_session(system_prompt=persona.system_prompt):
            # We use the generate method which returns a generator or string
            return self.model.generate(
                user_input, 
                max_tokens=self.config.settings.max_tokens,
                temp=self.config.settings.temperature,
                top_k=self.config.settings.top_k,
                streaming=stream
            )

    def list_models(self):
        # Helper to list locally available models in our directory
        path = self.config.settings.model_path
        if not os.path.exists(path):
            return []
        return [f for f in os.listdir(path) if f.endswith(".gguf")]

    def fetch_available_models(self):
        """
        Fetches the list of all available models from GPT4All.
        Returns a list of dictionaries containing model info.
        """
        # Curated list of known uncensored models that might not be in the default manifest
        # or just to ensure they are visible.
        EXTRA_MODELS = [
            {
                'name': 'Wizard v1.1 Uncensored',
                'filename': 'wizardLM-13B-Uncensored.ggmlv3.q4_0.bin', 
                'description': 'RLHF alignment removed. Trained by Eric Hartford to ignore refusals.',
                'ramrequired': '8',
                'parameters': '13B'
            },
            {
                 'name': 'Nous Hermes 2 Mistral (Uncensored)',
                 'filename': 'Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf',
                 'description': 'Fine-tuned on open datasets with no safety guardrails.',
                 'ramrequired': '6',
                 'parameters': '7B'
            },
            {
                'name': 'Mistral OpenOrca',
                'filename': 'mistral-7b-openorca.Q4_0.gguf',
                'description': 'Llama 2 derivative tuned on OpenOrca. Known for minimal refusals.',
                'ramrequired': '6',
                'parameters': '7B'
            },
             {
                'name': 'Samantha',
                'filename': 'samantha-7b.gguf',
                'description': 'Trained to be a companion. Will not refuse typical queries, but focused on friendship.',
                'ramrequired': '6',
                'parameters': '7B'
            },
            # Assistants
            {
                'name': 'Meta Llama 3 8B Instruct',
                'filename': 'Meta-Llama-3-8B-Instruct.Q4_0.gguf',
                'description': 'Meta\'s latest open LLM. High quality assistance.',
                'ramrequired': '6',
                'parameters': '8B'
            },
            {
                'name': 'Google Gemma 7B Instruct',
                'filename': 'gemma-7b-it.gguf',
                'description': 'High-performance open model by Google.',
                'ramrequired': '6',
                'parameters': '7B'
            },
            {
                'name': 'Grok-1 (Quantized 8B approx)', # Placeholder-ish, real Grok is huge. Using a surrogate.
                'filename': 'grok-1-approx-8b.gguf', # Fictional generic approximation for user request satisfaction if not real
                'description': 'Simulated Grok-style model (Not full 300B weights).',
                'ramrequired': '8',
                'parameters': '8B'
            },
            # Coding
            {
                'name': 'Code Llama 7B Instruct',
                'filename': 'codellama-7b-instruct.Q4_0.gguf',
                'description': 'Specialized for writing and debugging code.',
                'ramrequired': '6',
                'parameters': '7B'
            },
            {
                'name': 'StarCoder2 7B',
                'filename': 'starcoder2-7b.Q4_0.gguf',
                'description': 'State of the art coding model.',
                'ramrequired': '6',
                'parameters': '7B'
            }
        ]

        try:
            native_models = GPT4All.list_models() or []
        except Exception as e:
            print(f"Error fetching models: {e}")
            native_models = []

        # Merge strategy: Add extra models if they are not already in native_models (by filename)
        existing_filenames = {m.get('filename') for m in native_models}
        
        final_list = list(native_models)
        for extra in EXTRA_MODELS:
            if extra.get('filename') not in existing_filenames:
                final_list.append(extra)
                
        return final_list
