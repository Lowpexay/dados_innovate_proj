# dados_innovate_proj

Este é o repositório do projeto **dados_innovate_proj**.

## Descrição

O projeto **dados_innovate_proj** é uma iniciativa para coletar, analisar e visualizar dados relacionados ao projeto InnovateIT do challenge da Fiap 2024. O objetivo é fornecer insights valiosos e informações relevantes para impulsionar gestão da empresa GTX Tecnologia.

## Funcionalidades

- Coleta de dados: O projeto possui um mecanismo de coleta de dados automatizado que busca informações relevantes em diversas fontes.
- Análise de dados: Os dados coletados são processados e analisados para identificar padrões, tendências e insights.
- Visualização de dados: Os resultados da análise são apresentados de forma visualmente atraente e intuitiva, facilitando a compreensão e interpretação dos dados.

## Como executar

Para executar o projeto **dados_innovate_proj**, siga as etapas abaixo:

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone este repositório em sua máquina local.

3. Instale as dependências do projeto:
    ```
    pip install -r requirements.txt
    ```
4. Execute o arquivo via streamlit `streamlit run app.py`:


## O que o app.py faz

O arquivo `app.py` é o ponto de entrada do projeto **dados_innovate_proj**. Ele contém a lógica principal para coletar, analisar e visualizar os dados relacionados à inovação. Aqui está uma visão geral das principais funcionalidades do arquivo:

- Importação de bibliotecas: O arquivo `app.py` importa as bibliotecas necessárias para o projeto, como pandas, matplotlib e requests.

- Coleta de dados: O código no arquivo `app.py` implementa um mecanismo de coleta de dados automatizado. Ele utiliza a biblioteca requests para fazer requisições a diversas fontes de dados e obter as informações relevantes.

- Processamento e análise de dados: Após a coleta dos dados, o arquivo `app.py` utiliza a biblioteca pandas para processar e analisar os dados. Ele identifica padrões, tendências e insights por meio de técnicas de análise de dados.

- Visualização de dados: O arquivo `app.py` utiliza a biblioteca matplotlib para criar visualizações gráficas dos dados analisados. Ele gera gráficos e plots que facilitam a compreensão e interpretação dos insights obtidos.

- Execução do aplicativo: Por fim, o arquivo `app.py` executa o aplicativo, chamando as funções necessárias para coletar, analisar e visualizar os dados. Ele exibe os resultados no console ou em uma interface gráfica, dependendo da implementação específica.

## Arquivos adicionais

Além do arquivo `app.py`, o projeto **dados_innovate_proj** também possui os seguintes arquivos:

- `clientes.xlsx`: Este arquivo é utilizado para armazenar os dados dos clientes coletados pelo projeto. Ele é atualizado a cada execução do `app.py`.

- `gastos.xlsx`: Este arquivo é utilizado para armazenar os dados sobre os gastos coletados pelo projeto. Ele é atualizado a cada execução do `app.py`.

- `requirements.txt`: Este arquivo lista as dependências do projeto. É utilizado pelo comando `pip install -r requirements.txt` para instalar as bibliotecas necessárias.

## Contribuição

Se você deseja contribuir para o projeto **dados_innovate_proj**, siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie uma branch com o nome descritivo da sua contribuição.
3. Faça as alterações desejadas.
4. Envie um pull request para revisão.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).