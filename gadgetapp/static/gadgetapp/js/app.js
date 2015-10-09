var gadgetapp = angular.module('gadgetapp', ['ui.router', 'ui.bootstrap', 'ngResource', 'ngDragDrop'])

gadgetapp.factory('InventoryService', function ($http) {
    return {
        getInventoryList: function (callback) {
            $http.get('/inventoryapi/').success(callback);
        }
    }
})

gadgetapp.factory('RestaurantService', function ($http) {
    return {
        getRestaurantList: function (callback) {
            $http.get('/restaurantapi/').success(callback);
        }
    }
})

gadgetapp.factory('OrderDetailService', function ($http) {
    return {
        getOrderDetail: function (id, callback) {
            $http.get('/getorderdetail/' + id).success(callback);
        }
    }
})

gadgetapp.factory('UserService', function ($http) {
    return {
        getUserList: function (callback) {
            $http.get('/userapi/').success(callback);
        }
    }
})

gadgetapp.factory('UserIdService', function ($http) {
    return {
        getUser: function (callback) {
            $http.get('/getuser/').success(callback);
        }
    }
})

gadgetapp.factory('GetLatestOrder', function ($http) {
    return {
        getOrder: function (callback) {
            $http.get('/getlatestorderuser/').success(callback);
        }
    }
})

gadgetapp.factory('UserDashboardService', function ($http) {
    return {
        getOrder: function (callback) {
            $http.get('/userdashboardlist/').success(callback);
        }
    }
})

gadgetapp.config(function ($stateProvider, $urlRouterProvider, $httpProvider) {

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $stateProvider
        .state('menu', {
            url: "/menu/",
            templateUrl: "/menu"
        })
        .state('confirm', {
            url: "/confirmorder",
            templateUrl: "/confirmorder"
        })
        .state('checkout', {
            url: "/checkout",
            templateUrl: "/checkout"
        })
});

gadgetapp.service('ItemService', function () {

    my_items = [];
    minimum = 0;

    var addItem = function (newObj) {
        i = my_items.indexOf(newObj);
        if (i == -1) {
            newObj['quantity'] = 1;
            my_items.push(newObj);
        }
        else {
            my_items[i]['quantity'] += 1;
        }
    };

    var removeItem = function (newObj) {
        var toRemove = newObj;
        var indexOf = my_items.indexOf(toRemove);
        my_items.splice(indexOf, 1);
    };

    var resetItems = function () {
        my_items.length = 0;
    };

    var getItems = function () {
        return my_items;
    };

    var getMinimum = function (value) {
        minimum = value;
        return minimum;
    };

    var getMinimum2 = function () {
        return minimum;
    };

    return {
        addItem: addItem,
        removeItem: removeItem,
        resetItems: resetItems,
        getItems: getItems,
        getMinimum: getMinimum,
        getMinimum2: getMinimum2
    };
});

gadgetapp.controller('MenuCtrl', function ($scope, $http, $state, $stateParams, InventoryService, ItemService) {

    InventoryService.getInventoryList(function (data) {
        if (data != null) {
            $scope.menu_items = data;
        }
    });

    $scope.total = 0;
    $scope.toRemove = [];
    $scope.my_items = ItemService.getItems();

    $scope.sum = function () {
        $scope.total = 0
        for (var i = 0, _len = $scope.my_items.length; i < _len; i++) {
            $scope.total += $scope.my_items[i]['quantity'] * $scope.my_items[i]['price'];
        }
        return $scope.total;
    };

    $scope.myCheckPush = function (item) {
        ItemService.addItem(item);
        $scope.sum();
    }

    $scope.myCheckRemove = function (item) {
        ItemService.removeItem(item);
        $scope.sum();
    };

    $scope.reset = function () {
        ItemService.resetItems();
        $scope.sum();
    };
});

