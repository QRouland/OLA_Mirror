(function () {
    'use strict';
    
    angular.module('clientApp')
        .controller('ResponsableFormationSpaceCtrl', ['$scope', '$state', '$log', '$filter',
            function ($scope, $state, $log, $filter) {
              var imagePath = '../images/icon.png';
                $scope.logout = logout;
                $scope.tabs = [];
                init();
                
                function init() {
                    $scope.selectedIndex = 0;
                    var tabs = [
                    {//periode 1
                        "id":1,
                      "title": 'One',
                      "periodes": [//periodes pour tab0
                          {"id":1, "plages": [//Plage pour periode 1
                            {"id": 0,"name": "null"}
                            ]
                            
                          }
                        ],
                      "students": [ {"face" : imagePath, "nom_prenom": 'Normand Léa'} ]
                    },
                    {//periode 2
                        "id":2,
                      "title": 'Two',
                      "periodes": [],
                      "students": []
                    }],
                    selected = null,
                    previous = null;
                    $scope.tabs = tabs;
                    $scope.$watch('selectedIndex', function(current, old){
                      previous = selected;
                      selected = tabs[current];
                      if ( old + 1 && (old != current)) $log.debug('Goodbye ' + previous.title + '!');
                      if ( current + 1 )                $log.debug('Hello ' + selected.title + '!');
                    });
                }
                    $scope.addTab = function (title) {
                      //view = view || title + " Content View";
                      $scope.tabs.push({ title: title, disabled: false, periodes: [] });
                    };
                    $scope.removeTab = function (indexTab) {
                      $scope.tabs.splice(indexTab, 1);
                    };
                    $scope.addRecordPeriode = function(id_tab){
                      var temp = $filter('filter')(  $scope.tabs , {id: id_tab })[0];
                      temp.periodes.push({"id": temp.periodes.length + 1, "plages":[]});
                    }
                    $scope.addRecordPlage = function(id_tab, id_periode){
                      var temp = $filter('filter')(  $scope.tabs , {id: id_tab })[0];
                      var temp2 = $filter('filter')(  temp.periodes, {id: id_periode })[0];
                      temp2.plages.push({"id": id_periode + 1,"name": "null"});
                    }
                    $scope.addStudent = function(id_tab,nom_pre_s) {
                      var temp = $filter('filter')(  $scope.tabs , {id: id_tab })[0];
                      temp.students.push({ face: imagePath, nom_prenom: nom_pre_s });
                    };
  
          function logout() {
              $state.go('login');
          }
  
      }]);
  
})();