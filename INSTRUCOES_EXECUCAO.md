# Instruções de Execução do Projeto

Este projeto tem dois componentes:

- backend em .NET 8, compilado como biblioteca `Projeto.dll`
- frontend em Python/Tkinter, que carrega a DLL através de `pythonnet`

## Requisitos

- .NET SDK 8.0
- Python compatível com `pythonnet`
- Dependências Python instaladas a partir de `requirements.txt`

Nota prática: neste workspace, Python 3.12 funcionou com a ponte `clr`, enquanto Python 3.14 não carregou corretamente.

## Passos de Execução

### 1. Abrir a pasta do projeto

Na raiz do repositório:

```powershell
cd "c:\Users\filip\Desktop\Projeto\Repositório\LPEI_Filipe_Medeiros"
```

### 2. Ativar o ambiente virtual Python

Se existir o ambiente `.venv`, ative-o:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências Python

```powershell
pip install -r requirements.txt
```

### 4. Compilar o backend .NET

```powershell
dotnet build Projeto.sln
```

### 5. Iniciar a aplicação

O ponto de entrada do projeto é o frontend Python:

```powershell
python .\frontend\app.py
```

## O Que Acontece Ao Executar

- abre uma janela Tkinter com o simulador
- o frontend tenta carregar `bin\Debug\net8.0\Projeto.dll` ou `bin\Release\net8.0\Projeto.dll`
- os cenários geram logs na pasta `logs\`

## Problemas Comuns

### `Projeto.dll` não encontrado

O backend ainda não foi compilado. Execute:

```powershell
dotnet build Projeto.sln
```

### Erro ao importar `clr`

Normalmente indica que o `pythonnet` não está instalado ou que a versão de Python não é compatível com a ponte usada pelo projeto.

### O frontend não abre

Verifique se o Python ativo é o do ambiente correto e se a DLL foi gerada com sucesso.

## Documentação Relacionada

- [Guia de utilização](GUIA_UTILIZACAO.md)
- [Detalhes técnicos](DETALHES_TECNICOS.md)
