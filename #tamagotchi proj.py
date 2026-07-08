#tamagotchi proj

print(f"----------------------------------------\n WELCOME TO THIS INTERACTIVE SIMULATION\n----------------------------------------")
pet_name=input("What is your pet name")
pet_type=input("is your pet a dragon, cat, or dog")
if pet_type!="dragon" and pet_type!="cat" and pet_type!="dog":
        print("invalid pet type")
print("\nYour pet is hatched and is very happy to see you! He is great at shooting free throws somehow, and has mood swings ")

hunger=100
happiness=100
health=3
sleep=10
water=5
cleanliness=10

while True:
    
    
    
    
   

   

    print("\n your pet's hunger is at",hunger,"\n your pet's happiness is at",happiness,"\n your pet has",health,"lives. \n your pet's sleep is at",sleep,"\n your pet's water is at",water,"\n your pet's cleanliness is at",cleanliness,"\n If your stats hit zero, you lose")
    move= input("\nYou can feed your pet, play with your pet, take your pet to the doctor, put your pet to sleep, give your pet water, or clean your pet. You can also check on your pet's stats. Type 'exit' to exit the simulation. Respond with 'feed', 'play', 'doctor', 'sleep', 'water', 'clean', or 'stats' to make a move: ")

    if move=="exit":
        print("\nThanks for playing!")
        break
    if move!="feed" and move!="play" and move!="doctor" and move!="sleep" and move!="water" and move!="clean" and move!="stats":
        print("\n sorry, that's not a valid move")
    
    if move=="feed":
        hunger+=10
    if move=="play":
        happiness+=10
    if move=="doctor":
        health+=2
    if move=="sleep":
        sleep+=3
    if move=="water":
        water+=3
    if move=="clean":
        cleanliness+=5

    if move!="clean":
        cleanliness-=0.25
    if move!="water":
        water-=0.25
    if move!="sleep":
        sleep-=2
    if move!="doctor":
        health-=0.5
    if move!="play":
        happiness-=20
    if move!="feed":
        hunger-=20

    if hunger<=0 or happiness<=0 or health<=0 or sleep<=0 or water<=0 or cleanliness<=0:
        print("\n your pet's hunger is at",hunger,"\n your pet's happiness is at",happiness,"\n your pet has",health,"lives. \n your pet's sleep is at",sleep,"\n your pet's water is at",water,"\n your pet's cleanliness is at",cleanliness,"\n If your stats hit zero, you lose")
        print("\n Your pet has died. Game over.")
        break
    