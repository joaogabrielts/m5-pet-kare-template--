from rest_framework import serializers
from .models import Pet
from groups.models import Group
from traits.models import Trait
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer

class PetSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'age', 'weight', 'sex', 'group', 'traits']
        read_only_fields = ['id']

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        traits_data = validated_data.pop('traits')

        group_obj, _ = Group.objects.get_or_create(**group_data)
        pet = Pet.objects.create(**validated_data, group=group_obj)

        for trait in traits_data:
            trait_obj, _ = Trait.objects.get_or_create(**trait)
            pet.traits.add(trait_obj)

        return pet