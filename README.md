# Search Engine

Esse repositório possui um código de um motor de busca simples, que dado um termo de busca, retorna uma lista de URL's que possuem esse termo. Para realizar a busca, deve ser construido o index dado uma URL inicial.
___
This repository contains the code of a simple search engine that, given a search phrase, returns a list of URLs representing this term. To perform the search, it is necessary to create a initial index based on a initial URl

## Dependencies

A única bibliteca necessária é PyQt5 se quiser utilizar a GUI. Para instalar basta:
```bash
pip install PyQt5
```
___

The only required library is PyQt5 if you wish to use GUI. To install it, just run:
```bash
pip install PyQt5
```

## Usage

Antes de realizar a busca, deve ser construído o index dado uma URL, para construí-lo deve ser feito:

1) Alterar no arquivo `web_scrapping.py` a variável `url`:
```python
url = 'https://site.com'
```

2) Executar o arquivo `web_scrapping.py`:
```bash
python web_scrapping.py
```

3) Executar o arquivo `make_index.py`:
```bash
python make_index.py
```

4) Se quiser simplesmente realizar uma busca no terminal, basta executar:
```bash
python search.py [termo 1] [termo 2]...
```
Por exemplo:
```bash
python search.py comida de gato
```

5) Se quiser iniciar a interface de busca, basta executar:
```bash
python gui.py
```
___

Before performing the search, the index must be built given a URL, to build it the following steps should be done:

1) Modify the url variable in the `web_scrapping.py` file::
```python
url = 'https://site.com'
```

2) Run the `web_scrapping.py` file:
```bash
python web_scrapping.py
```

3) Run the `make_index.py` file:
```bash
python make_index.py
```

4) If you wish to perform a search in terminal, just execute:
```bash
python search.py [term 1] [term 2]...
```
For example:
```bash
python search.py cat food
```

5) If you wish to start the search interface, just execute:
```bash
python gui.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)