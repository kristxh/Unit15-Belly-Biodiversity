function buildMetadata(sample) {

    // Metadata panel   
    var metaDataUrl = `/metadata/${sample}`;

    // Use `d3.json` to fetch the metadata for a sample
    d3.json(metaDataUrl).then(function (response) {

        // Use d3 to select the panel with id of `#sample-metadata`
        var selection = d3.select("#sample-metadata")

        // Use `.html("") to clear any existing metadata
        selection.html("");

        // Use `Object.entries` to add each key and value pair to the panel
        Object.entries(response).forEach(([key, value]) => {
            selection.append("p").text(`${key}: ${value}`);
        })
        // });
        // Gauge Chart
        var level = response.WFREQ;

        // Trig to calc meter point
        var degrees = 140 - level,
            radius = .5;
        var radians = degrees * Math.PI / 180;
        var x = radius * Math.cos(radians);
        var y = radius * Math.sin(radians);

        // Needle path
        var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
            pathX = String(x),
            space = ' ',
            pathY = String(y),
            pathEnd = ' Z';
        var path = mainPath.concat(pathX, space, pathY, pathEnd);

        var gaugeTrace = [{
            type: 'scatter',
            x: [0], 
            y: [0],
            marker: { size: 10, color: 'black' },
            showlegend: false,
            name: 'washes',
            text: level,
            hoverinfo: 'text+name'
        },
        {
            values: [81/9, 81/9, 81/9, 81/9, 81/9, 81/9, 81/9, 81/9, 81/9, 81],
            rotation: 90,
            text: ['8-9','7-8','6-7','5-6', '4-5', '3-4', '2-3','1-2', '0-1', ''],
            textinfo: 'text',
            textposition: 'inside',
            marker: {colors:['#84B589','rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                             'rgba(170, 202, 42, .5)', 'rgba(202, 209, 95, .5)',
                             'rgba(210, 206, 145, .5)', 'rgba(232, 226, 202, .5)',
                             '#F4F1E4','#F8F3EC', 'rgba(255, 255, 255, 0)',]},
            labels: ['8-9','7-8','6-7','5-6', '4-5', '3-4', '2-3','1-2', '0-1', ''],
            hoverinfo: 'label',
            hole: .5,
            type: 'pie',
            showlegend: false
        }];

        var layout = {
            shapes: [{
                type: 'path',
                path: path,
                fillcolor: 'black',
                line: {
                    color: 'black'
                }
            }],
            title: 'Wash Frequency (Per Week)',
            height: 400,
            width: 400,
            xaxis: {
                zeroline: false, showticklabels: false,
                showgrid: false, range: [-1, 1]
            },
            yaxis: {
                zeroline: false, showticklabels: false,
                showgrid: false, range: [-1, 1]
            }
        };
        Plotly.newPlot('gauge', gaugeTrace, layout);
    });
}

function buildCharts(sample) {

    // Use `d3.json` to fetch the sample data for the plots
    var url = `/samples/${sample}`;

    d3.json(url).then(function (response) {
        // Build a Bubble Chart using the sample data
        var xValues = response.otu_ids;
        var yValues = response.sample_values;
        var bubbleData = [
            {
                x: xValues,
                y: yValues,
                mode: "markers",
                type: "scatter",
                text: response.otu_labels,
                size: yValues,
                marker: { size: yValues }
            }
        ];
        var layout = {
            title: 'OTU ID',
            showlegend: false,
            height: 600,
            width: 1400
          };

        Plotly.newPlot("bubble", bubbleData, layout);

        // Build a Pie Chart
        var labels = response.otu_ids.slice(0, 9);
        var values = response.sample_values.slice(0, 9);
        var hoverText = response.otu_labels.slice(0, 9);
        var trace = {
            "labels": labels,
            "values": values,
            "hoverinfo": 'label+percent',
            "type": "pie"
        }

        var layout = {
            title: 'Top 10 Samples',
            autosize: true,
            width: 600,
            height: 600,
            hovermode: 'closest',
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 100,
                pad: 4
            },
        };

        var pieData = [trace]

        Plotly.newPlot("pie", pieData, layout);

    });
}

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/names").then((sampleNames) => {
        sampleNames.forEach((sample) => {
            selector
                .append("option")
                .text(sample)
                .property("value", sample);
        });

        // Use the first sample from the list to build the initial plots
        const firstSample = sampleNames[0];
        buildCharts(firstSample);
        buildMetadata(firstSample);
    });
}

function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    buildCharts(newSample);
    buildMetadata(newSample);
}

// Initialize the dashboard
init();
