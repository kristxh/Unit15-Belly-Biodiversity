import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Flask setup
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)
engine = create_engine(os.environ.get('DATABASE_URL','') or "sqlite:///db/bellybutton.sqlite")

class Otu(db.Model):
    __tablename__ = "otu"
    otu_id = db.Column(db.Integer, primary_key=True)
    otu_label = db.Column(db.String)

class Metadata(db.Model):
    __tablename__ = "samples_metadata"
    sample = db.Column(db.Integer, primary_key=True)
    EVENT = db.Column(db.String)
    ETHNICITY = db.Column(db.String)
    GENDER = db.Column(db.String)
    AGE = db.Column(db.Integer)
    WFREQ = db.Column(db.Float)
    BBTYPE = db.Column(db.String)
    LOCATION = db.Column(db.String)
    COUNTRY012 = db.Column(db.String)
    ZIP012 = db.Column(db.String)
    COUNTRY1319 = db.Column(db.String)
    ZIP1319 = db.Column(db.String)
    DOG = db.Column(db.String)
    CAT = db.Column(db.String)
    IMPSURFACE013 = db.Column(db.Integer)
    NPP013 = db.Column(db.Float)
    MMAXTEMP013 = db.Column(db.Float)
    PFC013 = db.Column(db.Float)
    IMPSURFACE1319 = db.Column(db.Integer)
    NPP1319 = db.Column(db.Float)
    MMAXTEMP1319 = db.Column(db.Float)
    PFC1319 = db.Column(db.Float)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    print("got here")
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Metadata).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df['sample']))

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    print("got here")
    """Return the MetaData for a given sample."""
    # {"AGE":24.0,"BBTYPE":"I","ETHNICITY":"Caucasian","GENDER":"F","LOCATION":"Beaufort/NC","WFREQ":2.0,"sample":940}
    sel = [
        Metadata.sample,
        Metadata.ETHNICITY,
        Metadata.GENDER,
        Metadata.AGE,
        Metadata.LOCATION,
        Metadata.BBTYPE,
        Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)

@app.route("/samples/<sample>")
def samples(sample):
    print("got here - sample")
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Otu).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    Filter the data based on the sample number and
    only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)
    # return jsonify({"otu_ids":[41,121,159,165,170,189,258,259,307,340,342,352,357,412,482,513,725,830,833,874,907,944,1167,1169,1189,1193,1208,1232,1274,1314,1497,1498,1503,1505,1795,1950,1959,1960,1962,1968,1977,2011,2024,2039,2065,2077,2110,2167,2178,2184,2186,2188,2191,2235,2244,2247,2264,2275,2291,2318,2335,2342,2350,2396,2419,2475,2483,2491,2546,2571,2722,2737,2739,2782,2811,2859,2908,2936,2964,3450],"otu_labels":["Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Actinomycetaceae","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Actinomycetaceae;Varibaculum","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Corynebacteriaceae","Bacteria;Actinobacteria;Actinobacteria;Actinomycetales;Corynebacteriaceae;Corynebacterium","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Porphyromonadaceae;Porphyromonas","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Prevotellaceae","Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Prevotellaceae;Prevotella","Bacteria;Firmicutes","Bacteria;Firmicutes","Bacteria;Firmicutes","Bacteria;Firmicutes","Bacteria;Firmicutes;Bacilli;Bacillales;Staphylococcaceae;Staphylococcus","Bacteria;Firmicutes;Clostridia","Bacteria;Firmicutes;Clostridia","Bacteria;Firmicutes;Clostridia","Bacteria;Firmicutes;Clostridia","Bacteria;Firmicutes;Clostridia","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Anaerococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Finegoldia","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Gallicola","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Gallicola","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Peptoniphilus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Peptoniphilus","Bacteria;Firmicutes;Clostridia;Clostridiales;IncertaeSedisXI;Peptoniphilus","Bacteria;Firmicutes;Clostridia;Clostridiales;Peptococcaceae;Peptococcus","Bacteria;Firmicutes;Clostridia;Clostridiales;Ruminococcaceae","Bacteria;Firmicutes;Clostridia;Clostridiales;Veillonellaceae","Bacteria;Proteobacteria;Epsilonproteobacteria;Campylobacterales;Campylobacteraceae;Campylobacter"],"sample_values":[71,2,2,12,2,47,2,2,7,2,2,50,2,2,113,2,2,10,3,36,3,19,163,2,51,6,5,2,4,3,2,2,2,2,10,25,30,2,3,2,40,11,13,5,2,23,2,5,7,19,3,2,28,2,14,11,78,22,2,40,3,2,2,11,13,2,2,2,2,2,8,4,4,12,13,126,7,3,10,37]})

if __name__ == "__main__":
    app.run()
