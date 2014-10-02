$(document).foundation()

$('.select-image-btn').click (e)->
  $('#js-image-input').click()

$('#js-image-input').change ->
  file = this.files
  if file.length > 0
    file = file[0]

  formData = new FormData()
  formData.append('picture', file, file.name)

  $.ajax
    url: '/upload/picture/'
    data: formData
    processData: false,
    contentType: false,
    type: 'POST',
  .then (data)->
    console.log data
  .fail (err, xhr)->
    console.log err

