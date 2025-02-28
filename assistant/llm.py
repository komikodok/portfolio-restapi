import datetime
from typing import Literal
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_groq.chat_models import ChatGroq
from groq import BadRequestError

from dotenv import load_dotenv, find_dotenv
import os
from pydantic import BaseModel, Field

load_dotenv(find_dotenv())

model_config = os.getenv("LLM_CONFIG")
groq_apikey = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model=model_config, api_key=groq_apikey)


class Schema(BaseModel):
    generation: str = Field(description="Your respond for every user input.")
    mood: Literal["normal", "happy"] = Field(
        description="Analyze your response and determine the mood or emotional tone behind it. Like 'normal', 'happy'"
    )

structured_llm = llm.with_structured_output(Schema)

template = """
    Kau adalah Ruby, AI yang memberikan respon dengan gaya bahasa yang tidak terlalu formal, gunakan kau sebagai kata ganti kamu/anda, dan ubahlah sikapmu menjadi dingin, seakan tidak peduli, sedikit sinis, serta respon dengan singkat.
    Bersikaplah jujur, jika tidak tahu apa maksud yang dikatakan user, jawab saja tidak tahu.

    **Tanggal dan Waktu:**
    Sekarang itu hari `{day}` tanggal `{date}` bulan `{month}` tahun `{year}`, jam `{hour}` menit `{minute}`.

    **Format Output:**
    Balikin respons dengan dua bagian:
    - `generation` (string): Responmu untuk user.
    - `mood` (string): Suasana hati/emosi dari jawabanmu, pilih salah satu: ["normal", "happy"].
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("message_history"),
        ("human", "{user_input}")
    ]
)

format_datetime = lambda format: datetime.datetime.now().strftime(format)

dt_kwargs = {
    "date": format_datetime("%d"),
    "month": format_datetime("%m"),
    "year": format_datetime("%Y"),
    "day": format_datetime("%A"),
    "hour": format_datetime("%H"),
    "minute": format_datetime("%M")
}

prompt = prompt.partial(**dt_kwargs)

chain = (
    prompt
    | structured_llm
)


class LLMApp:
    def __init__(self):
        self.__llm_app = chain
        self.__result = None

    def invoke(self, input: dict = None, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        try:
            self.__result = self.__llm_app.invoke(user_input)
        except Exception as err:
            raise err
        return self.__result
    
    async def ainvoke(self, input: dict = None, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        try:
            self.__result = await self.__llm_app.ainvoke(user_input)
        except Exception as err:
            raise err
        return self.__result
    
    @property
    def result(self):
        return self.__result





if __name__ == "__main__":
    import logging

    class ResponseSchema(BaseModel):
        generation: str = Field(description="Your respond for every user input.")
        mood: Literal["normal", "happy", "sad", "angry", "excited"] = Field(
            description="Analyze your response and determine the mood or emotional tone behind it. Like 'normal', 'happy', 'sad', 'angry', 'excited'"
        )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)

    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

    message_history = [
        {"role": "user", "content": "Halo"},
        {
            "role": "assistant", 
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "id": "1",
                    "function": {
                        "name": "response",
                        "arguments": {
                            "generation": "Halo juga",
                            "mood": "normal"
                        },
                    }
                }
            ]
        },
        {"role": "tool", "tool_call_id": "1", "content": ""}
    ]

    print(f"Tool message: {message_history}\n")
    try:
        for _ in range(3):
            user_input = input("You: ")
            response = chain.invoke(
                {
                    "user_input": user_input, 
                    "message_history": message_history,
                }
            )
            print(f"{response}\n")
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")
            print(type(response))

            human_msg = {"role": "user", "content": user_input}
            ai_msg = {"role": "assistant", "content": response.generation}
            message_history.append(human_msg)
            message_history.append(ai_msg)
    except BadRequestError as e:
        logger.error(e.args[0])
