import subprocess
import psycopg2
from psycopg2 import sql

from core.config import settings
from core.database_manager import create_tenant_db
from models.master_models import Tenant
from services.tenant_service import TenantUserService, OrganizationService
from utils.security import generate_random_password, hash_password
from utils.email_utils import send_password_reset_email
from models.tenant_models import UserRole


def create_tenant_database(tenant_data: dict, user_data: dict):
    """
    Creates a new PostgreSQL database for the tenant and runs migrations.
    """
    db_name = tenant_data.get("db_name")
    if db_name is None:
        print("Error: 'db_name' key is missing from tenant_data.")
        return
    
    connection_params = {
        "dbname": "postgres",  # Connect to default postgres database
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_SERVER,
        "port": settings.POSTGRES_PORT,
    }

    # Establish connection to default database (postgres)
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**connection_params)
        conn.autocommit = True  # CREATE DATABASE needs autocommit to be True
        cursor = conn.cursor()

        # Use psycopg2.sql to safely pass the tenant_db_name
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name)
        ))
        print(f"Database {db_name} created successfully!")

    except psycopg2.Error as e:
        print(f"Error creating database: {str(e)}")
        raise
    finally:
        # Always close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # After database creation, run Alembic migrations
    run_migrations(db_name, user_data)


def run_migrations(tenant_db_name: str, user_data: dict):
    # Run the Alembic migration for the newly created tenant database
    try:
        result = subprocess.run([
            "poetry",
            "run",
            "alembic",
            "-x", f"db_name={tenant_db_name}",
            "upgrade",
            "head"
        ], check=True)
        
        if result.returncode == 0:
            print(f"Migrations for database {tenant_db_name} completed successfully!")
            save_user_to_tenant_db(tenant_db_name, user_data)
        else:
            print(f"Migration for database {tenant_db_name} failed with exit code {result.returncode}")
            print(f"Error: {result.stderr}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations for database {tenant_db_name}: {str(e)}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        
        
def save_user_to_tenant_db(tenant_db_name: str, user_data: dict):
    try:
        session = create_tenant_db(tenant_db_name) 
        with session: 
            organization_service = OrganizationService(session)
            user_service = TenantUserService(session)
            
            user_data.setdefault("user_name", f"{user_data.get('first_name_en', 'user')}.{user_data.get('last_name_en', 'guest')}")
            user_data.setdefault("profession", "Unknown Profession")
            user_data.setdefault("position", "Unknown Position")
            user_data.setdefault("role", UserRole.SUPER_ADMIN) 

            generated_password = generate_random_password()
            hashed_password = hash_password(generated_password)

            if isinstance(user_data, dict):
                user_creation_data = user_data.copy()
                user_creation_data["password"] = hashed_password
                user_creation_data["is_super_admin"] = True
                user_creation_data.pop("organization_name", None) 
                user_creation_data.pop("tenant_id", None) 
                user_creation_data.pop("commercial_id", None)
                user_creation_data.pop("sub_domain", None) 
                
                user = user_service.create(user_creation_data)

                organization_data = {
                    "name_en": user_data.get('organization_name'),
                    "commercial_id": user_data.get('commercial_id'), 
                    "created_by": user.id,
                    "tenant_id": user_data.get('tenant_id')
                }
                
                organization_service.create(organization_data)
                sub_domain = user_data.get('sub_domain')
                print(sub_domain)
                login_link = f"{sub_domain}.{settings.DOMAIN}/login/"
                subject = "Welcome to Our Platform"
                body = (f"Hello {user.first_name_en},\n\n"
                        f"Your account has been created successfully.\n"
                        f"Your login details are:\n"
                        f"Email: {user.email}\n"
                        f"Password: {generated_password}\n\n"
                        f"Please use the following link to login: {login_link}\n\n"
                        f"Please change your password after logging in.\n\n"
                        f"Thank you!")
                
                send_password_reset_email(user.email, subject, body)
            else:
                print(f"Expected user_data to be a dict but got {type(user_data)}")

        print(f"User {user_data.get('email')} added to {tenant_db_name} successfully!")

    except Exception as e:
        print(f"Error saving user data to {tenant_db_name}: {str(e)}")