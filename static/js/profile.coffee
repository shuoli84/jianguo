$('.select-image-btn').click ->
  $('#js-image-input').click()

$('#js-image-input').change ->
  file = this.files
  if file.length > 0
    file = file[0]

  formData = new FormData()
  formData.append('picture', file, file.name)


  $("#js-profile").cropper
      aspectRatio: 1.0

  $('.btn-set-profile').click (e)->
    e.preventDefault()
    data = $("#js-profile").cropper("getData")
    console.log data
    console.log $('#js-profile').attr('src')
    $.ajax
      url: '/accounts/profile/setProfile/',
      type: 'POST'
      data:{
        x: data.x
        y: data.y
        width: data.width
        height: data.height
        picture: $('#js-profile').attr('src')
      }
    .then (data)->
      $('#myModal').foundation('reveal', 'close')
      $('.profile-image').attr('src', data.path)
    .fail (err, xhr)->
      console.log err

  $.ajax
    url: '/upload/picture/'
    data: formData
    processData: false,
    contentType: false,
    type: 'POST',
  .then (data)->
    $('#myModal').foundation('reveal', 'open')
    $("#js-profile").cropper("setImgSrc", data.path)
  .fail (err, xhr)->
    console.log err

$('.btn-confirm').click ->
  career = $('input[name=career]').val()
  introduction = $('textarea[name=introduction]').val()

  $.ajax
    url: '/accounts/profile/'
    data: {
      career: career
      introduction: introduction
    }
    type: 'POST'
  .then ->
    console.log 'succeeded'
  .fail (err, xhr)->
    console.log err
