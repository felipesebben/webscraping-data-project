# Instructions #

## Installation and Setup ##
1. Clone the repo.
```bash
git clone https://github.com/felipesebben/webscraping-data-project.git
cd webscraping-data-project
```

2. Configure the correct Python version with `pyenv`. If you don't have it installed, make sure you have the right Python version in your machine (`3.11.5`).
```bash
pyenv install 3.11.5
pyenv local 3.11.5
```

3. Install the project dependencies. This project used `poetry`:
```bash
# install dependencies
poetry install
# run the created environment
poetry shell
```

4. To run the tests:
```bash
task test
```

5. To run the app:
```bash
task run
```
If you want to see the automation working pass the argument `headless` as `False`.

```python
# app/etl/extract.py
def extract():
    """
    Main function to run the extraction process.
    """
    # Pass argument as false. Default is True
    scraper = WebScraper(headless=False)
```
