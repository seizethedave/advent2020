"""
have series of 
ingredient1 ingredient2 ... ingredientN (contains allergen1, allergen2,...)
ingredient1 ingredient2 ... ingredientM (contains allergen1, allergen2,...)

Want to figure out which ingredientJ's cannot contain the listed allergens.
Then count how many times ingredientJ appears in any food.
Each step should eliminate ingredients that CAN/DO contain a listed allergen.

Food1
ingred:
    i1
    i2
allergen:
    a1

Food2
ingred:
    i2
    i3
allergen:
    a2
    a3

presume i1 -> a1.

Food1
ingred:
    i2
allergen:

Food2
ingred:
    i2
    i3
allergen:
    a2
    a3

if valid:
    presume i2 -> a2

    Food1
    ingred:
        i2
    allergen:

    Food2
    ingred:
        i3
    allergen:
        a3 
    
    if valid:
        presume i3 -> a3

        Food1
        ingred:
            i2
        allergen:

        Food2
        ingred:
        allergen:

        result is 1.

Ex 2:

Food1
ingred:
    i1
    i2
allergen:
    a1

Food2
ingred:
    i1
    i3
allergen:
    a2
    a3


presume i1 -> a1.



Food1
ingred:
    i2
allergen:
    -
Food2
ingred:
    i3
allergen:
    a2
    a3

Not valid, a2/3 must correspond to i1/i3.

revert:

Food1
ingred:
    i1
    i2
allergen:
    a1

Food2
ingred:
    i1
    i3
allergen:
    a2
    a3

next, presume i2 -> a1

Food1
ingred:
    i1
allergen:

Food2
ingred:
    i1
    i3
allergen:
    a2
    a3

(i2 -> a1)

if valid:
    presume i1->a2

    Food1
    ingred:
    allergen:

    Food2
    ingred:
        i3
    allergen:
        a3

    (i2 -> a1,
     i1 -> a2)

    valid, so presume i3 -> a3. done. 0 unknowns.

Top level:
{ingredient -> allergen}
initially {ingredient -> None}.

A = list of all allergens.

Food:
    set(ingredient)
    set(allergen)

F = list of Foods.

At each move: take unknown ingredient.

do {
    Assign arbitrary allergen.
} while invalid();

if valid:
    recurse

"""

from collections import Counter
import copy
from pprint import pprint
import sys

class Solver:
    def __init__(self):
        self.foods = []
        self.ingredients = {}
        self.unassigned_allergens = set()
        self.unassigned_ingredients = set()
        self.allergy_free_ingredients = set()

    def add_food(self, ingredients, allergens):
        self.foods.append((set(ingredients), set(allergens)))
        self.unassigned_allergens.update(allergens)
        self.unassigned_ingredients.update(ingredients)
        self.allergy_free_ingredients.update(ingredients)

    def is_valid(self):
        """
        Valid if:
        - an allergen does not appear under two different ingredients.
        - for each food f:
            |f.ingredients| >= |f.allergens|
        """
        c = Counter(self.ingredients.values())
        maxcount = max(c.values())
        if maxcount > 1:
            print(f"  not valid maxcount={maxcount}")
            return False

        for f_ingredients, f_allergens in self.foods:
            if len(f_ingredients) < len(f_allergens):
                print(f"  not valid maxcount={len(f_ingredients)} < {len(f_allergens)}")
                return False
        else:
            return True
        
    def assign(self, ingredient, allergen):
        self.ingredients[ingredient] = allergen
        self.unassigned_ingredients.remove(ingredient)
        self.unassigned_allergens.remove(allergen)
        foods_copy = copy.deepcopy(self.foods)
        for food_ingredients, food_allergens in self.foods:
            food_ingredients.discard(ingredient)
            food_allergens.discard(allergen)
        return foods_copy

    def unassign(self, ingredient, allergen, foods_copy):
        self.foods = foods_copy
        del self.ingredients[ingredient]
        self.unassigned_ingredients.add(ingredient)
        self.unassigned_allergens.add(allergen)

    def solve(self, level):
        if not self.unassigned_allergens:
            self.allergy_free_ingredients &= self.unassigned_ingredients

            print("  " * level, self.unassigned_ingredients)
            print("  " * level, self.ingredients)
            print("  " * level, self.foods)
            counter = Counter()
            for f_ingredients, _ in self.foods:
                counter.update(i for i in f_ingredients if i in self.unassigned_ingredients)
            print("  " * level, sum(counter.values()))
            return

        for ingredient in self.unassigned_ingredients:
            for allergen in self.unassigned_allergens:
                foods_copy = self.assign(ingredient, allergen)
                if self.is_valid():
                    print("  " * level, f"chose {ingredient} -> {allergen}")
                    self.solve(level + 1)
                self.unassign(ingredient, allergen, foods_copy)


s = Solver()

for line in sys.stdin:
    ingredients, allergens = line.split("(")
    ingredients = ingredients.strip().split(" ")
    allergens = allergens[9:-1].rstrip("\n)").split(", ")
    s.add_food(ingredients, allergens)

s.solve(0)
print(s.allergy_free_ingredients)