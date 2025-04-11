from rest_framework.pagination import PageNumberPagination


class PetPagination(PageNumberPagination):
    page_size = 2
