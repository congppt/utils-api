from typing import Annotated
import httpx
from pydantic import BaseModel, Field
from cache import aget_cache
from external.tax import TaxService
from external.tax.mst.schema import MSTTaxPayer


class MSTTaxService(httpx.AsyncClient, TaxService):
    BASE_URL: str = "https://masothue.com"
    TOKEN_KEY: str = "MST_token"
    class AuthenticateInfo(BaseModel):
        session_id: Annotated[str, Field(...)]
        token: Annotated[str, Field(...)]

    @classmethod
    async def get_tax_payer(cls, tax_code: str) -> MSTTaxPayer | None:
        client = cls.__create_base()
        url = await client.__get_tax_payer_url(tax_code)
        if not url:
            return None
        res = await client.get(url)
        print('Here')
        return None

    @classmethod
    def __create_base(cls):
        headers = {
                # masothue.com do check browser & screen size
                "User-Agent": "Edg/134.0.0.0",
        }
        cookies = {
            "res": "1920x1080"
        }
        return cls(
            base_url=cls.BASE_URL,
            headers=headers,
            cookies=cookies
        )
    
    async def __get_token(self) -> str:
        # url case sensitive
        res = await self.post(
            url="/Ajax/Token",
            # any string value for "r" is allowed
            data={"r":"a"})
        if res.status_code == 200:
            result: dict = res.json()
            return result["token"]
        raise Exception(f"{[self.BASE_URL]}: {res.status_code} Cannot authenticate")
    
    async def __get_tax_payer_url(self, tax_code: str) -> str | None:
        token = await self.__get_token()
        res = await self.post("/Ajax/Search", data={
            "q": tax_code,
            "token": token
        })
        if res.status_code == 200:
            result: dict = res.json()
            if result["success"] == 0:
                return None
            elif result.get("url", "/") != "/":
                return result["url"]
            raise Exception(f"{[self.BASE_URL]}: Cookie error ?")
        raise Exception(f"{[self.BASE_URL]}: {res.status_code} Cannot search")