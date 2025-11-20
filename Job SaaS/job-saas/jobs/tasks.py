from celery import shared_task

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from .models import Snapshot, LLMResult, JobListingResult
from .services import get_data
from .llm_schemas import JobListings


@shared_task
def process_snapshots_and_summarize(llm_result_id):
    try:
        llm_result = LLMResult.objects.get(id=llm_result_id)
        llm_result.status = 'processing'
        llm_result.save()

        snapshots = Snapshot.objects.filter(llm_result_id=llm_result_id)

        data_string = ""

        for snapshot in snapshots:
            snapshot.data = get_data(snapshot.snapshot_id)
            snapshot.save()

            data_string += str(snapshot.data)
            data_string += '\n'

        chat = init_chat_model('gpt-4o-mini')

        structured_chat = chat.with_structured_output(JobListings)

        result = structured_chat.invoke([
            SystemMessage(content="You are a helpful assistant that summarizes job search results. Make sure to always include links."),
            HumanMessage(content="Summarize the following job search results: " + data_string)
        ])

        for job_listing in result.listings:
            job_listing_result = JobListingResult(
                llm_result = llm_result,
                title=job_listing.title,
                job_type=job_listing.job_type,
                level=job_listing.level,
                summary=job_listing.summary,
                salary=job_listing.salary,
                posted=job_listing.posted,
                applicants=job_listing.applicants,
                job_url=job_listing.job_url,
            )
            job_listing_result.save()

        llm_result.status = 'ready'
        llm_result.save()

        return f"Successfully processed and summarized LLM result for {llm_result.id}"
    except Exception as e:
        print(str(e))
        raise