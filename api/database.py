import motor.motor_asyncio

from core.calculator import Calculator

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mdb:27017")
database = client["rpn_calculator"]
operations_collection = database["operations"]

calc = Calculator()

async def connect():
    """
    Establish a connection to the MongoDB database.
    """
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e

async def close():
    """
    Close the connection to the MongoDB database.
    """
    if client:
        client.close()
        print("Closed MongoDB connection")
        
def operation_helper(operation) -> dict:
    return {
        "id": str(operation["_id"]),
        "expression": operation["expression"],
        "result": operation["result"],
    }

async def retrieve_all_operations():
    """
    Retrieve all operations present in the database.
    """
    operations = []
    async for operation in operations_collection.find():
        operations.append(operation_helper(operation))
    return operations

async def add_operation(operation_data: dict) -> dict:
    """
    Add a new operation into to the database.
    """
    operation = await operations_collection.insert_one(operation_data)
    new_operation = await operations_collection.find_one({"_id": operation.inserted_id})
    return operation_helper(new_operation)

async def delete_all_operations():
    """
    Deletes all records from the 'operations' collection.
    """
    await operations_collection.delete_many({})