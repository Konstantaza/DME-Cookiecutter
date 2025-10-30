# Data Management Engineering

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Этот репозиторий содержит основной ETL-пайплайн для извлечения, трансформации и загрузки данных.

## Набор данных

![Микробиом растений](Plant_microbiome.jpg)


Этот ETL-пайплайн обрабатывает набор данных метабаркодинга генов 16S и ITS2, связанных с анализом микробного разнообразия озимых зерновых культур (рожь, пшеница и тритикале). Понимание микробного разнообразия растений позволит в будущем манипулировать составом их микробиома для повышения урожайности и устойчивости к неблагоприятным факторам среды сельскохозяйственных культур. Наобор данных был получен из лаборатории инфекционных заболеваний растений КИББ Фиц КазНЦ РАН, образцы были секвенированы на Illumina MiSeq.

Данные состоят из нескольких файлов, включая таблицы подсчета ASV (Amplicon Sequence Variants), таксономическую классификацию и метаданные образцов.

---

## Источник данных

Все исходные "сырые" данные для этого проекта хранятся на Google Drive.

**Ссылка на Google Drive:** [https://drive.google.com/drive/folders/1Azl5tjFB47B9aBVfpBObkG4WG7ohekdS?usp=sharing](https://drive.google.com/drive/folders/1Azl5tjFB47B9aBVfpBObkG4WG7ohekdS?usp=sharing)

---

## Основной ETL-пайплайн

Пакет `etl` представляет собой конвейер для извлечения, трансформации и загрузки набора геномных данных.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         etl and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── etl   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes etl a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

### Инструкция по запуску

Для запуска полного ETL-процесса необходимо:

Для запуска пайплайна необходимо сначала настроить окружение, а затем запустить сам скрипт.

#### Запуск ETL

```bash
# 1. Клонируйте этот репозиторий
git clone git@github.com:Konstantaza/Data-management-Engineering.git
cd DME-Cookiecutter

# 2. Создайте окружение conda (например, data_eng)
conda create -n data_eng python=3.13 pip
conda activate data_eng

# 3. Установите Poetry
pip install poetry

# 4. Установите все зависимости проекта
poetry install

# 5. Запустите полный ETL-процесс
poetry run python -m etl.main --step all

    # Только извлечение
    poetry run python -m etl.main --step extract

    # Только трансформация
    poetry run python -m etl.main --step transform

    # Только загрузка
    poetry run python -m etl.main --step load

```

### Дополнительные примеры
В папке `my_project/archive` находятся дополнительные скрипты, демонстрирующие:
1. `api_example`: Пример работы с API (получение данных о шутках).
2. `parse_example`: Пример парсинга HTML-таблиц с веб-страниц.