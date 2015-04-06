"use strict";var app=angular.module("app",["ngRoute","ui.bootstrap"]);app.run(function(API,Bots){API.getBots().then(function(bots){angular.forEach(bots,function(bot){Bots.add(bot.id,bot.address)})})}),app.config(function($routeProvider){var partial=function(name){return"/partials/"+name+".html"};$routeProvider.when("/dashboard",{templateUrl:partial("dashboard"),controller:"DashboardCtrl"}).otherwise({redirectTo:"/dashboard"})}),app.controller("BotCtrl",function($scope,BotPolling){$scope.properties=[],$scope.simulators=[],$scope.initialize=function(bot){$scope.bot=bot,$scope.properties=$scope.bot.properties,$scope.ai={running:!1}},$scope.isPolling=function(){return BotPolling.isPolling($scope.bot)},$scope.pollingRate=function(){return BotPolling.pollingRate($scope.bot)},$scope.data_test=[],$scope.updateBot=function(properties,simulators){$scope.data_test=[Math.random(),Math.random(),Math.random(),Math.random(),Math.random(),Math.random(),Math.random(),Math.random(),Math.random(),Math.random()],updateProperties(properties),$scope.simulators=simulators};var updateProperties=function(newProperties){for(var i in $scope.properties)$scope.properties[i]._exist=!1;for(var i in newProperties){var prop=newProperties[i],candidats=$scope.properties.filter(function(e){return e.name===prop.name});if(0===candidats.length)prop._exist=!0,$scope.properties.push(prop);else{var c=candidats[0];c.type=prop.type,c.value=prop.value,c._exist=!0}}for(var i=0;i<$scope.properties.length;i++)$scope.properties[i]._exist||($scope.properties.splice(i,1),i--)}}),app.controller("DashboardCtrl",function($scope,Bots){$scope.bots=Bots.all()}),app.controller("PollingCtrl",function($scope,BotPolling){$scope.polling=!1,$scope.startPolling=function(rate){$scope.polling||($scope.polling=!0,BotPolling.start($scope.bot,rate).update(function(data){$scope.updateBot(data.properties,data.simulators)}))},$scope.stopPolling=function(){$scope.polling&&($scope.polling=!1,BotPolling.stop($scope.bot))},$scope.restartPolling=function(rate){$scope.stopPolling(),$scope.startPolling(rate)}}),app.controller("SimulatorsCtrl",function($scope,API){$scope.startSimulator=function(name){$scope.simulators[name]=!0,API.startSimulator($scope.bot,name)},$scope.stopSimulator=function(name){$scope.simulators[name]=!1,API.stopSimulator($scope.bot,name)}}),Highcharts.SparkLine=function(options,callback){var defaultOptions={chart:{renderTo:options.chart&&options.chart.renderTo||this,animation:Highcharts.svg,backgroundColor:null,borderWidth:0,type:"area",margin:[2,0,2,0],width:120,height:20,style:{overflow:"visible"},skipClone:!0},title:{text:""},credits:{enabled:!1},xAxis:{labels:{enabled:!1},title:{text:null},startOnTick:!1,endOnTick:!1,tickPositions:[]},yAxis:{endOnTick:!1,startOnTick:!1,labels:{enabled:!1},title:{text:null},tickPositions:[0]},legend:{enabled:!1},tooltip:{useHTML:!0,hideDelay:0,shared:!0,positioner:function(w,h,point){return{x:point.plotX-w/2,y:point.plotY-h}},headerFormat:"",pointFormat:"<b>{point.y}</b>"},plotOptions:{series:{animation:!0,lineWidth:1,shadow:!1,states:{hover:{lineWidth:1}},marker:{radius:0,states:{hover:{radius:2}}},fillOpacity:.25}}};return options=Highcharts.merge(defaultOptions,options),new Highcharts.Chart(options,callback)},app.directive("sparkline",function(){return{restrict:"E",scope:{data:"=",options:"="},link:function(scope,element){var build=function(){var width=$(element[0].parentNode).width(),height=$(element[0].parentNode).height();$(element[0]).highcharts("SparkLine",{chart:{width:width,height:height},series:[{data:scope.data,pointStart:1}]})};scope.$watch("data",function(data){$(element[0]).highcharts()&&$(element[0]).highcharts().series[0].setData(data)},!0),scope.$watch("options",function(){build()})},controller:function(){}}}),app.directive("sparklineEvolution",function($interval){return{restrict:"E",scope:{value:"=",framerate:"=",playing:"=",nbData:"@",options:"="},link:function(scope,element){scope.nbData=parseInt(scope.nbData);var timer=null,build=function(){var width=$(element[0].parentNode).width(),height=$(element[0].parentNode).height();$(element[0]).highcharts("SparkLine",{chart:{width:width,height:height},series:[{data:scope.data,pointStart:1}]})},update=function(){if($(element[0]).highcharts()){var serie=$(element[0]).highcharts().series[0];serie.addPoint(parseFloat(scope.value),!0,serie.data.length>=parseInt(scope.nbData))}};scope.$watch("playing",function(playing){!playing&&timer?($interval.cancel(timer),timer=null):playing&&(timer=$interval(update,parseInt(scope.framerate)))}),scope.$watch("framerate",function(framerate){null!==timer&&($interval.cancel(timer),timer=$interval(update,parseInt(framerate)))}),scope.$watch("options",function(){build()})},controller:function(){}}}),app.service("API",function($http,$q){this.baseUrl="/api",this.getBots=function(){var deferred=$q.defer();return $http.get(this.baseUrl+"/bots").then(function(response){deferred.resolve(response.data.bots)}),deferred.promise},this.botState=function(bot){var deferred=$q.defer(),state={};return this.listProperties(bot).then(function(properties){state.properties=properties,state.simulators&&deferred.resolve(state)}),this.listSimulators(bot).then(function(simulators){state.simulators=simulators,state.properties&&deferred.resolve(state)}),deferred.promise},this.listProperties=function(bot){var deferred=$q.defer();return $http.get(this.baseUrl+"/"+bot.id+"/properties").then(function(response){deferred.resolve(response.data.properties)}),deferred.promise},this.listSimulators=function(bot){var deferred=$q.defer();return $http.get(this.baseUrl+"/"+bot.id+"/simulators").then(function(response){deferred.resolve(response.data.simulators)}),deferred.promise},this.startSimulator=function(bot,simulatorName){var deferred=$q.defer();return $http.post(this.baseUrl+"/"+bot.id+"/simulators/"+simulatorName).then(function(response){deferred.resolve(response.data.simulator)}),deferred.promise},this.stopSimulator=function(bot,simulatorName){var deferred=$q.defer();return $http["delete"](this.baseUrl+"/"+bot.id+"/simulators/"+simulatorName).then(function(response){deferred.resolve(response.data.simulator)}),deferred.promise}}),app.service("BotPolling",function(API,$q,$timeout){this.pollers={},this.rates={},this.start=function(bot,rate){var deferred=$q.defer(),that=this;return that.rates[bot.id]=rate,that.pollers[bot.id]=$timeout(function fn(){API.botState(bot).then(function(data){deferred.notify(data),that.pollers[bot.id]=$timeout(fn,rate)})},rate),{update:function(cb){deferred.promise.then(null,null,cb)}}},this.stop=function(bot){var timeoutId=this.pollers[bot.id];$timeout.cancel(timeoutId),this.pollers[bot.id]=void 0},this.isPolling=function(bot){return void 0!==this.pollers[bot.id]},this.pollingRate=function(bot){return this.rates[bot.id]}}),app.factory("Bots",function(){var bots=[];return{add:function(name,address){bots.push({id:name,address:address,properties:[]})},get:function(name){return bots[name]},all:function(){return bots}}});