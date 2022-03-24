import random
import tkinter

random.seed()


def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white')  # Was 350 x 280
    c.grid()
    # Create the x-axis.
    c.create_line(50, 350, 650, 350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x, 355, anchor='n', text='%s' % (.5 * (i + 2)))
    # Create the y-axis.
    c.create_line(50, 350, 50, 50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45, y, anchor='e', text='%s' % (.25 * i))
    # Plot the points.
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300 * (x - 1))
        ypixel = int(350 - 300 * y)
        c.create_oval(xpixel - 3, ypixel - 3, xpixel + 3, ypixel + 3, width=1, fill='red')
    root.mainloop()


# Constants: setting these values controls the parameters of your experiment.
injurycost = 10  # Cost of losing a fight
displaycost = 1  # Cost of displaying between two passive birds
foodbenefit = 8  # Value of the food being fought over
init_hawk = 50
init_dove = 50
init_defensive = 50
init_evolving = 150

########
''' world '''


# create a world that the birds live in
class World:
    # create a empty list to keep trace of the existing birds
    def __init__(self):
        self.bird_exist = []

    # update the situations of each existing bird (die or regenerate)
    def update(self):
        for bird in self.bird_exist:
            bird.update()

    #  randomly pick birds to feed free food
    def free_food(self, a):
        # create an index to trace the times of feeding birds
        index = 0

        # feed a times
        while index < a:
            # randomly pick a bird from existing birds and let it eat, times += 1
            random.choice(self.bird_exist).eat()
            index += 1

    # make b times of encounter, same procedures as free_food
    def conflict(self, b):
        index = 0
        while index < b:
            # randomly pick an existing bird to encounter another bird from that list, times += 1
            first_bird = random.choice(self.bird_exist)
            second_bird = random.choice(self.bird_exist)
            if first_bird == second_bird:
                second_bird = random.choice(self.bird_exist)
            first_bird.encounter(second_bird)
            index += 1

    # print the final statuses of birds in this world
    def status(self):
        # creating indexes for each type of the bird
        h = 0
        do = 0
        de = 0
        ev = 0
        # count how many birds for each type and print out the final result.
        for bird in self.bird_exist:
            if bird.species == 'Hawk':
                h += 1
            elif bird.species == 'Dove':
                do += 1
            elif bird.species == 'Evolving':
                ev += 1
            else:
                de += 1
        print(f'There are {h} hawks, {do} doves, {de} defensive birds, and {ev} evolving birds.')

    # create a plot for evolvingbirds using the plot
    def evolvingPlot(self):
        # create two empty lists to trace attributes of existing birds
        weight_list = []
        aggressiveness_list = []
        for bird in self.bird_exist:
            # add the weight and aggressiveness of each existing bird into the list to use PLOT
            weight_list.append(bird.weight)
            aggressiveness_list.append(bird.aggressiveness)
        plot(weight_list, aggressiveness_list)


''' Hawk, Dove and Defensive Bird '''


# creating bird class with actions like eat and injured for future uses
class Bird:
    # birds have their own world and health
    def __init__(self, obj):
        self.health = 100
        self.world = obj
        self.world.bird_exist.append(self)

    # add health point to this bird with FOODBENEFIT
    def eat(self):
        self.health += foodbenefit

    # minus the health point if the bird is injured with INJURYCOST
    def injured(self):
        self.health -= injurycost

    # minus the health point if the bird displays every time with DISPLAYCOST
    def display(self):
        self.health -= displaycost

    # if the bird dies, we remove this object from the existing bird list of our world
    def die(self):
        # remove this died bird from the existing bird list.
        self.world.bird_exist.remove(self)

    # if health <= 0, this bird dies, otherwise, health -= 1
    def update(self):
        self.health -= 1
        if self.health <= 0:
            self.die()


# Birds without defensiveness
class Dove(Bird):
    # indicates its type
    species = 'Dove'

    # if this bird's health >= 200, then we regenerate another 'DOVE' object as a new bird in the world.
    def update(self):
        # update method from Bird as to determine whether the bird is died or not
        Bird.update(self)
        # if health >= 200, then minus 100 as a cost to born a new bird
        if self.health >= 200:
            self.health -= 100
            Dove(self.world)

    # Dove never defend, so return False everytime
    def defend_choice(self):
        return False

    # when encounter another bird ...
    def encounter(self, obj):
        # if the other bird defend its food, then it will eat the food and this bird doesn't change.
        if obj.defend_choice():
            obj.eat()

        # if two doves...
        else:
            # both this bird and another bird need to display and pick one of them to eat randomly
            obj.display()
            self.display()
            random.choice([obj, self]).eat()


