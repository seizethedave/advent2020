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

    def solve(self):
        if not self.unassigned_allergens:
            self.allergy_free_ingredients &= self.unassigned_ingredients
            return

        def eligible_for_allergen(ing, allerg):
            for fi, fa in self.foods:
                if allerg in fa and ing not in fi:
                    return False
            return True

        for ingredient in self.unassigned_ingredients:
            candidate_allergens = set(self.unassigned_allergens)
            for allergen in candidate_allergens:
                if not eligible_for_allergen(ingredient, allergen):
                    continue

                foods_copy = self.assign(ingredient, allergen)
                self.solve()
                self.unassign(ingredient, allergen, foods_copy)

s = Solver()

for line in sys.stdin:
    ingredients, allergens = line.split("(")
    ingredients = ingredients.strip().split(" ")
    allergens = allergens[9:-1].rstrip("\n)").split(", ")
    s.add_food(ingredients, allergens)

s.solve()
print(s.allergy_free_ingredients)

c = Counter()
for f_i, _ in s.foods:
    c.update(f_i & s.allergy_free_ingredients)
    
print(sum(c.values()))