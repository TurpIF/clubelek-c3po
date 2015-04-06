app.controller('SimulatorsCtrl', function($scope, API) {
  $scope.startSimulator = function(name) {
    $scope.simulators[name] = true;
    API.startSimulator($scope.bot, name);
  };

  $scope.stopSimulator = function(name) {
    $scope.simulators[name] = false;
    API.stopSimulator($scope.bot, name);
  };
});
