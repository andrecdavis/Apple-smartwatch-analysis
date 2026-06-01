# Apple Smartwatch Analysis

We analyze thousands of third-party Apple smartwatch listings collected from online marketplaces. We analyze factors such as model, 




Our main question is: Which features drive price?


## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Analysis](#analysis)
- [Regression Model](#regression-model)
- [Key Findings](#key-findings)
- [Limitations](#limitations)


## Overview

What dataset contains, why interesting, question to answer, approach

## Dataset
Where did it come from
  Web-scraped

What does the raw data look like. 

Explain columns:
  Brand - Apple, Garmin, Xiaome, or Other
  Condition - New, Used, Open-Box, etc.
  Case_Size_mm - Size of smartwatch
  Country - Country of origin
  Price - In USD
  Seller_ID - Uniquely identifies each seller
  Is_Worldwide_Shipping - Boolean
  Title - the listing title

Give stats 
  number of entries
  price range
  number of countries
  number of models

## Methodology
Explain workflow:

How did we clean data?
  Standardized names and entries
  Removed non smartwatch things
  Clean condition column?

Which features were engineered?
  Model
  Family
  Gold/Hermes/Titanium

Analysis methods
  OLS model
  ANOVA

## Analysis

  ### Model
    -price differences by model
    -count differences by model
    -what is surprising
    -gold
    -hermes

    Limitations
      Left-skewedness of model distributions

  ### Country
    -Average prices by country
    -Average price differences by country
    -UK deep dive

    Limitations
      US dominates listings
    

  ### Condition
    -New vs Used vs Open Box?

    Limitations
      No post info, sometimes contradicts title


  ### Case size
    -price by case size
    -Ultra 1,2,3 deep dive?
    -Gold/Hermes deep dive?

  ### Shipping
    -shipping effects
    -shipping and country correlation

  ### Seller ID
    -individual vs power seller


## Regression Model
  Show OLS model results
    -interpret coefficients



## Key Findings
Most important takeaways
  Bullet points
    Aftermarket plating
    Old models listed high
    

  

## Limitations
Missing variables
  Post description

Listings, not sales

