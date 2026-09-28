from rest_framework import serializers


class PointSerializer(serializers.ListField):
    child = serializers.IntegerField()
    min_length = 2
    max_length = 2


class PathPlanningRequestSerializer(serializers.Serializer):
    grid = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(min_value=0),
            allow_empty=False,
        ),
        allow_empty=False,
    )
    start = PointSerializer()
    goal = PointSerializer()
    allow_diagonal = serializers.BooleanField(required=False, default=False)

    def validate_grid(self, value):
        column_count = len(value[0])
        if any(len(row) != column_count for row in value):
            raise serializers.ValidationError("Grid rows must have the same length")
        return value
