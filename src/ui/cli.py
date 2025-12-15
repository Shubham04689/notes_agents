import os
import sys
from typing import Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from ..models import OllamaAdapter, GeminiAdapter, MistralAdapter
from ..models.base import BaseModelAdapter
from ..core import Orchestrator, StorageManager, StateManager
from ..pdf import PDFGenerator


class CLI:
    """Command-line interface for the note generator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.console = Console()
        self.model: Optional[BaseModelAdapter] = None
        self.storage: Optional[StorageManager] = None
        self.state: Optional[StateManager] = None
        self.orchestrator: Optional[Orchestrator] = None
    
    def run(self):
        """Main CLI loop"""
        self.console.print(Panel.fit(
            "[bold cyan]AI Note Generator[/bold cyan]\n" +
            "Generate comprehensive, book-quality notes on any topic",
            border_style="cyan"
        ))
        
        # Check for existing session
        state_file = os.path.join(
            self.config['storage']['base_dir'],
            self.config['storage']['state_file']
        )
        
        temp_state = StateManager(state_file)
        if temp_state.has_active_session():
            session_info = temp_state.get_session_info()
            self.console.print(f"\n[yellow]Found existing session:[/yellow]")
            self.console.print(f"  Topic: {session_info['topic']}")
            self.console.print(f"  Model: {session_info['model']}")
            self.console.print(f"  Status: {session_info['status']}")
            
            resume = Confirm.ask("\nResume this session?", default=True)
            if resume:
                self._resume_session(temp_state)
                return
        
        # New session flow
        self._new_session()
    
    def _new_session(self):
        """Start a new generation session"""
        # Step 1: Select model provider
        provider = self._select_provider()
        if not provider:
            self.console.print("[red]No provider selected. Exiting.[/red]")
            return
        
        # Step 2: Initialize model adapter
        self.model = self._initialize_model(provider)
        if not self.model:
            self.console.print("[red]Failed to initialize model. Exiting.[/red]")
            return
        
        # Step 3: Select specific model
        if not self._select_model():
            self.console.print("[red]No model selected. Exiting.[/red]")
            return
        
        # Step 4: Get topic
        topic = Prompt.ask("\n[bold]Enter the topic for note generation[/bold]")
        if not topic:
            self.console.print("[red]No topic provided. Exiting.[/red]")
            return
        
        # Step 5: Initialize components
        self._initialize_components(topic)
        
        # Step 6: Start generation
        self._run_generation(topic, resume=False)
    
    def _resume_session(self, temp_state: StateManager):
        """Resume an existing session"""
        session_info = temp_state.get_session_info()
        topic = session_info['topic']
        model_name = session_info['model']
        
        # Determine provider from model name
        provider = self._detect_provider(model_name)
        
        # Initialize model
        self.model = self._initialize_model(provider)
        if not self.model:
            self.console.print("[red]Failed to initialize model. Exiting.[/red]")
            return
        
        self.model.set_model(model_name)
        
        # Initialize components
        self._initialize_components(topic)
        
        # Resume generation
        self._run_generation(topic, resume=True)
    
    def _select_provider(self) -> Optional[str]:
        """Select model provider"""
        self.console.print("\n[bold]Available Model Providers:[/bold]")
        
        providers = []
        
        # Check Ollama
        ollama = OllamaAdapter()
        if ollama.is_available():
            providers.append(("ollama", "Ollama (Local)", "✓ Available"))
        else:
            providers.append(("ollama", "Ollama (Local)", "✗ Not available"))
        
        # Check Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            providers.append(("gemini", "Google Gemini", "✓ Available"))
        else:
            providers.append(("gemini", "Google Gemini", "✗ No API key"))
        
        # Check Mistral
        mistral_key = os.getenv('MISTRAL_API_KEY')
        if mistral_key:
            providers.append(("mistral", "Mistral AI", "✓ Available"))
        else:
            providers.append(("mistral", "Mistral AI", "✗ No API key"))
        
        # Display table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Provider")
        table.add_column("Status")
        
        available_providers = []
        for i, (key, name, status) in enumerate(providers, 1):
            table.add_row(str(i), name, status)
            if "✓" in status:
                available_providers.append((i, key))
        
        self.console.print(table)
        
        if not available_providers:
            self.console.print("\n[red]No providers available. Please configure at least one.[/red]")
            return None
        
        choice = Prompt.ask(
            "\nSelect provider",
            choices=[str(i) for i, _ in available_providers]
        )
        
        for i, key in available_providers:
            if str(i) == choice:
                return key
        
        return None
    
    def _initialize_model(self, provider: str) -> Optional[BaseModelAdapter]:
        """Initialize model adapter"""
        try:
            if provider == "ollama":
                return OllamaAdapter(host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'))
            elif provider == "gemini":
                return GeminiAdapter()
            elif provider == "mistral":
                return MistralAdapter()
        except Exception as e:
            self.console.print(f"[red]Error initializing {provider}: {e}[/red]")
            return None
    
    def _select_model(self) -> bool:
        """Select specific model"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                progress.add_task(description="Fetching available models...", total=None)
                models = self.model.list_models()
            
            if not models:
                self.console.print("[red]No models available.[/red]")
                return False
            
            self.console.print("\n[bold]Available Models:[/bold]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=3)
            table.add_column("Model Name")
            
            for i, model_name in enumerate(models, 1):
                table.add_row(str(i), model_name)
            
            self.console.print(table)
            
            choice = Prompt.ask(
                "\nSelect model",
                choices=[str(i) for i in range(1, len(models) + 1)]
            )
            
            selected_model = models[int(choice) - 1]
            self.model.set_model(selected_model)
            self.console.print(f"[green]Selected: {selected_model}[/green]")
            
            return True
        except Exception as e:
            self.console.print(f"[red]Error selecting model: {e}[/red]")
            return False
    
    def _initialize_components(self, topic: str):
        """Initialize storage, state, and orchestrator"""
        base_dir = self.config['storage']['base_dir']
        state_file = os.path.join(base_dir, self.config['storage']['state_file'])
        
        self.storage = StorageManager(base_dir)
        self.state = StateManager(state_file)
        self.orchestrator = Orchestrator(self.model, self.storage, self.state, self.config)
    
    def _run_generation(self, topic: str, resume: bool):
        """Run the generation process"""
        self.console.print(f"\n[bold green]Starting generation for: {topic}[/bold green]")
        self.console.print("[dim]This may take a while depending on topic complexity...[/dim]\n")
        
        try:
            result = self.orchestrator.generate_notes(topic, resume=resume)
            
            if result['success']:
                self.console.print("\n[bold green]Generation completed![/bold green]")
                self.console.print(f"Total words: {result.get('total_word_count', 0):,}")
                
                if result.get('ready_for_pdf'):
                    self._generate_pdf(topic)
                else:
                    self.console.print("\n[yellow]Note: Content not yet complete for PDF generation.[/yellow]")
                    if Confirm.ask("Continue generation?", default=True):
                        self._run_generation(topic, resume=True)
            else:
                self.console.print(f"[red]Generation failed: {result.get('error')}[/red]")
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Generation interrupted. Progress has been saved.[/yellow]")
            self.console.print("[dim]Run again to resume from where you left off.[/dim]")
        except Exception as e:
            self.console.print(f"[red]Error during generation: {e}[/red]")
            import traceback
            traceback.print_exc()
    
    def _generate_pdf(self, topic: str):
        """Generate PDF from content"""
        if not Confirm.ask("\nGenerate PDF?", default=True):
            return
        
        try:
            pdf_gen = PDFGenerator(self.config)
            
            # Get all content files
            content_files = self.storage.get_all_content_files()
            
            if not content_files:
                self.console.print("[red]No content files found.[/red]")
                return
            
            # Generate output filename
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_')
            output_path = os.path.join(
                self.config['storage']['base_dir'],
                f"{safe_topic}_notes.pdf"
            )
            
            # Metadata
            metadata = {
                'model': self.model.model_name,
                'total_word_count': self.state.state.get('total_word_count', 0)
            }
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                progress.add_task(description="Generating PDF...", total=None)
                pdf_path = pdf_gen.generate(topic, content_files, output_path, metadata)
            
            self.console.print(f"\n[bold green]PDF generated successfully![/bold green]")
            self.console.print(f"Location: {pdf_path}")
        
        except Exception as e:
            self.console.print(f"[red]PDF generation failed: {e}[/red]")
            import traceback
            traceback.print_exc()
    
    def _detect_provider(self, model_name: str) -> str:
        """Detect provider from model name"""
        if 'gemini' in model_name.lower():
            return 'gemini'
        elif 'mistral' in model_name.lower():
            return 'mistral'
        else:
            return 'ollama'
