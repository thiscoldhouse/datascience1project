---
title: "False memories to fake news: The evolution of the term “misinformation” in academic literature"
theme: metropolis
fonttheme: serif
fontsize: 13pt
aspectratio: 169
header-includes:
- \usepackage{xcolor}
- \definecolor{darkbg}{HTML}{171D1C}
- \definecolor{lighttext}{HTML}{FFFFFF}
- \definecolor{darktext}{HTML}{171D1C}
- \definecolor{accent}{HTML}{DB9D47}
- \definecolor{accent2}{HTML}{8CC084}
- \setbeamercolor{background canvas}{bg=lighttext}
- \setbeamercolor{normal text}{fg=darktext,bg=lighttext}
- \setbeamercolor{title}{fg=darkbg,bg=accent!80}
- \setbeamercolor{frametitle}{fg=darktext,bg=accent!80}
- \setbeamercolor{structure}{fg=accent}
- \setbeamercolor{alerted text}{fg=accent}
- \setbeamercolor{item}{fg=accent}
- \setbeamercolor{subitem}{fg=accent2}
- \setbeamercolor{section in toc}{fg=accent}
- \setbeamercolor{subsection in toc}{fg=accent2}
- \setbeamercolor{block title}{fg=darkbg,bg=accent!60}
- \setbeamercolor{block body}{fg=darktext,bg=accent!10}
- \setbeamercolor{block title alerted}{fg=darkbg,bg=accent2}
- \setbeamercolor{block body alerted}{fg=darktext,bg=accent2!10}
- \setbeamercolor{block title example}{fg=lighttext,bg=darkbg}
- \setbeamercolor{block body example}{fg=darktext,bg=darkbg!5}
- \setbeamercolor{footline}{fg=darktext,bg=accent!40}
- \setbeamertemplate{navigation symbols}{}
- \setbeamertemplate{itemize item}{\color{accent}\large\textbullet}
- \setbeamertemplate{itemize subitem}{\color{accent!85}\small\textbullet}
- \setbeamertemplate{itemize subsubitem}{\color{accent!70}\tiny\textbullet}
- \metroset{progressbar=none}
- \metroset{progressbar=none}
- \setbeamertemplate{footline}{}

---

# History of the term in the literature

## 50s--60s: Medicine and Public Health
\scriptsize
- 1956: "Combating Food Misinformation and Quackery" [@HUENEMANN1956623]
- 1957: "Information and Misinformation Gained from Fasting Blood Sugar Alone in Diabetes Therapy" [@johnInformationMisinformationGained1957]

## 60s--70s: Public health dominates, but usage diversifies
\scriptsize
- 1970: "A Model of the Soviet Firm" discusses Soviet firms’ attempts to correct for “systematic misinformation” by  changing incentives [@gindinModelSovietFirm1970]

## 70s--90s: More specialized uses with technical meanings, e.g. associated with computation
\scriptsize
- **1974: "Reconstruction of automobile destruction: An example of the interaction between language and memory" introduces the "misinformation effect"[@loftus_reconstruction_1974]**
- 1989: "Categorical Approach to Distributed Systems, Expressibility and Knowledge: "It is asserted that to obtain a meaningful comparison of protocols, the adversary should be chosen not to send identical faulty messages but to 'convey' the same misinformation" [@michelCategoricalApproachDistributed1989]

# History of the term in the literature

## 2000s
- 2002: "Infodemiology: The Epidemiology of (Mis)Information" studies "the study of the determinants and distribution of health information and misinformation"[@eysenbachInfodemiologyEpidemiologyMisinformation2002]
- 2007--2010 - Infodemiology extends to study how (mis)information spreads during crises (earthquakes, epidemics, etc.) on social media [@suttonBackchannelsFrontLines2008, @chewPandemicsAgeTwitter2010, @ohEXPLORATIONSOCIALMEDIA2010]

## 2010s to today
- The *post-2016 paradigm* is born


# Birth of a paradigm on Twitter

\vfill
\begin{center}
\includegraphics[width=\textwidth,height=0.85\textheight,keepaspectratio]{misc-img/storywrangler.pdf}
\end{center}
\vfill

# How misinformation studies tells its history

- Misinformation has always existed because people have always said false things
- Technology affects the spread of misinformation
- Social media lead to a kind of misinformation inflection point

## Examples from two lit reviews
\scriptsize
- "While history shows that false and misleading information is not a new phenomenon, most observers seem to agree that misinformation, disinformation, and fake news have become much more prevalent during the last decade." [@broda_misinformation_2024]
- "Although misinformation can circulate exceedingly fast due to advances in social technologies and large-scale information cascades, the roots of fake news go back to the days before the Printing Revolution, when word-of-mouth was the primary method of news transmission." [@faedda_fake_2024]

# What's missing?

- *Misinformation* is a scientific paradigm [@kuhn_structure_1962] with more conceptual baggage than its literal definition
- Histories are told within the paradigm, not of the paradigm
- Where does the concept come from?
  - Two options: creatio ex nihilo vs creatio ex materia

\vfill
\begin{center}
\includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{mouse.png}
\end{center}
\vfill

# Brief anatomy of the paradigm

## Definition
\scriptsize
- There are false statements, i.e., \textit{misinformation}
- People make, read, and share misinformation, often (usually?) on social media
- The sum of many such events results in harm to society

## Example supplementary concepts

