from surrealdb import Surreal
import json
# from functools import 
import uuid

async def main():
    """Example of how to use the SurrealDB client."""
    async with Surreal("ws://localhost:8000/rpc") as db:
        await db.signin({"user": "root", "pass": "root"})
        await db.use("test", "test")
        # await db.create(
        #     "person",
        #     {
        #         "user": "root",
        #         "pass": "safe",
        #         "marketing": True,
        #         "tags": ["python", "documentation"],
        #     },
        # )
        # print(await db.select("person"))
        # print(await db.update("person", {
        #     "user":"you",
        #     "pass":"very_safe",
        #     "marketing": False,
        #     "tags": ["Awesome"]
        # }))
        # print(await db.delete("person"))

        # You can also use the query method 
        # doing all of the above and more in SurrealQl
        
        # In SurrealQL you can do a direct insert 
        # and the table will be created if it doesn't exist
        # await db.query("""
        # insert into person {
        #     user: 'me',
        #     pass: 'very_safe',
        #     tags: ['python', 'documentation']
        # };
        
        # """)
        # print(await db.query("select * from person"))
        
        with open("output.json") as f:
            data = json.load(f)

# Insert the data into the collection
        ii = 0
        for path, symbols in data.items():
            res_node = await db.create(
                "node",
                {
                    "path": path,
                }
            )
            if type(res_node) == list:
                assert(len(res_node) == 1)
                res_node = res_node[0]
            # collection.insert_one({"path": path, "symbols": symbols["deps"]})
            for i, symbol in enumerate(symbols["deps"]):
                symbol_id = "symbol:" + str(uuid.uuid4())
                # symbol = "symbol:" + symbol
                res_symbol = await db.create(
                    "symbol",
                    {
                        "name": symbol,
                        "node": res_node["id"] 
                    }
                )
                if type(res_symbol) is list:
                    symbols["deps"][i] = res_symbol[0]["id"]
                    assert(len(res_symbol) == 1)
                else:
                    symbols["deps"][i] = res_symbol["id"]
                symbol = symbols["deps"][i]

                # print(res_symbol)
            res_node = await db.update(
                res_node["id"],
                {
                    "path": path,
                    "symbols": symbols["deps"]
                }
            )
            print("RES NODE:")
            print(res_node)
            ii += 1
            if ii % 100 == 0: print(ii / 100)
        # print(await db.query("""
        # update person content {
        #     user: 'you',
        #     pass: 'more_safe',
        #     tags: ['awesome']
        # };
        
        # """))
        # print(await db.query("delete person"))
        

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())