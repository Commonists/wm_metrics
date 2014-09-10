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
          respond(process_api_results(data));
      });
}

/**
 * Process the MediaWiki api results
 * @param data The MediaWiki JSON response
 */
function process_api_results(data) {
    return data[1].map(cut_category_prefix);
}

/**
 * Cut a prefixed-category string into a non-prefixed
 * @param {String} str The string to cut.
 * @return {String}
 */
function cut_category_prefix(str) {
    return str.substring(9);
}
