$( "#category-search" ).autocomplete({
    source:
        function( request, respond ) {
            $.getJSON("http://commons.wikimedia.org/w/api.php?callback=?",
                      {
                          search: request.term,
                          action: "opensearch",
                          format: "json",
                          namespace: 14
                      },
                      function( data ) {
                          respond(data[1]);
                      });
        }
});

