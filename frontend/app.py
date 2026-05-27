from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk
from typing import Callable

try:
    from .backend_bridge import BackendBridge, BackendBridgeError, FrontendMetadata
except ImportError:
    from backend_bridge import BackendBridge, BackendBridgeError, FrontendMetadata


@dataclass(frozen=True)
class ScenarioFieldSpec:
    label: str
    default: int
    minimum: int = 1


@dataclass(frozen=True)
class ScenarioDefinition:
    title: str
    description: str
    fields: tuple[ScenarioFieldSpec, ...]
    tips: str


SCENARIO_DEFINITIONS = {
    "producer_consumer": ScenarioDefinition(
        title="Producer-Consumer",
        description="Defina os parâmetros do cenário Producer-Consumer.",
        fields=(
            ScenarioFieldSpec("Número de produtores", 2),
            ScenarioFieldSpec("Número de consumidores", 2),
            ScenarioFieldSpec("Tamanho do buffer", 5),
            ScenarioFieldSpec("Items por produtor", 10),
        ),
        tips=(
            "Conselhos:\n"
            "- Valores equilibrados entre produtores e consumidores (por exemplo 2 e 2) ajudam a observar melhor a alternância.\n"
            "- Um buffer muito pequeno provoca bloqueios frequentes; os produtores ficam à espera com mais frequência.\n"
            "- Um buffer muito elevado reduz bloqueios, mas pode esconder o comportamento concorrente que se pretende estudar.\n"
            "- Muitos produtores ou consumidores aumentam bastante o volume de logs e tornam a execução mais demorada."
        ),
    ),
    "readers_writers": ScenarioDefinition(
        title="Readers-Writers",
        description="Defina os parâmetros do cenário Readers-Writers.",
        fields=(
            ScenarioFieldSpec("Número de leitores", 3),
            ScenarioFieldSpec("Número de escritores", 2),
            ScenarioFieldSpec("Iterações por thread", 5),
        ),
        tips=(
            "Conselhos:\n"
            "- Uma configuração equilibrada, como 3 leitores e 2 escritores, mostra bem o padrão clássico do problema.\n"
            "- Muitos escritores fazem o recurso partilhado ficar mais tempo bloqueado, reduzindo a perceção de paralelismo.\n"
            "- Muitos leitores aumentam a concorrência, mas também podem prolongar a fila de espera dos escritores.\n"
            "- Iterações demasiado altas produzem logs extensos e a execução fica mais lenta."
        ),
    ),
    "dining_philosophers": ScenarioDefinition(
        title="Dining Philosophers",
        description="Defina os parâmetros do cenário Dining Philosophers.",
        fields=(
            ScenarioFieldSpec("Número de filósofos", 5, minimum=3),
            ScenarioFieldSpec("Rondas por filósofo", 4),
        ),
        tips=(
            "Conselhos:\n"
            "- O mínimo recomendado é 3 filósofos; com menos do que isso o cenário deixa de ser representativo.\n"
            "- Valores perto de 5 filósofos são bons para observar o padrão clássico sem sobrecarregar demasiado os logs.\n"
            "- Muitíssimos filósofos aumentam a contenção pelos garfos e fazem a simulação demorar mais.\n"
            "- Rondas muito elevadas geram muita repetição e tornam a análise mais pesada."
        ),
    ),
    "barrier_synchronization": ScenarioDefinition(
        title="Barrier Synchronization",
        description="Defina os parâmetros do cenário Barrier Synchronization.",
        fields=(
            ScenarioFieldSpec("Número de workers", 4),
            ScenarioFieldSpec("Número de fases", 3),
        ),
        tips=(
            "Conselhos:\n"
            "- 4 workers e 3 fases é uma configuração equilibrada para perceber a sincronização por barreira.\n"
            "- Muitos workers aumentam o tempo de espera na barreira e podem dar a sensação de que a aplicação está parada.\n"
            "- Fases muito elevadas multiplicam as sincronizações e deixam os logs bastante longos.\n"
            "- Se queres observar a barreira com clareza, evita combinar muitos workers com muitas fases em simultâneo."
        ),
    ),
}


