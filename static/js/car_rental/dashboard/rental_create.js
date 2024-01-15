$(document).on('submit', '#rental-form', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function(xhr, status, error) {
      const errors = JSON.parse(xhr.responseText).errors;
      const container = $('#error-container');
      container.text(errors['__all__']);
      container.attr('class', 'mb-3')
    }
  });
});