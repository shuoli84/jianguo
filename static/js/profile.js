// Generated by CoffeeScript 1.8.0
(function() {
  $(document).foundation();

  $(document).ajaxSend(function(event, xhr, settings) {
    var getCookie, safeMethod, sameOrigin;
    getCookie = function(name) {
      var cookie, cookieValue, cookies, i, _i, _ref;
      cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = _i = 0, _ref = document.cookie.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
          cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };
    sameOrigin = function(url) {
      var host, origin, protocol, sr_origin;
      host = document.location.host;
      protocol = document.location.protocol;
      sr_origin = '//' + host;
      origin = protocol + sr_origin;
      return (url === origin || url.slice(0, origin.length + 1) === origin + '/') || (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
    };
    safeMethod = function(method) {
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    };
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
      return xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  });

  $('.select-image-btn').click(function() {
    return $('#js-image-input').click();
  });

  $('#js-image-input').change(function() {
    var file, formData;
    file = this.files;
    if (file.length > 0) {
      file = file[0];
    }
    formData = new FormData();
    formData.append('picture', file, file.name);
    $("#js-profile").cropper({
      aspectRatio: 1.0
    });
    $('.btn-set-profile').click(function(e) {
      var data;
      e.preventDefault();
      data = $("#js-profile").cropper("getData");
      console.log(data);
      console.log($('#js-profile').attr('src'));
      return $.ajax({
        url: '/accounts/profile/setProfile/',
        type: 'POST',
        data: {
          x: data.x,
          y: data.y,
          width: data.width,
          height: data.height,
          picture: $('#js-profile').attr('src')
        }
      }).then(function(data) {
        $('#myModal').foundation('reveal', 'close');
        return $('.profile-image').attr('src', data.path);
      }).fail(function(err, xhr) {
        return console.log(err);
      });
    });
    return $.ajax({
      url: '/upload/picture/',
      data: formData,
      processData: false,
      contentType: false,
      type: 'POST'
    }).then(function(data) {
      $('#myModal').foundation('reveal', 'open');
      return $("#js-profile").cropper("setImgSrc", data.path);
    }).fail(function(err, xhr) {
      return console.log(err);
    });
  });

  $('.btn-confirm').click(function() {
    var career, introduction;
    career = $('input[name=career]').val();
    introduction = $('textarea[name=introduction]').val();
    return $.ajax({
      url: '/accounts/profile/',
      data: {
        career: career,
        introduction: introduction
      },
      type: 'POST'
    }).then(function() {
      return console.log('succeeded');
    }).fail(function(err, xhr) {
      return console.log(err);
    });
  });

}).call(this);

//# sourceMappingURL=profile.js.map
