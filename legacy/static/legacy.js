
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
            "<a href='/church/" + churches['church_id'][index] + "'>" + churches['church_name'][index] + "</a>" +
            "<table>";

        for (i = 0; i < churches['x'][index].length; i++) {
            details_html += "<tr>";
            details_html += "<td>" + churches['x'][index][i] + "</td>";
            details_html += "<td>" + churches['y'][index][i] + "</td>";
            details_html += "</tr>";
        }
        details_html += "</table>";

        $('.details ' + columnClass).append(details_html);

        currentColumn += 1;
        if (currentColumn > 2) currentColumn = 0;
    });
}

function showHistoryLine(historySource, historyPoints, church_indices) {
    var visibleHistory = {'x0': [], 'y0': [], 'x1': [], 'y1': []};
    for (i = 0; i < church_indices.length; i++) {
        var j = church_indices[i];
        for (k = 0; k < historyPoints['x'][j].length - 1; k++) {
            visibleHistory['x0'].push(historyPoints['x'][j][k]);
            visibleHistory['x1'].push(historyPoints['x'][j][k+1]);
            visibleHistory['y0'].push(historyPoints['y'][j][k]);
            visibleHistory['y1'].push(historyPoints['y'][j][k+1]);
        }
    }
    historySource.data = visibleHistory;
}
