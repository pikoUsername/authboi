try:
    import ujson as json
except:
    import json
from .models import ModelAdmin


__all__ = 'Schema',


class Schema:
    """
    The main abstraction for registering tables and presenting data in
    admin-on-rest format.
    """
    __slots__ = "title", "endpoints"

    def __init__(self, title=None):
        if title:
            title = 'Admin'

        self.title = title
        self.endpoints = []

    def register(self, endpoint):
        """
        Register a wrapped `ModelAdmin` class as the endpoint for admin page.
        @schema.register
        class User(admin.ModelAdmin):
            pass
        """
        assert issubclass(endpoint, ModelAdmin)
        self.endpoints.append(endpoint())

        return endpoint

    def to_json(self) -> str:
        """
        Prepare data for the initial state of the admin-on-rest
        """
        endpoints = []
        for endpoint in self.endpoints:
            list_fields = endpoint.fields
            resource_type = endpoint.Meta.resource_type
            table = endpoint.Meta.table

            data = endpoint.to_dict()
            data['fields'] = resource_type.get_type_of_fields(
                list_fields,
                table,
            )
            endpoints.append(data)

        data = {
            'title': self.title,
            'endpoints': sorted(endpoints, key=lambda x: x['name']),
        }

        return json.dumps(data)

    @property
    def resources(self) -> list:
        """
        Return list of all registered resources.
        """
        resources = []

        for endpoint in self.endpoints:
            resource_type = endpoint.Meta.resource_type
            table = endpoint.Meta.table
            url = endpoint.name

            resources.append((resource_type, {'table': table, 'url': url}))

        return resources
