app.controller('PollingCtrl', function($scope, BotPolling) {
  $scope.polling = false;

  $scope.startPolling = function(rate) {
    if ($scope.polling) { return; }
    $scope.polling = true;
    BotPolling.start($scope.bot, rate).update(function(data) {
      $scope.updateBot(data.properties, data.simulators);
    });
  };

  $scope.stopPolling = function() {
    if (!$scope.polling) { return; }
    $scope.polling = false;
    BotPolling.stop($scope.bot);
  };

  $scope.restartPolling = function(rate) {
    $scope.stopPolling();
    $scope.startPolling(rate);
  };
});
