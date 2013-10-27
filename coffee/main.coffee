mainApp = angular.module("mainApp",
  ["ngRoute", "metrics.controllers"])

mainApp.config ["$routeProvider", ($routeProvider) ->
  $routeProvider.when("/:user/:repo",
    templateUrl: "partials/repo.html"
    controller: "HomeCtrl"
  ).when("/",
    templateUrl: "partials/home.html"
    controller: "HomeCtrl"
  ).otherwise redirectTo: "/"
]


mainControllers = angular.module("metrics.controllers", [])
mainControllers.controller('HomeCtrl', ['$scope', 'Phone',
  ($scope, Phone) ->
  ])
