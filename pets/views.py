from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pet
from .serializers import PetSerializer
from .pagination import PetPagination
from traits.models import Trait

class PetView(APIView):
    def get(self, request):
        pets = Pet.objects.all()
        trait_param = request.query_params.get("trait")

        if trait_param:
            pets = pets.filter(traits__trait_name__iexact=trait_param)

        paginator = PetPagination()
        result_page = paginator.paginate_queryset(pets, request)
        serializer = PetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            pet = serializer.save()
            return Response(PetSerializer(pet).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetDetailView(APIView):
    def get_object(self, pet_id):
        return get_object_or_404(Pet, id=pet_id)

    def get(self, request, pet_id):
        pet = self.get_object(pet_id)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, request, pet_id):
        pet = self.get_object(pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pet_id):
        pet = self.get_object(pet_id)
        data = request.data.copy()

        group_data = data.pop("group", None)
        traits_data = data.pop("traits", None)

        if group_data:
            from groups.models import Group
            group_obj, _ = Group.objects.get_or_create(scientific_name=group_data["scientific_name"])
            pet.group = group_obj

        if traits_data is not None:
            from traits.models import Trait
            pet.traits.clear()
            for trait in traits_data:
                trait_name = trait["trait_name"].lower()
                trait_obj, _ = Trait.objects.get_or_create(trait_name__iexact=trait_name, defaults={"trait_name": trait_name})
                pet.traits.add(trait_obj)

        for key, value in data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)
