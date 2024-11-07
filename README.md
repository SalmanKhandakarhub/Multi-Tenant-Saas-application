# RINKU SAAS APPLICATION

### Access the container:
    $ sudo docker exec -ti src_container bash
### Run the Alembic Revision Command:
    $ poetry run alembic revision --autogenerate -m "Initial migration"
### Run Alembic migrations using Poetry:
    $ poetry run alembic upgrade head
### Tenancy Migration (No need to commandline)
    $ poetry run alembic -x db_name=test_db revision --autogenerate -m "Initial migration"
    $ poetry run alembic -x db_name=test_db upgrade head
## Create Super user in command line
    $ sudo docker compose run make_superuser

# Restart Appache2.server
    $ sudo kill -9 $(sudo lsof -t -i:80)
    $ sudo systemctl restart apache2.service 

# Restart Appache2.server
    $ cd /etc/apache2/sites-available/
    $ sudo nano rinku-ssl.conf
    $ sudo a2ensite rinku-ssl.conf 
    $ sudo nano /etc/hosts
    $ sudo kill -9 $(sudo lsof -t -i:80)
    $ sudo systemctl restart apache2.service 