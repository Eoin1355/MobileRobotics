import json
from channels.generic.websocket import WebsocketConsumer
from api.serializers import TeamSerializer
from base.models import Team


class TrackConsumer(WebsocketConsumer):
    consumers = {}  # Dictionary to store instances

    def connect(self):
        team_id = self.get_team_id_from_url()
        if self.is_valid_team_id(team_id):
            self.room_group_name = f"{team_id}"
            self.consumers[self.room_group_name] = self
            self.accept()
            self.send_team_data(team_id)
            print(self.consumers)
        else:
            self.close()

    def disconnect(self, close_code):
        self.close()
        team_id = self.get_team_id_from_url()
        self.consumers.pop(team_id)

    def update(self):
        team_id = self.get_team_id_from_url()

        if self.is_valid_team_id(team_id):
            self.send_team_data(team_id)
        else:
            self.close()

    def get_team_id_from_url(self):
        path = self.scope.get("path")
        parts = path.rstrip("/").split("/")
        team_id = parts[-1]
        return team_id

    def is_valid_team_id(self, team_id):
        if team_id is not None:
            try:
                team = Team.objects.get(teamId=team_id)
                return True
            except Team.DoesNotExist:
                pass
        return False

    def send_team_data(self, team_id):
        try:
            team = Team.objects.get(teamId=team_id)
            serialized_team = TeamSerializer(team).data
            self.send(text_data=json.dumps(serialized_team))

        except Team.DoesNotExist:
            serialized_team = {"error": "Team not found"}
        except Exception as e:
            serialized_team = {"error": str(e)}

    @classmethod
    def get_consumer_instance(cls, room_group_name):
        return cls.consumers.get(room_group_name)
