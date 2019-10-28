import qubesadmin

from flask_restful import Resource

from utils.api_formatter import ApiFormatter


class Labels(Resource):
    def __init__(self, qubes):
        self.formatter = ApiFormatter(["color", "name", "icon", "index"])
        self.qubes = qubes

    def get(self):
        """
        List labels
        ---
        definitions:
           - schema:
              xml:
                name: label
              id: Label
              properties:
                name:
                  type: string
                  example: green
                icon:
                  type: string
                  example: appvm-green
                index:
                  type: int
                  example: 4
                color:
                  type: string
                  example: 0x73d216
        tags:
         - Labels
        produces:
          - "application/xml"
          - "application/json"
        responses:
         200:
           description: Label list
           schema:
              type: "array"
              items:
                $ref: "#/definitions/Label"
              xml:
                name: labels
                wrapped : true

        """
        return [self.formatter.to_dict(label) for label in self.qubes.labels.values()]
