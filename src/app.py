from flask import Flask, request, make_response
from flask_cors import CORS
from vitessce import VitessceConfig, ViewType as vt, CoordinationType as ct, FileType as ft, hconcat, vconcat

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('instance/app.cfg')
FILE_URL = app.config['FILE_URL']


@app.route('/')
def say_hello():
    return 'Hello from vitessce-config-builder'


@app.route('/sn-rna-seq', methods=['GET'])
def add():
    token = request.headers.get('Authorization')
    if token is None:
        return make_response("No authentication token.", 401)

    vc = VitessceConfig(schema_version="1.0.14", name='My Config')
    my_dataset = vc.add_dataset(name='SNT753.WGBZ.884').add_file(
        url=FILE_URL,
        file_type=ft.ANNDATA_CELLS_ZARR,
        options={"factors": ["obs/marker_gene_0",
                             "obs/marker_gene_1",
                             "obs/marker_gene_2",
                             "obs/marker_gene_3",
                             "obs/marker_gene_4"],
                 "mappings": {"UMAP": {"dims": [0, 1], "key": "obsm/X_umap"}}}
    ).add_file(
        url=FILE_URL,
        file_type=ft.ANNDATA_CELL_SETS_ZARR,
        options=[{"groupName": "Leiden", "setName": "obs/leiden"}]
    ).add_file(
        url=FILE_URL,
        file_type="anndata-expression-matrix.zarr",
        options={"geneAlias": "var/hugo_symbol",
                 "matrix": "X",
                 "matrixGeneFilter": "var/marker_genes_for_heatmap"}
    )
    v1 = vc.add_view(vt.SCATTERPLOT, dataset=my_dataset, mapping="UMAP")
    v2 = vc.add_view(vt.CELL_SETS, dataset=my_dataset)
    v3 = vc.add_view(vt.GENES, dataset=my_dataset)
    v4 = vc.add_view(vt.CELL_SET_EXPRESSION, dataset=my_dataset)
    v5 = vc.add_view(vt.HEATMAP, dataset=my_dataset)

    vc.layout(vconcat(
        hconcat(v1, hconcat(v2, v3)),
        hconcat(v5, v4, )
    ))
    v = vc.to_dict()
    v['datasets'][0]['files'][0]['requestInit'] = {
                    "headers": {
                        "Authorization": token
                    }
                }
    return v


if __name__ == '__main__':
    app.run()
