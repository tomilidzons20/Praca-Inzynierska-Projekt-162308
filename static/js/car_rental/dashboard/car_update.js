const createDataTable = (id) => {
  const sumColumnNumber = 3;
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
    footerCallback: function (row, data, start, end, display) {
      let api = this.api();
      // Remove the formatting to get integer data for summation
      let Val = function (i) {
        return typeof i === 'string'
          ? i.replace(/[\ PLN]/g, '').replace(',', '.') * 1
          : typeof i === 'number'
            ? i
            : 0;
      };
      // Total over all pages
      total = api
        .column(sumColumnNumber)
        .data()
        .reduce((a, b) => Val(a) + Val(b), 0);
      // Total over this page
      pageTotal = api
        .column(sumColumnNumber, { page: 'current' })
        .data()
        .reduce((a, b) => Val(a) + Val(b), 0);
      // Update footer
      api.column(sumColumnNumber).footer().innerHTML =
        pageTotal + ' PLN' + ' (' + total + ' PLN)';
    },
  });
}

$(document).ready(() => {
  createDataTable('#maintenance-table');
})