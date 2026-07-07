#day5
torch="*\n|\n|"
def place_steps():
    for i in range(5):
        print("Place STEP")
    print("Stair complete")
    
def place_torches():
    for i in range(10):
       print(torch)
       print("placing torch at position X")

def place_steps_2(step):
    for step in range(step):
        print("Place STEP")
    print("Stair complete")


def build_guard_tower():
    for i in range(3):
        print("wall complete")
        for i in range(4):
            print("block placed")

def collect_logs():
   log=0
   while log<64:
       print("\nChop log\nYou now have ",log,"logs\n")
       log+=1
       
def build_reinforced_wall():
    for i in range(5):
        print("COBBLESTONE\n")
        for i in range(3):
            print("PLANK\n")

def night_patrol():
    energy=100
    minutes=0
    while energy>0 and minutes<10:
        minutes+=1
        print("Patrolling the village")
        energy-=12
        print("Energy level is now",energy)
        print({"Minutes patrolling:",minutes})
    if energy<=0:
        print("You are too tired to patrol. Go to sleep")
    if energy<30:
        print("Warning: Low power.")


stepamount=int(input("How many steps do you want? "))
place_steps_2(stepamount)
place_torches()
build_guard_tower()
collect_logs()
build_reinforced_wall()
night_patrol()