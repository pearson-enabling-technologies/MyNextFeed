/*jslint sloppy: true, vars: true, white: true, plusplus: true, newcap: true */
/*global $, MealPlanner, Hogan*/
(function() {
    var resourcesQueue = [];
    var templates = ['recipe', 'meal_criteria_bar'];
    var initView = function(cuisine, ingredient, calories) {
        $.ajax({
            url : 'http://ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:8080/plan/' + calories + '/' + cuisine + '/' + ingredient,
            dataType: 'jsonp'
        }).then(function(plan) {
            var daysContainer = $(".days-container");
            daysContainer.empty();
            var dayViews = plan.days.map(function(day) {
                return new MealPlanner.DayView({
                    model : new MealPlanner.DayModel(day)
                });
            });
            dayViews.forEach(function(view) {
                daysContainer.append(view.$el);
                view.render();
            });
        });
    };
    MealPlanner.templates = {};
    resourcesQueue = resourcesQueue.concat(
        $.ajax({
            url : 'http://ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:8080/cuisines',
            dataType: 'jsonp'
        }),
        $.ajax({
            url : 'http://ec2-54-216-139-182.eu-west-1.compute.amazonaws.com:8080/ingredients/100',
            dataType: 'jsonp'
        }),
        templates.map(function(templateName) {
            var jqxhr = $.get('templates/' + templateName + '.html');
            jqxhr.then(function(templateText) {
                MealPlanner.templates[templateName] = Hogan.compile(templateText);
            });
            return jqxhr;
        })
    );
    $.when.apply(null, resourcesQueue).then(function(cuisines, ingredients) {
        $(function() {

            var criteriaBar = new MealPlanner.MealCriteriaBar({
                cuisines: cuisines[0],
                ingredients: ingredients[0]
            });
            criteriaBar.render();

            criteriaBar.on('submit', function(criteria) {
                criteria = criteria.reduce(function(memo, field) {
                    memo[field.name] = field.value;
                    return memo;
                }, {});
                initView(criteria.cuisine, criteria.ingredient, criteria.calories);
            });

            $("#container h1").after(criteriaBar.$el);
        });
    });
}());