// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('edit-form');

//     form.addEventListener('submit', function (e) {
//         e.preventDefault();

//         if (navigator.geolocation) {
//             navigator.geolocation.getCurrentPosition(
//                 function (position) {
//                     document.getElementById("id_lat").value = position.coords.latitude;
//                     document.getElementById("id_lng").value = position.coords.longitude;

//                     console.log("Lat:", position.coords.latitude);
//                     console.log("Lng:", position.coords.longitude);

//                     form.submit();
//                 },
//                 function (error) {
//                     console.error("Geolocation failed:", error.message);
//                     form.submit();
//                 }
//             );
//         } else {
//             console.error("Geolocation is not supported by this browser.");
//             form.submit();
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    document.getElementById("id_lat").value = position.coords.latitude;
                    document.getElementById("id_lng").value = position.coords.longitude;
                    form.submit();
                },
                function (error) {
                    console.error("Geolocation failed:", error.message);
                    form.submit(); // fallback to submitting without location
                }
            );
        } else {
            console.error("Geolocation is not supported by this browser.");
            form.submit();
        }
    });
});
