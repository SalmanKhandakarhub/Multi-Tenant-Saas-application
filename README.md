# Multi-Tenant-Saas-application

## Create env.py through alembic with specific directory 
    $ alembic init app/models/migrations

### Create a migration
    $ alembic revision --autogenerate -m "Initial migration"
### Apply the migration
    $ alembic upgrade head
