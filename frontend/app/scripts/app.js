'use strict';

/**
 * @ngdoc overview
 * @name clientApp
 * @description
 * # clientApp
 *
 * Main module of the application.
 */
var app = angular.module('clientApp', [
    'ngAnimate',
    'ngCookies',
    'ngSanitize',
    'ngMaterial',
    'ui.router',
    'ngMdIcons',
    'angularFileUpload'
  ]);

app.config(function ($stateProvider, $urlRouterProvider) {

        //Set default route
        $urlRouterProvider.otherwise('/login');

        //Common state
        $stateProvider

        // Common state ------------------------------------------------------------------
        .state('login', {
            url: '/login',
            templateUrl: 'views/login.html',
            controller: 'LoginCtrl'
        })
        
        .state('studentSpace', {
            url: '/espace-etudiant',
            templateUrl: 'views/studentSpace.html',
            controller: 'StudentSpaceCtrl'
        })

        .state('administrationSpace', {
            url: '/espace-secretariat',
            templateUrl: 'views/administrationSpace.html',
            controller: 'AdministrationSpaceCtrl'
        });
    });