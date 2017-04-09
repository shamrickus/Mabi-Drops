//todo: incosistent code style

(function() {
	'use strict';

	var app = angular.module('mainApp', ['ngMaterial', 'ngMessages', 'ngAnimate', 'ngMdIcons']);

	app.config(['$interpolateProvider', function($interpolateProvider){
		$interpolateProvider.startSymbol('{a');
		$interpolateProvider.endSymbol('a}');
	}]);

	app.controller("mainCtrl", mainCtrl);

	/*
	//TODO: typescript
	interface IMonster {
		monster_id: string,
		name: string,
		desc: string,
		drop_one_probability: int,
		drop_two_probability: int,
		drop_three_probability: int,
		drop_one: IItem[],
		drop_two: IItem[],
		drop_three: IItem[],
		queried: boolean
	}
	
	interface IItem {
		item_id: string,
		manual_id: string,
		probability: int,
		name: string
	}

	interface IColumn {
		header: string;
		itemTier: string;
		tierKey: string;
	}
	*/

	function mainCtrl($http) {
		var self = this;
		//self.monsters: IMonster[];
		self.monsters = [];
		//self.monsterIndex: int;
		self.monsterIndex;
		//self.monsterText: string;
		self.monsterText = "";
		//self.columns: IColumn[];
		self.columns = [
			{
				"header": "Common",
				//same as index in columns array
				"itemTier": 1,
				"tierKey": "drop_one"
			},
			{
				"header": "Uncommon",
				//same as index in columns array
				"itemTier": 2,
				"tierKey": "drop_two"
			},
			{
				"header": "Rare",
				//same as index in columns array
				"itemTier": 3,
				"tierKey": "drop_three"
			}				
		];

		self.getMonsters = function() {
			if(!self.monsters.length){
				$http.get("/monsters").then(function(result){
					if(result.status == 200){
						self.monsters = result.data;
					}
				})
			}
		}

		self.process = function(result) {
			if(result.status == 200){
				var items = result.data
				console.log(items);
				for(var i = 0; i < items.length; ++i){
					//TODO: should use self.columns instead of magic strings
					var tier_key = "";
					if(items[i].drop_tier == 1) {
						tier_key = "drop_one";
					}
					else if(items[i].drop_tier == 2){
						tier_key = "drop_two";
					}
					else {
						tier_key = "drop_three";
					}
					if (!(tier_key in self.monsters[self.monsterIndex])) {
						self.monsters[self.monsterIndex][tier_key] = [];
					}

					self.monsters[self.monsterIndex][tier_key].push({
						item_id: items[i].item_id || null,
						manual_id: items[i].manual_id || null,
						probability: items[i].probability,
						name: items[i].name
					});
				}
				self.monsters[self.monsterIndex].queried = true;
			}
		}

		self.getManuals = function() {
			if(!self.monsters[self.monsterIndex].queried) {
				$http.get("/manuals/" + self.monsters[self.monsterIndex].monster_id).then(function(result){self.process(result)});
			}
		}

		self.getItems = function() {
			if(!self.monsters[self.monsterIndex].queried) {
				$http.get("/items/" + self.monsters[self.monsterIndex].monster_id).then(function(result){self.process(result)});
			}
		}

		//items: IItem[];
		self.totalItemDrops = function(items) {
			var count = 0;
			for(var i = 0; i < items.length; ++i) {
				count += parseInt(items[i].probability);
			}
			return count;
		}

		//column: IColumn
		//itemProb: int
		self.dropChance = function(column, itemProb) {
			var monster = self.monsters[self.monsterIndex];
			var tierChance = (parseInt(monster[column["tierKey"] + "_probability"]) / 10000)
			return (((tierChance * parseInt(itemProb)) / self.totalItemDrops(monster[column["tierKey"]]))).toFixed(2);
		}

		//column: IColumn
		self.getDropChance = function(column) {
			if(!self.monsterIndex) return;
			return " (" + (parseInt(this.monsters[self.monsterIndex][column.tierKey + "_probability"]) / 1000000).toFixed(4) + ")";
		}
	}
}());
