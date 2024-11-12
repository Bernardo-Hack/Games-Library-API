# GamesLibraryAPI (Back End Project)

Projeto desenvolvido para disciplina de Back-end: Web Services.

Este API conta com 2 classes (Publisher e Game) implementadas com um relacionamento Many to Many (M2M), com um jogo podem ter uma ou mais distribuidoras e uma distribuidora pode ter um ou mais jogos.

Operações implementadas:
- CRUD completo
- Busca de Jogos de uma Distribuidora escolhida
- Busca de Jogos por gênero escolhido
- Busca de Distribuidoras em um país escolhido

O API também conta com logs para todas operações, tratamento de exceções, testes unitários para quase todas funções, teste unitários para os 2 modelos, implementação do Swagger e validação de dados.

Para instalar as dependências:

```bash
    pip install -r requirements.txt
```

Para iniciar o servidor:

```bash
    python GamesLibrary/manage.py runserver
```

Para executar os testes:

```bash
    python GamesLibrary/manage.py test GamesLibrary/Games/tests 
```

## Author

- [@Bernardo-Hack](https://www.github.com/Bernardo-Hack)

