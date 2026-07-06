#number even or odd
level=12
weapon=False
health =70
has_armor=-False
magic_ring=True
if magic_ring==True:
    level>=10
    health>=50
    weapon=True
if level>=10:
    if weapon or has_armor ==True:
        if health >= 50:
            print ("You're ready for battle")
        else: print("you're health is too low")
    else:
        print("you need a weapon to fight")
         
