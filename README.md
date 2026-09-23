# ViaCEP Dashboard

Dashboard desktop em Python para consultar CEPs e buscar endereços brasileiros com uma interface moderna e intuitiva.

O projeto utiliza a API pública do ViaCEP para consultar informações como rua, bairro, cidade, UF, DDD e IBGE de forma rápida e prática.

##  Funcionalidades

- Consulta de CEP individual
- Busca por endereço: UF, cidade e logradouro
- Histórico de consultas na sessão atual
- Estatísticas de uso e estados consultados
- Interface moderna com tema visual personalizado
- Compatibilidade com Windows

##  Tecnologias

- Python 3
- CustomTkinter
- ViaCEP API

##  Estrutura do projeto

```text
viacep/
├── main.py
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   └── viacep.py
│   └── ui/
│       ├── dashboard.py
│       ├── theme.py
│       └── __init__.py
└── README.md
```

##  Requisitos

- Python 3.9 ou superior
- pip

##  Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/viacep.git
cd viacep
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
```

3. Ative o ambiente virtual:

- Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

- Windows (CMD):

```cmd
.venv\Scripts\activate.bat
```

4. Instale as dependências:

```bash
pip install customtkinter
```

##  Como executar

No diretório do projeto, execute:

```bash
python main.py
```

##  Como usar

- Na tela inicial, informe um CEP para realizar a consulta.
- Na aba "Buscar endereço", informe UF, cidade e logradouro.
- O histórico ficará disponível para consulta rápida.

##  Observações

Este projeto utiliza a API pública do ViaCEP, que pode exigir conexão com a internet para funcionar corretamente.

##  Contribuição

Contribuições são bem-vindas. Se quiser melhorar a interface, adicionar filtros, exportação de dados ou outros recursos, fique à vontade para abrir uma pull request.

##  Licença

Este projeto está sob licença MIT. Você pode usar, modificar e distribuir livremente.

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

##  Status do projeto

Projeto em desenvolvimento e pronto para uso local como ferramenta de consulta de CEP.
