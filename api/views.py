import re
from api.consumers import TrackConsumer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from .serializers import TeamSerializer, PostTeamSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from django.views import View
from base.models import Team


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "POST /api/arrived/<str:pk>",
        "GET /api/TEAM-ID",
    ]
    return Response(routes)


class TeamView(View):
    @api_view(["GET"])
    def get(request, teamId):
        try:
            # print(request)
            # teamId = request.data.get("teamId")
            # print(teamId)

            if not teamId:
                return Response(
                    {"error": "Missing 'teamId' in request data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                team = Team.objects.get(teamId=teamId)
                serializer = TeamSerializer(team)
                return Response(serializer.data)

            except Team.DoesNotExist:
                return Response(
                    {"error": f"Team with ID {teamId} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def getTeams(request):
        try:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def post(request):
        try:
            teamId = request.data.get("teamId")
            serializer = PostTeamSerializer(data=request.data)
            if Team.objects.filter(teamId=teamId).exists():
                return Response(
                    {"error": f"Team with ID {teamId} already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.is_valid():
                serializer.save()
            return Response(
                f"Team with ID {teamId} created successfully",
                status=status.HTTP_201_CREATED,
            )

        except KeyError:
            return Response(
                {"error": "Missing 'teamId' in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @api_view(["DELETE"])
    @permission_classes([IsAuthenticated])
    def delete(request, teamId):
        try:
            # teamId = request.data.get("teamId")

            if not teamId:
                return Response(
                    {"error": "Missing 'teamId' in request data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                team_instance = Team.objects.get(teamId=teamId)
                team_instance.delete()

                return Response(
                    f"Team with ID {teamId} deleted successfully",
                    status=status.HTTP_201_CREATED,
                )
            except Team.DoesNotExist:
                return Response(
                    {"error": f"Team with ID {teamId} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @api_view(["POST"])
    def arrived(request, teamId):
        headers = {"Content-Type": "text/plain; charset=utf-8,"}
        try:
            team = Team.objects.get(teamId=teamId)
            if not team:
                return Response(
                    {"error": "No Team with that id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            route = team.route.split(",")
            postion = request.POST.get("position", "")
            if team.index == len(route):
                return HttpResponse(
                    "Already Finished", headers=headers, status=status.HTTP_200_OK
                )
            else:
                if postion == route[team.index]:
                    team.index += 1
                    team.save()
                    consumer_instance = TrackConsumer.get_consumer_instance(teamId)
                    if consumer_instance:
                        consumer_instance.update()
                        print("updated")

                    if team.index == len(route):
                        return HttpResponse(
                            "Finished", headers=headers, status=status.HTTP_200_OK
                        )
                    return HttpResponse(
                        route[team.index], headers=headers, status=status.HTTP_200_OK
                    )
                else:
                    return HttpResponse(
                        "Incorrect position",
                        headers=headers,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        except Team.DoesNotExist:
            return HttpResponse(
                {"No Team with that id"}, status=status.HTTP_400_BAD_REQUEST
            )

        except KeyError:
            return HttpResponse(
                {"Missing 'team_id' in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @api_view(["POST"])
    def post_route(request):
        try:
            teamId = request.data.get("teamId")
            route = request.data.get("route")
            team = Team.objects.get(teamId=teamId)
            if not team:
                return Response(
                    {"error": "No Team with that id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            pattern = re.compile(r"^[0-5](,[0-5])*$")
            match = pattern.match(route)

            if bool(match):
                team.route = route
                team.index = 0
                team.save()
                consumer_instance = TrackConsumer.get_consumer_instance(
                    teamId
                )  # Calling for consumer to update
                if consumer_instance:
                    # Use async_to_sync to call the update method asynchronously
                    consumer_instance.update()
                    print("updated")

                return Response("Route Added", status=status.HTTP_200_OK)

            else:
                return Response(
                    "String incorrectly formatted", status=status.HTTP_400_BAD_REQUEST
                )

        except KeyError:
            return Response(
                {"error": "Missing 'team_id' in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @api_view(["POST"])
    def reset_route(request):
        try:
            teamId = request.data.get("teamId")
            team = Team.objects.get(teamId=teamId)
            if not team:
                return Response(
                    {"error": "No Team with that id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            team.index = 0
            team.save()
            consumer_instance = TrackConsumer.get_consumer_instance(
                teamId
            )  # Calling for consumer to update
            if consumer_instance:
                # Use async_to_sync to call the update method asynchronously
                consumer_instance.update()
                print("updated")
            return Response("Route Reset", status=status.HTTP_200_OK)

        except KeyError:
            return Response(
                {"error": "Missing 'team_id' in request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @api_view(["GET"])
    def getRoute(request, teamId):
        try:
            if not teamId:
                return Response(
                    {"error": "Missing 'teamId' in request data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                team_instance = Team.objects.get(teamId=teamId)
                team_instance.route

                return HttpResponse(team_instance.route)

            except Team.DoesNotExist:
                return HttpResponse(
                    {"error": f"Team with ID {teamId} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            return HttpResponse(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ValidationView(View):
    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def validate_token(request):
        # Token is already validated by the permission_classes(IsAuthenticated)
        return JsonResponse({"valid": True})

    @csrf_exempt
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def signout(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
