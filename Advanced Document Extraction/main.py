import os

import fitz
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class BoundingBoxField(BaseModel):
    bounding_box: list[int] = Field(..., description='The bounding box where the information was found [y_min, x_min, y_max, x_max]')
    page: int = Field(..., description='Page number where the information was found. Start counting with 1.')

class TotalAmountField(BoundingBoxField):
    value: float = Field(..., description='The total amount of the invoice.')

class RecipientField(BoundingBoxField):
    name: str = Field(..., description='The name of the recipient.')

class TaxAmountField(BoundingBoxField):
    value: float = Field(..., description='The total amount of the tax.')

class SenderField(BoundingBoxField):
    name: str = Field(..., description='The name of the sender.')

class AccountNumberField(BoundingBoxField):
    account_no: str = Field(..., description='The number of the account.')


class InvoiceModel(BaseModel):
    total: TotalAmountField
    recipient: RecipientField
    tax: TaxAmountField
    sender: SenderField
    account_no: AccountNumberField


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

file_in = 'invoice.pdf'
file_out = 'invoice_annotated.pdf'
pdf = client.files.upload(file=file_in) 

prompt = """
Extract the invoice recipient name and invoice total.
Return ONLY JSON that matches the provided schema.
If a field is missing, set it to null (and bounding_box to [0,0,0,0]).
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[pdf, prompt],
    config={
        "response_mime_type": "application/json",
        "response_schema": InvoiceModel
    },
)

invoice = InvoiceModel.model_validate_json(response.text)
print(invoice.model_dump())


items_to_draw = [
    ("TOTAL", invoice.total.bounding_box, invoice.total.page),
    ("RECIPIENT", invoice.recipient.bounding_box, invoice.recipient.page),
    ("TAX", invoice.tax.bounding_box, invoice.tax.page),
    ("SENDER", invoice.sender.bounding_box, invoice.sender.page),
    ("ACCOUNT_NO", invoice.account_no.bounding_box, invoice.account_no.page)
]

doc = fitz.open(file_in)

for label, box, page_no in items_to_draw:
    if not box or box == [0, 0, 0, 0] or page_no is None:
        continue

    page = doc[page_no - 1]
    y0, x0, y1, x1 = box

    # From Gemini 2.0 onwards, models are further trained to detect objects in an image and get their bounding box coordinates.
    # The coordinates, relative to image dimensions, scale to [0, 1000]. You need to descale these coordinates based on your original image size.

    r = page.rect

    rect = fitz.Rect(
        (x0 / 1000) * r.width,
        (y0 / 1000) * r.height,
        (x1 / 1000) * r.width,
        (y1 / 1000) * r.height,
    )

    page.draw_rect(rect, color=(1,0,0), width=2)
    page.insert_text((rect.x0, rect.y0 - 2), label, fontsize=6, color=(1,0,0)) 

doc.save(file_out)
doc.close()
