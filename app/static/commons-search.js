$( "#category-search" ).autocomplete({
    source:
        search_category
});

/**
 * Search for categories on Wikimedia Commons
 * @param request The HTTP request
 * @param respond The Callback
 */
function search_category(request, respond){
    return $.getJSON("http://commons.wikimedia.org/w/api.php?callback=?",
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
