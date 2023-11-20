from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from api.model import CheckRPNInput, CheckRPNOutput, InfixExpressionInput, Operation, OperationOut, RPNExpressionOutput
from core.calculator import Calculator
import pandas as pd
from api.database import add_operation, delete_all_operations, retrieve_all_operations

router = APIRouter()
calc = Calculator()


@router.get("/operations", summary="RPN operations retrieved")
async def get_operations():
    """
    Retrieve all RPN operations stored in the database.

    This endpoint queries the database for all stored Reverse Polish Notation (RPN) operation data.
    It returns a list of operations, each containing the expression and its result.
    If there are no operations stored, it returns an empty list.

    """
    try:
        operations = await retrieve_all_operations()
        if operations:
            return {"message": "RPN operations data retrieved successfully", "data": operations}
        return {"message": "No operations found", "data": operations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate_rpn", summary="Calculate RPN Expression", response_model=OperationOut)
async def calculate_rpn_expression(input: Operation = Body(...)):
    """
    Calculate a given expression in Reverse Polish Notation (RPN).
    """
    try:
        formatted_expression = calc.format_expression(input.expression)
        result = calc.calculate(formatted_expression)

        operation_data = input.model_dump()
        operation_data['result'] = result
        operation_data_encoded = jsonable_encoder(operation_data)
        await add_operation(operation_data_encoded)
        return OperationOut(expression=input.expression, result=result)
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/convert_to_rpn", summary="Convert Infix to RPN", response_model=RPNExpressionOutput)
def convert_to_rpn(input: InfixExpressionInput = Body(..., description="The infix expression to be converted to RPN")):
    """
    Convert an infix arithmetic expression to Reverse Polish Notation (RPN).

    - **expression**: Infix arithmetic expression as a string.
    """
    try:
        format_expression = calc.format_expression(input.infix_expression)
        rpn_expression = calc.to_rpn(format_expression)
        return RPNExpressionOutput(rpn_expression=rpn_expression)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/check_rpn", summary="Check if Expression is RPN", response_model=CheckRPNOutput)
def check_if_rpn(input: CheckRPNInput = Body(..., description="The expression to be checked")):
    """
    Check if a given expression is in Reverse Polish Notation (RPN).
    """
    try:
        format_expression = calc.format_expression(input.expression)
        result = calc.is_rpn(format_expression)
        return CheckRPNOutput(is_rpn=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/operations_csv", summary="Get RPN Operations as CSV")
async def get_operations_csv():
    """
    Retrieve all operation data from the database and return it in CSV format.
    """
    operations = await retrieve_all_operations()
    df = pd.DataFrame.from_dict(operations)
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
    )
    
@router.delete("/delete_all_operations", summary="Delete All Operations")
async def delete_all():
    """
    Delete all records from the operations collection.

    Warning: This action is irreversible and should be used with caution.
    """
    try:
        await delete_all_operations()
        return {"message": "All operations have been deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))