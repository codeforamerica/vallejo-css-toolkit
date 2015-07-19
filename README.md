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
If needed, create an account here: https://www.twilio.com/try-twilio

Add the following to `env/bin/activate`:
```
export TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
export TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXX
```

Activate environment and install dependencies:
```
source env bin activate
pip install 
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
foreman start
```

Launch an instance on Heroku:
Purchase a Twilio phone number: https://www.twilio.com/user/account/phone-numbers/search

Create a heroku account if needed: https://signup.heroku.com/www-header
```
heroku create
git push heroku master
heroku ps:scale web=1
heroku run python manage.py syncdb
heroku run python manage.py migrate
heroku config:set TWILIO_ACCOUNT_SID=XXXXXXXXXXXXX
heroku config:set TWILIO_AUTH_TOKEN=XXXXXXXXXXXXXX
```

Finally, route incoming calls to your Twilio phone number to your Heroku app url

[TODO: attach screenshot]


