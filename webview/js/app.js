'use strict';

var app = angular.module('app', ['ngRoute', 'ui.bootstrap']);

app.run(function(API, Bots) {
  // load up the available bots
  API.getBots().then(function(bots) {
    angular.forEach(bots, function(bot) {
      Bots.add(bot.id, bot.address);
    });
  });
});
