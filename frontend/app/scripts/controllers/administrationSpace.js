(function () {
  'use strict';

  /**
   * @ngdoc function
   * @name frontendApp.controller:AdministrationSpaceCtrl
   * @description
   * # AdministrationSpaceCtrl
   * Controller of the frontendApp
   */
  angular.module('clientApp')
    .controller('AdministrationSpaceCtrl', function ($scope, $state, $mdDialog, FileUploader) {

      angular.extend($scope, {
        logout,
        deleteAbsence,
        deleteTrackingSheet,
        importAbsences,
        importVisitSheets
      })

      init();

      // Public methods -------------------  

      function logout() {
        $state.go('login');
      }

      function deleteAbsence(groupIndex, periodIndex, absenceIndex) {
        $scope.formationGroups[groupIndex].formattedAbsences[periodIndex].absences.splice(absenceIndex, 1);
      }

      function deleteTrackingSheet(groupIndex, trackingSheetIndex) {
        $scope.formationGroups[groupIndex].trackingSheets.splice(trackingSheetIndex, 1);
      }

      function importVisitSheets(ev) {
        $mdDialog.show({
          controller: 'AdministrationDialogCtrl',
          templateUrl: 'import-fiches-visite',
          parent: angular.element(document.body),
          targetEvent: ev,
          clickOutsideToClose: true,
          fullscreen: 'false',
          locals : { type : 'visit'}
        })
          .then(function (answer) {
            $scope.status = 'You said the information was "' + answer + '".';
          }, function () {
            $scope.status = 'You cancelled the dialog.';
          });
      }

      function importAbsences(ev) {
        $mdDialog.show({
          controller: 'AdministrationDialogCtrl',
          templateUrl: 'import-fiches-absences',
          parent: angular.element(document.body),
          targetEvent: ev,
          clickOutsideToClose: true,
          fullscreen: 'false',
          locals : { type : 'absence'}
        })
          .then(function (answer) {
            $scope.status = 'You said the information was "' + answer + '".';
          }, function () {
            $scope.status = 'You cancelled the dialog.';
          });
      }

      // Private methods ------------------

      function init() {
        var formationGroups = [{
          label: "Master2 ICE",
          absences: [
            { id: 1, title: "Absence_Matthieu_Penchenat_P1" },
            { id: 2, title: "Absence_Renan_Husson_P1" },
            { id: 3, title: "Absence_Renan_Husson_P2" },
            { id: 1, title: "Absence_Renan_Husson_P3" },
            { id: 2, title: "Absence_Matthieu_Penchenat_P2" },
            { id: 3, title: "Absence_Matthieu_Penchenat_P3" },
            { id: 1, title: "Absence_Quentin_Rouland_P1" },
            { id: 2, title: "Absence_Quentin_Rouland_P2" },
            { id: 3, title: "Absence_Quentin_Rouland_P3" },
            { id: 1, title: "Absence_Sitan_Coulibaly_P1" },
            { id: 2, title: "Absence_Sitan_Coulibaly_P2" },
            { id: 3, title: "Absence_Sitan_Coulibaly_P3" }
          ],
          trackingSheets: [
            { id: 3, fileName: "FicheVisite_Sitan_Coulibaly_1" },
            { id: 2, fileName: "FicheVisite_Sitan_Coulibaly_2" },
            { id: 1, fileName: "FicheVisite_Sitan_Coulibaly_3" }
          ]
        }, {
          label: "Master1 ISMAG",
          absences: [
            { id: 1, title: "Absence_Matthieu_Penchenat_P1" },
            { id: 2, title: "Absence_Matthieu_Penchenat_P2" },
            { id: 3, title: "Absence_Matthieu_Penchenat_P3" }
          ],
          trackingSheets: [
            { id: 3, fileName: "FicheVisite_Renan_Husson_1" },
            { id: 2, fileName: "FicheVisite_Renan_Husson_2" },
            { id: 1, fileName: "FicheVisite_Renan_Husson_3" }
          ]
        }];

        $scope.formationGroups = formationGroups.map(function (formationGroup) {
          formationGroup.formattedAbsences = reformatAbsences(formationGroup.absences);
          return formationGroup;
        });
      }

      function reformatAbsences(absences) {
        var myObj = _.groupBy(absences, function (absence) { return absence.title.split('_').pop(); });

        return _.map(myObj, function (value, index) {
          return { period: index, absences: value };
        });
      }
    });

})();