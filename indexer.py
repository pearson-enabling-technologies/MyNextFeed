import sys
import json
import os
import random

def write_recipes(courses):
  for course in courses['results']:
    if os.path.isfile("data/courses/" + course['id'] + ".json") is False:
      os.system("curl -H \"Accept: application/json\" \"http://api.pearson.com/kitchen-manager/v1/courses/" + course['id'] + "?limit=200&apikey=9b7305c0523c3902ec01b44e5a5c53ad\" > data/courses/" + course['id'] + ".json")



def post_recipes(courses):
  for course in courses['results']:
    if course['id'] == 'custards-and-creams':
      continue
    # print course['id']
    result = json.load(open("data/courses/" + course['id'] + ".json"))
    for recipe in result['recipes']:
      recipe['calories'] = random.random()
      print "POSTing\t" + course['id'] + "\t" + recipe['name']
      # print json.dumps(recipe)
      # print("curl -X POST \"ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:9200/recipes/"+course['id']+"/"+recipe['id']+"\" -d '" + json.dumps(recipe)+"'")
      os.system("curl -X POST \"ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:9200/recipes/"+course['id']+"/"+recipe['id']+"\" -d '" + json.dumps(recipe)+"'")



def main():
  courses = json.load(open(sys.argv[1]))
  # write_recipes(courses)
  post_recipes(courses)

if __name__ == '__main__':
  main()
