from botasaurus.browser import Driver, Wait, browser
from botasaurus.window_size import WindowSize
from botasaurus.user_agent import UserAgent
from typing import Literal, Optional
import time

from ..utility.utility import Utils

DRIVER: Optional[Driver] = None
HITBTNSEND = 0
DEFAULT_PROMPT_WEBSCRAPING = """
kamu adalah seorang ahli SEO dan copywriting, saat ini kamu sedang melakukan paraphrasing dari beberapa website berita lokal dan mancanegara untuk situs berita kamu sendiri.
Berikut adalah hasil scraping dari website berita lain dalam format JSON. Lakukan paraphrasing pada bagian content dengan bahasa yang baik menurut SEO.
Hasilkan output dalam format JSON tanpa tambahan noise teks, penjelasan, atau sejenisnya.
"""

DEFAULT_PROMPT_NICHE = """
kamu adalah seorang ahli seo dan copywriting, saat ini kamu akan membuat artikel seo dengan niche [kontraktor] buatkan title artikel nya, yang sangat unik dan 100% beda yang dapat menggundang orang lain sangat tertarik,buatlan artikel nya sesuai dengan kaidah seo yang kreatif dan inovatif untuk konten nya kemudian sertakan element tag header kemudian paragraf subheader dan carikan image di google yang relevan hingga internal linking jadikan output nya dengan bentuk .json, tanpa ada noise teks tambahan, penjelasan, pilihan  dan sejenis nya, target output .json nya seperti di bawah ini patuhi dan jangan di langgar!, jangan menggunakan tag ul langsung li terus konten seusai di template!
buatkan setiap konten sangat variatif, unik, out of the box, dan sangat bisa menarik orang lain untuk membaca dan menaikan trafik sangat tinggi
kemudian untuk semua tag [img, src gunakan https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png] untuk image placeholder nya, maksimalkan untuk internal link nya maksimal 2 internal link di posisi yg berbeda
[
  {
    "tag": "title",
    "content": "content"
  },
  {
    "tag": "h1",
    "content": "content"
  },
  {
    "tag": "img",
    "src": "https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png",
    "alt": "contoh untuk alt"
  },
  {
    "tag": "p",
    "content": "content"
  },
  {
    "tag": "li",
    "content": "content"
  },
  {
    "tag": "h2",
    "content": "content"
  },
  {
    "tag": "a",
    "href":"#",
    "content": "content"
  }

]
"""


def inject_text_with_js(driver: Driver, element_selector: str, text: str):
    """
    Inject teks langsung ke elemen dengan menggunakan JavaScript.
    """
    js_code = f"""
    document.querySelector("{element_selector}").innerText = `{text}`;
    """
    driver.run_js(js_code)


def send_prompt(driver: Driver, content: str = "", generateContent: str = "gpt"):
    """
    Mengirim prompt ke ChatGPT melalui interaksi langsung dengan elemen input.
    """
    global HITBTNSEND

    if generateContent == "gpt":
        default_promt = DEFAULT_PROMPT_NICHE
    else:
        default_promt = DEFAULT_PROMPT_WEBSCRAPING

    full_prompt = f"{default_promt} {content}"

    # Tunggu hingga elemen input tersedia
    driver.wait_for_element("div[id='prompt-textarea']", wait=60)

    # Inject teks ke elemen input
    inject_text_with_js(driver, "div[id='prompt-textarea']", full_prompt)

    # Klik tombol kirim
    driver.click("button[aria-label='Send prompt']", Wait.LONG)
    HITBTNSEND += 1
    time.sleep(2)


def get_response(
    driver: Driver, content: str, generateContent: str, timeout: int = 60
) -> str:
    """
    Mengambil respons dari ChatGPT setelah prompt dikirim.
    """
    global HITBTNSEND
    check_and_close_popup(driver)
    hit_latest_response(driver)
    send_prompt(driver, content, generateContent)

    start_time = time.time()
    while time.time() - start_time < timeout:
        btnCopy = driver.select_all("button[aria-label='Copy']", wait=60)
        if HITBTNSEND == len(btnCopy):
            responses = driver.select_all(".markdown", wait=60)
            if responses:
                return responses[-1].text
            time.sleep(1)
    print("[Error]: Respons ChatGPT timeout.")
    return ""


@browser(
    reuse_driver=True,
    close_on_crash=True,
    user_agent=UserAgent.HASHED,
    window_size=WindowSize.HASHED,
    output=None,
    headless=True,
    profile="pikachu",
)
def open_chatgpt(driver: Driver, data={}):
    """
    Membuka halaman ChatGPT menggunakan driver dan mengatur driver global.
    """
    global DRIVER
    try:
        # ini akan mentriger error karean tidak suskes bypas cloudflare
        driver.google_get("https://chatgpt.com/", bypass_cloudflare=True)
    except:
        pass
    DRIVER = driver


def check_and_close_popup(driver: Driver):
    """
    Memeriksa apakah popup muncul dan menutupnya jika ada.
    """
    try:
        popup = driver.wait_for_element(
            "a[class='mt-5 cursor-pointer text-sm font-semibold text-token-text-secondary underline']",
            wait=Wait.VERY_LONG,
        )
        if popup:
            popup.click()
    except Exception:
        pass


def hit_latest_response(driver: Driver):
    try:
        element = driver.wait_for_element(
            'button[class="cursor-pointer absolute z-10 rounded-full bg-clip-padding border text-token-text-secondary border-token-border-light right-1/2 translate-x-1/2 bg-token-main-surface-primary w-8 h-8 flex items-center justify-center bottom-5"]'
        )
        if element:
            element.click()
    except Exception:
        pass


def run_ai(
    text: str = "", generateContent: Literal["gpt", "webscraping"] = "gpt"
) -> str:
    """
    Menjalankan ChatGPT untuk memproses prompt yang diberikan.
    """
    try:
        response = get_response(DRIVER, text, generateContent)
        return Utils.parseResponseGpt(response, text)
    except Exception as e:
        print(f"[Error]: {e}")
        return ""