\scriptsize
- Disinformation
- Fact-check
- Infodemic
- Fake news
- Faith in institutions
- (Anti-)science
  
## Notably missing
\scriptsize
- Epistemology
- Mediation


# Birth of a paradigm in academic literature

\vfill
\begin{center}
\includegraphics[width=\textwidth,height=0.9\textheight,keepaspectratio]{term-frequency-img/fig.pdf}
\end{center}
\vfill

# Creatio ex nihilo vs creatio ex materia

## Methodology

- Louvain community detection [@blondel2008fast]
- Papers as nodes; authors as edges
- Penalize edges representing prolific authors

$$W(P_1, P_2) = \frac{1}{len(P_1.\text{authors}) \times len(P_2.\text{authors})}$$


## Graph options
  - The top ten communities of 2023 through all time
  - The top two communities of every year through all time


# Creatio ex nihilo vs creatio ex materia

\vfill
\begin{center}
\includegraphics[width=\textwidth,height=0.9\textheight,keepaspectratio]{ network-img/both-communities.pdf }
\end{center}
\vfill

# TF-IDF

```{=latex}
\tiny
\begin{tabular}{rp{12cm}}
\hline
Community & TF-IDF (unigram-trigram) \\
\hline
5282 & pertinent symbolic, misleading content, symbolic, pertinent, content based, content, language, linguistic, representative, detection, real world, accuracy also, additional training, aggregating representative, also time, alternative multi, analyzes linguistic, attributes characterize, based analytical, board showing \\
426 & business organizations, media governments, news media, pandemic research, governments, pandemic, health crises, trust, crises, business, arise 2024, building unbuilding, businesses communication, chapter aimed, chapter proposed, competent curbing, compliance stopping, crises arise, crises public, curbing global \\
2350 & multimodal, dis, multimodal analysis, multimodal dis, disciplines, review, computer science, computer, science, analysis, gaps, studies, research, communication, 2020 start, analysis dis, attention academics, beyond words, bird eye, brings research \\
6075 & democracy, attacks involves, campaigns undermining, citizens example, contribute countermeasures, countermeasures 2025, democracy democracy, democracy relies, discredited recent, elections reliable, epistemic integrity, evidence widespread, example trust, frontier attacks, involves researchers, knowledge establish, list several, pattern science, psychology contribute, recent frontier \\
1277 & claim, claim task, task, claims, social media, spread false, false, media, participation, social, fake news, 2023 forum, 2023 primary, 2023 uncovering, 28 teams, 40 registrations, age 2024, become spread, behemoths, behemoths hire \\
\textcolor{accent!60!black}{1432} & \textcolor{accent!60!black}{ethical, debriefing, ethical practices, ethical research, researchers, research, dialogue, deception, adopting reporting, balance deception, benefits individual, challenges insurmountable, conducting ethical, consent value, consider three, debriefing make, debriefing research, deception dialogue, deception informed, dialogue debriefing} \\
\hline
\end{tabular}
```

# Random example from Loftus community

## Protecting Against Misinformation: Examining the Effect of Empirically Based Investigative Interviewing on Misinformation Reporting [@otgaar_protecting_2020]
- "Children who are involved in legal cases are often interviewed about events they witnessed or that might have happened to them... We found that children’s recall during the NICHD interview protected children against the incorporation of misinformation in their accounts of the event ..."
- Published in *Journal for Police and Criminal Psychology*

# Returning to term frequencies

\vfill
\begin{center}
\includegraphics[width=\textwidth,height=0.9\textheight,keepaspectratio]{term-frequency-img/fig.pdf}
\end{center}
\vfill

# Context: Satanic panic

## 1980: *Michelle Remembers*
\scriptsize
- Michelle Smith co-authors Michelle Remembers with her psychiatrist and soon-to-be-husband, Lawrence Pazder.
- Kicks off media circus and marks the beginning of the mainstream Satanic panic [@shewan_conviction_2015] [@hearst_qanon_2022].

## 1983--1990: McMartin preschool trials [@linderMcMartinPreschoolAbuse2007] [@Schreiber2006Suggestive] [@Reinhold1990LongestTrial] [@WildClaimsMass2024]
\scriptsize
- A single parent accuses ex-husband and school staff member of child abuse.
- Police send letter to 200 parents at the school saying that their children might have been victims of sexual abuse, outlining the potential abuse in detail, and asking parents for any additional information.
- Police systematically coerce confessions from children.
- School's owners and staff were accused of ritually abusing of hundreds of children as part of their Satanic worship. All charges finally dropped after seven years.


# Elizabeth Loftus and the Misinformation Effect

## 1993: "The reality of repressed memories" [@loftus_reality_1993]
- "a rise in reported memories of childhood sexual abuse that were allegedly repressed for many years."
- "(a) How common is it for memories of child abuse to be repressed? (b) How are jurors and judges likely to react to these repressed memory claims? (c) When the memories surface, what are they like? and (d) How authentic are the memories?"

# Misinformation

## What it is
- The misinformation paradigm considers individuals making, reading, and sharing false statements, usually on social media, producing research that often warns of the harm to society resulting from the sum of many such events.

## What it's not
- Poltical economy of social media like @chomsky1988manufacturing did for mass media in 1988
- Media theory: @williamsTelevisionTechnologyCultural2004 brings together the technology of broadcasting and the cultural form of television to describe the “flow” state of watching television, simultaneously communal yet private





	
	
# References {.allowframebreaks}
