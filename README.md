# Events Sheet Updater Action

Esta GitHub Action analisa um arquivo `events.dart` de um projeto Flutter, extrai nomes e descrições de eventos de um `enum`, e atualiza uma planilha do Google Sheets com os novos eventos encontrados.

A action foi projetada para ser reutilizável, permitindo que qualquer repositório de projeto a utilize para manter uma documentação de eventos de analytics sempre atualizada e automatizada.

## Pré-requisitos

Antes de usar esta action, você precisa configurar a autenticação com a API do Google Sheets.

**1. Conta de Serviço do Google Cloud:**

 - Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
 - Ative a **API do Google Sheets** para o seu projeto.
 - Crie uma **Conta de Serviço** (em "IAM e Admin" > "Contas de Serviço").
 - Gere **uma chave JSON** para essa conta de serviço. O conteúdo deste arquivo JSON será usado como um secret no GitHub.

**2. Compartilhar a Planilha:**

 - Abra o arquivo JSON da conta de serviço e copie o valor de `client_email`.
 - Na sua planilha do Google Sheets, clique em **"Compartilhar"** e cole o email da conta de serviço, concedendo a ela permissão de **"Editor"**.

**3. Configurar Segredos do GitHub:**

 - No repositório do seu **projeto principal** (o que contém o `events.dart`), vá para `Settings > Secrets and variables > Actions`.
 - Crie os seguintes segredos:
 - `GCP_SA_KEY`: Cole **todo o conteúdo** do arquivo de chave JSON que você baixou do Google Cloud.
 - `SPREADSHEET_ID`: O ID da sua planilha. Você pode encontrá-lo na URL da planilha (`.../spreadsheets/d/ESTE_É_O_ID/edit...`).

## Entradas (Inputs)

Esta action aceita as seguintes entradas:

| Input                | Descrição                                                                               | Obrigatório |
|----------------------|-----------------------------------------------------------------------------------------|-------------|
| `events_file_path`   | O caminho para o arquivo `events.dart` no repositório que está usando a action.         | `true`      |

## Exemplo de Uso

Para usar esta action, crie um arquivo de workflow (ex: `.github/workflows/update_analytics_sheet.yml`) no repositório do seu projeto principal.

    # .github/workflows/update_analytics_sheet.yml

    name: Atualizar Planilha de Eventos de Analytics

    on:
    # Permite a execução manual pela aba "Actions"
    workflow_dispatch:

    # Dispara a action em pushes para a branch main que alterem o arquivo de eventos
    push:
        branches:
        - main
        paths:
        - '**/events.dart' # Ajuste o caminho conforme necessário

    jobs:
    update-sheet:
        runs-on: ubuntu-latest
        steps:
        # 1. Faz o checkout do código do seu projeto para que o arquivo de eventos esteja acessível
        - name: Checkout do Código do Projeto
            uses: actions/checkout@v4

        # 2. Executa a action para analisar o arquivo e atualizar a planilha
        - name: Parse Events and Update Sheet
            uses: SEU_USUARIO_OU_ORG/SEU_REPO_DE_SCRIPTS@main # <-- SUBSTITUA PELO SEU REPO
            with:
            # Informa à action onde encontrar o arquivo de eventos
            events_file_path: './Konsi/lib/src/core/enumerators/analytics/events.dart' # <-- AJUSTE O CAMINHO
            env:
            # Passa os segredos necessários para a action
            GCP_SA_KEY: ${{ secrets.GCP_SA_KEY }}
            SPREADSHEET_ID: ${{ secrets.SPREADSHEET_ID }}

## Estrutura deste Repositório

    .
    ├── action.yml          # Arquivo de metadados que define a GitHub Action.
    ├── events_to_table.py  # Script principal que executa a lógica de parsing.
    ├── sheets.py           # Módulo que lida com a autenticação e comunicação com a API do Sheets.
    └── requirements.txt    # Lista de dependências Python.


