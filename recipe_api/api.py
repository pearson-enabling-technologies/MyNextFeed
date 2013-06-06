import bottle
import simplejson
import rawes
import hashlib
from pprint import pprint
from bottle import route, run
from random import randint, choice


"""
Notes...

Each plan object has two top-level elements: "metadata" and "days".

"metadata" contains the original query options used to generate the plan:
    "calories" (number)
    "cuisine" (string)
    "ingredients" (string, may be comma-separated list)

"days" contains list of objects, each of which has "breakfast", "lunch" & "dinner".

Each of these are in turn an array of recipes, because a meal could consist of
more than one recipe.
"""


es = rawes.Elastic('ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:9200')

courses = {
    'breakfast' : 'breakfast-brunch',
    'lunch' : 'appetizers,pasta,salads,sandwiches,soups,bread',
    'dinner' : 'entrees,grains,hors-d-oeuvres,legumes,pastries,pies-and-tarts,pies-and-tarts,vegetables,potatoes' # removed sauces
}

calorie_avgs = {
    'breakfast' : 0.2,
    'lunch' : 0.3,
    'dinner' : 0.5
}

@route('/', method='GET')
def homepage():
    return es.get('/')
    

@route('/plan/:calories/:cuisine/:ingredients', method='GET')
def get_plan(calories, cuisine, ingredients):
    weekPlan = []
    for i in range(7):
        dayPlan = {}
        for meal in courses.keys():
            recipeList = query_recipes(meal, cuisine, ingredients, calories)
            dayPlan[meal] = choice(recipeList['hits']['hits']) # TODO check field names
        weekPlan.append(dayPlan)
    plan = dict( 
        days = weekPlan, 
        metadata = dict(
            calories = calories,
            cuisine = cuisine,
            ingredients = ingredients)
        )
    plan['metadata']['id'] = store_plan(plan)
    return plan


@route('/substitute/:id/:day/:meal', method='GET')
def get_substitute(id, day, meal):
    new_plan = modify_plan(id, day, meal)
    plan['metadata']['id'] = store_plan(plan)
    return plan

def query_recipes(meal, cuisine, ingredients, calories):
    ingredients_clause = []
    name_clause = []
    for ingredient in ingredients.split(','):
        ingredients_clause.append({ 'match' : { 'ingredients' : ingredient } })
        name_clause.append({ 'match' : { 'name' : { 'query' : ingredient, 'boost' : 3 } } })
    should_clause = [{ 'match' : { 'cuisine' : { 'query' : cuisine, 'boost' : 3 } } }] \
        + ingredients_clause \
        + name_clause \
        + [{ 'match_all' : {} }]
    query = {
        "query": {
            "custom_filters_score": {
                "query": { 
                    'bool' : {
                        'should' : should_clause
                    }
                },
                "filters": [
                    {
                        "filter": {
                            "exists": {
                                "field": "calories"
                            }
                        },
                        "script": "(0 - min( " + str(calories) + "/ doc['calories'].value, doc['calories'].value / " + str(calories) + "))"
                    }
                ]
            }
        }
    }
    return es.get('recipes/' + courses[meal] + '/_search?size=20', data=query)


def store_plan(plan):
    sha1 = hashlib.sha1()
    sha1.update(str(plan))
    new_id = sha1.hexdigest()
    es.put('recipe_plans/plan/' + new_id, data=plan)
    return new_id


def retrieve_plan(id):
    return es.get('recipe_plans/plan/' + id)


def modify_plan(id, day, meal):
    plan = retrieve_plan(id)['_source']
    # Re-run old query
    cuisine = plan['metadata']['cuisine']
    calories = plan['metadata']['calories']
    ingredients = plan['metadata']['ingredients']
    recipes = query_recipes(meal, cuisine, ingredients, calories)
    # Replace unwanted recipe with a random new recipe from the results (if not already used)
    used_recipes = set(day[meal]['name'] for day in plan['days']) # TODO check field names
    candidate_recipes = [recipe for recipe in recipes if recipe['name'] not in used_recipes]
    chosen_recipe = choice(candidate_recipes)
    plan['days'][day][meal] = chosen_recipe
    return plan

bottle.debug(True) 
run(host='0.0.0.0', reloader=True)
#pprint(query_recipes('dinner', 'Italian', 'chicken,basil,tomato', 0.1))




