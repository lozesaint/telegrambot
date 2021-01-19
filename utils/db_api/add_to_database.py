import asyncio

from utils.db_api.database import create_db
from utils.db_api.db_commands import add_item


async def add_items():
    await add_item(name="Shirt",
                   category_name="👚 Shirts/Blouses", category_code="shirts",
                   price=100, photo="-")
    await add_item(name="Blouse",
                   category_name="👚 Shirts/Blouses", category_code="shirts",
                   price=100, photo="-")
    await add_item(name="Dress1",
                   category_name="👗 Dresses", category_code="dresses",
                   price=100, photo="-")
    await add_item(name="Dress2",
                   category_name="👗 Dresses", category_code="dresses",
                   price=100, photo="-")
    await add_item(name="Skirt1",
                   category_name="🩳 Skirts", category_code="skirts",
                   price=100, photo="-")
    await add_item(name="Skirt2",
                   category_name="🩳 Skirts", category_code="skirts",
                   price=100, photo="-")
    await add_item(name="Trouser1",
                   category_name="👖 Trousers", category_code="trousers",
                   price=100, photo="-")
    await add_item(name="Trouser2",
                   category_name="👖 Trousers", category_code="trousers",
                   price=100, photo="-")
    await add_item(name="Sundress1",
                   category_name="🥻 Sundresses", category_code="sundresses",
                   price=100, photo="-")
    await add_item(name="Sundress2",
                   category_name="🥻 Sundresses", category_code="sundresses",
                   price=100, photo="-")


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
# loop.run_until_complete(add_items())
