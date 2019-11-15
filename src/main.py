from flask import Flask, jsonify
from flask_restful import Api

import qubesadmin
from resources.label import Labels
from resources.pool import Pools
from resources.qube import Qube, Qubes

debug = True

app = Flask(__name__)
api = Api(app)

resource_kwargs = {"qubes":qubesadmin.Qubes()}
api.add_resource(Qubes, '/qubes', resource_class_kwargs=resource_kwargs)
api.add_resource(Qube, '/qubes/<string:name>', resource_class_kwargs=resource_kwargs)
api.add_resource(Labels, '/labels', resource_class_kwargs=resource_kwargs)
api.add_resource(Pools, '/pools', resource_class_kwargs=resource_kwargs)

#api.add_resource(Device, '/qubes/<string:qube_name>/devices')
#api.add_resource(Devices, '/qubes/<string:qube_name>/devices/<string:device_identifier>')
#api.add_resource(Storage, '/qubes/<string:domain_identifier>/storages')
#api.add_resource(Storages, '/qubes/<string:domain_identifier>/storages/<string:storage_identifier>')
#api.add_resource(Tag, '/qubes/<string:domain_identifier>/tags')
#api.add_resource(Tags, '/qubes/<string:domain_identifier>/tags/<string:tag_identifier>')

if debug:
    from flask_swagger import swagger
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_SPECS = "/v2/swagger.json"
    SWAGGER_UI = '/api/docs'

    # Add blueprint to serve UI
    app.register_blueprint(get_swaggerui_blueprint(SWAGGER_UI, SWAGGER_SPECS), url_prefix=SWAGGER_UI)

    # Add route to serve specs
    @app.route(SWAGGER_SPECS)
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "0.1"
        swag['info']['title'] = "QubeOS Administration API"
        return jsonify(swag)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
