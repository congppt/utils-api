from typing import Annotated
import httpx
from pydantic import BaseModel, Field
from parsel import Selector

from external.tax import TaxService
from external.tax.mst.schema import MSTTaxPayer


class MSTTaxService(httpx.AsyncClient, TaxService):
    BASE_URL: str = "https://masothue.com"
    TOKEN_KEY: str = "MST_token"
    class AuthenticateInfo(BaseModel):
        session_id: Annotated[str, Field(...)]
        token: Annotated[str, Field(...)]

    @classmethod
    async def get_tax_payer(cls, tax_identifier: str) -> MSTTaxPayer | None:
        client = cls.__create_base()
        url = await client.__get_tax_payer_url(tax_identifier)
        if not url:
            return None
        res = await client.get(url)
        if res.status_code != 200:
            raise Exception(f"{[client.BASE_URL]}: {res.status_code} Cannot access")
        dom = Selector(body=res.content)
        tables = dom.css('table.table-taxinfo')
        if not tables:
            raise Exception(f"{[client.BASE_URL]}: Cannot find data block")
        table = tables[0]
        data = {
            "tax_code":table.css('td[itemprop="taxID"] span::text').get(),
            "issue_date":table.css('td:contains("Ngày hoạt động") + td span::text').get(),
            "name":table.css('thead th[itemprop="name"] span::text').get(),
            "address":table.css('td[itemprop="address"] span::text').get(),
            "rep_name":table.css('tr[itemprop="alumni"] td span[itemprop="name"] a::text').get(),
            "phone":table.css('td[itemprop="telephone"] span::text').get(),
            "source":client.BASE_URL
        }
        return MSTTaxPayer.model_validate(data)

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
    
    async def __get_tax_payer_url(self, tax_identifier: str) -> str | None:
        token = await self.__get_token()
        res = await self.post("/Ajax/Search", data={
            "q": tax_identifier,
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