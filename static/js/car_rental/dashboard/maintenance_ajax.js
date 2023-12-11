$(document).on('submit', '#maintenance-form', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  const table = $('#maintenance-table');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let car;
  if(form.attr('data-car')){
    car = form.attr('data-car');
  } else {
    car = $('#maintenance-form select[name=car]').val()
  }
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    dataType: 'json',
    headers: {
      'X-CSRFToken': csrftoken,
    },
    data: {
      'car': car,
      'date_of_repair': $('#maintenance-form input[name=date_of_repair]').val(),
      'cost_of_repair': $('#maintenance-form input[name=cost_of_repair_0]').val(),
      'status': $('#maintenance-form select[name=status]').val(),
    },
    success: function (data) {
      location.reload();
    },
  });
});