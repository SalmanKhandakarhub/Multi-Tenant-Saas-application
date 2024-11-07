import click
from datetime import datetime
from passlib.hash import bcrypt # type: ignore
from sqlalchemy.orm import Session

from utils.security import hash_password
from core.database_manager import get_master_db
from models.master_models import User, UserStatus
from services.master_service import UserService


user_service = UserService(get_master_db())

@click.command()
@click.option('--first-name', prompt=True, help='Enter the first name: ')
@click.option('--last-name', prompt=True, help='Enter the last name: ')
@click.option('--email', prompt=True, help='Enter the email: ')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Enter the password: ')
@click.option('--contact-number', prompt=True, help='Enter the contact number (optional): ', default=None)
@click.option('--status', default=UserStatus.ACTIVE.value, help='User status (default: active)')
def create_super_user(first_name, last_name, email, password, contact_number, status):
    existing_user = user_service.get_one({"email": email})
    if existing_user:
        click.echo(f"User with email {email} already exists!")
        return

    hashed_password = hash_password(password)
    user = user_service.create({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password,
        "contact_no": contact_number,
        "is_super_admin": True 
    })

    click.echo(f"User {user.first_name} {user.last_name} created successfully with status {user.status}!")
    click.echo(f"Username is {user.email}!")
    click.echo(f"You are a Super Admin {user.is_super_admin}!")
        
if __name__ == '__main__':
    create_super_user()



