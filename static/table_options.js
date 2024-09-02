// new DataTable('#table', {
//     fixedHeader: true, 
//     paging: false,
//     // pages: 10,
//     fixedColumns: true,
//     // scrollCollapse: true,
//     scrollX: true,
//     scrolly:10,   
//     // deferRender: true, 
// });

// let table = new DataTable('#table', {
//     fixedHeader: true, 
//     paging: false,
//     // pages: 10,
//     fixedColumns: true,
//     scrollCollapse: true,
//     scrollX: true,
//     scrolly:300,   
// });

// $(document).ready(function() {
//     $('#table').DataTable({
//         fixedHeader: true, 
//         paging: false,
//         fixedColumns: true,
//         // scrollCollapse: true,
//         // scrollX: true,
//         scrolly:300, 
//     });

//     $('#table tbody').on('mouseenter', 'tr', function () {
//         $(this).css('background-color', '#f1f1f3');
//     });

//     $('#table tbody').on('mouseleave', 'tr', function () {
//         $(this).css('background-color', '');
//     }); 
// });

table = $('table').DataTable({
    fixedColumns:true, 
    fixedHeader:true,
    paging: false,
    scrollX: true, 
    scrollY:'80vmin', 
    info:false,
})

$('table').on( 'draw.dt', function () {
    table.columns.adjust();
});

$('#table tbody').on('mouseenter', 'tr', function () {
            $(this).css('background-color', '#f1f1f3');
        });