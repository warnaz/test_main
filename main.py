from datetime import datetime, timedelta
import random
import sys
from typing import List, Union

import questionary
import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from questionary import Choice

from models import CRUD, Action, ActionWallet, Project, Route
from prepare_data import get_data

async def create_wallet_client(
        crud: CRUD, 
        client_name: str, 
        private_key: str, 
        project: Project, 
        route: Route
    ):
    try:
        client, wallet = await crud.create_client_wallet(client_name, private_key)
        return client, wallet
    except Exception as e:
        await crud.create_status(
                code=400,
                desc=str(e),
                client=client if client else None,
                wallet=wallet,
                project=project,
                route=route,
            )
        logger.error(e)
        raise e    

app = FastAPI()

class RequestData(BaseModel):
    data: dict


@app.post("/")
async def root(request_data: RequestData):
    data = request_data.data       
    crud = CRUD()
    route, project, action_list, client_name, private_key, min_time, max_time, max_amount, gas = await get_data(crud, data)
    client, wallet = await create_wallet_client(crud, client_name, private_key, project, route)

    transaction_time = datetime.now()
    amount_for_action = max_amount / len(action_list)

    for item in action_list:
        number = random.randint(min_time, max_time)
        logger.info(f"Wait {number} minutes")

        transaction_time = transaction_time + timedelta(minutes=number)
        action = await crud.get_single_action(route.id, item.id)

        action_wallet = await crud.create_action_wallet(
            status="WAIT",
            amount=amount_for_action,
            gas=gas,
            wallet_id=wallet.id,
            action_id=action.id,
            estimated_time=transaction_time
        )


@app.post("/create_test_data")
async def create_test_data(request_data: RequestData):
    data = request_data.data
    crud = CRUD()
    route_id_one, route_id_two, route_id_three = await crud.create_test_data()

    return {"Были созданы данные с маршрутами: ", route_id_one, route_id_two, route_id_three}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost")
