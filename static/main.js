(function() {
	'use strict';

	var app = angular.module('mainApp', ['ngMaterial', 'ngMessages', 'ngAnimate', 'ngMdIcons']);

	app.config(['$interpolateProvider', function($interpolateProvider){
		$interpolateProvider.startSymbol('{a');
		$interpolateProvider.endSymbol('a}');
	}]);

	app.controller("mainCtrl", mainCtrl);

	function mainCtrl($http) {
		var self = this;

		self.getItems = function() {
			$http.get("/monsters").then(function(result){
				if(result.status == 200){
					self.monsters = result.data;
				}
			})
		}

		self.getMonsters = function() {

			$http.get("/items/" + self.monster).then(function(result){
				if(result.status == 200){
					self.items = result.data
					console.log(self.items)
				}
			})
		}
	}
}());