FUNDAMENTAL_TOPICS: tuple[tuple[str, str], ...] = (
    (
        "1. O que é programação concorrente",
        "Programação concorrente é a organização de tarefas que podem progredir em paralelo ou de forma intercalada. "
        "O objetivo não é apenas acelerar a execução, mas também modelar problemas em que várias atividades precisam "
        "de partilhar recursos, esperar umas pelas outras ou avançar em fases coordenadas.",
    ),
    (
        "2. Processos, threads e partilha de memória",
        "Um processo é uma instância isolada de execução. Threads vivem dentro de um processo e partilham o mesmo espaço "
        "de memória, o que facilita a troca de dados mas aumenta o risco de interferências. Nesta aplicação, os cenários "
        "mostram precisamente como essa partilha exige controlo cuidadoso.",
    ),
    (
        "3. Secções críticas e condições de corrida",
        "Uma secção crítica é a parte do código que acede a um recurso partilhado. Se duas threads entrarem ao mesmo tempo "
        "sem proteção adequada, pode surgir uma condição de corrida: o resultado passa a depender da ordem exata de execução, "
        "e esse comportamento pode variar entre execuções.",
    ),
    (
        "4. Exclusão mútua e sincronização",
        "A exclusão mútua impede que mais do que uma thread altere um recurso sensível em simultâneo. Já a sincronização "
        "serve para coordenar momentos específicos de execução, por exemplo quando várias threads precisam de terminar uma "
        "fase antes de avançarem para a seguinte. Mutexes, semáforos e barreiras são mecanismos clássicos para estes casos.",
    ),
    (
        "5. Problemas clássicos demonstrados aqui",
        "Producer-Consumer mostra a coordenação entre quem produz e quem consome dados num buffer limitado. Readers-Writers "
        "ilustra o equilíbrio entre múltiplos leitores e escritores num recurso partilhado. Dining Philosophers evidencia "
        "contenção por recursos e o risco de deadlock. Barrier Synchronization mostra como forçar vários workers a esperar "
        "uns pelos outros antes de prosseguirem.",
    ),
    (
        "6. Interpretação dos logs",
        "Os logs ajudam a observar a ordem real dos eventos. Em programação concorrente, isso é importante porque o comportamento "
        "não é apenas definido pelo algoritmo, mas também pelo agendamento das threads, pelo tempo de espera e pela forma como "
        "os recursos são protegidos. Ler os logs com atenção ajuda a perceber bloqueios, alternância entre threads e fases de espera.",
    ),
)


