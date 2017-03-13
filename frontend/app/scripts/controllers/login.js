(function () {
  'use strict';

  /**
   * @ngdoc function
   * @name frontendApp.controller:MainCtrl
   * @description
   * # MainCtrl
   * Controller of the frontendApp
   */
  angular.module('clientApp')
    .controller('LoginCtrl', function ($scope, $state) {

      $scope.login = login;

      // Public methods -------------------  

      function login() {
        console.log('login');

        $state.go('userspace');
      }

      // Private methods ------------------
    });

})();