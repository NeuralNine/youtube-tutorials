import sys
from datetime import datetime
from typing import Annotated, Optional

import httpx
import requests
from arcade_mcp_server import Context, MCPApp
from arcade_mcp_server.auth import Reddit

app = MCPApp(name="medical_data_server", version="1.0.0", log_level="DEBUG")


@app.tool
def get_side_effect_reports_from_clinicaltrials(drug_name: Annotated[str, "The name of the drug to get side effect reports for"], from_date: Annotated[Optional[str], "The minimum date to get side effect reports from (format = YYYY-MM-DD). Optional."] = None, to_date: Annotated[Optional[str], "The maximum date to get side effect reports to (format = YYYY-MM-DD). Optional."] = None) -> list[dict]:
    """Get side effect reports from ClinicalTrials.gov for a given drug name and optional date range."""
    base_url = 'https://clinicaltrials.gov/api/v2'

    params = {
        'query.term': drug_name,
        'pageSize': 25,
        'sort': 'ResultsFirstPostDate'
    }

    response = requests.get(base_url + '/studies', params=params)

    from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d') if from_date else None
    to_date_parsed = datetime.strptime(to_date, '%Y-%m-%d') if to_date else None

    studies = response.json()['studies']

    aggregated = {}

    for study in studies:
        if study['hasResults']:
            study_date = datetime.strptime(study['protocolSection']['statusModule']['resultsFirstPostDateStruct']['date'], '%Y-%m-%d')
            if from_date_parsed and to_date_parsed:
                date_in_range = study_date >= from_date_parsed and study_date <= to_date_parsed
            else:
                date_in_range = True

            if date_in_range:
                if 'seriousEvents' in study['resultsSection']['adverseEventsModule']:
                    events = study['resultsSection']['adverseEventsModule']['seriousEvents']
                    for event in events:
                        if event['stats'][0]['numAtRisk'] > 0:
                            name = event['term']
                            prob = event['stats'][0]['numAffected'] / event['stats'][0]['numAtRisk']
                            
                            if name not in aggregated:
                                aggregated[name] = {'probabilities': [], 'latest_date': study_date}
                            
                            aggregated[name]['probabilities'].append(prob)
                            if study_date > aggregated[name]['latest_date']:
                                aggregated[name]['latest_date'] = study_date

    results = [
        {
            'side_effect_name': name,
            'side_effect_probability': sum(data['probabilities']) / len(data['probabilities']),
            'side_effect_date': data['latest_date'].strftime('%Y-%m-%d')
        }
        for name, data in aggregated.items()
    ]

    return [x for x in results if x['side_effect_probability'] > 0.01]


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    app.run(transport=transport, host="127.0.0.1", port=8000)