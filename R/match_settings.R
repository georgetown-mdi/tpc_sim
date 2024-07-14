#!/usr/bin/Rscript

### Specify Parameters.
block_vars <- list()
for (ms in c('e','f','g','h','i','m','n','o')) {
    block_vars[[ms]] <- 'mailing_address_zipcode'
}
for (ms in c('j','k','l','p','q','r')) {
    block_vars[[ms]] <- 'zip3'
}
for (ms in c('s','t')) {
    block_vars[[ms]] <- c('age')
}
for (ms in c('a','b','c','d','u','v')) {
    block_vars[[ms]] <- c()
}

comp_vars <- list()
comp_vars[['a']] <- c('ssn','ch4_last_name')
comp_vars[['b']] <- c('ssn')
comp_vars[['c']] <- c('ssn','ch4_last_name')
comp_vars[['d']] <- c('ssn4','last_name')
comp_vars[['e']] <- c('first_name','last_name','middle_initial')
comp_vars[['f']] <- c('first_name','last_name','mailing_address_street_name')
comp_vars[['g']] <- c('first_name','last_name','middle_name')
comp_vars[['h']] <- c('first_name','last_name','middle_initial')
comp_vars[['i']] <- c('ch2_first_name','last_name')
comp_vars[['j']] <- c('first_name','last_name','middle_name')
comp_vars[['k']] <- c('first_name','last_name','middle_name')
comp_vars[['l']] <- c('last_name','ch2_first_name')
comp_vars[['m']] <- c('last_name','first_name','age')
comp_vars[['n']] <- c('last_name','first_initial','mailing_address_street_name')
comp_vars[['o']] <- c('last_name','first_initial','age')
comp_vars[['p']] <- c('last_name','first_name','age')
comp_vars[['q']] <- c('last_name','first_initial','age')
comp_vars[['q']] <- c('last_name','first_name','age')
comp_vars[['r']] <- c('last_name','first_name','age')
comp_vars[['s']] <- c('last_name','ch2_first_name','zip3')
comp_vars[['t']] <- c('ch4_last_name','ch2_first_name','zip3')
comp_vars[['u']] <- c('last_name','ch2_first_name','middle_initial','age')
comp_vars[['v']] <- c('last_name','ch2_first_name','middle_initial','age')

comp_type <- list()
for (ms in c('a','b','d','e','f','j','m','n','p','q','u')) {
    comp_type[[ms]] <- 'exact'
}
for (ms in c('c','g','h','i','k','l','o','r','s','t','v')) {
    comp_type[[ms]] <- 'fuzzy'
}

### Construct settings.
match_vars <- list()
for (ms in names(comp_vars)) {
    match_vars[[ms]] <- c(block_vars[[ms]],comp_vars[[ms]])
}