gadgetapp.controller('ConfirmCtrl', function ($scope, $state, $stateParams, $http, ItemService) {

    $scope.my_items = ItemService.getItems();
    $scope.notes = "";

    $scope.sum = function () {
        total = 0
        for (var i = 0, _len = $scope.my_items.length; i < _len; i++) {
            total += $scope.my_items[i]['quantity'] * $scope.my_items[i]['price'];
        }
        return total;
    };

    $scope.checkout = function(){
        var variablesToSend = angular.toJson($scope.my_items);

        var more_variables =    {
                                    "notes": $scope.notes,
                                }
        
        $http.post('/postorder/', variablesToSend).then(function(response){

            $http.post('/postnotes/', more_variables).then(function (response) {
                $state.go('checkout');
                console.log(response);
            }, function (response) {
                alert('Unable to post notes');
                console.log(response);
            });

        }, function (response) {
            alert('Unable to post order');
            console.log(response);
        });
    }
});

gadgetapp.controller('CheckoutCtrl', function ($scope, $state, $stateParams, $http, GetLatestOrder) {

    $scope.GetData = function () {
        GetLatestOrder.getOrder(function (data) {
            if (data != null) {
                $scope.order = data[0];
                $scope.order_items = $scope.order.orders;
                $scope.customer = $scope.order.customer;
                if ($scope.order.order_type == "PI")
                    $scope.order_type = "Pickup";
                else
                    $scope.order_type = "Parcel";

                if ($scope.order.order_status == 'R') {
                    $scope.progress_type = 'Received';
                }
                else if ($scope.order.order_status == 'P' || $scope.order.order_status == 'A') {
                    $scope.progress_type = 'Accepted';
                }
                else if ($scope.order.order_status == 'D') {
                    $scope.progress_type = 'Delivered';
                }
                else if ($scope.order.order_status == 'RE') {
                    $scope.progress_type = 'Rejected';
                }
            }
        });
    }

    $scope.getPercentage = function () {
        if ($scope.progress_type == 'Received') {
            return 33;
        }
        else if ($scope.progress_type == 'Accepted') {
            return 66;
        }
        else if ($scope.progress_type == 'Delivered') {
            return 100;
        }
    };

    $scope.getProgressType = function () {
        var percent = $scope.getPercentage();
        if (percent < 40) return 'primary';
        if (percent < 70) return 'warning';
        if (percent == 100) return 'success';
    };

    $scope.GetData();

    setInterval($scope.GetData, 10000);
});

gadgetapp.controller('RestaurantCtrl', function ($scope, $modal, $state, $stateParams, $http, RestaurantService) {

    $scope.currentPageReceived = 1;
    $scope.currentPagePending = 1;
    $scope.currentPageDelivered = 1;
    $scope.currentPageRejected = 1;
    $scope.numPerPage = 5;

    $scope.getData = function () {

        RestaurantService.getRestaurantList(function (data) {
            if (data != null) {
                $scope.order_items = data;

                $scope.received = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'R');
                }));
                $scope.pending = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'P' || item.order_status == 'A');
                }));
                $scope.delivered = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'D');
                }));
                $scope.rejected = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'RE');
                }));
                $scope.totalReceived = $scope.received.length;
                $scope.totalPending = $scope.pending.length;
                $scope.totalDelivered = $scope.delivered.length;
                $scope.totalRejected = $scope.rejected.length;
            }
        });

    };

    $scope.getData();

    $scope.paginatereceived = function (value) {
        var begin, end, index;
        begin = ($scope.currentPageReceived - 1) * $scope.numPerPage;
        end = begin + $scope.numPerPage;
        index = $scope.received.indexOf(value);
        return (begin <= index && index < end);
    };

    $scope.paginatepending = function (value) {
        var begin, end, index;
        begin = ($scope.currentPagePending - 1) * $scope.numPerPage;
        end = begin + $scope.numPerPage;
        index = $scope.pending.indexOf(value);
        return (begin <= index && index < end);
    };

    $scope.paginatedelivered = function (value) {
        var begin, end, index;
        begin = ($scope.currentPageDelivered - 1) * $scope.numPerPage;
        end = begin + $scope.numPerPage;
        index = $scope.delivered.indexOf(value);
        return (begin <= index && index < end);
    };

    $scope.paginaterejected = function (value) {
        var begin, end, index;
        begin = ($scope.currentPageRejected - 1) * $scope.numPerPage;
        end = begin + $scope.numPerPage;
        index = $scope.rejected.indexOf(value);
        return (begin <= index && index < end);
    };

    $scope.changeorderstatus = function (order_id, status) {
        $http.get('/changeorderstatus/' + order_id + '/' + status);
    };

    $scope.dropSuccessHandler = function ($event, index, array) {
        array.splice(index, 1);
    };

    $scope.onDrop = function ($event, $data, array) {
        array.push($data);
        if (array == $scope.received)
            $scope.changeorderstatus($data.id, 'R');
        else if (array == $scope.pending)
            $scope.changeorderstatus($data.id, 'P');
        else if (array == $scope.delivered)
            $scope.changeorderstatus($data.id, 'D');
        else if (array == $scope.rejected)
            $scope.changeorderstatus($data.id, 'RE');
    };

    $scope.open = function (id) {
        var modalInstance = $modal.open({
            templateUrl: 'myOrderContent.html',
            controller: OrderInstanceCtrl,
            resolve: {
                order_id: function () {
                    return id;
                }
            }
        });
    };

    setInterval($scope.getData, 5000);
});

