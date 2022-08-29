from pydantic import BaseModel, Field


class SurahModel(BaseModel):
    id: int = Field(alias="id")
    surah_name: str = Field(alias="surat_name")
    surah_text: str = Field(alias="surat_text")
    surah_translate: str = Field(alias="surat_terjemahan")
    surah_type: str = Field(alias="golongan_surah")
    count_ayah: int = Field(alias="count_ayat")


class AyahModel(BaseModel):
    id: int = Field(alias="id_ayat")
    surah_number: int = Field(alias="no_surah")
    ayah_number: int = Field(alias="no_ayat")
    ayah_text: str = Field(alias="teks_ayat")
    ayah_theme: str = Field(alias="tema")
    ayah_translate: str = Field(alias="teks_terjemah")
    no_fn: str = Field(alias="no_fn")
    teks_fn: str = Field(alias="teks_fn")
