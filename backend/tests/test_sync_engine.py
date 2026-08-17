from langchain_core.documents import Document
from app.sync.web_crawler import WebCrawler
from app.sync.diff_engine import DocumentDiffEngine
from app.sync.version_store import DocumentVersionStore
from app.sync.sync_scheduler import SyncScheduler

def test_web_crawler_html_cleaner():
    crawler = WebCrawler()
    raw_html = """
    <html>
      <head><title>API Authentication Docs</title></head>
      <body>
        <nav><a href="/">Home</a></nav>
        <main>
          <h1>API Authentication</h1>
          <p>Bearer tokens are required for all endpoints.</p>
        </main>
        <footer>(c) 2026 Company Inc.</footer>
      </body>
    </html>
    """
    doc = crawler.clean_html(raw_html, "https://docs.company.com/auth")
    assert "Bearer tokens are required" in doc.page_content
    assert "Home" not in doc.page_content  # stripped nav
    assert "Company Inc" not in doc.page_content  # stripped footer
    assert doc.metadata["document_name"] == "API Authentication Docs"


def test_diff_engine_chunk_and_unified_diff():
    old_text = "Line 1: Refund window is 14 days.\nLine 2: Contact billing@company.com"
    new_text = "Line 1: Refund window is 30 days.\nLine 2: Contact billing@company.com"

    diff = DocumentDiffEngine.generate_unified_diff(old_text, new_text)
    assert "-Line 1: Refund window is 14 days." in diff
    assert "+Line 1: Refund window is 30 days." in diff

    c_old = [Document(page_content="Old Chunk A", metadata={"section": "SecA"})]
    c_new = [
        Document(page_content="New Chunk A", metadata={"section": "SecA"}),
        Document(page_content="Added Chunk B", metadata={"section": "SecB"}),
    ]
    res = DocumentDiffEngine.compute_diff(c_old, c_new)
    assert len(res.added) == 1
    assert len(res.modified) == 1
    assert len(res.removed) == 0


def test_version_store_and_scheduler():
    vstore = DocumentVersionStore()
    v1 = vstore.record_version("doc_1", "Policy.md", "Content v1", 4, "Initial upload")
    v2 = vstore.record_version("doc_1", "Policy.md", "Content v2", 5, "Updated pricing")

    assert v1.version_id == 1
    assert v2.version_id == 2
    assert v1.checksum != v2.checksum
    assert len(vstore.get_versions("doc_1")) == 2

    sched = SyncScheduler()
    job = sched.register_job("https://docs.company.com", "hourly")
    assert job.schedule == "hourly"
    updated_job = sched.trigger_job_run(job.job_id)
    assert updated_job.docs_updated == 2