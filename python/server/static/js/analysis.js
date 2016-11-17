angular.module('Analysis', [
  'ngAnimate',
  'ngCookies',
  'ngRoute',
  'ui.bootstrap',
])

.controller('AnalysisCtrl', ['$scope', '$http', '$location', '$route', '$sce',
  function ($scope, $http, $location, $route, $sce) {
    $scope.videos = []
    $scope.chosen_video_src = ""
    $scope.chosen_video = {}

    var items = $location.$$absUrl.split('/')
    var file = items[items.length - 1]
    $http({
      method: 'GET',
      url: '/api/' + file
    })
      .then(function (response) {
        for (var key in response.data) {
          angular.forEach(response.data[key], function (video) {
            $scope.videos.push(video)
          })
        }
        $scope.chosen_video_src = $sce.trustAsResourceUrl('http://www.dailymotion.com/embed/video/' + $scope.videos[0].id)
        $scope.chosen_video = $scope.videos[0]
      })

    $scope.choose_video = function (video) {
      $scope.chosen_video = video
      $scope.chosen_video_src = $sce.trustAsResourceUrl('http://www.dailymotion.com/embed/video/' + video.id)
      console.log($scope.chosen_video)
    }

}])

.run(['$http', '$cookies',
  function ($http, $cookies) {
    $http.defaults.headers.common['_csrf_token'] = $cookies.csrftoken;
}]);
