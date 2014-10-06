editor = new MediumEditor('.editable')
edited = false

$('.editable').on('input', (e)->
  edited = true
)

$('.editable').mediumInsert
  editor: editor
  addons: {
    images: {
      uploadFile: ($placeholder, file, that)->
        formData = new FormData()
        formData.append('picture', file, file.name)

        $.ajax
          url: '/upload/picture/'
          data: formData
          processData: false,
          contentType: false,
          type: 'POST',
          xhr: ->
            xhr = new XMLHttpRequest()
            xhr.upload.onprogress = that.updateProgressBar
            return xhr
        .then (data)->
          that.uploadCompleted({
            responseText: data.path
          }, $placeholder)
        .fail (err, xhr)->
          that.uploadCompleted({}, $placeholder)
    }
  }

saveArticle = ->
  ob = editor.serialize()
  console.log ob
  $.ajax
    url: '/article/edit/'
    type: 'POST'
    data: {
      'article_id': 1
      title: $('input[name=title]').val()
      content: ob['element-0'].value
    }
  .then (data)->
    console.log 'succeeded'
  .fail (err)->
    console.log 'failed ' + err

$('.btn-save').click (e)->
  e.preventDefault()
  saveArticle()