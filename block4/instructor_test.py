import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Optional

def _extract_user(client: instructor.Instructor, model_id: str):

    user_prompt = "John Doe is 30 years old."

    # Define your desired output structure
    class ExtractUser(BaseModel):
        name: str = Field(description="The name of the user.")
        age: int  = Field(description="The age of the user.")
        email: Optional[str] = Field(description="The email of the user.", default=None)

    # Extract structured data from natural language
    res = client.chat.completions.create(
        model=model_id,
        response_model=ExtractUser,
        messages=[{"role": "user", "content": user_prompt}],
    )
    print(res)
    assert res.name == "John Doe"
    assert res.age == 30


def _extract_shoppingcart(client: instructor.Instructor, model_id: str):

    user_prompt = "Carol puts 7 cans of peas in her shopping cart."

    # Define your desired output structure
    class ShoppingCart(BaseModel):
        product: str = Field(description="The procuct beeing purchased.")
        quantity: int  = Field(description="the quantity purchased of the product")

    # Extract structured data from natural language
    res = client.chat.completions.create(
        model=model_id,
        response_model=ShoppingCart,
        messages=[{"role": "user", "content": user_prompt}],
    )
    print(res)
    assert res.product.lower() == "cans of peas"
    assert res.quantity == 7




if __name__ == "__main__":
    model_id = "llama3.2:latest"

    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        ),
        mode=instructor.Mode.JSON, # does not without for ollama and llama3.2
    )

    _extract_user(client, model_id)
    _extract_shoppingcart(client, model_id)
