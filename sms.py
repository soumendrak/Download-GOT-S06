from twilio.rest import TwilioRestClient
SID = "<your SID>"
Token = "<your token id>"
twilioCli = TwilioRestClient(SID, Token)
myTwilioNumber = '+1xxxxxxxx'
numbers = '+91xxxxxxxxx +91xxxxxxxxxx'


def texting(message, numbers):
    numbers = numbers.split(' ')
    for i in range(len(numbers)):
        print numbers[i]
        twilioCli.messages.create(body=message, from_=myTwilioNumber,
                                  to=str(numbers[i]))