class SimulatorStartView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self._bridge = BackendBridge()
        self._metadata = None
        self._current_view: ttk.Frame | None = None

        self.title("Simulador Interativo de Programação Concorrente")
        self.configure(bg="#101827")
        self.geometry("960x560")
        self.minsize(760, 460)

        self._configure_style()
        self._build_layout()
        self._load_metadata()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Root.TFrame", background="#101827")
        style.configure("Card.TFrame", background="#162033")
        style.configure("MenuCard.TFrame", background="#111c2f")
        style.configure(
            "Title.TLabel",
            background="#162033",
            foreground="#f8fafc",
            font=("Segoe UI", 30, "bold"),
            justify="center",
            wraplength=760,
        )
        style.configure(
            "MenuTitle.TLabel",
            background="#111c2f",
            foreground="#f8fafc",
            font=("Segoe UI", 24, "bold"),
            justify="center",
            wraplength=640,
        )
        style.configure(
            "Start.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(22, 12),
            background="#0f766e",
            foreground="#ffffff",
        )
        style.configure(
            "MenuButton.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(18, 12),
            background="#1f2937",
            foreground="#ffffff",
        )
        style.map(
            "Start.TButton",
            background=[("active", "#115e59"), ("pressed", "#134e4a")],
            foreground=[("disabled", "#d1d5db")],
        )
        style.map(
            "MenuButton.TButton",
            background=[("active", "#334155"), ("pressed", "#475569")],
            foreground=[("disabled", "#d1d5db")],
        )

    def _build_layout(self) -> None:
        self._view_container = ttk.Frame(self, style="Root.TFrame", padding=28)
        self._view_container.pack(fill="both", expand=True)
        self._show_start_view()

    def _show_view(self, view: ttk.Frame) -> None:
        if self._current_view is not None:
            self._current_view.destroy()

        self._current_view = view
        self._current_view.pack(fill="both", expand=True)

    def _show_start_view(self) -> None:
        view = StartView(self._view_container, self._on_start)
        self._show_view(view)

    def _load_metadata(self) -> None:
        try:
            metadata = self._bridge.get_metadata()
        except BackendBridgeError as exc:
            self._metadata = None
            if self._current_view is not None and hasattr(self._current_view, "set_metadata"):
                self._current_view.set_metadata(None)
            return

        self._metadata = metadata
        if self._current_view is not None and hasattr(self._current_view, "set_metadata"):
            self._current_view.set_metadata(metadata)

    def _on_start(self) -> None:
        if self._metadata is None:
            return

        try:
            self._bridge.initialize_session()
        except BackendBridgeError:
            return

        self.title("Menu Principal")  # Fixed typo in title
        self._show_main_menu_view()

    def _show_main_menu_view(self) -> None:
        self._show_view(
            MainMenuView(
                self._view_container,
                self._on_exit,
                self._show_scenarios_view,
                self._show_fundamentals_view,
            )
        )

    def _show_fundamentals_view(self) -> None:
        self.title("Conceitos Fundamentais")
        self._show_view(FundamentalsView(self._view_container, self._show_main_menu_view))

    def _show_scenarios_view(self) -> None:
        self.title("Lista de Cenários")
        self._show_view(
            ScenariosView(
                self._view_container,
                self._show_main_menu_view,
                self._show_scenario_config_view,
            )
        )

    def _show_scenario_config_view(self, scenario_key: str) -> None:
        definition = SCENARIO_DEFINITIONS[scenario_key]
        self.title(definition.title)
        self._show_view(
            ScenarioConfigView(
                self._view_container,
                scenario_key,
                definition,
                self._show_scenarios_view,
                lambda: self._show_scenario_tips_view(scenario_key),
                lambda values: self._show_scenario_run_view(scenario_key, values),
            )
        )

    def _show_scenario_tips_view(self, scenario_key: str) -> None:
        definition = SCENARIO_DEFINITIONS[scenario_key]
        self.title(f"Dicas - {definition.title}")
        self._show_view(
            ScenarioTipsView(
                self._view_container,
                definition,
                lambda: self._show_scenario_config_view(scenario_key),
            )
        )

    def _show_scenario_run_view(self, scenario_key: str, values: dict[str, int]) -> None:
        definition = SCENARIO_DEFINITIONS[scenario_key]
        self.title(f"Acompanhamento - {definition.title}")
        ordered_values = [values[field.label] for field in definition.fields]
        log_path = self._build_log_path(definition.title)

        try:
            execution_result = self._bridge.execute_scenario(scenario_key, ordered_values, log_path)
        except BackendBridgeError as exc:
            self._show_view(
                ScenarioExecutionErrorView(
                    self._view_container,
                    definition,
                    str(exc),
                    lambda: self._show_scenario_config_view(scenario_key),
                )
            )
            return

        Path(execution_result.log_path).write_text("\n".join(execution_result.logs) + "\n", encoding="utf-8")

        self._show_view(
            ScenarioRunView(
                self._view_container,
                definition,
                execution_result.logs,
                execution_result.log_path,
                execution_result.summary,
                self._show_main_menu_view,
            )
        )

    def _build_log_path(self, scenario_title: str) -> str:
        project_root = Path(__file__).resolve().parents[1]
        logs_directory = project_root / "logs"
        logs_directory.mkdir(parents=True, exist_ok=True)
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        return str(logs_directory / f"{scenario_title}_{timestamp}.txt")

    def _on_exit(self) -> None:
        self.destroy()


class StartView(ttk.Frame):
    def __init__(self, owner: ttk.Frame, on_start: Callable[[], None]) -> None:
        super().__init__(owner, style="Card.TFrame", padding=(40, 34))
        self._on_start = on_start

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)

        self._title_label = ttk.Label(self, style="Title.TLabel")
        self._title_label.grid(row=0, column=0, sticky="", pady=(44, 0))

        self._start_button = ttk.Button(self, style="Start.TButton", command=self._on_start)
        self._start_button.grid(row=1, column=0, sticky="s", pady=(0, 68))

    def set_metadata(self, metadata: FrontendMetadata | None) -> None:
        if metadata is None:
            self._title_label.config(text="Simulador Interativo de Programação Concorrente")
            self._start_button.config(text="Iniciar", state="disabled")
            return

        self._title_label.config(text=metadata.title)
        self._start_button.config(text=metadata.start_button_text, state="normal")


