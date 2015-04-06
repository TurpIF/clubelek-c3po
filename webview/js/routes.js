app.config(function($routeProvider) {
  var partial = function(name) {
    return '/partials/' + name + '.html';
  };

  $routeProvider
    .when('/dashboard', {
      templateUrl: partial('dashboard'),
      controller: 'DashboardCtrl'
    })
    .otherwise({
      redirectTo: '/dashboard'
    })
});
