import json
import re
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class ViaCEPError(Exception):
    """Erro previsivel ao consultar ou interpretar a API ViaCEP."""


@dataclass(frozen=True)
class Address:
    cep: str
    logradouro: str = ""
    complemento: str = ""
    bairro: str = ""
    localidade: str = ""
    uf: str = ""
    estado: str = ""
    regiao: str = ""
    ibge: str = ""
    ddd: str = ""

    @classmethod
    def from_payload(cls, payload):
        return cls(
            cep=payload.get("cep", ""),
            logradouro=payload.get("logradouro", ""),
            complemento=payload.get("complemento", ""),
            bairro=payload.get("bairro", ""),
            localidade=payload.get("localidade", ""),
            uf=payload.get("uf", ""),
            estado=payload.get("estado", ""),
            regiao=payload.get("regiao", ""),
            ibge=payload.get("ibge", ""),
            ddd=payload.get("ddd", ""),
        )


def normalize_cep(value):
    digits = re.sub(r"\D", "", value)
    if len(digits) != 8:
        raise ViaCEPError("Informe um CEP com 8 digitos.")
    return digits


def _get_json(url):
    request = Request(url, headers={"User-Agent": "ViaCEP Dashboard/1.0"})
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ViaCEPError(f"A API recusou a consulta (HTTP {error.code}).") from error
    except (URLError, TimeoutError, OSError) as error:
        raise ViaCEPError("Nao foi possivel conectar ao ViaCEP.") from error
    except (ValueError, UnicodeDecodeError) as error:
        raise ViaCEPError("A resposta do ViaCEP nao pode ser lida.") from error


def lookup_cep(value):
    cep = normalize_cep(value)
    payload = _get_json(f"https://viacep.com.br/ws/{cep}/json/")
    if payload.get("erro") is True:
        raise ViaCEPError("CEP nao encontrado na base do ViaCEP.")
    return Address.from_payload(payload)


def search_address(uf, city, street):
    uf = uf.strip().upper()
    city = city.strip()
    street = street.strip()
    if len(uf) != 2 or not uf.isalpha():
        raise ViaCEPError("Informe uma UF valida com 2 letras.")
    if len(city) < 3 or len(street) < 3:
        raise ViaCEPError("Cidade e logradouro precisam ter ao menos 3 caracteres.")
    url = f"https://viacep.com.br/ws/{quote(uf)}/{quote(city)}/{quote(street)}/json/"
    payload = _get_json(url)
    return [Address.from_payload(item) for item in payload if "cep" in item]