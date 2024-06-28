// new DataTable('#table'); 
// $(document).ready(function (){
//     $('#table').DataTable({
//         dom: 'Bfrtip', 
//         // pageLength:25,
//         paging: false,
//         fixedHeader:{
//             header: true
//         }
//     });
// });
// $.fn.dataTable.FixedHeader.defaults
new DataTable('#table', {
    // dom: 'PRS', 
    fixedHeader: true, 
    // pageLength:100
    paging: false
});