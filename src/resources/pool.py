import qubesadmin

from flask_restful import Resource

from utils.api_formatter import ApiFormatter


class Pools(Resource):
    def __init__(self, qubes):
        self.formatter = ApiFormatter(["name", "config", "size", "usage", "driver"])
        self.qubes = qubes

    def get(self):
        """
        List pools
        ---
        definitions:
           - schema:
              xml:
                name: pool
              id: Pool
              properties:
                name:
                  type: string
                  example: lvm
                config:
                  type: dict
                size:
                  type: int
                  example: 973749616640
                usage:
                  type: int
                  example: 41676483592
                driver:
                  type: string
                  example: file
        tags:
         - Labels
        produces:
          - "application/xml"
          - "application/json"
        responses:
         200:
           description: Pool list
           schema:
              type: "array"
              items:
                $ref: "#/definitions/Pool"
              xml:
                name: pools
                wrapped : true

        """
        return [self.formatter.to_dict(pool) for pool in self.qubes.pools.values()]
