(function() {
  var mainApp, mainControllers;

  mainApp = angular.module("mainApp", ["ngRoute", "metrics.controllers"]);

  mainApp.config([
    "$routeProvider", function($routeProvider) {
      return $routeProvider.when("/:user/:repo", {
        templateUrl: "partials/repo.html",
        controller: "HomeCtrl"
      }).when("/", {
        templateUrl: "partials/home.html",
        controller: "HomeCtrl"
      }).otherwise({
        redirectTo: "/"
      });
    }
  ]);

  mainControllers = angular.module("metrics.controllers", []);

  mainControllers.controller('HomeCtrl', ['$scope', 'Phone', function($scope, Phone) {}]);

}).call(this);
