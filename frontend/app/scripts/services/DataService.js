(function () {
	'use strict';

	angular.module('clientApp')
		.factory('DataService', ['$http', '$q',
			function ($http, $q) {

				// ---------------------------------------------------------------------------
				// PUBLIC API.
				// ---------------------------------------------------------------------------
				return ({
                    login: login,
					logout: logout
				});

				// ---------------------------------------------------------------------------
				// PUBLIC METHODS.
				// ---------------------------------------------------------------------------

				function login(credentials) {
					// var request = $http.post(apiServer + '/api/AppUsers/login', credentials);
					// return request.then(handleSuccess, handleError);
				}

				function logout() {
					// var request = $http.post(apiServer + '/api/AppUsers/logout', {});
					// return request.then(handleSuccess, handleError);
				}

				// ---------------------------------------------------------------------------
				// PRIVATE METHODS.
				// ---------------------------------------------------------------------------

				function handleSuccess(response) {
					return response.data;
				}

				function handleError(response) {
					if (response.data === '' ||
						!angular.isDefined(response.status) ||
						response.statusText === '') {

						return ($q.reject("An unknown error occurred."));
					}

					// Otherwise, use expected error message.
					return ($q.reject('Error ' + response.status + ' (' + response.statusText + '): ' + response.data));
				}
			}
		]);

})();