class MainMenuView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        on_exit: Callable[[], None],
        on_scenarios: Callable[[], None],
        on_fundamentals: Callable[[], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._on_exit = on_exit
        self._on_scenarios = on_scenarios
        self._on_fundamentals = on_fundamentals

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text="Menu principal",  # Fixed typo in title
        )
        title.grid(row=0, column=0, sticky="n", pady=(22, 30))

        buttons_frame = ttk.Frame(self, style="MenuCard.TFrame")
        buttons_frame.grid(row=1, column=0, sticky="n")
        buttons_frame.columnconfigure(0, weight=1)

        ttk.Button(
            buttons_frame,
            text="Lista de cenários",
            style="MenuButton.TButton",
            command=self._on_scenarios,
        ).grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Conceitos Fundamentais",
            style="MenuButton.TButton",
            command=self._on_fundamentals,
        ).grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Sair",
            style="MenuButton.TButton",
            command=self._on_exit,
        ).grid(row=2, column=0, sticky="ew")

class ScenariosView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        on_back: Callable[[], None],
        on_open_scenario: Callable[[str], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._on_back = on_back
        self._on_open_scenario = on_open_scenario

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text="Lista de cenários.",
        )
        title.grid(row=0, column=0, sticky="n", pady=(22, 30))

        buttons_frame = ttk.Frame(self, style="MenuCard.TFrame")
        buttons_frame.grid(row=1, column=0, sticky="n")
        buttons_frame.columnconfigure(0, weight=1)

        ttk.Button(
            buttons_frame,
            text="Producer-Consumer",
            style="MenuButton.TButton",
            command=lambda: self._on_open_scenario("producer_consumer"),
        ).grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Readers-Writers",
            style="MenuButton.TButton",
            command=lambda: self._on_open_scenario("readers_writers"),
        ).grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Dining Philosophers",
            style="MenuButton.TButton",
            command=lambda: self._on_open_scenario("dining_philosophers"),
        ).grid(row=2, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Barrier Synchronization",
            style="MenuButton.TButton",
            command=lambda: self._on_open_scenario("barrier_synchronization"),
        ).grid(row=3, column=0, sticky="ew", pady=(0, 14))

        ttk.Button(
            buttons_frame,
            text="Regressar ao menu principal",
            style="MenuButton.TButton",
            command=self._on_back,
        ).grid(row=4, column=0, sticky="ew")


class FundamentalsView(ttk.Frame):
    def __init__(self, owner: ttk.Frame, on_back: Callable[[], None]) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._on_back = on_back

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text="Conceitos Fundamentais",
        )
        title.grid(row=0, column=0, sticky="n", pady=(10, 18))

        content_card = ttk.Frame(self, style="MenuCard.TFrame")
        content_card.grid(row=1, column=0, sticky="nsew")
        content_card.columnconfigure(0, weight=1)
        content_card.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(content_card, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        content = tk.Text(
            content_card,
            wrap="word",
            relief="flat",
            bg="#111c2f",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            font=("Segoe UI", 11),
            padx=18,
            pady=18,
            borderwidth=0,
            yscrollcommand=scrollbar.set,
        )
        content.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=content.yview)

        content.insert("1.0", self._build_content())
        content.configure(state="disabled")

        ttk.Button(
            self,
            text="Voltar ao menu principal",
            style="MenuButton.TButton",
            command=self._on_back,
        ).grid(row=2, column=0, sticky="ew", pady=(18, 0))

    def _build_content(self) -> str:
        paragraphs: list[str] = []

        intro = (
            "Esta secção resume os conceitos que ajudam a interpretar os cenários desta aplicação. "
            "A leitura destes tópicos dá contexto ao comportamento observado nos logs e nas fases de sincronização.\n\n"
        )
        paragraphs.append(intro)

        for heading, body in FUNDAMENTAL_TOPICS:
            paragraphs.append(f"{heading}\n{body}\n\n")

        conclusion = (
            "Sugestão de leitura: começa por secções críticas, exclusão mútua e sincronização, "
            "e depois revê cada cenário procurando identificar onde esses mecanismos aparecem na prática."
        )
        paragraphs.append(conclusion)

        return "".join(paragraphs)

