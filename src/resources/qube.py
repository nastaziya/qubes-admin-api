from enum import Enum

from flask_restful import Resource, reqparse

from utils.api_formatter import ApiFormatter

qube_formatter = ApiFormatter(["name", "klass", "get_power_state", "label"],
                              rename={"klass": "type", "get_power_state": "state"})


class QubeStatus(Enum):
    RUNNING = "Running"
    HALTED = "Halted"
    PAUSED = "Paused"


class Qube(Resource):

    def __init__(self, qubes):
        self.qubes = qubes

    def get(self, name):
        """
        Get Qube
        ---
        parameters:
          - in: path
            name: name
            type: string
            example: fedora-29
        definitions:
           - schema:
              xml:
                name: qube
              id: Qube
              properties:
                name:
                  type: string
                  example: fedora-29
                type:
                  type: string
                  enum:
                     - "AppVM"
                     - "TemplateVM"
                     - "AdminVM"
                net_vm:
                  type: string
                  example: sys-firewall
                disk_usage:
                  type: float
                  example: 1024
                  description: Disk size in MB
                status:
                    type: "string"
                    enum:
                     - "Running"
                     - "Paused"
                     - "Halted"
        tags:
         - Qubes
        responses:
         200:
           description: Qube
           schema:
            $ref: "#/definitions/Qube"
        produces:
          - "application/xml"
          - "application/json"
        """
        return qube_formatter.to_dict(self.qubes.domains[name])

    def delete(self, name):
        """
        Delete Qube
        ---
        parameters:
          - in: path
            name: name
            type: string
            example: fedora-29
        tags:
         - Qubes
        responses:
         204:
           description: No Content
        """
        del self.qubes.domains[name]
        return [], 204

    def put(self, name):
        """
        Edit qube (and change status)
        ---

        parameters:
          - in: path
            name: name
            type: string
            example: fedora-29
          - in: body
            name: body
            schema:
              xml:
                  name: qube
              properties:
                  status:
                    type: string
                    enum:
                      - Running
                      - Paused
                      - Halted
                  force:
                    type: bool
                    example: False
        tags:
         - Qubes
        responses:
         204:
           description: No Content
        """
        parser = reqparse.RequestParser()
        parser.add_argument('status')
        parser.add_argument('force', type=bool, action="store_true")
        args = parser.parse_args()
        vm = self.qubes.domains[name]
        current_state = vm.get_power_state()
        if current_state != args.status:
            if args.status == QubeStatus.RUNNING.value:
                if current_state == QubeStatus.PAUSED.value:
                    vm.unpause()
                else:
                    vm.start()
            elif args.status == QubeStatus.HALTED.value:
                if args.force:
                    vm.kill()
                else:
                    vm.shutdown()
            elif args.status == QubeStatus.PAUSED.value and current_state == QubeStatus.RUNNING.value:
                vm.pause()

        return None, 204

    def post(self, name):
        """
        Clone qube
        ---
        parameters:
          - in: path
            name: name
            type: string
            example: fedora-29
          - in: body
            name: body
            schema:
              xml:
                name: qube
              required:
                - name
              properties:
                  name:
                    type: string
                    example: fedora-29-copy
                  type:
                    type: string
                    default: AppVM
                    enum:
                     - AppVM
                     - TemplateVM
        tags:
         - Qubes
        responses:
         201:
           description: Created vm
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('type')
        args = parser.parse_args()
        # add ignore_error for qvm-appmenus missing
        new_vm = self.qubes.clone_vm(name, args.name, ignore_errors=True, new_cls=args.type)
        return qube_formatter.to_dict(new_vm), 201


class Qubes(Resource):

    def __init__(self, qubes):
        self.qubes = qubes

    def get(self):
        """
        List Qubes
        ---
        tags:
         - Qubes
        produces:
          - "application/xml"
          - "application/json"
        responses:
         200:
           description: Qubes list
           schema:
              type: "array"
              items:
                $ref: "#/definitions/Qube"
              xml:
                name: qubes
                wrapped : true

        """
        return [qube_formatter.to_dict(vm) for vm in self.qubes.domains.values()]

    def post(self):
        """
        Create Qube
        ---
        consumes:
          - "application/xml"
          - "application/json"
        parameters:
          - in: body
            name: body
            schema:
              xml:
                name: qube
              required:
                - name
                - type
                - label
              properties:
                  name:
                    type: string
                    example: my-appvm
                  label:
                    type: string
                    example: red
                  type:
                    type: string
                    default: AppVM
                    enum:
                     - AppVM
                     - TemplateVM
                  template:
                    type: string
                    example: fedora-29
                  pool_identifier:
                    type: string
                    example: lvm
        tags:
         - Qubes
        produces:
          - "application/xml"
          - "application/json"
        responses:
         201:
           description: Created
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('type', required=True)
        parser.add_argument('label', required=True)
        parser.add_argument('template')
        args = parser.parse_args()
        vm = self.qubes.add_new_vm(args.type, args.name, args.label, template=args.template)
        return qube_formatter.to_dict(vm), 201
