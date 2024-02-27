from rest_framework import generics, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from foto_flux.permissions import IsOwnerOrReadOnly

class ContactMessageList(generics.ListCreateAPIView):
    """
    List all contact messages or create a new one.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ContactMessageDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a contact message.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # Ensure that only the owner of the message can delete it
    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this message.")