class ScenarioConfigView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        scenario_key: str,
        definition: ScenarioDefinition,
        on_back: Callable[[], None],
        on_tips: Callable[[], None],
        on_execute: Callable[[dict[str, int]], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._scenario_key = scenario_key
        self._definition = definition
        self._on_back = on_back
        self._on_tips = on_tips
        self._on_execute = on_execute
        self._field_vars: dict[str, tk.StringVar] = {}
        self._info_var = tk.StringVar(value=definition.description)

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text=self._definition.title,
        )
        title.grid(row=0, column=0, sticky="n", pady=(10, 18))

        form = ttk.Frame(self, style="MenuCard.TFrame")
        form.grid(row=1, column=0, sticky="nsew")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        for index, field in enumerate(self._definition.fields):
            row = index // 2
            column = (index % 2) * 2

            field_label = ttk.Label(
                form,
                style="MenuTitle.TLabel",
                text=field.label,
                font=("Segoe UI", 11, "bold"),
                wraplength=280,
            )
            field_label.grid(row=row * 2, column=column, columnspan=2, sticky="w", pady=(0, 6))

            variable = tk.StringVar(value=str(field.default))
            self._field_vars[field.label] = variable

            entry = ttk.Entry(form, textvariable=variable, width=18)
            entry.grid(row=row * 2 + 1, column=column, sticky="ew", padx=(0, 16), pady=(0, 18))

            helper = ttk.Label(
                form,
                text=f"Valor mínimo: {field.minimum}",
                style="MenuTitle.TLabel",
                font=("Segoe UI", 9),
                wraplength=240,
            )
            helper.grid(row=row * 2 + 1, column=column + 1, sticky="w", pady=(0, 18))

        buttons_frame = ttk.Frame(self, style="MenuCard.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)

        ttk.Button(
            buttons_frame,
            text="Executar Cenário",
            style="MenuButton.TButton",
            command=self._execute_scenario,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ttk.Button(
            buttons_frame,
            text="Dicas",
            style="MenuButton.TButton",
            command=self._on_tips,
        ).grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Button(
            buttons_frame,
            text="Voltar à lista de cenários",
            style="MenuButton.TButton",
            command=self._on_back,
        ).grid(row=0, column=2, sticky="ew")

        info_label = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            textvariable=self._info_var,
            font=("Segoe UI", 10),
            wraplength=760,
        )
        info_label.grid(row=3, column=0, sticky="n", pady=(16, 0))

    def _collect_values(self) -> dict[str, int] | None:
        values: dict[str, int] = {}

        for field in self._definition.fields:
            raw_value = self._field_vars[field.label].get().strip()

            try:
                value = int(raw_value)
            except ValueError:
                self._info_var.set(f"O campo '{field.label}' tem de ser um número inteiro positivo.")
                return None

            if value < field.minimum:
                self._info_var.set(f"O campo '{field.label}' tem de ser pelo menos {field.minimum}.")
                return None

            values[field.label] = value

        return values

    def _execute_scenario(self) -> None:
        values = self._collect_values()
        if values is None:
            return

        ordered_values = ", ".join(f"{name}={value}" for name, value in values.items())
        self._info_var.set(f"Cenário preparado com sucesso: {ordered_values}")
        self._on_execute(values)

    def _show_tips(self) -> None:
        self._info_var.set(self._definition.tips)


class ScenarioTipsView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        definition: ScenarioDefinition,
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._definition = definition
        self._on_back = on_back

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text=f"Dicas - {self._definition.title}",
        )
        title.grid(row=0, column=0, sticky="n", pady=(10, 18))

        tips_card = ttk.Frame(self, style="MenuCard.TFrame")
        tips_card.grid(row=1, column=0, sticky="nsew")
        tips_card.columnconfigure(0, weight=1)

        tips_text = tk.Text(
            tips_card,
            wrap="word",
            height=14,
            relief="flat",
            bg="#111c2f",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            font=("Segoe UI", 11),
            padx=16,
            pady=16,
            borderwidth=0,
        )
        tips_text.grid(row=0, column=0, sticky="nsew")
        tips_text.insert("1.0", self._definition.tips)
        tips_text.configure(state="disabled")

        ttk.Button(
            self,
            text="Voltar à configuração do cenário",
            style="MenuButton.TButton",
            command=self._on_back,
        ).grid(row=2, column=0, sticky="ew", pady=(18, 0))


