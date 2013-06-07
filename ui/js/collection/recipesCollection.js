/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true */
/*global MealPlanner, Backbone*/

MealPlanner.RecipesCollection = Backbone.Collection.extend({
    model : MealPlanner.RecipeModel
});