#!/usr/bin/Rscript
#  match_av.R Author "Nathan Wycoff <nathanbrwycoff@gmail.com>" Date 07.04.2024

library(fastLink)
source("R/match_settings.R")

#mode <- 'default'
mode <- 'splink'

df1_targs <- c('CT40_output3', 'CT40_output2')
df2_targs <- c('CT99_aug', 'CT40_aug')

for (df1t in df1_targs) {
    for (df2t in df2_targs) {
        df1 <- read.csv(paste(df1t,'.csv', sep =''))
        df2 <- read.csv(paste('./data/',df2t,'.csv', sep =''))

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

        ## Loop over match passes here.
        tta <- Sys.time()
        precs <- rep(NA, 22)
        recls <- rep(NA, 22)
        times <- rep(NA, 22)
        names(precs) <- names(recls) <- names(times) <- letters[1:22]
        for (ms in letters[1:22]) {
            print(ms)
            tt <- Sys.time()
            #keepcols <- c("first_name", "last_name")

            ## Blocking
            if (length(block_vars[[ms]])>0) {
                capture.output(blocks <- blockData(df1, df2, varnames = block_vars[[ms]]))
            } else {
                blocks <- list(list(dfA.inds = 1:nrow(df1), dfB.inds = 1:nrow(df2)))
            }
            print(length(blocks))

            ## Fuzzy match settings
            if (comp_type[[ms]]=='fuzzy') {
                if (mode=='default') {
                    options <- list()
                } else if (mode=='splink') {
                    options <- list(cut.a=0.9, cut.p = 0.8)
                }
            } else if (comp_type[[ms]]=='exact') {
                options <- list('cut.a' = 1., 'cut.p' = 1, 'cut.a.num' = 0., 'cut.p.num' = 0.)
            } else {
                stop("Bad comptype")
            }
            options$n.cores = 40

            if (length(blocks)>1) {
                preoptions <- options
                preoptions$dfA <- df1
                preoptions$dfB <- df2
                preoptions$varnames = comp_vars[[ms]]
                capture.output(pre_ret <- do.call(fastLink, preoptions))
            }

            ## Actual Linking
            m <- matrix(NA,nrow=0,ncol=2)
            colnames(m) <-c("inds.a", "inds.b") 
            minrow <- 3
            bi <- 0
            for (block in blocks) {
                bi <- bi + 1
                print(bi)
                #isbad <- (bi==174) & ms=='e' & df1t == 'CT40_output2' & df2t == 'CT40_aug'
                #isbad <- (bi==1) & ms=='e' & df1t == 'CT40_output2' & df2t == 'CT40_aug'
                options$dfA = df1[block$dfA.inds,]
                options$dfB = df2[block$dfB.inds,]
                options$varnames = comp_vars[[ms]]
                #isbad <- ((dim(options$dfA)[1]) == 0 || dim(options$dfB)[1]==0)
                isbad <- dim(options$dfA)[1] <= minrow || dim(options$dfB)[1] <= minrow
                print(dim(options$dfA))
                print(dim(options$dfB))
                print(isbad)
                if (isbad) {
                    print("Skipped")
                } else {
                    #capture.output(ret <- fastLink(dfA = df1[block$dfA.inds,], dfB = df2[block$dfB.inds,], varnames = comp_vars[[ms]], n.cores = 40)) 
                    #capture.output(ret <- do.call(fastLink, options))
                    if (length(blocks)>1) {
                        options$em.obj <- pre_ret$EM
                    }
                    capture.output(ret <- do.call(fastLink, options))
                    ret$matches$inds.a <- block$dfA.inds[ret$matches$inds.a]
                    ret$matches$inds.b <- block$dfB.inds[ret$matches$inds.b]
                    m <- rbind(m, ret$matches)
                }
            }

            ## Extract match information and store.
            sid1 <- df1[m[,1],'simulant_id']
            sid2 <- df2[m[,2],'simulant_id']

            num_correctly_matched <- sum(sid1==sid2)
            num_matched <- nrow(m)
            num_incorrectly_matched <- sum(sid1!=sid2)
            common_records <- length(intersect(df1$simulant_id, df2$simulant_id))

            recall <- num_correctly_matched/common_records
            precision <- num_correctly_matched/num_matched

            print(recall)
            print(precision)

            print("pr:")
            precs[ms] = precision
            recls[ms] = recall
            times[ms] <- as.numeric(Sys.time()-tt, units = 'secs')
            print("time:")
            print(Sys.time()-tt
        ) 
        }

        resdf <- data.frame(Precision = precs, Recall = recls, Time = times)
        write.csv(resdf, file = paste('sim_out/fastLink_', df1t, '_', df2t, '_',mode,'.csv', sep=''))

        print("overall:")
        print(Sys.time() - tta)
    }
}
