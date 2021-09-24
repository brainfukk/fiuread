from rest_framework.viewsets import ModelViewSet


class ModelViewSetMixin(ModelViewSet):
    serializer_classes = None

    def get_serializer_class(self):
        if self.serializer_classes is not None:
            action = self.action
            return self.serializer_classes.get(action)
        return super().get_serializer_class()
