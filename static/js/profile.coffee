$(document).foundation()

$(document).ajaxSend (event, xhr, settings)->
  getCookie = (name)->
    cookieValue = null
    if document.cookie and document.cookie != ''
      cookies = document.cookie.split(';')
      for i in [0..document.cookie.length-1]
        cookie = jQuery.trim(cookies[i])
        if (cookie.substring(0, name.length + 1) == (name + '='))
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
    cookieValue

  sameOrigin = (url)->
    host = document.location.host
    protocol = document.location.protocol
    sr_origin = '//' + host
    origin = protocol + sr_origin
    (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      !(/^(\/\/|http:|https:).*/.test(url))

  safeMethod = (method)->
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

  if not safeMethod(settings.type) and sameOrigin(settings.url)
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))

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
