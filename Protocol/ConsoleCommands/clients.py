class Command:
    def __init__(self):
        self.name = "clients"

    async def execute(self, server, websocket, *args):
        from Utils.Logger import Logger
        from Utils.Helpers import Helpers
        import json
        
        serialized_clients = {
            'ClientsCount': Helpers.connected_clients['ClientsCount'],
            'Clients': Helpers.serialize_clients(Helpers.connected_clients['Clients'])
        }        

        await websocket.send(json.dumps(serialized_clients))