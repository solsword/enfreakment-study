% Analyzing Virtual Enfreakment: Methodology
% Sercan Şengün, James Bowie-Wilson, Peter Mawhorter, Yusef Audeh, Haewoon Kwak, and D. Fox Harrell

This document describes the details of the methodology used for the
survey described in the paper: "Contours of Virtual Enfreakment in
Fighting Game Characters." The code used to construct the survey, as well
as the data that were gathered (in anonymous form) are available at [this
repository's main page](index.html).

In our survey, we presented each character using three images: official online game art,¹ a screenshot of their character select screen image, and a screenshot of the character alone in a practice match in an idle pose.
It should be noted that although game play is also staged against background environments that can convey additional racial/ethnic stereotyping, we avoided showing those and instead focused on the characters.

::: {.sidenote}
¹All material was collected either in-game or from an official English-language website. For Street Fighter V, we referenced [http://streetfighter.com/characters](http://streetfighter.com/characters),
while for Tekken 7 we referenced
[http://tk7.tekken.com/fighters](http://tk7.tekken.com/fighters).
:::

Besides images, we listed official countries of origin (both Street Fighter V and Tekken 7 characters included this information in their online character descriptions), default characterization quotes (usually spoken by the character at the start of a match, as well as listed in online material), and an official description (again found in official online material, on character pages for Tekken 7 and transcribed from character introduction videos for Street Fighter V).
[An example survey](turk/template-local.html) is available, and shows how this information was displayed to participants.
For each survey, we included only 5 of the 60 characters to avoid rater fatigue; these surveys took an estimated 25–35 minutes to complete (we did not measure actual completion rates, due to difficulties in determining how long a participant spends actually engaged with the survey). 


To balance character presentation, we used a constraint solver to produce 84 groupings of five of our 60 characters such that:
- Every group contained at least one male character and at least one female character (Leo was counted as neither, so any group with Leo had to also include at least one (other) male character and at least one (other) female character).
- Every group contained at least one character from each game.
- Every group contained included at least two different nationalities.
- No group contained both the Street Fighter V and Tekken 7 versions of Akuma.
- Each character appeared in exactly seven groups ($(84 \times 5)/ 7 = 60$).
- For every possible pair of characters, that pair appeared together no more than once (to minimize possible interaction biases).

The final constraint necessitated the use of a constraint solver rather than a simple shuffle.
Based on this grouping scheme, we obtain seven ratings (from different participants) per character for every 84 subjects that take a survey (where each subject rates five characters).
In total, we ran a pilot batch of 84 participants that we used to tune the questions (we didn't use this data in our analysis), and three more batches, each using a different grouping solution.
For the first two batches, we ran 84 participants, while for the third batch we ran $84\times4=336$ participants, for a total target of 504 participants and 42 ratings per character.
Due to incomplete (we threw out responses where more than 15% of the survey questions were left blank) and repeat responses (unfortunately, our automated system for preventing repeats failed, although we could still detect them), we actually received a total of 486 usable responses, with 37–43 ratings per character (mean 40.9).


We ran the study as an Amazon Mechanical Turk (AMT) Human Intelligence Task (HIT).
Participants were paid ($6 for the ~30-minute survey), resulting in sampling biases based on at least interest and internet access.
The interest bias was useful in a way, because our respondents were much more likely to be people who had played one of the games we asked about (or at least games from one of the respective franchises) than the general population.
Our only prerequisite on AMT was 97% acceptance, although our survey asked participants to return the HIT if they could not understand the questions, could not view the embedded images, or if they were under 18 years of age.
We did reject some HITs that were clearly incomplete, or where participants did not follow very basic instructions (e.g., did not fill out the consent question), and we suspect that even some accepted responses may have been from participants who did not fill out the survey in earnest.
However, our analysis methods were tolerant of some noise in the responses, and we have no reason to believe that a significant number of responses were nonsense.
Replication of our results with other study populations would be a welcome extension of this research.

## Survey Content

Our code for both data analysis and survey construction is publicly available [in this repository](index.html).
For a full list of the questions we asked, consult the example survey linked from that page.
All of our per-character questions were seven-point Likert items (we did not combine items to form a Likert scale); participants were asked about their level of agreement on a scale using "Strongly disagree," "Disagree," "Somewhat disagree," "Neutral," "Somewhat agree," "Agree," and "Strongly agree."
Our questions were designed to investigate design dimensions rather than personal opinions and to construct an etic perspective which "*involves the evaluation of phenomena using more culturally neutral or objective constructs*".²
Based on previous studies which suggest that the perceptions of some personal aspects, such as the emic "sexual appeal" category, may exhibit cross-cultural agreement,³ we felt confident that our data would be able to distinguish between characters with significantly different designs even if subtler trends might not be detectable.
The design constructs we focused on were specific to fighting games and included the following questions (each actually probed via two opposite-coded items):

::: {.sidenote}
² Margarita, Alegria et al. (2004). “Cultural relevance and equivalence in the NLAAS instrument: integrating etic and emic in the development of cross-cultural measures for a psychiatric epidemiology and services study of Latinos”. In: International Journal of Methods in Psychiatric Research 13.4, pp. 270–288. URL: [https://onlinelibrary.wiley.com/doi/abs/10.1002/mpr.181](https://onlinelibrary.wiley.com/doi/abs/10.1002/mpr.181).<br>
³ Albright, L. et al. (1997). “Cross-Cultural Consensus in Personality Judgements”. In: Journal of Personality and Social Psychology 72.3, pp. 558–569. URL: [http://psycnet.apa.org/buy/1997-07966-008](http://psycnet.apa.org/buy/1997-07966-008).
:::

::: {.hanglists}
- Exaggeration scores (how much does the character stand out?):
    * *(body realism)* Is the character's body designed to appear realistic or exaggerated?
    * *(attire realism)* Is the character's clothing realistic or exaggerated?
    * *(general cues)* Is the character designed to make her/their/his race/ethnicity⁴ obvious?
    * *(attire cues)* Is the character's clothing designed to make her/their/his race/ ethnicity obvious?
- Aspect scores (which aspects of a character are emphasized?):
    * *(musculature)* Is the character designed to appear muscular or not?
    * *(body type)* Is the character designed to appear thin, or overweight?
    * *(youth)* Is the character designed to appear young, or old?
    * *(attractiveness)* Is the character designed to appear attractive, or ugly?
    * *(sexualization)* Is the character sexualized or not?
    * *(attire sexualization)* Is the character's clothing designed to sexualize her/them/him or not?
- Affect scores (is the design generally positive or negative?):
    * *(admirability)* Is the character designed to be admirable, or detestable?
    * *(ethnic representation)* Is the character a positive or negative representative of her/their/his racial/ethnic group?
    * *(gender representation)* Is the character a positive or negative representative of her/their/his gender group (men or women)?
:::

::: {.sidenote}
⁴ The reason we point out race and ethnicity as different constructs is because we use the term ethnic to indicate difference in a more international sense than implied by race, but not limited to difference of nationality either.
:::

Note that the items were not always strictly exclusive; for example Street Fighter V's Zeku is a character that transforms between old and young versions, so his design emphasizes both his youth and his old age.
For analysis, we ended up combining the *general cues* and *attire cues* questions into a single *ethnic cues* item by averaging all four responses instead of just two.

Besides questions about design, we used three statements per character to assess participant familiarity/identification rather than relying on attempts to match demographic information:

::: {.hanglists}
  * *(similarity)* "[Character] is similar to me."
  * *(ethnic match)* "My race/ethnicity is similar to [Character's]."
  * *(ethnic familiarity)* "I am very familiar with [Character's] racial/ethnic group."
:::

These three questions were all positively coded and combined into a single measure of *identification*.


After filling out five survey sections for different characters, participants were finally asked demographic questions, including seven questions about playing and/or watching videogames, one general feedback question, and the following personal questions (see [the example survey](turk/template-local.html) for details):

::: {.hanglists}
- "How old are you?" (seven decade-binned options from "18–24 years old" to "75 years old or older")
- "What is the highest degree or level of school you have completed?" (10 different levels)
- "What language(s) do you use for everyday conversation in your community, home, school, and/or workplace? (please list in order of frequency of use)" (three slots plus a text box for "Additional language(s)")
- "What is your gender?" (free-text response)
- "What racial/ethnic group(s) do you consider yourself a part of? (Be as specific as possible, and list multiple if appropriate.)" (free-text response)
- "What is your nationality?" (free-text response)
:::

We used free-text response for the gender, ethnicity, and nationality questions because we wanted to avoid the problems of othering and inaccurate binning that tend to happen with fixed-response options for these questions (see e.g., ⁵ and ⁶)
However, one of the authors also hand-categorized each reply to create normalized versions of each response for the purposes of potential cross-group comparisons.
This coding resulted in three genders ("Male," "Female," and "Agender\footnote{The only participant who didn't specify some variant of `male' or `female' stated their gender as "Agender."}"), 38 ethnicities (including nation-based, religion-based, and heritage-based ethnicities; many participants claimed more than one), and 17 nationalities (five participants listed multiple nationalities).
One of the ethnicities ("ASIS") and two of the nationalities ("HISPANIC" and "white") were left uncoded and may represent participant confusion; a few participants left some of these fields blank and were coded as "unknown."

::: {.sidenote}
⁵ Burton, Jonathan, Alita Nandi, and Lucinda Platt (2010). “Measuring Ethnicity:
Challenges and Opportunities for Survey Research”. In: Ethnic and Racial
Studies 33.8, pp. 1332–1349. URL: [https://doi.org/10.1080/01419870903527801](https://doi.org/10.1080/01419870903527801).<br>
⁶ Goins, Elizabeth S. and Danee Pye (2013). “Check the Box that Best Describes You: Reflexively Managing Theory and Praxis in LGBTQ Health Communi- cation Research”. In: Health Communication 28.4. PMID: 22809164, pp. 397– 407. URL: [https://doi.org/10.1080/10410236.2012.690505](https://doi.org/10.1080/10410236.2012.690505).
:::


<div class="figure twocolumn">
![A histogram of the gender of participants, showing 3 unknown gender, 346 male, 136 female, and 1 agender participants.](data/plots/demo-gender.svg)
![A histogram of the age of participants, showing ](data/plots/demo-age.svg)
![A histogram of the age of participants, showing ](data/plots/demo-edu.svg)
![A histogram of the age of participants, showing ](data/plots/demo-play.svg)
<div class="caption spancolumns">
Figure 1: The demographics of our participants in terms of gender, age, education, and gameplay frequency (zoom in to inspect details).
</div>
</div>

## Demographics

Figure 1 shows the breakdowns of our participants by gender, age, education, and gameplay frequency.
Our median participant was a 25–34-year-old white U.S. American male with a bachelor's degree who played games daily, and who had played some game from either the *Street~Fighter* or *Tekken* franchises (or both).
17 (3.5%) of our 486 participants had all of these traits, while 368 (75.7%) had more than half of them; considering just gender, ethnicity, national origin, and education, there were 79 (16.3%) white U.S. American men with bachelor's degrees among our participants.


In terms of ethnicities, because we allowed self identification, there were a total of 37 different ethnic groups that participants identified, plus some responses categorized as "Unknown."
Self-identified categories included broad racial categories (e.g., "White" and "Asian"), geographic categories (e.g., "American," "African," "Southeast Asian," and "Hawaiian"), religious categories (e.g., "Jewish," "Hindu," and "Protestant"), ethnic categories (e.g., "Hispanic" and "Latinx"), and national categories (in some but not all cases clearly based on ancestry rather than citizenship; examples include "German," "Filipino," and "Mexican").
Ethnic categories listed by at least 10 participants were: White (313 participants of which 38 listed at least one other ethnicity), Asian (75 participants, 10 multi-ethnic), American (41 participants; 31 multi-ethnic), Black (34 participants; 25 multi-ethnic), Hispanic (28 participants; 9 multi-ethnic; note that ethnicities like "Latinx" and "Mexican" were also listed), European (14 participants; 4 multi-ethnic), Unknown (15 participants), German (11 participants, all multi-ethnic), and Native American (10 participants, 6 multi-ethnic).
Because of their common association, we did not count "White" as a second ethnicity when either "American" or "European" was listed as well (so if you listed just "White" and "European" as your ethnicities, you were counted under both of those categories, but not as multi-ethnic, but if you listed "White," "American," and "Finnish," you were counted as multi-ethnic).
The 29 ethnic categories not listed above each had fewer than 10 participants, with European and Asian geographic groups being the most prominent.
In total, 79 of our 486 participants (16.3%) listed more than one ethnicity, even after collapsing "American" and "European" with "White."


The most interesting aspect of our demographics was the intersection with interest in the games we studied.
Furthermore, 444 (91.4%) of our participants watched other people play fighting games at least occasionally, while 412 (84.8%) watched games from one of the two franchises at least occasionally.
Needless to say, these demographics don't reflect the general population in terms of game play, and our skewed gender, age, and education distributions likely reflect interest in the games we were studying as a driving factor in participants' decisions to participate in our study (the study was titled "Survey on Fighting Games").
To some degree these biases actually lend more weight to our results: the ratings we gathered represent not the views of the general public, but views of people who are actually engaged with these games as audience members (with the obvious caveat that the very enfreakment we are studying ends up affecting who feels comfortable being part of that audience).
They also back up our claim that Street Fighter V and Tekken 7 are broadly popular games that are culturally influential: at least among the population of Amazon Mechanical Turk workers, there are enough interested fans to quickly fill up our survey slots (for each batch of results, all tasks were claimed within 12 hours of posting, and we did not use any forum posts or other advertisements to promote our surveys outside of posting them on AMT).


## Statistical Methodology

Our anonymized data (sufficient to re-analyze all of our hypotheses) and the code that we used to analyze our data are available in [this repository](index.html).
To test hypotheses concerning group differences on our non-parametric response data where an assumption of normality is obviously false (at the very least because our scale is discrete and bounded), we used a Monte Carlo permutation test procedure (related to jackknifing and bootstrapping).
Effectively, we simulated multiple possible worlds in which the participants had assigned the same set of scores to characters at random (instead of intentionally), and asked the question: in what percentage of those worlds was the difference in mean values between the two groups in question at least as large as the difference we observed.
These percentages became our p-values (chances that despite there being no actual relationship, we observed one due to "lucky" data), and we used the Benjamini-Hochberg procedure to control our false discovery rate⁷ and determine which hypotheses were supported by the data.
In all cases, we used a two-sided test, and we set our base threshold for acceptance at $p = 0.05$.
In other words, if the likelihood of our data given no actual relationship was less than 5\%, we would presume a relationship existed, with that threshold made stricter to account for the fact that we did lots of tests (essentially, we used the procedure described in ⁷ to ensure that statistically, no more than 5% of cases where we presumed a relationship should have been false positives).

::: {.sidenote}
⁷ Benjamini, Yoav and Yosef Hochberg (1995). “Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing”. In: Journal of the Royal Statistical Society. Series B (Methodological) 57.1, pp. 289–300. ISSN: 00359246. URL: [http://www.jstor.org/stable/2346101](http://www.jstor.org/stable/2346101).
:::


We used 15000 permutations for each hypothesis test, and used Python 3.8's built-in `random.shuffle` to construct each permutation.
Due to our design, we had no direct control over how many participants of which genders/ethnicities/nationalities saw which characters, so we controlled for these factors.
When testing hypotheses about character attributes, we controlled for participant properties by shuffling assigned scores *within* each participant, so we essentially constructed alternate worlds where participants assigned the same five scores randomly across the characters they saw instead of as they had in our results.
That way, if, for example, female participants assigned higher *sexualization* scores than male participants, that difference would also be reflected in our alternate worlds and our judgement of the likelihood of the actual world would not be affected if some group of characters happened to be rated more or less frequently by female participants.
Similarly, when testing hypotheses about participants, we controlled for character attributes by shuffling scores within those assigned to each character.
