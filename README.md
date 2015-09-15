# vallejo-css-toolkit
Intake and manage reports of nuisance properties.

### Getting Started

Check out repository:
```
git clone git@github.com:codeforamerica/vallejo-css-toolkit.git
cd vallejo-css-toolkit
```

Create virtual environment:
```
virtualenv env
```

Define Twilio auth variables:
If needed, create an account [here](https://www.twilio.com/try-twilio).

Add the following to `env/bin/activate`:
```
export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
export TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXX
```

Activate environment and install dependencies:
```
source env/bin/activate
pip install -r requirements.txt
```

Set the Django settings module:
```
export DJANGO_SETTINGS_MODULE=vallejo_css_toolkit.development
```

The development and test environments use Postgres. If you're on OS X, it's recommended to install it with the [Postgres App](http://postgresapp.com/). You'll also need to configire your `$PATH`, using your version of psql, e.g.:
```
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin
```

Create the database and role:
```
psql -c 'CREATE DB vallejo_css_toolkit; CREATE ROLE vallejo_css_toolkit WITH LOGIN;'

```

Set up Django base tables:
```
python manage.py syncdb
```

Apply migrations:
```
python manage.py migrate
```

Launch an instance locally:
```
python manage.py runserver
```

####Running tests
Allow the default user to create a test database (one-time setup):
```
psql -c 'ALTER ROLE vallejo_css_toolkit CREATEDB;'
```
Tests can be run with:
```
python manage.py test
```

####Launch an instance on Heroku:
Purchase a Twilio phone number [here](https://www.twilio.com/user/account/phone-numbers/search).

If needed, create a heroku account [here](https://signup.heroku.com/www-header).
```
heroku create
git push heroku master
heroku ps:scale web=1
heroku run python manage.py syncdb
heroku run python manage.py migrate
heroku config:set TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
heroku config:set TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXX
heroku config:set DJANGO_SETTINGS_MODULE=vallejo_css_toolkit.[development|staging|production]
```

Finally, route incoming calls to your Twilio phone number to your Heroku app url.
