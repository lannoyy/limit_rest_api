from aiohttp import web
from db import engine
from sqlalchemy.orm import sessionmaker
from models import Limit, Transaction
from sqlalchemy.exc import IntegrityError

routes = web.RouteTableDef()
Session = sessionmaker(bind=engine)


@routes.get("/limits")
async def all_limits_view(request):
    session = Session()
    query = session.query(Limit).all()
    output = []
    for item in query:
        output.append(item.serialize)
    return web.json_response(data=output)


@routes.get("/limit/{user_id}")
async def limit_view(request):
    session = Session()
    year = request.rel_url.query.get('year', None)
    month = request.rel_url.query.get('month', None)
    id_obj = int(request.match_info.get("user_id", None))
    obj = session.query(Limit).get({"user_id": id_obj})
    if not obj:
        return web.json_response(data={'error': 'not found'}, status=404)
    data = []
    if year and month:
        data = obj.check_for_transactions(year=year, month=month)
    obj = obj.serialize
    obj['transactions'] = data
    return web.json_response(data=obj)


@routes.post("/limits")
async def limits_create(request):
    session = Session()
    content = await request.json()
    try:
        limit = Limit(**content)
        session.add(limit)
        session.commit()
    except (AttributeError, TypeError) :
        return web.json_response(data={'error': 'invalid body'}, status=400)
    except IntegrityError:
        return web.json_response(data={'error': 'object with this user id exists'}, status=400)
    return web.json_response(data=limit.serialize)


@routes.post("/transaction")
async def transaction_create(request):
    session = Session()
    content = await request.json()
    try:
        transaction = Transaction(**content)
        session.add(transaction)
        session.commit()
    except (AttributeError, TypeError):
        return web.json_response(data={'error': 'invalid body'}, status=400)
    except ValueError:
        return web.json_response(data={'error': 'unavailable amount'}, status=400)
    return web.json_response(data=transaction.serialize)


@routes.put("/transaction/{id}")
async def transaction_update(request):
    session = Session()
    id_obj = int(request.match_info.get("id", None))
    content = await request.json()
    try:
        obj = session.query(Limit).get({"id": id_obj})
        if not obj:
            return web.json_response(data={'error': 'not found'}, status=404)
        obj.update(**content)
        session.commit()
    except (AttributeError, TypeError):
        return web.json_response(data={'error': 'invalid body'}, status=400)
    except ValueError:
        return web.json_response(data={'error': 'unavailable amount'}, status=400)
    return web.json_response(data=obj.serialize)


@routes.delete("/transaction/{id}")
async def transaction_delete(request):
    session = Session()
    id_obj = int(request.match_info.get("id", None))
    obj = session.query(Limit).get({"id": id_obj})
    if not obj:
        return web.json_response(data={'error': 'not found'}, status=404)
    session.delete(obj)
    session.commit()
    return web.json_response(data=obj.serialize)


@routes.put("/limit/{user_id}")
async def limit_update(request):
    session = Session()
    id_obj = int(request.match_info.get("user_id", None))
    content = await request.json()
    try:
        obj = session.query(Limit).get({"user_id": id_obj})
        if not obj:
            return web.json_response(data={'error': 'not found'}, status=404)
        obj.update(**content)
        session.commit()
    except (AttributeError, TypeError):
        return web.json_response(data={'error': 'invalid body'}, status=400)
    return web.json_response(data=obj.serialize)


@routes.delete("/limit/{user_id}")
async def limit_delete(request):
    session = Session()
    id_obj = int(request.match_info.get("user_id", None))
    obj = session.query(Limit).get({"user_id": id_obj})
    if not obj:
        return web.json_response(data={'error': 'not found'}, status=404)
    session.delete(obj)
    session.commit()
    return web.json_response(data=obj.serialize)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app)