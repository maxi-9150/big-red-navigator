/* Deployment adapter: same curated evidence policy as engine.py, no remote AI. */
(function(root){
 const stop=new Set('i a an the to for in on of and is are can how do my me with need help where what get cornell student students'.split(' '));
 function tokens(text){return new Set((text.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(x=>!stop.has(x)));}
 function answer(question,language,records){
  const query=tokens(question),lower=question.toLowerCase();
  const evidence=records.map(record=>{const matched=record.keywords.filter(k=>/^[\x00-\x7F]+$/.test(k)&&!k.includes('-')?query.has(k):lower.includes(k));return {record,score:matched.length?matched.length+[...tokens(record.title)].filter(t=>query.has(t)).length*.25:0};}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.record.id.localeCompare(b.record.id)).slice(0,3).map(x=>x.record);
  const sensitive=/\b(eligible|eligibility|guarantee|approved|deadline|cost|fee|hours|today|tomorrow|diagnos|legal|allowed|qualify)\w*\b|资格|截止|费用|几点|今天|批准/.test(lower);
  const status=evidence.length?(sensitive?'limited':'supported'):'insufficient';
  const messages={en:{supported:'Here are relevant summaries from the reviewed resource collection. They may not answer every part of your question.',limited:'I cannot determine personal eligibility, approval, costs, deadlines, or current availability from this seed collection. These resources may help you contact the right office.',insufficient:'I do not have enough relevant evidence in this small collection to answer. Try browsing resources or ask the relevant Cornell office.'},zh:{supported:'在已核验的资源中找到了相关内容。这些摘要不一定能回答问题的每个部分。',limited:'现有资料无法判断个人资格、批准结果、费用、截止日期或实时服务情况。请通过以下资源联系对应办公室确认。',insufficient:'这个小型资源库没有足够的相关证据。请尝试按主题浏览，或联系对应的 Cornell 办公室。'}};
  return {status,message:messages[language==='zh'?'zh':'en'][status],sources:evidence,claims:evidence.map(r=>({text:language==='zh'?r.summary_zh:r.summary,source_id:r.id,next_step:language==='zh'?r.next_step_zh:r.next_step})),mode:'browser-evidence',generated:false};
 }
 root.BigRedEvidence={answer};
})(typeof globalThis!=='undefined'?globalThis:window);
