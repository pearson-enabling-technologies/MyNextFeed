import sys
import json
import os
import random

def write_recipes(courses):
  for course in courses['results']:
    if os.path.isfile("data/courses/" + course['id'] + ".json") is False:
      os.system("curl -H \"Accept: application/json\" \"http://api.pearson.com/kitchen-manager/v1/courses/" + course['id'] + "?limit=200&apikey=9b7305c0523c3902ec01b44e5a5c53ad\" > data/courses/" + course['id'] + ".json")



def print_recipes(courses, i):
  course = courses['results'][i]
  if course['id'] == 'custards-and-creams':
    return
  # print course['id']
  result = json.load(open("data/courses/" + course['id'] + ".json"))
  for recipe in result['recipes']:
    recipe_url = recipe['url']
    os.system("curl -H \"Accept: application/json\" "+ recipe_url +" > \"data/recipes/" + recipe['id'] + ".json\"")
    # print "POSTing\t" + course['id'] + "\t" + recipe['name']
    # print json.dumps(recipe_json)
    # os.system("curl -X POST \"ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:9200/recipes/"+course['id']+"/"+recipe['id']+"\" -d '" + json.dumps(recipe)+"'")

def post_recipes(courses, calories):
  hasCalories = 0
  noCalories = 0
  for course in courses['results']:
    if course['id'] == 'custards-and-creams':
      continue
    # print course['id']
    result = json.load(open("data/courses/" + course['id'] + ".json"))
    for recipe in result['recipes']:
      if calories[recipe['id']] != 0:
        recipe['calories'] = calories[recipe['id']]
        hasCalories += 1
      else:
        print course['id'], recipe['id']
        noCalories += 1
      # print "POSTing\t" + course['id'] + "\t" + recipe['name']
      # print json.dumps(recipe)
      # os.system("curl -X POST \"ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:9200/recipes/"+course['id']+"/"+recipe['id']+"\" -d '" + json.dumps(recipe)+"'")
  print "hasCalories: ", hasCalories
  print "noCalories: ", noCalories

def main():
  courses = json.load(open(sys.argv[1]))
  calories = open(sys.argv[2])
  # i = int(sys.argv[3])
  # write_recipes(courses)
  # print_recipes(courses, i)
  post_recipes(courses, json.load(calories))

if __name__ == '__main__':
  main()
 