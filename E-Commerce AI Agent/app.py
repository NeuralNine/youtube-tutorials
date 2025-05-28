import os
import json
import asyncio
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from flask import Flask, render_template, redirect, url_for, flash, request
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


load_dotenv()
model = ChatOpenAI(model='gpt-4o')

server_params = StdioServerParameters(
    command='npx',
    args=['@brightdata/mcp'],
    env = {
        'API_TOKEN': os.getenv('API_TOKEN'),
        'BROWSER_AUTH': os.getenv('BROWSER_AUTH'),
        'WEB_UNLOCKER_ZONE': os.getenv('WEB_UNLOCKER_ZONE')
    }
)

SYSTEM_PROMPT = (
    "To find products, first use the search_engine tool. When finding products, use the web_data tool for the platform. If none exists, scrape as markdown."
    "Example: Don't use web_data_bestbuy_products for search. Use it only for getting data on specific products you already found in search."
)

PLATFORMS = ['Amazon', 'Best Buy', 'Ebay', 'Walmart', 'Target', 'Costco', 'Newegg']


class Hit(BaseModel):
    url: str = Field(..., description='The URL of the product that was found')
    title: str = Field(..., description='The title of the product that was found')
    rating: str = Field(..., description='The rating of the product (stars, number of ratings given etc.)')


class PlatformBlock(BaseModel):
    platform: str = Field(..., description='Name of the platform')
    results: list[Hit] = Field(..., description='List of results for this platform')


class ProductSearchResponse(BaseModel):
    platforms: list[PlatformBlock] = Field(..., description='Aggregated list of all results grouped by platform')



app = Flask(__name__)
app.secret_key = 'mysecretkey-not-for-prod'


async def run_agent(query, platforms):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as sess:
            await sess.initialize()

            tools = await load_mcp_tools(sess)

            agent = create_react_agent(model, tools, response_format=ProductSearchResponse)

            prompt = f'{query}\n\nPlatforms: {",".join(platforms)}'

            result = await agent.ainvoke(
                {
                    'messages': [
                        {'role': 'system', 'content': SYSTEM_PROMPT},
                        {'role': 'user', 'content': prompt}
                    ]
                }
            )

            structured = result['structured_response']

            return structured.model_dump()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query      = request.form.get("query", "").strip()
        platforms  = request.form.getlist("platforms")
        if not query:
            flash("Please enter a search query.", "danger")
            return redirect(url_for("index"))
        if not platforms:
            flash("Select at least one platform.", "danger")
            return redirect(url_for("index"))

        try:
            response_json = asyncio.run(run_agent(query, platforms))
        except Exception as exc:
            flash(f"Agent error: {exc}", "danger")
            return redirect(url_for("index"))

        return render_template(
            "index.html",
            query=query,
            platforms=PLATFORMS,
            selected=platforms,
            response=response_json,
        )

    return render_template(
        "index.html",
        query="",
        platforms=PLATFORMS,
        selected=[],
        response=None,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
