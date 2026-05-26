namespace Projeto.Backend;

public sealed class FrontendMetadata
{
    public FrontendMetadata(string title, string subtitle, string startButtonText, string readyMessage)
    {
        Title = title;
        Subtitle = subtitle;
        StartButtonText = startButtonText;
        ReadyMessage = readyMessage;
    }

    public string Title { get; }

    public string Subtitle { get; }

    public string StartButtonText { get; }

    public string ReadyMessage { get; }
}

public static class ConcurrentSimulationBridge
{
    public static FrontendMetadata GetFrontendMetadata()
    {
        return new FrontendMetadata(
            "Simulador Interativo de Programação Concorrente",
            "Frontend em Python com backend em C# ligado por biblioteca .NET.",
            "Iniciar",
            "Backend C# carregado com sucesso. Pronto para iniciar o simulador.");
    }

    public static string InitializeSession()
    {
        FrontendMetadata metadata = GetFrontendMetadata();
        return metadata.ReadyMessage;
    }
}