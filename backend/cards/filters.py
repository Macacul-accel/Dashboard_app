from django_filters import FilterSet, CharFilter, ChoiceFilter, RangeFilter
from django_filters.widgets import RangeWidget
from django import forms
from .models import Card, Set
from .constant import *


class CardFilterSet(FilterSet):
    """
    Filtre pour le model Card, permettant d'obtenir les cartes souhaitées selon certains critères.
    Les variables *CHOICES sont dans le fichier 'constant.py'.
    """
    name = CharFilter(field_name='name', 
        lookup_expr='icontains',
        label='Nom de carte',
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher par nom'}),
        required=False,
    )
    type = ChoiceFilter(choices=MONSTER_TYPE_CHOICES,
        method='filter_by_monster_type',
        label='Autre',
        empty_label='Tous',
        required=False,
    )
    frame_type = ChoiceFilter(choices=FRAME_TYPE_CHOICES,
        method='filter_by_frametype',
        label='Type de carte',
        empty_label='Tous',
        required=False,
    )
    attack = RangeFilter(
        label="Attaque",
        method='filter_range_atk_def',
        widget=RangeWidget(attrs={'class': 'range-slider'}),
        required=False,
    )
    defense = RangeFilter(
        label="Défense",
        method='filter_range_atk_def',
        widget=RangeWidget(attrs={'class': 'range-slider'}),
        required=False,
    )
    level_rank = RangeFilter(
        label="Niveau/Rang",
        widget=RangeWidget(attrs={'class': 'range-slider'}),
        required=False,
    )
    spell_trap_race = ChoiceFilter(choices=SPELL_TRAP_RACE_CHOICES,
        method='filter_by_spell_trap_race',
        label='Type de magie, piège', 
        empty_label='Tous', 
        required=False,
    )
    monster_race = ChoiceFilter(choices=MONSTER_RACE_CHOICES,
        method='filter_by_monster_race', 
        label='Type de monstre', 
        empty_label='Tous', 
        required=False,
    )
    attribute = ChoiceFilter(choices=MONSTER_ATTRIBUTE_CHOICES,
        method='filter_by_monster_attribute', 
        label='Attribut', 
        empty_label='Tous', 
        required=False,
    )
    set_code = ChoiceFilter(
        field_name='card_sets__set__code', 
        label='Code du set', 
        empty_label='Tous',
        choices=lambda: [(set_.code, set_.name) for set_ in Set.objects.all()],
        method='filter_by_set_code',
        required=False,
    )

    class Meta:
        model = Card
        fields = ['name', 'type','frame_type', 'attack', 'defense', 'level_rank', 'spell_trap_race', 'monster_race', 'attribute', 'set_code']


    def filter_by_frametype(self, queryset, name, value):
        """
        Fonctions pour récupérer les mots clés de chaque filtre et laisser le choix aux utilisateurs avec des filtres prédéfinis.
        """
        return filter_by_mapping(queryset, FRAME_TYPE_MAPPING, name, value, 'frame_type')

    def filter_by_monster_type(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_TYPE_MAPPING, name, value, 'type')

    def filter_by_spell_trap_race(self, queryset, name, value):
        return filter_by_mapping(queryset, SPELL_TRAP_RACE_MAPPING, name, value, 'spell_trap_race')

    def filter_by_monster_race(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_RACE_MAPPING, name, value, 'monster_race')

    def filter_by_monster_attribute(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_ATTRIBUTE_MAPPING, name, value, 'attribute')

    def filter_by_set_code(self, queryset, name, value):
        """
        Filtre en fonction du code du set.
        """
        return queryset.filter(card_sets__set__code=value).distinct()
    
    
    def filter_range_atk_def(self, queryset, name, value):
        """Filter attack and defense by min and max values."""
        if value:
            min_value, max_value = value

            min_value = int(min_value) if min_value else None
            max_value = int(max_value) if max_value else None

            if min_value is None:
                min_value = 0
            if max_value is None:
                max_value = 5000

            if min_value is not None:
                queryset = queryset.filter(**{f"{name}__gte": min_value})

            if max_value is not None:
                queryset = queryset.filter(**{f"{name}__lte": max_value})

        return queryset
    
    def filter_lvl(self, queryset, name, value):
        """Filter level_rank by min and max values."""
        if value:
            min_value, max_value = value

            min_value = int(min_value) if min_value else None
            max_value = int(max_value) if max_value else None

            if min_value is None:
                min_value = 1
            if max_value is None:
                max_value = 13

            if min_value is not None:
                queryset = queryset.filter(level_rank__gte=min_value)

            if max_value is not None:
                queryset = queryset.filter(level_rank__lte=max_value)

        return queryset