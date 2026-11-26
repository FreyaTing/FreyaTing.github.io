"""Generate dependency-free bilingual pages from the curated public profile."""
import json, html, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'profile.json').read_text())
def esc(s): return html.escape(str(s),quote=True)
def external(url,label,cls=''): return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true"> ↗</span></a>'
def wave(n):
    lines=[]
    for j in range(5):
        pts=' '.join(f'{x},{50+math.sin(x/24+j*.55)*math.sin(x/190*math.pi)*(13+j*4)}' for x in range(0,221,2))
        lines.append(f'<polyline points="{pts}" opacity="{.25+j*.15}"/>')
    return '<svg viewBox="0 0 220 100" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">'+''.join(lines)+'</svg>'
CURRENT=[('独立培养','Primary supervision',[('袁艺轩',''),('张艺菲','')]),('与清华大学张丹老师联合指导','Co-supervised with Dan Zhang · Tsinghua University',[('欧柔妮',''),('储娜',''),('张昕怡',''),('梁越铭','')]),('与上海交通大学吴梦玥老师联合指导','Co-supervised with Mengyue Wu · Shanghai Jiao Tong University',[('梅嘉豪',''),('金乐源',''),('李师萌','')])]
ALUMNI=[('独立培养','Primary supervision',[('丁佳欣',('悉尼大学','The University of Sydney'))]),('与首都医科大学杨志老师联合指导','Co-supervised with Zhi Yang · Capital Medical University',[('刘静静',('上海市精神卫生中心','Shanghai Mental Health Center')),('谢舒淇',('慕尼黑工业大学','Technical University of Munich')),('金书玉',('厦门仙岳医院','Xiamen Xianyue Hospital'))]),('与清华大学张丹老师联合指导','Co-supervised with Dan Zhang · Tsinghua University',[('孙博',('清华大学','Tsinghua University')),('刘嘉萌',('香港理工大学','The Hong Kong Polytechnic University')),('付雯雯',('华西医院','West China Hospital'))])]
SELECTED={3,4,9,14,18,21,24,25,28}
for lang in ['en','zh']:
    zh=lang=='zh'
    t=lambda en,cn: cn if zh else en
    get=lambda v: v[lang]
    nav=[('about',t('About','关于')),('research',t('Research','研究')),('publications',t('Publications','论文')),('group',t('Group members','团队')),('experience',t('Experience','经历'))]
    navhtml=''.join(f'<a href="#{i}">{s}</a>' for i,s in nav)
    bio=get(D['bio'])
    themes=''.join(f'<article class="theme"><span class="eyebrow">0{i+1}</span>{wave(i)}<h3>{esc(x[lang])}</h3><p>{esc(get(x["description"]))}</p></article>' for i,x in enumerate(D['themes']))
    pubs=[]
    for p in sorted(D['publications'],key=lambda p:-p['year']):
        status=p['status']; title=esc(p['title'])
        title=external(p['url'],title) if p.get('url') else title
        authors=esc(p['authors']).replace('Yue Ding','<strong>Yue Ding</strong>')
        badge=f'<span class="preprint">{t("Preprint · not peer reviewed","预印本 · 未经同行评审")}</span>' if status=='preprint' else (f'<span class="preprint">{t("In press · link opens preprint","接收待刊 · 链接为预印本")}</span>' if status=='in_press' else '')
        search=esc(' '.join(str(p[k]) for k in ['title','authors','venue','year']).lower())
        pubs.append(f'<article class="publication" data-kind="{status}" data-selected="{str(p["id"] in SELECTED).lower()}" data-search="{search}"><div class="pub-year">{p["year"]}</div><div><div class="pub-venue">{esc(p["venue"])} {badge}</div><h3>{title}</h3><p class="authors">{authors}</p></div></article>')
    def members(groups):
        out=[]
        for cn,en,people in groups:
            names=''.join(f'<li><span class="student-name" lang="zh-CN">{name}</span>'+ (f'<span class="destination"><span aria-hidden="true">↗ </span>{esc(dest[0 if zh else 1])}</span>' if dest else '')+'</li>' for name,dest in people)
            out.append(f'<div class="supervision"><h4>{esc(t(en,cn))}</h4><ul>{names}</ul></div>')
        return ''.join(out)
    def timeline(key): return ''.join(f'<li><span class="timeline-date">{esc(x["years"].replace("Present","至今").replace("Current","现任") if zh else x["years"])}</span><p>{esc(x[lang])}</p></li>' for x in D[key])
    grants=''.join(f'<article class="grant"><span class="tag">{esc(get(g["role"]))}{t(' · Awarded; starts 2027',' · 已获资助，2027 年启动') if g['status']=='awarded' else ''}</span><h4>{esc(get(g["title"]))}</h4><p>{esc(get(g["description"]).split(" — ",1)[-1])}</p></article>' for g in D['grants'] if g['status'] in ('ongoing','awarded'))
    patents=''.join(f'<li><strong>{p["year"]} · {esc(p["number"])}</strong><br>{esc(get(p["title"]))}</li>' for p in sorted(D['patents'],key=lambda p:-p['year']))
    pastgrants=''.join(f'<li>{esc(get(g["description"]))}</li>' for g in D['grants'] if g['status']=='completed')
    service=''.join(f'<li><span>{esc(x["years"].replace("Present","至今").replace("Current","现任") if zh else x["years"])}</span><p>{esc(x[lang])}</p></li>' for x in D['service'])
    desc=t('Yue Ding, Ph.D. — neuroscience, music-based interventions, affective computing and mental health at Shanghai Mental Health Center.','丁悦，上海交通大学医学院附属精神卫生中心助理研究员、硕士生导师。研究音乐干预、神经调控、情感计算与精神健康。')
    currentpage='zh.html' if zh else 'index.html'
    other='index.html' if zh else 'zh.html'
    site=f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">
