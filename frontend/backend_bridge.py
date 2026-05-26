from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class FrontendMetadata:
    title: str
    subtitle: str
    start_button_text: str
    ready_message: str


@dataclass(frozen=True)
class ScenarioExecutionResult:
    log_path: str
    logs: list[str]
    summary: str


class BackendBridgeError(RuntimeError):
    pass


class BackendBridge:
    def __init__(self) -> None:
        self._dll_path = self._resolve_dll_path()

    def _resolve_dll_path(self) -> Path:
        root = Path(__file__).resolve().parents[1]
        candidates = [
            root / "bin" / "Debug" / "net8.0" / "Projeto.dll",
            root / "bin" / "Release" / "net8.0" / "Projeto.dll",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        raise BackendBridgeError(
            "Nao foi possivel encontrar o assembly C# Projeto.dll. "
            "Execute primeiro `dotnet build Projeto.sln`."
        )

    def _load_bridge_type(self):
        try:
            import clr  # type: ignore[import-not-found]
        except ImportError as exc:
            raise BackendBridgeError(
                "A biblioteca pythonnet nao esta instalada. Instale os requisitos do frontend."
            ) from exc

        dll_dir = str(self._dll_path.parent)
        if dll_dir not in sys.path:
            sys.path.append(dll_dir)

        clr.AddReference(str(self._dll_path))

        from Projeto.Backend import ConcurrentSimulationBridge  # type: ignore[import-not-found]

        return ConcurrentSimulationBridge

    def get_metadata(self) -> FrontendMetadata:
        bridge_type = self._load_bridge_type()
        metadata = bridge_type.GetFrontendMetadata()
        return FrontendMetadata(
            title=str(metadata.Title),
            subtitle=str(metadata.Subtitle),
            start_button_text=str(metadata.StartButtonText),
            ready_message=str(metadata.ReadyMessage),
        )

    def initialize_session(self) -> str:
        bridge_type = self._load_bridge_type()
        return str(bridge_type.InitializeSession())

    def execute_scenario(self, scenario_key: str, values: list[int], log_path: str) -> ScenarioExecutionResult:
        bridge_type = self._load_bridge_type()
        execution_result = bridge_type.ExecuteScenario(scenario_key, values, log_path)

        return ScenarioExecutionResult(
            log_path=str(execution_result.LogPath),
            logs=[str(log_entry) for log_entry in execution_result.Logs],
            summary=str(execution_result.Summary),
        )