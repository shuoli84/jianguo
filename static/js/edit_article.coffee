editor = new MediumEditor('.editable')
edited = false

$('.editable').on('input', (e)->
  edited = true
)

setInterval ->
  if edited
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

    edited = false
, 20000