class ScenarioRunView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        definition: ScenarioDefinition,
        logs: list[str],
        log_path: str,
        summary: str,
        on_main_menu: Callable[[], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._definition = definition
        self._logs = logs
        self._log_path = log_path
        self._on_main_menu = on_main_menu
        self._index = 0
        self._finished = False
        self._current_log_var = tk.StringVar(value=logs[0] if logs else "Sem logs disponíveis.")
        self._status_var = tk.StringVar(value=summary)

        self._build_layout()
        self._refresh_navigation()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text=f"Acompanhamento - {self._definition.title}",
        )
        title.grid(row=0, column=0, sticky="n", pady=(10, 18))

        log_card = ttk.Frame(self, style="MenuCard.TFrame", padding=(24, 24))
        log_card.grid(row=1, column=0, sticky="nsew")
        log_card.columnconfigure(0, weight=1)
        log_card.rowconfigure(0, weight=1)

        self._log_label = ttk.Label(
            log_card,
            textvariable=self._current_log_var,
            style="MenuTitle.TLabel",
            font=("Segoe UI", 14),
            justify="center",
            wraplength=760,
            anchor="center",
        )
        self._log_label.grid(row=0, column=0, sticky="nsew")

        self._status_label = ttk.Label(
            self,
            textvariable=self._status_var,
            style="MenuTitle.TLabel",
            font=("Segoe UI", 10),
            wraplength=760,
        )
        self._status_label.grid(row=2, column=0, sticky="n", pady=(16, 10))

        path_label = ttk.Label(
            self,
            text=f"Log guardado em: {self._log_path}",
            style="MenuTitle.TLabel",
            font=("Segoe UI", 9),
            wraplength=760,
        )
        path_label.grid(row=3, column=0, sticky="n", pady=(0, 10))

        controls = ttk.Frame(self, style="MenuCard.TFrame")
        controls.grid(row=4, column=0, sticky="ew")
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(2, weight=1)

        self._previous_button = ttk.Button(
            controls,
            text="Anterior",
            style="MenuButton.TButton",
            command=self._previous_log,
        )
        self._previous_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self._next_button = ttk.Button(
            controls,
            text="Próximo",
            style="MenuButton.TButton",
            command=self._next_log,
        )
        self._next_button.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        self._main_menu_button = ttk.Button(
            controls,
            text="Voltar ao menu principal",
            style="MenuButton.TButton",
            command=self._on_main_menu,
        )
        self._main_menu_button.grid(row=0, column=2, sticky="ew")

    def _refresh_navigation(self) -> None:
        if self._finished:
            self._status_var.set("Cenário concluído. A única opção disponível é regressar ao menu principal.")
            self._previous_button.grid_remove()
            self._next_button.grid_remove()
            self._current_log_var.set(self._logs[-1] if self._logs else "Cenário concluído.")
            self._main_menu_button.state(["!disabled"])
            return

        self._current_log_var.set(self._logs[self._index])
        self._status_var.set(f"Log {self._index + 1} de {len(self._logs)}")

        if self._index == 0:
            self._previous_button.state(["disabled"])
        else:
            self._previous_button.state(["!disabled"])

        if self._index >= len(self._logs) - 1:
            self._next_button.state(["disabled"])
        else:
            self._next_button.state(["!disabled"])

    def _previous_log(self) -> None:
        if self._finished or self._index == 0:
            return

        self._index -= 1
        self._refresh_navigation()

    def _next_log(self) -> None:
        if self._finished:
            return

        if self._index < len(self._logs) - 1:
            self._index += 1

        if self._index >= len(self._logs) - 1:
            self._finished = True

        self._refresh_navigation()


class ScenarioExecutionErrorView(ttk.Frame):
    def __init__(
        self,
        owner: ttk.Frame,
        definition: ScenarioDefinition,
        error_message: str,
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(owner, style="MenuCard.TFrame", padding=(42, 36))
        self._definition = definition
        self._error_message = error_message
        self._on_back = on_back

        self._build_layout()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        title = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text=f"Erro ao executar - {self._definition.title}",
        )
        title.grid(row=0, column=0, sticky="n", pady=(10, 18))

        message = ttk.Label(
            self,
            style="MenuTitle.TLabel",
            text=self._error_message,
            font=("Segoe UI", 11),
            wraplength=760,
            justify="center",
        )
        message.grid(row=1, column=0, sticky="n", pady=(12, 12))

        ttk.Button(
            self,
            text="Voltar à configuração do cenário",
            style="MenuButton.TButton",
            command=self._on_back,
        ).grid(row=2, column=0, sticky="ew")

    def _next_log(self) -> None:
        if self._finished:
            return

        if self._index < len(self._logs) - 1:
            self._index += 1

        if self._index >= len(self._logs) - 1:
            self._finished = True

        self._refresh_navigation()



def main() -> None:
    app = SimulatorStartView()

    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        if app.winfo_exists():
            app.destroy()


if __name__ == "__main__":
    main()