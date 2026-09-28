from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PathPlanningRequestSerializer
from .services.a_star import a_star


class FzaHealthView(APIView):
    def get(self, request):
        return Response(
            {
                "service": "fza path planning",
                "status": "ready",
            }
        )


class PathPlanningView(APIView):
    def post(self, request):
        serializer = PathPlanningRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = a_star(
                grid=data["grid"],
                start=data["start"],
                goal=data["goal"],
                allow_diagonal=data["allow_diagonal"],
            )
        except (TypeError, ValueError) as exc:
            return Response(
                {
                    "success": False,
                    "path": [],
                    "cost": None,
                    "visited_count": 0,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result, status=status.HTTP_200_OK)
