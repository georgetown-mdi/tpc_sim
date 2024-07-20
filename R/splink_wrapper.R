#!/usr/bin/Rscript

library(reticulate)
use_python("./.venv/bin/python", required = T)
use_virtualenv("./.venv/", required = T)
source("R/match_settings.R")

# Essentially imports
splink <- import('splink')
DuckDBLinker <- splink$duckdb$linker$DuckDBLinker
cl <- splink$duckdb$comparison_library 
ctl <- splink$duckdb$comparison_template_library 

## Read in data.
df1t <- 'CT40_output3'
df2t <- 'CT99_aug'

df1 <- read.csv(paste(df1t,'.csv',sep=''))
df2 <- read.csv(paste('./data/',df2t,'.csv',sep=''))

names(df1)[names(df1) == 'simulant_id'] <- 'unique_id'
names(df2)[names(df2) == 'simulant_id'] <- 'unique_id'

## Add subset vars.
df1$ch2_first_name <- substr(df1$first_name, 1, 2)
df2$ch2_first_name <- substr(df2$first_name, 1, 2)

df1$first_initial <- substr(df1$first_name, 1, 1)
df2$first_initial <- substr(df2$first_name, 1, 1)

df1$ch4_last_name <- substr(df1$last_name, 1, 4)
df2$ch4_last_name <- substr(df2$last_name, 1, 4)

df1$zip3 <- substr(df1$mailing_address_zipcode, 1, 3)
df2$zip3 <- substr(df2$mailing_address_zipcode, 1, 3)

df1$ssn4 <- substr(df1$ssn, 11-3,11)
df2$ssn4  <- substr(df2$ssn, 11-3,11)

## Prepare linkage settings
ms <- 'v'
keepcols <- c('unique_id', match_vars[[ms]], 'zip3')

df1_sub <- df1[keepcols]
df2_sub <- df2[keepcols]

print(comp_vars[['v']])
comps <- list(
    ctl$name_comparison('last_name'),
    ctl$name_comparison('ch2_first_name'),
    ctl$name_comparison('middle_initial'),
    cl$damerau_levenshtein_at_thresholds('age', list(1))
)

blocks <- list(splink$duckdb$blocking_rule_library$block_on('zip3'))

settings <- list(
    link_type = "link_and_dedupe",
    comparisons = comps,
    retain_matching_columns = TRUE,
    retain_intermediate_calculation_columns = FALSE,
    blocking_rules_to_generate_predictions = blocks
)

## Prepare linkage settings
dfl <- list(df1_sub, df2_sub)
linker <- DuckDBLinker(dfl, settings)

### Estimate parameters
#drs = "AND".join([' (l.'+v+' = r.'+v+') ' for v in match_vars[ms]])
deterministic_rules  <- list(paste(paste('l.',match_vars[['v']], ' = r.', match_vars[['v']], sep = ''), collapse = ' AND '))
linker$estimate_probability_two_random_records_match(deterministic_rules, recall=0.7)
linker$estimate_u_using_random_sampling(max_pairs=1e6)

for (v in c('last_name','ch2_first_name','middle_initial')) {
    training_blocking_rule <- splink$duckdb$blocking_rule_library$block_on(v)
    training_session_fname_sname <- linker$estimate_parameters_using_expectation_maximisation(training_blocking_rule)
}

### Do actual matching.
df_predictions <- linker$predict(threshold_match_probability=0.1)
mdf <- df_predictions$as_pandas_dataframe()

print("Matches:")
print(mdf)
