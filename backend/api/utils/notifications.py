from django.core.mail import send_mail
from django.conf import settings

def send_bill_email(customer_email, bill_data):
    """Send bill receipt via email"""
    if not customer_email:
        return False
    
    subject = f"Bill Receipt - {bill_data['id']}"
    message = f"""Dear Customer,

Thank you for your purchase!

Bill ID: {bill_data['id']}
Date: {bill_data['bill_date']}
Total Amount: ${bill_data['total_amount']}

Items:
{bill_data['items_text']}

Thank you for shopping with us!
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_whatsapp_message(phone, bill_data):
    """Send bill notification via WhatsApp"""
    if not phone:
        return False
    
    phone = phone.replace(" ", "").replace("-", "")
    if not phone.startswith("+"):
        phone = f"+91{phone}"
    
    message = f"""Bill Receipt
Bill ID: {bill_data['id']}
Date: {bill_data['bill_date']}
Total: ${bill_data['total_amount']}
Thank you for shopping with us!"""
    
    print(f"WhatsApp to {phone}: {message}")
    return True
