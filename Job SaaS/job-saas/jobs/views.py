from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .services import search_jobs_with_agent, is_ready
from .models import LLMResult, Snapshot
from .tasks import process_snapshots_and_summarize


def home_view(request):
    return render(request, 'jobs/home.html')


@login_required
def search_job_view(request):
    context = {}

    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            try:
                llm_result = LLMResult(
                    title = 'New Job Search',
                    prompt = prompt,
                    status = 'pending',
                    owner = request.user
                )
                llm_result.save()

                result = search_jobs_with_agent(llm_result.id, prompt)
                context['result'] = result
                context['prompt'] = prompt
            except Exception as e:
                context['error'] = str(e)
    
    return render(request, 'search.html', context)
    

@login_required
def results_list_view(request):
    for llm_result in LLMResult.objects.filter(owner=request.user, status='pending'):
        snapshots = Snapshot.objects.filter(llm_result_id=llm_result.id)

        for snapshot in snapshots:
            if not snapshot.ready and is_ready(snapshot.snapshot_id):
                snapshot.ready = True
                snapshot.save()

        if snapshots.exists() and all(s.ready for s in snapshots):
            process_snapshots_and_summarize.delay(llm_result.id)

    results = LLMResult.objects.filter(owner=request.user).order_by('-id')
    results_data = []

    for result in results:
        total_snapshots = Snapshot.objects.filter(llm_result_id=result.id).count()
        ready_snapshots = Snapshot.objects.filter(llm_result_id=result.id, ready=True).count()

        results_data.append({
            'result': result, 
            'job_listings': list(result.job_listing_results.all()),
            'total_snapshots': total_snapshots,
            'ready_snapshots': ready_snapshots,
        })

    return render(request, 'jobs/results_list.html', {'results': results_data})



