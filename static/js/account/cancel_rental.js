$(document).ready(() => {
  $('.rental-button').on('click', (e) => {
    const argument = $(e.currentTarget).attr('data-rental-id');
    $('#rental-id').val(argument);
  });
})


$(document).on('submit', '#cancel-rental', (e) => {
  e.preventDefault();
  const form = $(e.currentTarget);
  $.ajax({
    type: 'POST',
    url: form.attr('data-url'),
    data: form.serialize(),
    success: function(data) {
      location.reload();
    },
    error: function(data) {
      console.log('Error:', data);
    }
  });
});