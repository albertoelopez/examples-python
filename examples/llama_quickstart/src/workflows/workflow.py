from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.hn.search import hn_search
    from src.functions.hn.schema import HnSearchInput
    from src.functions.crawl.website import crawl_website
    from src.functions.llm.chat import llm_chat, FunctionInputParams
    

@workflow.defn(name="hn_workflow")
class hn_workflow:
    @workflow.run
    async def run(self, input: dict):

        log.info("Search Court Information", extra={"query": input["query"]})
        query = input["query"]  # This would be the case number
        url = f"https://www.lacourt.org"
        
        log.info("court_case", extra={"url": url})
        content = await workflow.step(crawl_website, url, start_to_close_timeout=timedelta(seconds=30))
        
        system_prompt = f"Search Los Angeles County Court Case Information: {query}"
        user_prompt = f"Summarize the following content in layman's terms: {content}"
        summary = await workflow.step(llm_chat, FunctionInputParams(system_prompt=system_prompt, user_prompt=user_prompt), task_queue="llm_chat",start_to_close_timeout=timedelta(seconds=120))

        return summary