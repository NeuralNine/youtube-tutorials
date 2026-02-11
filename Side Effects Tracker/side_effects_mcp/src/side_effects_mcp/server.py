#!/usr/bin/env python3
"""side_effects_mcp MCP server"""

import sys
from typing import Annotated

import requests
from arcade_mcp_server import MCPApp

app = MCPApp(name="side_effects_mcp", version="1.0.0", log_level="DEBUG")


@app.tool
def get_side_effects_for_drug(drug_name: Annotated[str, "The name of the medical drug to find side effects for"]) -> list[dict]:
    """Get side effect reports from ClinicalTrials.gov for a given drug name"""
    base_url = 'https://clinicaltrials.gov/api/v2'

    params = {
        'query.term': drug_name,
        'pageSize': 25,
        'sort': 'ResultsFirstPostDate'
    }

    response = requests.get(base_url + '/studies', params=params)

    studies = response.json()['studies']

    print(studies)

    aggregated = {}

    for study in studies:
        if study['hasResults']:
            if 'seriousEvents' in study['resultsSection']['adverseEventsModule']:
                events = study['resultsSection']['adverseEventsModule']['seriousEvents']
                
                for event in events:
                    if event['stats'][0]['numAtRisk'] > 0:
                        name = event['term']
                        probability = event['stats'][0]['numAffected'] / event['stats'][0]['numAtRisk']

                        if name in aggregated:
                            aggregated[name].append(probability)
                        else:
                            aggregated[name] = [probability]

    results = [
        {
            'side_effect_name': name,
            'side_effect_probability': sum(probabilities) / len(probabilities)
        } for name, probabilities in aggregated.items()
    ]

    return [x for x in results if x['side_effect_probability'] > 0.01]


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    app.run(transport=transport, host="127.0.0.1", port=8000)