var OrderInstanceCtrl = function ($scope, $http, $log, $modalInstance, order_id, OrderDetailService) {

    $scope.order_id = order_id;
    $scope.reject_notes = "";

    OrderDetailService.getOrderDetail($scope.order_id, function (data) {
        if (data != null) {
            $scope.order = data[0];
            $scope.order_items = $scope.order.orders;
            $scope.customer = $scope.order.customer;

            if ($scope.order.order_type == "PI")
                $scope.order_type = "Pickup";
            else
                $scope.order_type = "Parcel";
        }
    });

    $scope.changeorderstatus = function (order_id, status) {
        $http.get('/changeorderstatus/' + order_id + '/' + status);
    };

    $scope.acceptorder = function () {
        $scope.changeorderstatus($scope.order_id, 'A');
        $modalInstance.dismiss('close');
    };

    $scope.completeorder = function () {
        $scope.changeorderstatus($scope.order_id, 'D');
        $modalInstance.dismiss('close');
    };

    $scope.rejectorder = function (notes) {
        var more_variables = {
            "comments": notes,
            "order_id": $scope.order_id,
        }
        $http.post('/postcomments/', more_variables).then(function (response) {
            $scope.changeorderstatus($scope.order_id, 'RE');
            $modalInstance.dismiss('close');
        }, function (response) {
            alert('Unable to post comment');
            console.log(response);
        });
    };

    $scope.close = function () {
        $modalInstance.dismiss('close');
    };
};

gadgetapp.controller('UserCtrl', function ($scope, $rootScope, $state, $stateParams, $http, UserService, UserDashboardService) {

    $scope.received = 0;
    $scope.pending = 0;
    $scope.delivered = 0;
    $scope.rejected = 0;

    $scope.GetData = function () {
        UserService.getUserList(function (data) {
            if (data != null) {
                $scope.order_items = data;

                $scope.received = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'R');
                }));
                $scope.pending = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'P' || item.order_status == 'A');
                }));
                $scope.delivered = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'D');
                }));
                $scope.rejected = ($scope.order_items.filter(function (item) {
                    return (item.order_status == 'RE');
                }));
            }
        });

        UserDashboardService.getOrder(function (data) {
            if (data != null) {
                $scope.order = data;
            }
        });
    }

    $scope.getPercentage = function (item) {
        if (item.order_status == 'R') {
            $scope.progress_type = 'Received';
            return 33;
        }
        else if (item.order_status == 'P' || item.order_status == 'A') {
            $scope.progress_type = 'Accepted';
            return 66;
        }
        else if (item.order_status == 'D') {
            $scope.progress_type = 'Delivered';
            return 100;
        }
    };

    $scope.getProgressType = function (item) {
        var percent = $scope.getPercentage(item);
        if (percent < 40) return 'primary';
        if (percent < 70) return 'warning';
        if (percent == 100) return 'success';
    };

    $scope.GetData();

    setInterval($scope.GetData, 10000);
});