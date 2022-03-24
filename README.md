# Hawk_and_Dove_Simulation
An elementary simulation of the hawk and dove game, which is a game-theoretical model of aggressive behavior. \
From lines 33 to 39, users are allowed to change the variables to see how different things can affect the outcomes.

# Simulation 1 - Hawks vs. Doves
In the file, hawkdove.py, uncomment the line 334 to 337 and comment lines 338 to 341 and 348 to see how the world will end up if there are just two types of birds, aggressive one and never-fight one. \
Basically, in this world, there exist two types of birds. Hawk is the one who will always fight for food and dove is the one who never defends itself. So, when a hawk meets a dove, the hawk will always have food. And when a hawk meets a hawk, they will fight and the program will choose one hawk to win the fight to have the food. Moreover, when two doves meet, the one who comes first will have the food. \
More things are explained in the codes. \
(Try to set injurycost, displaycost, and foodbenefit to 11, 1, and 8 respectively. And they try changing injurycost to 7)

# Simulation 2 - Hawks vs. Defensive Birds
In the file, hawkdove.py, uncomment the line 336 to 339 and comment lines 334 to 335, 340 to 341, and 348 to see how the world will end up if there are just two types of birds, aggressive one and defensive one. \
This type of bird is “defensive”—if it finds food first, it will fight to defend it from other birds, but it will not attack other birds to take their food. And the behaviors of hawks will stay the same. \
(Try to set injurycost, displaycost, and foodbenefit to 10, 1, and 12 respectively. And they try changing foodbenefit to 8)

# Simulation3 - Evolving Birds
In the file, hawkdove.py, uncomment the line 340 to 341, and line 348 and comment lines 334 to 339 to see how the world will end up if there is just one type of bird, the evolving birds. \
Now, the major change is that they will have different levels of aggression, choosing to fight more or less frequently. The other is that they’ll vary by weight, with heavier birds winning fights more often but also burning more calories over time. Then, we’ll let these birds evolve— children of a bird will have roughly the same (but not identical) attributes as the parent—and we can see how the birds change over time. \
Finally, the program creates a simple scatter plot of the weights and aggressiveness of the birds. \
(Try to set injurycost to 10, displaycost to 1 and foodbenefit to 8)