<title>{t('Yue Ding · Neuroscience & Mental Health','丁悦 · 神经科学与精神健康')}</title>
<meta name="description" content="{esc(desc)}"><meta property="og:title" content="Yue Ding 丁悦 · Neuroscience & Mental Health"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="https://freyating.github.io/assets/portrait.png">
<link rel="canonical" href="https://freyating.github.io/{'zh.html' if zh else ''}"><link rel="alternate" hreflang="en" href="https://freyating.github.io/"><link rel="alternate" hreflang="zh-CN" href="https://freyating.github.io/zh.html"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip" href="#main">{t('Skip to content','跳转到正文')}</a>
<header class="site-header"><div class="header-inner"><a href="#" class="brand" aria-label="Yue Ding home"><span class="brand-symbol" aria-hidden="true">yd<span>.</span></span><span>YUE DING <span class="brand-cn" lang="zh-CN">丁悦</span></span></a><nav aria-label="{t('Main navigation','主导航')}">{navhtml}</nav><a class="language" href="{other}" lang="{'en' if zh else 'zh-CN'}" aria-label="{t('Switch to Chinese','切换至英文')}">{t('中文','EN')} <span aria-hidden="true">↗</span></a></div></header>
<main id="main"><section class="hero wrap" id="about"><div class="hero-copy"><p class="eyebrow"><span class="small-dot"></span> {t('NEUROSCIENCE × MENTAL HEALTH','神经科学 × 精神健康')}</p><h1>{t('Yue Ding<span class="name-cn" lang="zh-CN">丁悦</span>','丁悦<span class="name-cn">Yue Ding</span>')}</h1><p class="role">{esc(get(D['title']))}</p><p class="affiliation">{esc(get(D['institution']))}</p><p class="hero-statement">{t('Understanding the brain.<br><em>Tuning emotion.</em>','理解大脑，<br><em>探索情绪调节。</em>')}</p><p class="intro">{esc(bio)}</p><div class="hero-links">{external(D['scholar'],'Google Scholar','button primary')}{external(D['orcid'],'ORCID','text-link')}<a class="text-link" href="#contact">{t('Get in touch','联系我')} <span aria-hidden="true">↗</span></a></div></div><div class="portrait-column"><div class="portrait-frame"><img src="assets/portrait.png" alt="{t('Portrait of Yue Ding','丁悦个人照片')}" width="410" height="389" fetchpriority="high"></div><div class="portrait-caption"><span>{t('Yue Ding, Ph.D.','丁悦 博士')}</span><span>Shanghai, China</span></div><div class="hero-wave">{wave(0)}<span>{t('Music · Brain · Emotion','音乐 · 大脑 · 情绪')}</span></div></div></section>
<div class="research-strip"><div class="wrap"><span>{t('RESEARCH AT THE INTERSECTION OF','交叉研究')}</span><p>{t('Music & rhythm','音乐与节律')}<i> / </i>{t('Neural dynamics','神经动力学')}<i> / </i>{t('Mental health','精神健康')}</p></div></div>
<section id="research" class="section wrap"><div class="section-heading"><div><p class="eyebrow">01 / {t('RESEARCH','研究方向')}</p><h2>{t('From neural mechanisms<br>to personalized interventions.','从神经机制，<br>到个体化干预。')}</h2></div><p>{t('Connecting human neuroscience, intelligent technologies and clinical questions to investigate how we perceive, feel and regulate emotion.','结合人类神经科学、智能技术与临床问题，探索感知、情绪及其调节机制。')}</p></div><div class="themes">{themes}</div></section>
<section id="publications" class="section publications-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">02 / {t('PUBLICATIONS','学术论文')}</p><h2>{t('Ideas, tested.','研究与发现。')}</h2></div>{external(D['scholar'],t('View on Google Scholar','访问 Google Scholar'),'text-link')}</div><div class="publication-tools" hidden><div class="filter-group" role="group" aria-label="{t('Filter publications','筛选论文')}"><button class="filter active" data-filter="selected" aria-pressed="true">{t('Selected','代表作')}</button><button class="filter" data-filter="all" aria-pressed="false">{t('All','全部')}</button><button class="filter" data-filter="published" aria-pressed="false">{t('Journal articles','期刊论文')}</button><button class="filter" data-filter="in_press" aria-pressed="false">{t('In press','接收待刊')}</button><button class="filter" data-filter="preprint" aria-pressed="false">{t('Preprints','预印本')}</button></div><label class="search"><span aria-hidden="true">⌕</span><span class="sr-only">{t('Search title, author, venue or year','搜索标题、作者、期刊或年份')}</span><input type="search" id="paper-search" placeholder="{t('Search publications…','搜索论文…')}"></label></div><p class="pub-note">{t('Yue Ding in bold · # Equal contribution · * Corresponding author','粗体为本人 · # 共同贡献 · * 通讯作者')}</p><p id="result-count" class="sr-only" role="status" aria-live="polite"></p><div class="publication-list">{''.join(pubs)}</div><p id="no-results" class="empty-state" hidden>{t('No matching publications. Try another keyword or filter.','没有匹配的论文，请尝试其他关键词或分类。')}</p><p class="source-note">{t('Publication list updated from the revised December 2026 CV.','论文目录已根据修订后的 2026 年 12 月版 CV 更新。')}</p></div></section>
<section id="group" class="section wrap"><div class="section-heading"><div><p class="eyebrow">03 / {t('GROUP MEMBERS','团队成员')}</p><h2>{t('People & collaboration.','共同探索，一起成长。')}</h2></div><p>{t('Students under primary supervision and joint supervision across collaborating institutions.','独立培养与跨机构联合指导的学生。')}</p></div><div class="members-columns"><div class="member-panel"><div class="member-title"><h3>{t('Current students','在读学生')}</h3><span>09</span></div>{members(CURRENT)}</div><div class="member-panel alumni"><div class="member-title"><h3>{t('Student alumni','毕业学生')}</h3><span>07</span></div>{members(ALUMNI)}</div></div></section>
<section id="experience" class="section experience-section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">04 / {t('BACKGROUND','学术经历')}</p><h2>{t('A cross-disciplinary path.','跨学科的研究旅程。')}</h2></div></div><div class="experience-grid"><div><h3>{t('Appointments','工作经历')}</h3><ol class="timeline">{timeline('experience')}</ol></div><div><h3>{t('Education','教育背景')}</h3><ol class="timeline">{timeline('education')}</ol></div></div></div></section>
<section class="section wrap" id="projects"><div class="section-heading"><div><p class="eyebrow">05 / {t('FUNDED RESEARCH','科研项目')}</p><h2>{t('Current & awarded projects.','在研与获批项目。')}</h2></div></div><div class="grants">{grants}</div><details class="past-projects"><summary>{t('Completed projects','已结题项目')} <span aria-hidden="true">＋</span></summary><ul>{pastgrants}</ul></details><details class="past-projects" id="patents"><summary>{t('Authorized patents','授权专利')} · {len(D['patents'])} <span aria-hidden="true">＋</span></summary><ul>{patents}</ul></details></section>
<section class="section service-section"><div class="wrap service-grid"><div><p class="eyebrow">06 / {t('ACADEMIC COMMUNITY','学术服务')}</p><h2>{t('Service & teaching.','学术服务与教学。')}</h2><div class="teaching"><h3>{t('Courses','教学课程')}</h3>{''.join('<p>'+esc(x[lang])+'</p>' for x in D['teaching'])}</div></div><ul class="service-list">{service}</ul></div></section>
<section class="contact wrap section" id="contact"><div><p class="eyebrow">{t('GET IN TOUCH','联系我')}</p><h2>{t('Let’s connect.','期待交流。')}</h2><p>{t('For research and academic enquiries.','欢迎就研究合作与学术问题交流。')}</p></div><div class="contact-details"><a class="email" href="mailto:{D['email']}">{D['email']} <span aria-hidden="true">↗</span></a><p>{esc(get(D['institution']))}<br>{t('Shanghai, China','中国 · 上海')}</p><div class="contact-links">{external(D['scholar'],'Google Scholar')}{external(D['orcid'],'ORCID')}{external('https://www.smhc.org.cn/njkyjy/info/4633/3362.htm',t('Institutional profile','机构主页'))}</div></div></section></main>
<footer><div class="wrap"><span>© 2026 {t('Yue Ding','丁悦')} · {t('Academic homepage','个人学术主页')}</span><span>{t('Updated 26 November 2026','更新于 2026 年 11 月 26 日')} <a href="#">{t('Back to top','返回顶部')} ↑</a></span></div></footer></body></html>'''
    (ROOT/currentpage).write_text(site)
print('Built index.html and zh.html')
