app.controller('BotCtrl', function($scope, BotPolling) {
  $scope.properties = [];
  $scope.simulators = [];

  // initialization
  $scope.initialize = function(bot) {
    $scope.bot = bot;
    $scope.properties = $scope.bot.properties;

    // TODO
    $scope.ai = { running: false };
  };

  $scope.isPolling = function() {
    return BotPolling.isPolling($scope.bot);
  };

  $scope.pollingRate = function() {
    return BotPolling.pollingRate($scope.bot);
  };

  $scope.data_test = [];

  $scope.updateBot = function(properties, simulators) {
    $scope.data_test = [ //FIXME
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random(),
      Math.random()
    ];

    updateProperties(properties);
    $scope.simulators = simulators;
  };

  var updateProperties = function(newProperties) {
    for (var i in $scope.properties) {
      $scope.properties[i]._exist = false;
    }

    for (var i in newProperties) {
      var prop = newProperties[i];
      var candidats = $scope.properties.filter(function(e) {
        return e.name === prop.name;
      });
      if (candidats.length === 0) {
        prop._exist = true;
        $scope.properties.push(prop);
      }
      else {
        var c = candidats[0];
        c.type = prop.type;
        c.value = prop.value;
        // c.value = [Math.random(), Math.random(), Math.random()]; // FIXME
        c._exist = true;
      }
    }

    for (var i = 0; i < $scope.properties.length; i++) {
      if (!$scope.properties[i]._exist) {
        $scope.properties.splice(i, 1);
        i--;
      }
    }
  };
});
