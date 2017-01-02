
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

function getElementsAt(array, indices, keys) {
    var els = [];
    indices.forEach(function(i) { 
        var obj = {};
        keys.forEach(function(key) { obj[key] = array[key][i]; });
        els.push(obj);
    });
    return els;
}

function makeChurchesDetailsArray(prop1, prop2, churches) {
    var details = [];
    churches.forEach(function(church) {
        var html = "<div class='church'>" +
            "<a href='church/" + church['church_id'] + "'>" + church['church_name'] + "</a>" +
            "<table><tr><th>" + prop1 + "</th><th>" + prop2 + "</th><tr>";
        for(i = 0; i < church['x'].length; i++)
            html += "<tr><td>" + church['x'][i] + "</td>" +
                    "<td>" + church['y'][i] + "</td></tr>";
        html += "</table></div>";
        details.push(html);
    });
    return details;
}

function makeChurchList(property, prop_string, churches) {
    var html = "<div class='church_list'>" + 
        "<table><tr><th>Church</th><th>" + prop_string + "</th>";
    churches.forEach(function(church) {
        html += "<tr><td><a href='/church/" + church['church_id'] + "'>"
            + church['name'] + "</a></td><td>" + church[property] + "</td>";
    });
    html += "</table></div>";
    return [html];
}

function makeChurchComparisonList(prop0_string, prop1_string, churches) {
    var html = "<div class='church_list'>" + 
        "<table><tr><th>Church</th><th>" + prop0_string + "</th><th>" + prop1_string + "</th>";
    churches.forEach(function(church) {
        html += "<tr><td><a href='/church/" + church['church_id'] + "'>"
            + church['church_name'] + "</a></td><td>" + church['x'] + "</td><td>" + church['y'] + "</td></tr>";
    });
    html += "</table></div>";
    return [html];
}

function populateDetailsColumns(details) {
    var currentColumn = 0;
    var columnClass = '.invalid'
    $('.details .column-left, .details .column-center, .details .column-right').text('')
    details.forEach(function(html) {
        switch (currentColumn) {
            case 0: columnClass = '.column-left'; break;
            case 1: columnClass = '.column-center'; break;
            case 2: columnClass = '.column-right'; break;
        }

        $('.details ' + columnClass).append(html);

        currentColumn += 1;
        if (currentColumn > 2) 
            currentColumn = 0;
    });
}

function histogramSliderCallback(year, property, histBins, histItems, maxVals, plot, barData) {
    plot.title["text"] = property + " in " + year;
    histCounts = histItems[year].map(function(c) { return c.length; });
    plot.x_range.end = Math.max(...histBins[year]);
    plot.y_range.end = Math.max(...histCounts);
    var barWidth  = histBins[year][1] - histBins[year][0];
    barData.data['top'] = histCounts;
    barData.data['left'] = histBins[year].map(function(x) { return Math.round( x - barWidth / 2); });
    barData.data['right'] = histBins[year].map(function(x) { return Math.round(x + barWidth / 2); });
    barData.data['right'][histBins[year].length - 1] = maxVals[year];
    barData.data['items'] = histItems[year];
    barData.data['x'] = histBins[year];
    barData.data['width'] = Array(histBins[year].length).fill(barWidth);
    barData.trigger('change');
}

function showHistoryLine(comparisonData, hoverData, history, churchIndices) {

    var newSegments = {'x0': [], 'x1': [], 'y0': [], 'y1': []}
    churchIndices.forEach(function(j) {
        for (k = 0; k < history['x'][j].length - 1; k++) {
            newSegments['x0'].push(history['x'][j][k]);
            newSegments['x1'].push(history['x'][j][k+1]);
            newSegments['y0'].push(history['y'][j][k]);
            newSegments['y1'].push(history['y'][j][k+1]);
        }
    });

    hoverData.data = newSegments;
}
