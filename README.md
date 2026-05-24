
# Análise de Futebol TCC

Este repositório contém os notebooks e scripts utilizados para o Trabalho de Conclusão de Curso (TCC) focado na análise de dados de futebol.

## Scripts Úteis do Colab

### `tcc-commit-github.py`

Este script é projetado para automatizar o processo de commit e push de alterações para este repositório GitHub diretamente do ambiente Google Colab. Ele garante que seu repositório local esteja sempre sincronizado com o remoto antes de enviar novas alterações.

#### Funcionalidades:
1.  **Autenticação**: Puxa as credenciais (usuário, e-mail, token, nome do repositório) do Secrets do Colab para autenticação segura com o GitHub.
2.  **Navegação**: Altera o diretório de trabalho para a pasta raiz do repositório (`/content/tcc-futebol-analise`).
3.  **Configuração Remota**: Define a URL remota do Git com o token de acesso pessoal, concedendo permissões de escrita.
4.  **Configuração do Usuário Git**: Configura o `user.email` e `user.name` globalmente para os commits.
5.  **Sincronização (`git pull --rebase`)**: Antes de qualquer commit, executa `git pull --rebase` para buscar as últimas alterações do repositório remoto e aplicar seus commits locais sobre elas. Isso ajuda a evitar conflitos e mantém um histórico de commits limpo.
6.  **Mensagem de Commit Dinâmica**: Permite que você insira uma mensagem de commit personalizada através de uma caixa de diálogo no Colab. Se nenhuma mensagem for fornecida, uma mensagem padrão será usada.
7.  **Commit e Push**: Adiciona todas as alterações pendentes (`git add .`), realiza o commit com a mensagem especificada e, finalmente, empurra as alterações para a branch `main` do repositório remoto (`git push origin main`).

#### Como usar:
Para executar o script, basta chamá-lo em uma célula do seu notebook Colab:

```python
%run "/content/drive/MyDrive/Colab Notebooks/tcc-commit-github.py"
```

Certifique-se de que suas credenciais do GitHub (GITHUB_REPO, GITHUB_USER, GITHUB_EMAIL, GITHUB_TOKEN) estejam configuradas corretamente no Secrets do Colab.
