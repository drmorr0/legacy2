
function reloadWithParams(new_params, values) {
    var uri = new URI(window.location.href);
    params = uri.search(true);
    if (new_params.constructor === Array) {
        $.each(new_params, function(i, p) {
            if (values[i] === null)
                delete params[p];
            else params[p] = values[i];
        });
    }
    else params[new_params] = values;
    window.location.href = uri.search(params);
}

function populateDetailsColumns(property, indices, churches) {
    var currentColumn = 0;
    $('.details h3').text(property)
    $('.details .column-left, .details .column-center, .details .column-right').text('')
    indices.forEach(function(index) {
        var columnClass = '.invalid'
        switch (currentColumn) {
            case 0: columnClass = '.column-left'; break;
            case 1: columnClass = '.column-center'; break;
            case 2: columnClass = '.column-right'; break;
        }

        var details_html = 
            "<div class='church'>" + 
            "<div class='name'>" + churches['church_name'][index] + "</div>";
        for (i = 0; i < churches['x'][index].length; i++) {
            details_html += "<div class='data-point'>";
            details_html += "<span class='x'>" + churches['x'][index][i] + "</span>";
            details_html += "<span class='y'>" + churches['y'][index][i] + "</span>";
            details_html += "</div>";
        }
        details_html += "</div>";

        $('.details ' + columnClass).append(details_html);

        currentColumn += 1;
        if (currentColumn > 2) currentColumn = 0;
    });
}
