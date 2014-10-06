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
