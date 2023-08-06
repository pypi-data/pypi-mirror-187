# Projeto: Pacote para Converter Dataframes em Script SQL
## Autora do Projeto: Francisco Fádio
[(clique aqui para ver o meu perfil na plataforma)](https://github.com/franciscofabio)
#### Tecnologia: Python | SQL
#### Data: 22/01/2023
-----------------------------------------
### Descrição
O pacote "df_to_sql" é usado para:

- Módulo "converter":
  - possui a função converter_df_in_sql que com os.mkdir('SCRIPTS')
  - a função recece como parametro 3 variaveis:
    - df -> nome do dataframe.
    - tb_name -> nome da tabela do banco sql.
    - name_script -> nome do arquivo
  - cria a pasta para saída dos scripts sql
  - Atraves de for adiciona '' nas colunas do tipo object 'categorias'

---------------------------------------------
## Passo a passo da configuração para hospedar um pacote em Python no ambiente de testes Test Pypi

- [x] Instalação das últimas versões de "setuptools" e "wheel"

```
python -m pip install --user --upgrade setuptools wheel
```
- [x] Tenha certeza que o diretório no terminal seja o mesmo do arquivo "setup.py"

```
python setup.py sdist bdist_wheel
```

- [x] Após completar a instalação, verifique se as pastas abaixo foram adicionadas ao projeto:
  - [x] build;
  - [x] dist;
  - [x] image_processing_test.egg-info.

- [x] Basta subir os arquivos, usando o Twine, para o Test Pypi:

```
py -m twine upload --repository testpypi dist/*
```

- [x] Após rodar o comando acima no terminal, será pedido para inserir o usuário e senha. Feito isso, o projeto estará hospedado no Test Pypi.hospedá-lo no Pypi diretamente.

### Aqui o objetivo não é disponibilizar um pocote simplis mas que solucionou um problema real para mim e acredito que possa solucionar problemas com outros dataframes.
----------------------------------------------------
## Instalação local, após hospedagem no Test Pypi

- [x] Instalação de dependências
```
pip install -r requirements.txt
```

- [x] Instalção do Pacote

Use o gerenciador de pacotes ```pip install -i pip install -i https://test.pypi.org/simple/ image-processing-package-myPy ```para instalar image-processing-package-myPy

```bash
pip install image-processing-package-myPy
```
-------------------------------------------------
## Como usar em qualquer projeto

```python
from image-processing-package-myPy.processing import combination
combination.find_difference(image1, image2)
```


## Autor:
Francisco Fábio de Almeida Ferreira

