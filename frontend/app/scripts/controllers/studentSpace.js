(function () {
    'use strict';

    angular.module('clientApp')
        .controller('StudentSpaceCtrl', ['$scope', '$state',
            function ($scope, $state) {

                $scope.toggleAccordion = toggleAccordion;
                $scope.isOpenAccordion = isOpenAccordion;
                $scope.logout = logout;
                $scope.exportBooklet = exportBooklet;

                init();

                // ---------------------------------------------------------------

                function init() {

                    $scope.periods = [
                        {
                            number : 2,
                            company: {
                                icon : 'add',
                                comment: ''
                            }, 
                            university: {
                                icon : 'add',
                                comment: ''
                            }
                        },{
                            number : 1,
                            company: {
                                icon : 'add',
                                comment: ''
                            }, 
                            university: {
                                icon : 'add',
                                comment: ''
                            }
                        }
                    ];
                }

                function toggleAccordion(value, isCompany, index) {
                    var newValue = (value === 'add') ? 'remove': 'add';
                    if(isCompany === 'true') {
                        $scope.periods[index].company.icon = newValue;
                    } else {
                        $scope.periods[index].university.icon = newValue;
                    }
                }

                function isOpenAccordion(value) {
                    return (value === 'remove');
                }

                function logout() {
                     $state.go('login');
                }

                function exportBooklet() {
                    console.log('export booklet .. TODO ');
                }

                // ---------------------------------------------------------------
                // Public method -------------------------------------------------
                // ---------------------------------------------------------------

            }]);

})();
