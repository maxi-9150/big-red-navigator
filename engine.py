"""Local retrieval + evidence-only response composition. No external requests."""
import json, re, math
from pathlib import Path
from datetime import date
from typing import Protocol

DATA = Path(__file__).parent / 'data/resources.json'
STOP = set('i a an the to for in on of and is are can how do my me with need help where what get cornell student students'.split())

def tokens(text):
    return set(re.findall(r'[a-z0-9]+', text.lower())) - STOP

class Retriever(Protocol):
    def retrieve(self, question: str) -> list[dict]: ...

class LocalRetriever:
    """Transparent keyword retrieval; aliases enable limited Chinese discovery."""
    def __init__(self, records): self.records = records
    def retrieve(self, question):
        query = tokens(question)
        ranked = []
        for record in self.records:
            aliases = record['keywords']
            matched = [k for k in aliases if (k in query if k.isascii() and '-' not in k else k in question.lower())]
            if not matched: continue
            score = len(matched) + len(query & tokens(record['title'])) * .25
            ranked.append((score, record))
        return [r for _, r in sorted(ranked, key=lambda x: (-x[0], x[1]['id']))[:3]]

class AnswerProvider(Protocol):
    def compose(self, question: str, evidence: list[dict]) -> dict: ...

class EvidenceProvider:
    """Returns curated evidence verbatim, never invents a generated claim."""
    def compose(self, question, evidence):
        sensitive = bool(re.search(r'\b(eligible|eligibility|guarantee|approved|deadline|cost|fee|hours|today|tomorrow|diagnos|legal|allowed|qualify)\w*\b|资格|截止|费用|几点|今天|批准', question.lower()))
        status = 'limited' if sensitive and evidence else ('supported' if evidence else 'insufficient')
        return dict(status=status, message=(
            'I cannot determine personal eligibility, approval, costs, deadlines, or current availability from this seed collection. These resources may help you contact the right office.' if status == 'limited' else
            'Here are relevant summaries from the reviewed resource collection. They may not answer every part of your question.' if evidence else
            'I do not have enough relevant evidence in this small collection to answer. Try browsing resources or ask the relevant Cornell office.'),
            claims=[dict(text=r['summary'],source_id=r['id'],next_step=r['next_step']) for r in evidence])

class Navigator:
    def __init__(self, records=None, retriever=None, provider=None):
        self.records = records if records is not None else json.loads(DATA.read_text())
        self.retriever = retriever or LocalRetriever(self.records)
        self.provider = provider or EvidenceProvider()
    def answer(self, question, language="en"):
        evidence=self.retriever.retrieve(question)
        result=self.provider.compose(question,evidence)
        # Fail closed: an adapter must cite only supplied evidence, and every claim needs a citation.
        allowed={r['id'] for r in evidence}
        if result.get('status') not in {'supported','limited','insufficient'} or any(c.get('source_id') not in allowed or not isinstance(c.get('text'),str) for c in result.get('claims',[])):
            raise ValueError('Provider returned invalid evidence citations')
        if language == 'zh':
            result['message'] = {
                'supported': '在已核验的资源中找到了相关内容。这些摘要不一定能回答问题的每个部分。',
                'limited': '现有资料无法判断个人资格、批准结果、费用、截止日期或实时服务情况。请通过以下资源联系对应办公室确认。',
                'insufficient': '这个小型资源库没有足够的相关证据。请尝试按主题浏览，或联系对应的 Cornell 办公室。'
            }[result['status']]
            for claim in result['claims']:
                record = next(r for r in evidence if r['id'] == claim['source_id'])
                claim.update(text=record.get('summary_zh', record['summary']), next_step=record.get('next_step_zh',record['next_step']))
        result.update(sources=[dict(r,stale=(date.today()-date.fromisoformat(r['verified_on'])).days>90) for r in evidence],mode='local-evidence',generated=False)
        return result
