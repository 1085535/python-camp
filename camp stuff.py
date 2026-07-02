print ("This is a madlibs generator ")
print("Answer the prompts to create a hilarious story")

place = input("Enter a place: ")
noun1 = input("Enter a noun: ")
celebrity1 = input("Enter a famous celebrity: ")
verb1 = input("Enter a verb: ")
animal = input("Enter a animal: ")
wacky_sport = input("Enter a wacky sport: ")
relative = input ("Enter a relative: ")
adjective1= input("Enter a adjective: ")
noun_2 = input("Enter a noun: ")
past_tense_verb = input ("Enter a past-tense verb: ")
adjective2 = input("Enter a adjective: ")

story = f"""
The other day I went to the {place} and ate {noun1}. Then I saw {celebrity1} {verb1} all over the place.
Then I won a pet{animal} in a {wacky_sport} contest. My {relative} was very {adjective1}. Out of the blue
a {noun_2}exploded. We all gathered around and {past_tense_verb}. To this day I've never had such a {adjective2} 
day
"""

print ("Here's your madlibs story")
print(story)

