import requests
import smtplib

# User inputs
recipient=input("\nWhere should I send the email : ")
city=input("\nWhich city would you like to receive the weather from : ").title()
unit=input("\nWould you like to receive it in imperial, standard, or metric units : ").lower()
senderEmail=input("\nWhich email should I send it from : ")
senderPassword=input("\nWhat is the password of that email : ")
APIKEY=input("\nWhat is yout APIKEY : ")

# Get request to the API
url="https://api.openweathermap.org/data/2.5/weather"
params={
    "appid":APIKEY,
    "q":city,
    "units":unit,
}
response=requests.get(url=url,params=params)
response.raise_for_status()

# Check if error occurs
if (response.status_code==200):
    with smtplib.SMTP("YOUR EMAIL SERVER") as connection:
        # Set up the connection
        connection.starttls()
        connection.login(user=senderEmail,password=senderPassword)
        chosenUnit="Kelvin" if unit=="standard" else ("Celcius" if unit=="metric" else "Fahrenheit")

        # Parse through the data
        data=response.json()
        weatherDescription=data["weather"][0]["description"]
        weatherTemperature=data["main"]["temp"]

        # Send the email
        msg=f"Subject:Weather data in {city}\n\nIn {city}, the weather is currently {weatherDescription} with a temperature of {weatherTemperature} degrees {chosenUnit}.\n\nHope this helps!"
        connection.sendmail(from_addr=senderEmail,to_addrs=recipient,msg=msg)
        print("I sent you the email, please check it out")
else:
    print("Error in retrieving data, was there a typo?")



