# Ambiente

Toda a aplicação foi desenvolvida utilizando a distribuição mint do linux na versão 20.

### Documentação

A documentação pode ser acessada em:

http://localhost:8000/docs/
http://localhost:8000/redoc/

## Desenvolvimento

### Requisitos
- python v3.8.5
- Make [Opcional]
> Foi utilizado um Makefile para facilitar a execução de comando
> repetitivos no sistema, é perfeitamente possível desenvolver se ele,
> executando manualmente os comandos descritos no arquivo.

```sh
# Testes
make test # Executa todos os testes da aplicação
make test-match Q=<filtro-de-teste> # Executa os testes que batem com o filtro informado
make test-coverage # Análise de cobertura de código da aplicação

# Utilitários
make clean # Limpa todos os arquivos gerados pela execução da aplicação/testes
make lint # Análise de guia de estilo do código
make format # Formata o código para se adequar ao guia de estilo
make safety # Análise de segurança dos pacotes utilizados

# Execução
make install # Instala todas as dependências de devolvimento da aplicação
make webapi-dev # Inicia um servidor local de desenvolvimento (Requer uma instância de mongodb em execução)
make webapi # Cria uma imagem docker da aplicação e a executa (Nesse cenário o mongodb já é providenciado pelo docker-compose)
```

### Requisitos
- docker
- docker-compose
> A aplicação está preparada para execução em containers, tornando mais simples a execução futura em um gerenciador de container como kubernetes.

# Requisitos de negócio

- [x] Deve ser possível criar, atualizar, visualizar e remover Clientes
- [x] O cadastro dos clientes deve conter apenas seu nome e endereço de e-mail
- [x] Um cliente não pode se registrar duas vezes com o mesmo endereço de e-mail
- [x] Cada cliente só deverá ter uma única lista de produtos favoritos
- [x] Em uma lista de produtos favoritos podem existir uma quantidade ilimitada de produtos
- [x] Um produto não pode ser adicionado em uma lista caso ele não exista
- [x] Um produto não pode estar duplicado na lista de produtos favoritos de um cliente
- [x] O dispositivo que irá renderizar a resposta fornecida por essa nova API irá apresentar o Título, Imagem, Preço e irá utilizar o ID do produto para formatar o link que ele irá acessar. Quando existir um review para o produto, o mesmo será exibido por este dispositivo.
- [ ] O acesso à api deve ser aberto ao mundo, porém deve possuir autenticação e autorização.

# Notas

## Autenticação/Autorização
Autenticação/autorização no escopo de aplicação dificulta demais a integração entre sistemas já que cada aplicação se autentica de um forma diferente e as bases de usuários/permissões dificilmente são pareadas.

Apesar de ser uma prática comum, pensando em um cenário de grande escala, seria mais indicável unificar essa responsabilidade, com algum provedor de sso como o keycloak.