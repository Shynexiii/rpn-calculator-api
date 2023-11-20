from pydantic import BaseModel, Field


class Operation(BaseModel):
    expression: str = Field(..., description="The arithmetic expression, either in infix or RPN format")
    result: float = Field(None, description="The result of the RPN calculation")


    class Config:
        json_schema_extra = {
            "example": {
                "expression": "4 3 + 2 1 - * 5 /",
            }
        }
        
class OperationOut(BaseModel):
    expression: str = Field(..., description="The arithmetic expression, either in infix or RPN format")
    result: float = Field(..., description="The result of the RPN calculation")

    class Config:
        json_schema_extra = {
            "example": {
                "expression": "4 3 + 2 1 - * 5 /",
                "result": 1.4
            }
        }
        
class InfixExpressionInput(BaseModel):
    infix_expression: str = Field(..., example="3 + 4 * (2 - 1)")

    class Config:
        json_schema_extra = {
            "example": {
                "infix_expression": "3 + 4 * (2 - 1)"
            }
        }
        
class RPNExpressionOutput(BaseModel):
    rpn_expression: str

    class Config:
        json_schema_extra = {
            "example": {
                "rpn_expression": "3 4 2 1 - * +"
            }
        }
        
        
class CheckRPNInput(BaseModel):
    expression: str = Field(..., example="4 3 + 2 1 - * 5 /")

    class Config:
        json_schema_extra = {
            "example": {
                "expression": "4 3 + 2 1 - * 5 /"
            }
        }
        
class CheckRPNOutput(BaseModel):
    is_rpn: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_rpn": True
            }
        }

        
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}