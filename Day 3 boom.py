#breathing, using devices, electricity, water, food, transportation. 
bus=0.04
computers=0.06
electriccar = 0.14
gascar=0.4
ledlight=0.02
lightrail=1.3
shower=1.2
electricalstove=0.3
ac1=2.5
natgas=0.45

print("welcome...to my information steal-i mean my calculator")
transport= input("How did you come here today?")
miles = input("how many miles did you travel")
food =input("How many meals cooked per day")
stove=input("What kind of stove")
lights1=input("How many hours are your lights on")
light2=input("How many lights do you have")
showers=input("How many showers per day")
ac=input("How many hours did you have AC on")
computer=input("How many hours on computer at home")


if transport=="bus":
    transport=bus
elif transport=="electric car":
    transport=electriccar
elif transport==gascar:
    transport=gascar

finaltransport=float(miles)*float(transport)

if stove=="natural gas":
    stove=natgas
elif stove=="electrical stove":
    stove=electricalstove

finalstove=float(stove)*float(food)
finallights=float(light2)*float(lights1)*ledlight
finalac=float(ac)*ac1
finalshower=float(showers)*shower
finalcomputer=float(computer)*computers

finalemissions=(finalstove)+(finalshower)+(finalcomputer)+(finallights)+(finaltransport)+(finalac)
print("Your final daily CO2 emissions are", finalemissions, "kilos")
