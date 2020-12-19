# rest-api-python
We have created framework with user registration for authentication. 


In user.py we added registration class where JSON values from POSTMAN /register will insert into DB
Security.py will verify authentication from DB values to POSTMAN /auth values

Also we update authentication in app.py (change expiration time, return id in postman)


How to run;

First run create_table and make sure table created and data inserted  =>	 python create_table.py

then run app.py =>	python app.py
 >> it will generate url server http://<IP Number>.5000/

once it is ran the, open POSTMAN
	=> TO Insert run PUT
	=> TO Requst run GET
  => TO create user for registration run POST/register
	=> to Authenticate run POST/AUTH (its body JSON param should match to earlier inserted data into table)
