# WGI Scraping


## Introduction

Welcome to my Scraping_WGI_score_sheets repository for Unstructured Data
Analytics at the University of Notre Dame. This repository documents my
end-to-end process for extracting, cleaning, and structuring competitive
scoring data from Winter Guard International (WGI).

Several files in this repository represent earlier development steps,
experiments, or partial attempts. The main file to focus on is
project.qmd, which contains the final scraping pipeline and analysis
workflow.

## Student task

For this assignment, students were asked to:

- Identify a problem or question involving unstructured or
  semi-structured data

- Acquire the data directly from the web (no Kaggle, no pre-cleaned
  datasets)

- Clean, normalize, and analyze the data using tools of our choosing

This meant not only scraping the data, but also restructuring messy
HTML, discovering hidden APIs, and building a repeatable pipeline.

## My topic: Winter Gaurd International (WGI)

As someone who participated in high school marching band and winter
percussion, this topic was a natural and meaningful choice. In a
previous machine learning project, I worked with Drum Corps
International (DCI) data obtained from Kaggle, which inspired me to take
on a this challenging task with less structured dataset for this
assignment.

### What is WGI

Winter Guard International (WGI) is the largest competitive circuit for:

- Indoor percussion ensembles

- Color guard teams

- Winds groups

Although labeled “international,” most events occur in the United
States. Each ensemble competes across several regional contests, leading
up to the WGI World Championships each April.

Performances are evaluated by panels of judges who score multiple
captions (Effect, Music, Visual, etc.), resulting in detailed score
sheets and ranking information.

## The problem

At a glance, the score pages on the competition suite link look
structured and readable. However, the HTML underneath is extremely
inconsistent:

- Some data “tables” were not actually tables

- Column headers were stacked, repeated, or missing entirely

- Score cells contained two numbers at once (score + rank)

- Rank values were embedded in a second hidden table

- Different events had different numbers of judges which meant there was
  going to be a different numbers of columns for some competitions.

- Some tables were split across multiple HTML fragments

- Links to recaps were dynamically loaded and could only be scraped
  through json, which was something newer to me.

In short: nothing was reliably extractable without a custom scraping and
cleaning pipeline.

### Approach to Solving the Problem

To address the formatting issues on the WGI website, my workflow
naturally broke into three phases: evaluating the page structure,
testing different extraction methods, and finally building a reliable
scraping pipeline.

#### 1. Evaluating the Structure of the Webpages

Before building anything, I needed to understand what I was scraping.

Key discoveries:

- Many HTML

  <table>

  elements were used for layout, not data

- The scoring table was actually two overlapping tables, which explained
  the “double numbers” phenomenon

- Rank values were visually in the same cell but structurally located in
  a separate hidden table

- Some recap pages had header rows repeated or missing columns

- Classification tables always appeared right before scoring tables,
  which became important later on for addiing distinguishing factors.

#### 2. Testing Different Parsing Strategies

Because of inconsistent HTML, I tested multiple extraction approaches:

- Using pd.read_html() with different identifiers

- Filtering tables by length and structure

- Using regex to inject parentheses around rank values

- Identifying patterns that distinguished “big tables” (two-judge
  panels) from “small tables” (one-judge panels)

- Validating which tables truly contained scoring data vs. navigation or
  layout data

Eventually, the workflow used:

- String-matching to find scoring tables

- Column-count checks to route tables into “large” or “small” processing
  pipelines

- Regex extraction to split score and rank into separate numerical
  columns

Please refer to the large_and_small_tables.py

#### 3. Scraping the Data from the 2025 url

2025 url: https://www.wgi.org/historical_score_per/2025/

Initially, I attempted to scrape all recap links directly from the HTML.
This failed because:

- The recap links were not present in the HTML source

- Many URLs were inserted dynamically by front-end JavaScript

- Playwright did load the page, but still could not expose the missing
  links consistently

However, when I was inspecting browser DevTools i took a look at the
Network tab and found this API endpoint:

https://wgiserver.org/v1/seasonapi=pvk7syNgSZbCyTtTf_tWAw?Division=perc&SeasonId=a0sUy0000007hTFIAY

This endpoint turned out to be the key to everything. It provided all
competition links, full dates, classifications, IDs, and more—far more
structured and complete than what the website showed visually. Although
I didn’t need every field it returned, it allowed me to build a clean
reference dataframe and reliably construct the URLs needed for scraping
each event.

## Viewing the code

To see the final code, please look at the file project.qmd. If you would
like to run it yourself use all the code cells except for the last one
since the csv files are already included in this repository.

## Things to know

This code is fairly restricted. It can only truly be applied to the
2022-2025 seasons. All prior seasons did not utilize competition suite.
Therefore, it is impossible to get the full detailed recap tables for
analysis, at least from the WGI website. Anything from 2019 and prior
will only contain the scores of the groups at the competitions and not
their caption scores. While unfortunate, I believe there is still a some
good insight that could be gained from viewing the overall scores.

## Thanks

Big thank you to Seth for all your help you have given me throughout the
school year so far. Looking forward to next semester!
