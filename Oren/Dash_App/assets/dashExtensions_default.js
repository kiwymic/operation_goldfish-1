window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
            const icon_church = L.icon({
                iconUrl: './assets/icon_church.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_church
            });
        },
        function1: function(feature, latlng) {
            const icon_public = L.icon({
                iconUrl: './assets/icon_public.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_public
            });
        },
        function2: function(feature, latlng) {
            const icon_health = L.icon({
                iconUrl: './assets/icon_health.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_health
            });
        },
        function3: function(feature, latlng) {
            const icon_parks = L.icon({
                iconUrl: './assets/icon_parks.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_parks
            });
        },
        function4: function(feature, latlng) {
            const icon_food = L.icon({
                iconUrl: './assets/icon_food.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_food
            });
        },
        function5: function(feature, latlng) {
            const icon_hotel = L.icon({
                iconUrl: './assets/icon_hotel.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_hotel
            });
        },
        function6: function(feature, latlng) {
            const icon_shop = L.icon({
                iconUrl: './assets/icon_shop.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_shop
            });
        },
        function7: function(feature, latlng) {
            const icon_finance = L.icon({
                iconUrl: './assets/icon_finance.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_finance
            });
        },
        function8: function(feature, latlng) {
            const icon_tourism = L.icon({
                iconUrl: './assets/icon_tourism.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_tourism
            });
        },
        function9: function(feature, latlng) {
            const icon_fountain = L.icon({
                iconUrl: './assets/icon_fountain.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_fountain
            });
        },
        function10: function(feature, latlng) {
            const icon_misc = L.icon({
                iconUrl: './assets/icon_misc.png',
                iconSize: [15, 25]
            });
            return L.marker(latlng, {
                icon: icon_misc
            });
        },
        function11: function(feature, context) {
            return context.props.hideout.name.includes(feature.properties.PID);
        }
    }
});