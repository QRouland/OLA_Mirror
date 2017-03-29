(function () {
    'use strict';


    angular.module('clientApp')
        .filter('fileName', function () {

            return function (queue, type) {

                var reg = (type === 'absence') ?/^Absence_[A-Z][a-z]*_[A-Z][a-z]*_P\d*.pdf$/ : /^Visite_[A-Z][a-z]*_[A-Z][a-z]*_P\d*.pdf$/;
                return queue.filter(function (item) {
                    return reg.test(item.file.name);
                });
            };
        })
        .filter('illegalFileNames', function () {

            return function (queue, type) {

                var reg = (type === 'absence') ?/^Absence_[A-Z][a-z]*_[A-Z][a-z]*_P\d*.pdf$/ : /^Visite_[A-Z][a-z]*_[A-Z][a-z]*_P\d*.pdf$/;
                return queue.filter(function (item) {
                    return !reg.test(item.file.name);
                }).map(function(item) {
                    return item.file.name;
                });
            };
        });
})();