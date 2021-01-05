from collections import Counter
import copy
from operator import itemgetter
from pprint import pprint
import sys

class Solver:
    def __init__(self):
        self.foods = []
        self.ingredients = {}
        self.unassigned_allergens = set()
        self.unassigned_ingredients = set()
        self.allergy_free_ingredients = set()
        self.solution = None

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
            if self.solution is None:
                self.solution = copy.deepcopy(self.ingredients)
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

c = Counter()
for f_i, _ in s.foods:
    c.update(f_i & s.allergy_free_ingredients)

# Part 1:
print(sum(c.values()))

# Part 2:
print(
    ",".join(k for k, _ in sorted(s.solution.items(), key=itemgetter(1)))
)