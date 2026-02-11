import os

from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import db, Drug, SideEffectReport

GATEWAY_URL='https://api.arcade.dev/mcp/gw_39TzUVKFdP5OrtcwKVf3qJRlmbH'

flask_app = None

@tool
def list_drugs() -> list[str]:
    """List all drugs in the database"""
    with flask_app.app_context():
        return [drug.drug_name for drug in Drug.query.all()]


@tool
def create_drug(drug_name: str) -> str:
    """Create a new drug in the database. IMPORTANT: Always use list_drugs first to check if the drug already exists before creating."""
    with flask_app.app_context():
        existing = Drug.query.filter_by(drug_name=drug_name).first()
        if existing:
            return f"Drug '{drug_name}' already exists with ID {existing.id}"
        drug = Drug(drug_name=drug_name)
        db.session.add(drug)
        db.session.commit()
        return f"Drug '{drug_name}' created with ID {drug.id}"


@tool
def create_side_effect(drug_name: str, side_effect_name: str, probability: float) -> str:
    """Create a new side effect report for an existing drug. IMPORTANT: Always use list_side_effects first to check if this side effect already exists for this drug."""
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return f"Drug '{drug_name}' not found"
        
        existing = SideEffectReport.query.filter_by(drug_id=drug.id, side_effect_name=side_effect_name).first()
        if existing:
            return f"Side effect '{side_effect_name}' already exists for '{drug_name}'"
        
        report = SideEffectReport(
            side_effect_name=side_effect_name,
            side_effect_probability=probability,
            drug_id=drug.id
        )

        db.session.add(report)
        db.session.commit()
        return f"Side effect '{side_effect_name}' added to '{drug_name}'"


@tool
def list_side_effects(drug_name: str) -> list[dict]:
    """List all side effects for a specific drug"""
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return f"Drug '{drug_name}' not found"
        
        return [
            {
                "name": report.side_effect_name,
                "probability": report.side_effect_probability,
            }
            for report in drug.side_effect_reports
        ]


async def get_mcp_tools():
    client = MultiServerMCPClient(
        {
            'arcade': {
                'transport': 'http',
                'url': GATEWAY_URL,
                'headers': {
                    'Authorization': f'Bearer {os.getenv("ARCADE_API_KEY")}',
                    'Arcade-User-ID': os.getenv('ARCADE_USER_ID')
                }
            }
        }
    )

    return await client.get_tools()


local_tools = [list_drugs, list_side_effects, create_drug, create_side_effect]