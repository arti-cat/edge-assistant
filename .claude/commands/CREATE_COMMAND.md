You are an experienced software developer. Your task is to create a new scraper for the product-prices tool.

## 1. READ THE ARCHITECTURE DOCUMENTATION

To understand the system architecture and how to build a new scraper, read the following documentation:

- `docs/architecture.md`: Provides a high-level overview of the project's architecture.
- `docs/scrapers.md`: Details the scraper-specific architecture and the base classes.

## 2. CREATE THE SCRAPER

1.  Create a new Python file in `src/product_prices/scrapers/`. The filename should be the name of the new scraper, e.g., `new_scraper.py`.
2.  In this file, define a new class that inherits from one of the base scraper classes defined in `src/product_prices/scrapers/base.py`.
3.  Implement the required methods in your new scraper class. You can use the existing scrapers as a reference.

## 3. INTEGRATE THE SCRAPER INTO THE CLI

1.  Open `src/product_prices/cli.py`.
2.  Import your new scraper class.
3.  Create a new function to run your scraper. This function should instantiate your scraper class and call its `main` method.
4.  Add a new command to the `main` function to trigger your new scraper function. This will make it accessible via the CLI.

## 4. ADD TESTS

1.  Create a new test file in the `tests/` directory. The filename should be `test_` followed by the name of your scraper, e.g., `test_new_scraper.py`.
2.  Write unit tests for your new scraper to ensure it functions correctly.

## 5. UPDATE DOCUMENTATION

1.  Open `docs/cli-usage.md`.
2.  Add a new section documenting the command for your new scraper, including a description and example usage.

By following these steps, you will have successfully created and integrated a new scraper into the product-prices tool.
