### Install
```
git clone github.com/drlinggg/my-django-project
cd my-django-project
```

### Build & Run
1. create .env from example.env and replace some variables 
```
mv example.env .env

# generate new django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# change SECRET_KEY="SECRET_KEY"
```
2. choose to build & run via docker or natively
```
docker compose up --build
```
```
# via poetry
poetry install --no-root
poetry run python manage.py runserver 8000

# via pip
pip install -r requirements.txt
python manage.py runserver 8000
```

