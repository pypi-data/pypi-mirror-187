# c2s_mobiz

c2s_mobiz is a package that allows you to send SMS messages through an API. It includes a function to send SMS messages and handle the response, as well as a model to log the result of the message.

## Installation

To install c2s_mobiz, simply run:

```bash
pip install c2s_mobiz
```

## Requirements

A Mobiz API key, which can be obtained from the Mobiz website.
A BASE_MOBIZ_URL and MOBIZ_API_KEY setting in your Django settings file.
The SMSLog and models modules imported in your file.
Usage
To use the module, import it in your file and call the send_sms function, passing in the trigger key for the SMS message and the data to be sent in the message.

check if the URL hasn't changed  then in your settings.py it should look like this 
```python
MOBIZ_API_KEY = '<Your_api_key>'
BASE_MOBIZ_URL = 'https://api.mobiz.co.za/api/2.0/triggerMessage.php'
```


## Usage

To send an SMS message, use the `send_sms` function:
```python
from c2s_mobiz import send_sms

response = send_sms(trigger_key='your_trigger_key', data={'A': '1234567890', 'B': 'Hello, World!'})
#A is phone number and B is the content according to your mobiz created message template
```

### send_sms function takes two arguments :
trigger_key: The trigger key to use for the SMS message.
data: The data to be sent in the SMS message.

## Configuration

You need to add your API_KEY and BASE_URL in your django settings.py file:

```python
MOBIZ_API_KEY = 'YOUR_API_KEY'
BASE_MOBIZ_URL = 'https://api.mobiz.co.za/api/2.0/triggerMessage.php'
```

you will also need to create a logger in your settings


## Logging

The package uses the model SMSLog to log the result of the message.
The table will be created in your database after running the command:

```bash
python manage.py makemigrations
python manage.py migrate
```

## if not installed automatically  
you will need to also create those 2 models SMSLog and sms_lookup below is how they should look like 

```python
class SMSLog(models.Model):
    sent_at = models.DateTimeField(auto_now_add=True)
    data  = models.TextField()
    messge_trigger_key = models.CharField(max_length=255)
    response = models.TextField()
    status = models.CharField(max_length=255)
```

## Support 
For support or any other inquiries, please email khaled.yasser@click2sure.co.za