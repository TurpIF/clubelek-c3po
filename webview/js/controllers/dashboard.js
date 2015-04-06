app.controller('DashboardCtrl', function($scope, Bots) {
  $scope.bots = Bots.all();
});
