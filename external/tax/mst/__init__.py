from typing import Annotated

import httpx
from parsel import Selector
from pydantic import BaseModel, Field

from cache import aget_cache, aset_cache
from external.tax import TaxService
from external.tax.mst.schema import MSTTaxPayer


class MSTTaxService(httpx.AsyncClient, TaxService):
    AUTH_KEY = "masothue"
    class AuthenticateInfo(BaseModel):
        session_id: Annotated[str, Field(...)]
        token: Annotated[str, Field(...)]

    @classmethod
    async def get_tax_payer(cls, tax_identifier: str) -> MSTTaxPayer | None:
        client = cls.__create_base()
        url = await client.__get_tax_payer_url(tax_identifier)
        if not url:
            return None
        if url.startswith("/Search/?q"):
            res = await client.get(url)
            if res.status_code != 200:
                raise Exception(f"{[client.base_url.host]}: {res.status_code} Cannot search multiple result")
            dom = Selector(body=res.content)
            tax_elements = dom.css('div.tax-listing > div[data-prefetch]')
            personal_tax_elements = tax_elements.css('div:contains("Mã số thuế cá nhân")')
            if personal_tax_elements:
                url = personal_tax_elements[0].css('::attr(data-prefetch)').get()
            else:
                # Fallback to the first element
                url = tax_elements[0].css('::attr(data-prefetch)').get()
        assert url
        res = await client.get(url)
        if res.status_code != 200:
            raise Exception(f"{[client.base_url.host]}: {res.status_code} Cannot access")
        dom = Selector(body=res.content)
        tables = dom.css("table.table-taxinfo")
        if not tables:
            raise Exception(f"{[client.base_url.host]}: Cannot find data block")
        table = tables[0]
        data = {
            "tax_code": table.css('td[itemprop="taxID"] span::text').get(),
            "issue_date": table.css(
                'td:contains("Ngày hoạt động") + td span::text'
            ).get(),
            "name": table.css('thead th[itemprop="name"] span::text').get(),
            "address": table.css('td[itemprop="address"] span::text').get(),
            "rep_name": table.css(
                'tr[itemprop="alumni"] td span[itemprop="name"] a::text'
            ).get(),
            "phone": table.css('td[itemprop="telephone"] span::text').get(),
            "source": client.base_url.host,
        }
        data["id_number"] = tax_identifier if int(data["tax_code"][0:2]) > 63 and len(data["tax_code"]) < 14 else None
        return MSTTaxPayer.model_validate(data)

    @classmethod
    def __create_base(cls):
        headers = {
            # masothue.com do check browser & screen size
            "User-Agent": "Edg/134.0.0.0",
        }
        cookies = {"res": "1920x1080"}
        return cls(base_url="https://masothue.com", headers=headers, cookies=cookies)

    async def __get_token(self) -> str:
        auth_info = await aget_cache(self.AUTH_KEY, MSTTaxService.AuthenticateInfo)
        auth_info = auth_info if isinstance(auth_info, MSTTaxService.AuthenticateInfo) else None
        if auth_info:
            self.cookies.set("PHPSESSID", auth_info.session_id)
            return auth_info.token
        # url case sensitive
        res = await self.post(
            url="/Ajax/Token",
            # any string value for "r" is allowed
            data={"r": "a"},
        )
        if res.status_code == 200:
            result: dict = res.json()
            session_id = self.cookies.get("PHPSESSID")
            assert session_id
            await aset_cache(self.AUTH_KEY, MSTTaxService.AuthenticateInfo(session_id=session_id, token=result["token"]), 60 * 30)
            return result["token"]
        raise Exception(f"{[self.base_url.host]}: {res.status_code} Cannot authenticate")

    async def __get_tax_payer_url(self, tax_identifier: str) -> str | None:
        token = await self.__get_token()
        res = await self.post(
            "/Ajax/Search", data={"q": tax_identifier, "token": token}
        )
        if res.status_code == 200:
            result: dict = res.json()
            if result["success"] == 0:
                return None
            elif result["numRows"] > 1:
                return f"/Search/?q={tax_identifier}&type=auto&token={token}&force-search=1"
            elif result.get("url", "/") != "/":
                return result["url"]
            raise Exception(f"{[self.base_url.host]}: Cookie error ?")
        raise Exception(f"{[self.base_url.host]}: {res.status_code} Cannot search")
