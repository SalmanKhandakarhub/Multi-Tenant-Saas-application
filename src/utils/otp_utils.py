import random



def generate_otp() -> int:
    """Generate a 6-digit random OTP."""
    return random.randint(100000, 999999)



def send_sms(phone_number: str, message: str):
    # Implement SMS sending logic here (e.g., Twilio)
    print(f"Sending SMS to {phone_number}: {message}")
    
def send_otp_to_phone(contact_no: str, otp: int):
    # Implement your SMS sending logic here
    print(f"Sending OTP {otp} to phone number {contact_no}.")