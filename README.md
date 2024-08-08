# Pokedex

## Getting started
Use the Advanced Search to explore Pokémon by type, weakness, Ability, and more! Search for a Pokémon by name.

### Versions
Pokedex runs on Python 3.13.* and Django 5.0.7.



### Virtual Environment
Create and activate the virtual environment, and install the required packages.

- Create the virtual environment.
  ``` 
  python -m venv env
  ```

- Activate the virtual environment.
  - For bash (Linux):
    ```
    source env/bin/activate 
    ```
  - For console (Windows):
    ```
    .\env\Scripts\activate
    ```
- Install the required packages.
  ```
  pip install -r requirements.txt
  ```
- Run Migrations
  ```
  sh migrate.sh
  ``` 


### Preloaded data to execute
This are the scripts needed to run.
```
python manage.py populate_pokedex 
```


### Unit testing
```
python manage.py test app_web
python manage.py test app_pokemon
```


### Run Project
  ```
  python manage.py runserver
  ``` 
  
### URL Access
```
Login page - http://127.0.0.1:8000
Redocs - http://127.0.0.1:8000/docs/schema/redoc/
Swagger - http://127.0.0.1:8000/docs/schema/swagger-ui/
```
 

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`
