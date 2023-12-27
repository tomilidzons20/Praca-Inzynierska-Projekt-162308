$(document).on('submit', '#maintenance-form', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function(data) {
      console.log('Error:', data);
    }
  });
});