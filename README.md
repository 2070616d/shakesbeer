![ShakesBeer header](http://theehteam.pythonanywhere.com/static/images/header.png)
# ShakesBeer - the world's leading app that makes your petty alcoholism easier, Web-enabled and fun!

## Website: <http://theehteam.pythonanywhere.com>

## To run on your machine:

* `git clone https://github.com/2070616d/shakesbeer.git`
* `mkvirtualenv <environmentName>`
* `pip install -r requirements.txt`
* create/populate database
  * `cd shakesbeer`
  * `python manage.py makemigrations`
  * `python manage.py migrate`
  * `python populate_db.py`
*  `python manage.py runserver`
