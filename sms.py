from twilio.rest import TwilioRestClient
SID = "AC5xxxxxxxxxxxxxxxxxxxxxxxxxxx"
Token = "23b46xxxxxxxxxxxxxxxxxxxxxxxxxx"
twilioCli = TwilioRestClient(SID, Token)
myTwilioNumber = '+1XXXXXXXXXXXX'

def texting(message, numbers):
    numbers = numbers.split(' ')
    for i in range(len(numbers)):
        print numbers[i]
        twilioCli.messages.create(body=message, from_=myTwilioNumber, to=str(numbers[i]))    
