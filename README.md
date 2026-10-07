# TASKUNI

Sistema acadêmico desenvolvido em Python para auxiliar estudantes na organização de disciplinas, conteúdos, tarefas e estudos.

O projeto está sendo desenvolvido como atividade da disciplina de **Laboratório de Programação**, utilizando programação estruturada e organização modular.

## Funcionalidades atuais

O sistema possui, atualmente:

### Disciplinas
- cadastrar disciplina;
- listar disciplinas;
- atualizar disciplina;
- remover disciplina.

### Conteúdos
- cadastrar conteúdos vinculados a disciplinas;
- listar conteúdos;
- atualizar conteúdos;
- remover conteúdos.

### Tarefas
- cadastrar tarefas acadêmicas ou pessoais;
- vincular opcionalmente tarefas acadêmicas a disciplinas;
- listar tarefas;
- filtrar por status;
- editar tarefas;
- concluir tarefas;
- reabrir tarefas;
- calcular prioridade;
- identificar tarefas atrasadas;
- identificar tarefas próximas do prazo.

## Organização do projeto

```text
TASKUNI/
│
├── main.py
│
├── src/
│   ├── academico/
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   └── avaliacoes.py
│   │
│   ├── estudos/
│   │   ├── sessoes.py
│   │   ├── metas.py
│   │   └── gamificacao.py
│   │
│   ├── interface/
│   │   ├── menu_principal.py
│   │   ├── menu_disciplinas.py
│   │   ├── menu_conteudos.py
│   │   └── menu_tarefas.py
│   │
│   ├── persistencia/
│   │   ├── _armazenamento.py
│   │   ├── disciplinas.py
│   │   ├── conteudos.py
│   │   ├── tarefas.py
│   │   ├── avaliacoes.py
│   │   ├── sessoes_estudo.py
│   │   └── metas.py
│   │
│   └── sistema/
│       ├── analise_tarefas.py
│       └── validacoes.py
│
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Responsabilidade das camadas

O projeto foi dividido em módulos para evitar concentração de lógica em um único arquivo.

### `main.py`

É o ponto de entrada da aplicação.

Sua responsabilidade é apenas iniciar o sistema e chamar o menu principal.

### `src/interface`

Responsável pela interação com o usuário no terminal.

Contém:

- menus;
- `input()`;
- `print()`;
- leitura das opções escolhidas pelo usuário;
- apresentação dos resultados.

A interface não deve implementar regras de negócio nem acessar arquivos JSON diretamente.

### `src/academico`

Contém as regras relacionadas à parte acadêmica do sistema.

Exemplos:

- validação de disciplinas;
- validação de conteúdos;
- criação e edição de tarefas;
- regras de status;
- filtros e consultas relacionadas às tarefas.

### `src/estudos`

Responsável pelas funcionalidades relacionadas ao estudo do usuário.

Exemplos previstos:

- sessões de estudo;
- metas;
- gamificação.

### `src/persistencia`

Responsável pelo armazenamento e recuperação dos dados.

Os módulos dessa pasta realizam operações como:

- adicionar;
- buscar;
- listar;
- atualizar;
- remover;
- salvar.

O módulo `_armazenamento.py` concentra operações comuns de leitura e escrita dos arquivos JSON.

### `src/sistema`

Contém funcionalidades compartilhadas ou de análise que não pertencem diretamente à interface ou à persistência.

Atualmente inclui a análise das tarefas, como:

- cálculo de prioridade;
- cálculo de urgência;
- identificação de tarefas atrasadas;
- identificação de tarefas próximas do prazo.

## Fluxo da aplicação

De forma geral, o sistema segue o fluxo:

```text
Usuário
   ↓
Interface
   ↓
Domínio
   ↓
Persistência
   ↓
Arquivos JSON
```

Exemplo para tarefas:

```text
menu_tarefas.py
        ↓
academico/tarefas.py
        ↓
persistencia/tarefas.py
        ↓
persistencia/_armazenamento.py
        ↓
tarefas.json
```

As análises de prioridade e prazo ficam separadas em:

```text
sistema/analise_tarefas.py
```

## Persistência

Os dados são armazenados em arquivos JSON.

Cada tipo de informação possui sua própria coleção, como:

```text
disciplinas.json
conteudos.json
tarefas.json
avaliacoes.json
metas.json
sessoes_estudo.json
```

Esses arquivos são gerados durante a execução do sistema e não precisam ser versionados no Git.

## Executando o projeto

Na raiz do projeto, execute:

```bash
python main.py
```

O menu principal será exibido:

```text
=== TASKUNI ===
1 - Disciplinas
2 - Conteúdos
3 - Tarefas
0 - Sair
```

## Tecnologias utilizadas

- Python
- JSON
- Git
- GitHub

O projeto utiliza apenas recursos compatíveis com os conteúdos estudados na disciplina, priorizando uma implementação simples e compreensível.

## Desenvolvimento colaborativo

A branch utilizada para integração durante o desenvolvimento é:

```text
develop
```

A branch:

```text
main
```

é reservada para a versão estável/final do projeto.

Antes de iniciar uma nova funcionalidade:

```bash
git switch develop
git pull origin develop
git switch -c feature/nome-da-funcionalidade
```

Após concluir a funcionalidade, ela deve ser integrada novamente à `develop`.

## Padrão de branches

Exemplos:

```text
feature/avaliacoes
feature/metas
feature/gamificacao
feature/dashboard
```

## Padrão de commits

O projeto utiliza commits descritivos, como:

```text
feat: adiciona cadastro de tarefas
fix: corrige validacao de prazo
refactor: organiza camada de interface
test: adiciona testes de tarefas
docs: atualiza documentacao do projeto
chore: atualiza configuracoes do repositorio
```

## Regras importantes para colaboração

Ao desenvolver novas funcionalidades:

- não colocar lógica de negócio dentro dos menus;
- não manipular arquivos JSON diretamente fora da camada de persistência;
- evitar alterar arquivos de outras funcionalidades sem necessidade;
- atualizar a `develop` antes de criar uma nova branch;
- testar a funcionalidade antes de enviar;
- evitar commits diretamente na `main`;
- manter as responsabilidades dos módulos existentes.

## Status do projeto

Em desenvolvimento.

Funcionalidades já integradas:

- disciplinas;
- conteúdos;
- tarefas;
- persistência em JSON;
- prioridade de tarefas;
- alertas de atraso e proximidade de prazo.

Funcionalidades ainda em desenvolvimento podem incluir:

- avaliações;
- sessões de estudo;
- metas;
- gamificação;
- análises adicionais;
- dashboard.
