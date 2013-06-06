import bottle
import simplejson
import uuid
import rawes
from pprint import pprint
from bottle import route, run


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


es = rawes.Elastic('localhost:9200')

courses = {
    'breakfast' : 'breakfast-brunch',
    'lunch' : 'appetizers,pasta,salads,sandwiches,soups,bread',
    'dinner' : 'entrees,grains,hors-d-oeuvres,legumes,pastries,pies-and-tarts,pies-and-tarts,vegetables,potatoes' # removed sauces
}


@route('/', method='GET')
def homepage():
    return es.get('/')
    

@route('/plan/:calories/:cuisine/:ingredients', method='GET')
def get_plan(calories, cuisine, ingredients):
    return dict(
        id = 'new plan id',
        todo = '7-day recipe plan with 3 meals per day, max %d calories/person/day, preferring %s cuisine and including %s'
            % (int(calories), cuisine, ingredients))


@route('/substitute/:id/:day/:meal', method='GET')
def get_substitute(id, day, meal):
    return dict(
        id = 'new plan id',
        old_id = 'original plan id',
        todo = 'Substitute %s on day %d with another random choice' % (meal, int(day)))


def query_recipes(meal, cuisine, ingredients):
    ingredients_clause = []
    name_clause = []
    for ingredient in ingredients.split(','):
        ingredients_clause.append({ 'match' : { 'ingredients' : ingredient } })
        name_clause.append({ 'match' : { 'name' : { 'query' : ingredient, 'boost' : 3 } } })
        should_clause = [{ 'match' : { 'cuisine' : { 'query' : cuisine, 'boost' : 3 } } }] \
            + ingredients_clause \
            + name_clause \
            + [{ 'match_all' : {} }]
    query={
        'query' : {
            'bool' : {
                'should' : should_clause
            }
        }
    }
    return es.get('recipes/' + courses[meal] + '/_search?size=20', data=query)


def store_plan(plan):
    new_id = uuid.uuid5('recipe_plan', repr(plan))
    es.put('recipe_plans/plan/' + new_id, data=plan)
    return plan


def retrieve_plan(id):
    return es.get('recipe_plans/plan/' + id)


def modify_plan(id, day, meal):
    old_plan = retrieve_plan(id)
    # Re-run old query
    cuisine = old_plan['metadata']['cuisine']
    calories = old_plan['metadata']['calories']
    ingredients = old_plan['metadata']['ingredients']
    recipes = query_recipes(meal, cuisine, ingredients)
    # TODO replace old_plan['days'][day][meal] with a random new recipe from the results

#bottle.debug(True) 
#run(host='0.0.0.0', reloader=True)




