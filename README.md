1.Set Up a Virtual Environment
  python -m venv venv
2. Activate the Virtual Environment
  venv\Scripts\Activate
3. Install Dependencies
	1.pip install --upgrade pip
  2.pip install django djangorestframework django-cors-headers
  3.pip freeze > requirements.txt
4 Database Connection
		1.Create MySql db
		2.Configuration in our project (settings.py file)
			DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'KICKOFF',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',  
        'PORT': '3306',       
    }
}
5. Makemigartions
		Python manage.py makemigrations
6. Migrate DB
		Python manage.py migrate
