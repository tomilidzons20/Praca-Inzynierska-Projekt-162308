$(document).on('submit', '#address-form', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    data: form.serialize(),
    success: function(data) {
    console.log('Success:', data);
    $('#address-modal').modal('hide');
    },
    error: function(data) {
    console.log('Error:', data);
    }
  });
});