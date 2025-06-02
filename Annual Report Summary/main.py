import os
import json
from datetime import datetime
from typing import List, Optional

import PyPDF2
import tiktoken
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from markdown2 import markdown
from weasyprint import HTML


load_dotenv()


def load_file(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "".join(page.extract_text() or "" for page in reader.pages)


text = load_file('meta_10k.pdf')


class AnnualReport(BaseModel):
    company_name: str = Field(..., description="Name of the company as reported in the 10-K")
    cik: str = Field(..., description="Central Index Key (CIK) identifier assigned by the SEC")
    fiscal_year_end: datetime = Field(..., description="Fiscal year end date")
    filing_date: datetime = Field(..., description="Date when the 10-K was filed with the SEC")
    total_revenue: Optional[float] = Field(None, description="Total revenue for the fiscal year (in USD)")
    net_income: Optional[float] = Field(None, description="Net income (profit) for the fiscal year (in USD)")
    total_assets: Optional[float] = Field(None, description="Total assets at fiscal year end (in USD)")
    total_liabilities: Optional[float] = Field(None, description="Total liabilities at fiscal year end (in USD)")
    operating_cash_flow: Optional[float] = Field(None, description="Net cash provided by operating activities (in USD)")
    cash_and_equivalents: Optional[float] = Field(None, description="Cash and cash equivalents at fiscal year end (in USD)")
    num_employees: Optional[int] = Field(None, description="Number of employees reported")
    auditor: Optional[str] = Field(None, description="Name of the external auditor")
    business_description: Optional[str] = Field(None, description="Company’s business overview (Item 1)")
    risk_factors: Optional[List[str]] = Field(None, description="Key risk factors (Item 1A)")
    management_discussion: Optional[str] = Field(None, description="Management’s Discussion & Analysis (Item 7)")


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

schema_definition = json.dumps(AnnualReport.model_json_schema(), indent=2, ensure_ascii=False)

prompt = f"Analyze the following annual report (10-K) and fill the data model based on it:\n\n{text}\n\n"
prompt += f"The output needs to be in the following format:\n\n{schema_definition}\n\nNo extra fields allowed at all!"

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': AnnualReport
    }
)

ar = AnnualReport.model_validate_json(response.text)

print(ar)



md_lines = [
    f"# {ar.company_name} Annual Report {ar.fiscal_year_end.year}",
    f"**CIK:** {ar.cik}",
    f"**Fiscal Year End:** {ar.fiscal_year_end.strftime('%Y-%m-%d')}",
    f"**Filing Date:** {ar.filing_date.strftime('%Y-%m-%d')}",
    "## Financials"
]

if ar.total_revenue is not None:
    md_lines.append(f"- **Total Revenue:** ${ar.total_revenue:,.2f}")
if ar.net_income is not None:
    md_lines.append(f"- **Net Income:** ${ar.net_income:,.2f}")
if ar.total_assets is not None:
    md_lines.append(f"- **Total Assets:** ${ar.total_assets:,.2f}")
if ar.total_liabilities is not None:
    md_lines.append(f"- **Total Liabilities:** ${ar.total_liabilities:,.2f}")
if ar.operating_cash_flow is not None:
    md_lines.append(f"- **Operating Cash Flow:** ${ar.operating_cash_flow:,.2f}")
if ar.cash_and_equivalents is not None:
    md_lines.append(f"- **Cash & Equivalents:** ${ar.cash_and_equivalents:,.2f}")
if ar.num_employees is not None:
    md_lines.append(f"- **Number of Employees:** {ar.num_employees}")
if ar.auditor:
    md_lines.append(f"- **Auditor:** {ar.auditor}")

if ar.business_description:
    md_lines += ["\n## Business Description", ar.business_description]
if ar.risk_factors:
    md_lines += ["\n## Risk Factors"] + [f"- {rf}" for rf in ar.risk_factors]
if ar.management_discussion:
    md_lines += ["\n## Management Discussion & Analysis", ar.management_discussion]

md = "\n\n".join(md_lines)
html = markdown(md)
company = ar.company_name.replace(" ", "_")
filename = f"annual_report_{company}_{ar.fiscal_year_end.year}.pdf"
HTML(string=html).write_pdf(filename)

