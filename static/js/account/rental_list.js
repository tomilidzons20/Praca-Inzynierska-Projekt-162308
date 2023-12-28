const createDataTable = (id, column) => {
  let table = new DataTable(id, {
    "autoWidth": true,
    responsive: {
      details: {
        display: $.fn.dataTable.Responsive.display.modal({
          header: (row) => {
            const data = row.data();
            const rowIndex = row.index() + 1
            return 'Details for ' + rowIndex + ''
          }
        }),
        renderer: $.fn.dataTable.Responsive.renderer.tableAll(),
      }
    },
    "info": false,
    "searching": false,
    columnDefs: [
      { orderable: false, targets: column }
    ],
    order: [[2, 'desc']],
  });
}

$(document).ready(() => {
  createDataTable('#car-rental-table', 5);
})