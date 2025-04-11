# lab-4-boletos

Este projeto implementa um serviço de autenticação de boletos utilizando Python, Flask e MongoDB. Ele permite gerar boletos simplificados, validar códigos de barras e armazenar/consultar informações dos boletos em um banco de dados NoSQL.

## Funcionalidades

* **Geração de Boletos:** Permite criar registros de boletos com valor, data de vencimento, pagador e beneficiário (opcionais). Um código de barras simples é gerado.
* **Validação de Código de Barras:** Valida o formato básico de um código de barras.
* **Armazenamento:** Persiste as informações dos boletos em um banco de dados MongoDB.
* **Consulta:** Permite verificar a validade de um boleto através do seu código de barras.
* **API REST:** Exponha funcionalidades através de endpoints HTTP utilizando Flask.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flask:** Microframework web para construir a API.
* **PyMongo:** Driver oficial do MongoDB para Python.
* **MongoDB:** Banco de dados NoSQL para armazenamento dos boletos.

## Pré-requisitos

* **Python 3.x** instalado no seu sistema.
* **pip** (gerenciador de pacotes do Python) instalado.
* **MongoDB** instalado e rodando na sua máquina (ou acesso a uma instância remota).

## Instalação

1.  **Clone o repositório (opcional, se você já tem o código):**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_PROJETO>
    ```

2.  **Instale as dependências:**
    ```bash
    pip install Flask pymongo
    ```

3.  **Configure o MongoDB:**
    * Certifique-se de que o MongoDB esteja rodando.
    * O URI de conexão padrão está definido na classe `Config` (`mongodb://localhost:27017/boletos_db`). Se necessário, ajuste a variável `MONGO_URI` no arquivo do seu código Python.

## Execução

1.  **Execute o serviço Flask:**
    ```bash
    python <nome_do_arquivo>.py
    ```
    (Substitua `<nome_do_arquivo>.py` pelo nome do arquivo principal do seu projeto, por exemplo, `servico_autenticador_boletos.py`).

2.  **Acesse os endpoints da API:** O serviço estará disponível por padrão em `http://127.0.0.1:5000`.

## Endpoints da API

* **`POST /gerar`:**
    * **Descrição:** Gera um novo boleto e o armazena no banco de dados.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "valor": 100.50,
            "data_vencimento": "2025-05-15",
            "pagador": "Nome do Pagador (opcional)",
            "beneficiario": "Nome do Beneficiário (opcional)"
        }
        ```
    * **Resposta (JSON - Sucesso - Status 201):**
        ```json
        {
            "id": "<ID_DO_BOLETO_NO_MONGODB>",
            "codigo_barras": "<CODIGO_DE_BARRAS_GERADO>"
        }
        ```
    * **Resposta (JSON - Erro - Status 400):**
        ```json
        {
            "erro": "<Mensagem de erro>"
        }
        ```

* **`POST /validar`:**
    * **Descrição:** Valida um código de barras e verifica se o boleto existe no banco de dados.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "codigo": "<CODIGO_DE_BARRAS_A_VALIDAR>"
        }
        ```
    * **Resposta (JSON - Boleto Válido e Encontrado - Status 200):**
        ```json
        {
            "valido": true,
            "boleto": {
                "codigo_barras": "<CODIGO_DE_BARRAS>",
                "valor": <VALOR_DO_BOLETO>,
                "data_vencimento": "<DATA_DE_VENCIMENTO>",
                "status": "<STATUS_DO_BOLETO>"
                // Outros campos do boleto
            }
        }
        ```
    * **Resposta (JSON - Código Inválido - Status 400):**
        ```json
        {
            "valido": false,
            "mensagem": "Código de barras inválido."
        }
        ```
    * **Resposta (JSON - Boleto Não Encontrado - Status 404):**
        ```json
        {
            "valido": false,
            "mensagem": "Boleto não encontrado."
        }
        ```

## Observações e Melhorias Futuras

* **Lógica de Geração de Código de Barras:** A geração de código de barras atualmente é simplificada. Em um cenário real, seria necessário implementar a lógica específica de cada banco, incluindo dígitos verificadores e formatação detalhada.
* **Validação de Código de Barras:** A validação do código de barras é básica. Uma validação completa envolveria a verificação dos dígitos verificadores e a estrutura completa do código.
* **Segurança:** Considerar a implementação de mecanismos de segurança como autenticação e autorização para proteger a API.
* **Tratamento de Erros:** Melhorar o tratamento de erros para fornecer mensagens mais informativas.
* **Testes Unitários:** Adicionar testes unitários para garantir a robustez e a qualidade do código.
* **Configuração:** Utilizar variáveis de ambiente para configurações sensíveis como a URI do MongoDB.
* **Atualização de Status:** Adicionar endpoints para atualizar o status de um boleto (por exemplo, para "pago").

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests com melhorias, correções de bugs ou novas funcionalidades.

## Licença

MIT License