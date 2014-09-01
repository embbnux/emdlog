emdlog
======

blog_use_flask_on_raspberry

This is a lightweight blog that you can use it on raspberry pi.

=============================
User Guide:

sudo apt-get install python-pip
 
sudo pip install flask

git clone https://github.com/embbnux/emdlog.git
 
cd emdlog/emdlog
 
sudo apt-get install sqlite3
 
sqlite3  db/flaskr.db < schema.sql
 
cd ../
 
python runserver.py

------------------------------------

from Blog of Embbnux :
http://www.embbnux.com/2014/08/25/raspberry_use_python_flask_to_web_development/


