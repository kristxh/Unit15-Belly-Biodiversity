function buildMetadata(sample) {

     // Metadata panel   
    var metaDataUrl = `/metadata/${sample}`;

    // Use `d3.json` to fetch the metadata for a sample
    d3.json(metaDataUrl).then(function(response) {
      console.log(response);   
  
      // Use d3 to select the panel with id of `#sample-metadata`
      var selection = d3.select("#sample-metadata")
  
      // Use `.html("") to clear any existing metadata
      selection.html("");
  
      // Use `Object.entries` to add each key and value pair to the panel
      Object.entries(response).forEach(([key, value]) => {
        selection.append("p").text(`${key}: ${value}`);
      });
      // });
      // BONUS: Build the Gauge Chart
      // buildGauge(data.WFREQ);
      // Plotly.newPlot('gauge', data);
    });
}

function buildCharts(sample) {

  // Use `d3.json` to fetch the sample data for the plots
  var url = `/samples/${sample}`;
 
  d3.json(url).then(function(response) {
    // @TODO: Build a Bubble Chart using the sample data
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
    ]

    Plotly.newPlot("bubble", bubbleData); 
    
    // Build a Pie Chart
    var labels = response.otu_ids.slice(0,9);
    var values = response.sample_values.slice(0,9);
    var hoverText = response.otu_labels.slice(0,9);
    var trace = {
      "labels": labels,
      "values": values,
      "text": hoverText,
      "type": "pie"}
    
    var layout = {
      autosize: false,
      width: 800,
      height: 800,
      hovermode:'closest',
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