# similar construction as Dove with some changes of defend_choice and encounter
class Hawk(Bird):
    # indicate its species
    species = 'Hawk'

    # same as Dove, but to generate Hawk
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Hawk(self.world)

    # always defend, so return true every time
    def defend_choice(self):
        return True

    # define encounter action of Hawk
    def encounter(self, obj):
        # if meet up with a Dove, Hawk with eat the food
        if not obj.defend_choice():
            self.eat()
        # if two Hawks meet up...
        else:
            # randomly pick a winner
            choice = random.choice([obj, self])
            # and for this bird and another bird...
            for bird in [obj, self]:
                # the chosen bird eats
                if bird == choice:
                    bird.eat()
                # the lost bird loses hp
                else:
                    bird.injured()


# mixed type of Dove and Hawk
class Defensive(Bird):
    # define species
    species = 'Defensive'

    # same as Hawk and Dove
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Defensive(self.world)

    # if another bird trying to take its food, then it will defend itself
    def defend_choice(self):
        return True

    def encounter(self, obj):
        # when defensive bird encounters another bird, and the another bird has food, it will not take it, so act like
        # a Dove.
        Dove.encounter(self, obj)

    # setting InjuredCost = 10, DisplayCost = 1, FoodBenefit = 9 - mix of hawks and defensive birds


''' Evolving Bird '''


# still a type of Bird
class Evolving(Bird):
    species = 'Evolving'

    # we still need upper class's __init__ as health and world
    def __init__(self, obj, parent):
        super().__init__(obj)

        # if this bird has no parent...
        if parent is None:
            # Give this bird initial attributes as weight and aggressiveness
            # by using random.random() and random.uniform()
            self.weight = random.uniform(1.0, 3.0)
            self.aggressiveness = random.random()
        # if this bird has parent ...
        else:
            # we want its attributes look like its parent, so add randomly small nums to its parent's attributes
            self.weight = parent.weight + random.uniform(-0.1, 0.1)
            # we don't want the attributes to go over the limit, so give limitation of 1-3
            if self.weight > 3.0:
                self.weight = 3.0
            elif self.weight < 1.0:
                self.weight = 1.0
            # similarly, give limitation of 0-1 for its aggressiveness.
            self.aggressiveness = parent.aggressiveness + random.uniform(-0.05, 0.05)
            if self.aggressiveness > 1.0:
                self.aggressiveness = 1.0
            elif self.aggressiveness < 0.0:
                self.aggressiveness = 0.0

    # decide whether to defend itself (or attack since the order doesn't matter anymore)
    def defend_choice(self):
        # pick a random nums between 0-1, since its aggressiveness is between 0-1, it can
        # perfectly simulate the aggressiveness of this bird (as aggressiveness gets higher, the possibility
        # for random.random() to be smaller than its aggressiveness is higher, which means it has a higher
        # possibility to attack.
        if random.random() > self.aggressiveness:
            return False
        else:
            return True

    # when two birds encounter ...
    def encounter(self, obj):
        # if self is aggressive ...
        if self.defend_choice():
            # if another bird wants to fight as well ...
            if obj.defend_choice():
                # the chance for self to win is self.weight/(self.weight + obj.weight)
                # heavier birds have more chance to win
                winning_chance = self.weight / (self.weight + obj.weight)
                random_chance = random.random()
                # if a random number between 0-1 is greater than winning chance, self injured and another bird eats
                if random_chance > winning_chance:
                    self.injured()
                    obj.eat()
                # if winning_chance for self is greater of equal to random number between 0-1,
                # then self.eat and another bird injured
                else:
                    self.eat()
                    obj.injured()
            # if another bird is not aggressive, then self eats
            else:
                self.eat()
        # if self is not aggressive ...
        else:
            # if another bird is aggressive, then it eats
            if obj.defend_choice():
                obj.eat()
            # if both birds are not aggressive, then follow dove.encounter
            else:
                obj.display()
                self.display()
                eat_choice = random.choice([self, obj])
                eat_choice.eat()

    # new method of update
    def update(self):
        # new way of calculating health by using weight (fatter means burn more health)
        self.health -= (0.4 + 0.6 * self.weight)
        if self.health <= 0:
            self.die()

        # if its hp >= 200 ...
        if self.health >= 200:
            self.health -= 100
            # create its own child with similar attribute as itself
            Evolving(self.world, self)

    # when foodbenefits > injurycost, there only exists one clump as heavier and aggressive birds


########
# The code below actually runs the simulation.  You can change the codes according to the instructions given to run different simulations.
########
w = World()
# for i in range(init_dove):
#     Dove(w)
# for i in range(init_hawk):
#     Hawk(w)
# for i in range(init_defensive):
#     Defensive(w)
for i in range(init_evolving):
    Evolving(w, None)

for t in range(10000):
    w.free_food(10)
    w.conflict(50)
    w.update()
w.status()
w.evolvingPlot()  # This line adds a plot of evolving birds. Uncomment it when needed.
