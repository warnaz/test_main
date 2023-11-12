from models import CRUD, Route, Project


async def get_data(crud: CRUD, data: dict) -> tuple:
    max_amount = data.get('max_amount')
    gas = data.get('gas')
    route_id = data.get('route_id')
    private_key = data.get("private_key")
    client_name = data.get("client_name")
    min_time = data.get("min_time")
    max_time = data.get("max_time")

    route: Route = await crud.get(route_id, obj=Route)
    project: Project = await crud.get(route.project_id, obj=Project)
    action_list: list = await crud.get_actions(route.id)

    return route, project, action_list, client_name, private_key, min_time, max_time, max_amount, gas
