#tamagotchi proj

print(f"----------------------------------------\n WELCOME TO THIS INTERACTIVE SIMULATION\n----------------------------------------")
pet_name=input("What is your pet name")
pet_type=input("is your pet a dragon, cat, or dog")
if pet_type!="dragon" and pet_type!="cat" and pet_type!="dog":
        print("invalid pet type")


if pet_type=="dog":
    print(f"Your pet is a dog named {pet_name} He is very friendly and loves to play fetch. However he has mood swings.")
    hunger=80
    cleanliness=50
    happiness=100
    water=80
    sleep=50
    health=50
if pet_type=="cat":
    print(f"Your pet is a cat named {pet_name} He is very friendly and loves to play with yarn. However he has mood swings.")
    hunger=60
    cleanliness=80
    happiness=60
    water=80
    sleep=100
    health=50
if pet_type=="dragon":
    print(f"Your pet is a dragon named {pet_name} He is very friendly and loves to play with fire. However he has mood swings.")
    hunger=100
    cleanliness=20
    happiness=80
    water=40
    sleep=60
    health=50
while True:
    
    
    
    
   

   

    print("\n your pet's hunger is at",hunger,"\n your pet's happiness is at",happiness,"\n your pet has",health,"lives. \n your pet's sleep is at",sleep,"\n your pet's water is at",water,"\n your pet's cleanliness is at",cleanliness,"\n If your stats hit zero, you lose")
    move= input("\nYou can feed your pet, play with your pet, take your pet to the doctor, put your pet to sleep, give your pet water, or clean your pet. You can also check on your pet's stats. Type 'exit' to exit the simulation. Respond with 'feed', 'play', 'doctor', 'sleep', 'water', 'clean', or 'stats' to make a move: ")

    if move=="exit":
        print("\nThanks for playing!")
        break
    if move!="feed" and move!="play" and move!="doctor" and move!="sleep" and move!="water" and move!="clean" and move!="stats":
        print("\n sorry, that's not a valid move")
    
    if move=="feed":
        hunger+=30
    if move=="play":
        happiness+=30
    if move=="doctor":
        health+=30
    if move=="sleep":
        sleep+=30
    if move=="water":
        water+=30
    if move=="clean":
        cleanliness+=30

    if move!="clean":
        cleanliness-=10
    if move!="water":
        water-=10
    if move!="sleep":
        sleep-=10
    if move!="doctor":
        health-=10
    if move!="play":
        happiness-=20
    if move!="feed":
        hunger-=20

    if hunger<=0 or happiness<=0 or health<=0 or sleep<=0 or water<=0 or cleanliness<=0:
        print("\n your pet's hunger is at",hunger,"\n your pet's happiness is at",happiness,"\n your pet has",health,"lives. \n your pet's sleep is at",sleep,"\n your pet's water is at",water,"\n your pet's cleanliness is at",cleanliness,"\n If your stats hit zero, you lose")
        print("\n Your pet has died. Game over.")
        break
    