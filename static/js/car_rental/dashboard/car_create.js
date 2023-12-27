$(document).on('submit', '#car-form', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  const formData = new FormData(form[0]);
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      location.reload();
    },
    error: function(data) {
      console.log('Error:', data);
    }
  });
});